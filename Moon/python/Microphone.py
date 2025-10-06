import sounddevice as sd
import numpy as np

from scipy import signal
from scipy.fft import fft, fftfreq

class SimpleMicrophone:
    def __init__(self, samplerate=44100, chunk_duration=0.1):
        self.samplerate = samplerate
        self.chunk_duration = chunk_duration
        self.current_volume = 0.0
        self.previous_volume = 0.0
        self.current_pitch = 0.0
        self.stream = None
        self.audio_buffer = None
    
    def _audio_callback(self, indata, frames, time, status):
        # Обновляем данные в буфере
        self.audio_buffer = indata.copy()
        
        # Обновляем громкость
        self.previous_volume = self.current_volume
        self.current_volume = float(np.sqrt(np.mean(indata**2)))
        
        # Вычисляем высоту звука
        if self.current_volume > 0.001:  # Минимальный порог для анализа
            self.current_pitch = self._calculate_pitch(indata.flatten())
        else:
            self.current_pitch = 0.0
    
    def _calculate_pitch(self, audio_data, min_freq=80, max_freq=1000):
        """
        Вычисляет основную частоту (высоту звука) с помощью автокорреляции
        """
        try:
            # Применяем оконную функцию для уменьшения краевых эффектов
            window = np.hanning(len(audio_data))
            windowed_data = audio_data * window
            
            # Вычисляем автокорреляцию
            correlation = np.correlate(windowed_data, windowed_data, mode='full')
            correlation = correlation[len(correlation)//2:]
            
            # Находим пики в автокорреляции
            peaks, _ = signal.find_peaks(correlation, height=0.1*np.max(correlation))
            
            if len(peaks) > 1:
                # Первый значимый пик (после нулевого лага) дает период
                fundamental_period = peaks[1] - peaks[0]
                
                if fundamental_period > 0:
                    fundamental_freq = self.samplerate / fundamental_period
                    
                    # Фильтруем по разумному диапазону частот
                    if min_freq <= fundamental_freq <= max_freq:
                        return fundamental_freq
            
            return 0.0
            
        except Exception as e:
            print(f"Ошибка при вычислении высоты звука: {e}")
            return 0.0
    
    def _calculate_pitch_fft(self, audio_data, min_freq=80, max_freq=1000):
        """
        Альтернативный метод вычисления высоты звука с помощью FFT
        """
        try:
            # Применяем оконную функцию
            window = np.hanning(len(audio_data))
            windowed_data = audio_data * window
            
            # Вычисляем FFT
            n = len(windowed_data)
            fft_data = fft(windowed_data)
            frequencies = fftfreq(n, 1/self.samplerate)
            
            # Берем только положительные частоты
            positive_freq_idx = np.where(frequencies > 0)
            frequencies = frequencies[positive_freq_idx]
            magnitudes = np.abs(fft_data[positive_freq_idx])
            
            # Фильтруем по интересующему нас диапазону частот
            freq_mask = (frequencies >= min_freq) & (frequencies <= max_freq)
            frequencies = frequencies[freq_mask]
            magnitudes = magnitudes[freq_mask]
            
            if len(magnitudes) > 0:
                # Находим частоту с максимальной амплитудой
                max_idx = np.argmax(magnitudes)
                fundamental_freq = frequencies[max_idx]
                return fundamental_freq
            
            return 0.0
            
        except Exception as e:
            print(f"Ошибка при вычислении высоты звука (FFT): {e}")
            return 0.0
    
    def start(self):
        """Запуск прослушивания микрофона"""
        self.audio_buffer = np.zeros(int(self.samplerate * self.chunk_duration))
        self.stream = sd.InputStream(
            callback=self._audio_callback,
            channels=1,
            samplerate=self.samplerate,
            blocksize=int(self.samplerate * self.chunk_duration)
        )
        self.stream.start()
    
    def stop(self):
        """Остановка прослушивания микрофона"""
        if self.stream:
            self.stream.stop()
            self.stream.close()
    
    def get_volume(self):
        """Получение текущей громкости"""
        return self.current_volume
    
    def get_pitch(self):
        """
        Получение текущей высоты звука в Герцах
        Возвращает 0.0 если звук слишком тихий для анализа
        """
        return self.current_pitch
    
    def get_pitch_note(self, concert_pitch=440.0):
        """
        Возвращает ближайшую музыкальную ноту и отклонение в центах
        """
        if self.current_pitch == 0:
            return "No sound", 0
        
        # Вычисляем номер полутона от A4
        semitones_from_a4 = 12 * np.log2(self.current_pitch / concert_pitch)
        
        # Округляем до ближайшего полутона
        nearest_semitone = round(semitones_from_a4)
        
        # Вычисляем отклонение в центах (100 центов = 1 полутон)
        cents_deviation = (semitones_from_a4 - nearest_semitone) * 100
        
        # Определяем ноту
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        note_index = (nearest_semitone + 9) % 12  # A4 = 9-я нота в списке
        octave = 4 + (nearest_semitone + 9) // 12
        
        note_name = f"{note_names[note_index]}{octave}"
        
        return note_name, cents_deviation
    
    def is_volume_increased(self, threshold=0.01):
        """
        Возвращает True, если текущая громкость выше предыдущей 
        на величину больше threshold
        """
        return (self.current_volume - self.previous_volume) > threshold
    
    def is_volume_decreased(self, threshold=0.01):
        """
        Возвращает True, если текущая громкость ниже предыдущей 
        на величину больше threshold
        """
        return (self.previous_volume - self.current_volume) > threshold
    
    def get_volume_change(self, threshold=0.01):
        """
        Возвращает информацию об изменении громкости с учетом порога
        """
        difference = self.current_volume - self.previous_volume
        
        if difference > threshold:
            return "increased"
        elif difference < -threshold:
            return "decreased"
        else:
            return "unchanged"
    
    def get_volume_difference(self):
        """Возвращает разницу между текущей и предыдущей громкостью"""
        return self.current_volume - self.previous_volume

