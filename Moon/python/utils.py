import os
from typing import final
from Moon import DLL_FOUND_PATH, DLL_LOCAL_FOUND_PATH

class LibraryLoadError(Exception):
    """Ошибка загрузки нативной библиотеки"""
    pass

@final
def find_library() -> str:
    """
    #### Поиск пути к нативной библиотеке BUILD.dll
    
    ---
    
    :Returns:
        str: Абсолютный путь к библиотеке
        
    ---
    
    :Raises:
        LibraryLoadError: Если библиотека не найдена
    """
    try:
        # Поиск в папке dlls относительно корня пакета
        
        lib_path = DLL_FOUND_PATH
        if not os.path.exists(lib_path):
            print("Library not found at", lib_path)
            lib_path = DLL_LOCAL_FOUND_PATH
            if not os.path.exists(lib_path):
                print("Library not found at", lib_path)
                raise FileNotFoundError(f"Library not found at {lib_path}")
        
        return lib_path
    except Exception as e:
        raise LibraryLoadError(f"Library search failed: {e}")
