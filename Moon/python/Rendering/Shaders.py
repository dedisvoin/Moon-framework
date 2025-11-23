"""
#### *Модуль работы с шейдерами в PySGL*

---

##### Версия: 1.1.9

*Автор: Павлов Иван (Pavlov Ivan)*

*Лицензия: MIT*
##### Реализованно на 95% 

---

✓ Полноценная работа с шейдерами:
    - Загрузка вершинных и фрагментных шейдеров
    - Поддержка геометрических шейдеров
    - Установка uniform переменных различных типов

✓ Гибкая система загрузки:
    - Загрузка из файлов (vertex/fragment)
    - Загрузка из строк в коде
    - Загрузка по типу шейдера

✓ Расширенные возможности:
    - Поддержка текстур в шейдерах
    - Векторные и цветовые uniform'ы
    - Интеграция с системой рендеринга

✓ Готовые интерфейсы:
    - Shader - основной класс для работы с шейдерами
    - Type - перечисление типов шейдеров
    - Методы класса для быстрого создания

---

:Requires:

• Python 3.8+

• Библиотека ctypes (для работы с DLL)

• PySGL.dll (нативная библиотека рендеринга)

• OpenGL 3.3+ (для поддержки шейдеров)

---

== Лицензия MIT ==================================================

[MIT License]
Copyright (c) 2025 Pavlov Ivan

Данная лицензия разрешает лицам, получившим копию данного программного обеспечения 
и сопутствующей документации (в дальнейшем именуемыми «Программное Обеспечение»), 
безвозмездно использовать Программное Обеспечение без ограничений, включая неограниченное 
право на использование, копирование, изменение, слияние, публикацию, распространение, 
сублицензирование и/или продажу копий Программного Обеспечения, а также лицам, которым 
предоставляется данное Программное Обеспечение, при соблюдении следующих условий:

[ Уведомление об авторском праве и данные условия должны быть включены во все копии ]
[                 или значительные части Программного ОбеспечениЯ.                  ]

ПРОГРАММНОЕ ОБЕСПЕЧЕНИЕ ПРЕДОСТАВЛЯЕТСЯ «КАК ЕСТЬ», БЕЗ КАКИХ-ЛИБО ГАРАНТИЙ, ЯВНО 
ВЫРАЖЕННЫХ ИЛИ ПОДРАЗУМЕВАЕМЫХ, ВКЛЮЧАЯ, НО НЕ ОГРАНИЧИВАЯСЬ ГАРАНТИЯМИ ТОВАРНОЙ 
ПРИГОДНОСТИ, СООТВЕТСТВИЯ ПО ЕГО КОНКРЕТНОМУ НАЗНАЧЕНИЮ И ОТСУТСТВИЯ НАРУШЕНИЙ ПРАВ. 
НИ В КАКОМ СЛУЧАЕ АВТОРЫ ИЛИ ПРАВООБЛАДАТЕЛИ НЕ НЕСУТ ОТВЕТСТВЕННОСТИ ПО ИСКАМ О 
ВОЗМЕЩЕНИИ УЩЕРБА, УБЫТКОВ ИЛИ ДРУГИХ ТРЕБОВАНИЙ ПО ДЕЙСТВУЮЩЕМУ ПРАВУ ИЛИ ИНОМУ, 
ВОЗНИКШИМ ИЗ, ИМЕЮЩИМ ПРИЧИНОЙ ИЛИ СВЯЗАННЫМ С ПРОГРАММНЫМ ОБЕСПЕЧЕНИЕМ ИЛИ 
ИСПОЛЬЗОВАНИЕМ ПРОГРАММНОГО ОБЕСПЕЧЕНИЯ ИЛИ ИНЫМИ ДЕЙСТВИЯМИ С ПРОГРАММНЫМ ОБЕСПЕЧЕНИЕМ.
"""

import ctypes
from enum import Enum
import os
from typing import Any
from colorama import Fore

from Moon.python.Vectors import Vector2f, Vector2i
from Moon.python.Colors import Color

from Moon.python.utils import find_library

##################################################################
#                   `C / C++` Bindings                           #
#   Определение аргументов и возвращаемых типов для функций      #
#   из нативной DLL библиотеки PySGL, используемых через ctypes. #
##################################################################

# Загружаем DLL библиотеку
try:
        LIB_MOON = ctypes.CDLL(find_library())
except Exception as e:
        raise ImportError(f"Failed to load PySGL library: {e}")

# Определения сигнатур функций из библиотеки PySGL
LIB_MOON._Shader_Create.argtypes = None
LIB_MOON._Shader_Create.restype = ctypes.c_void_p
LIB_MOON._Shader_Delete.argtypes = [ctypes.c_void_p]
LIB_MOON._Shader_Delete.restype = None
LIB_MOON._Shader_IsAvailable.argtypes = None
LIB_MOON._Shader_IsAvailable.restype = ctypes.c_bool
LIB_MOON._Shader_LoadFromFile.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
LIB_MOON._Shader_LoadFromFile.restype = ctypes.c_bool
LIB_MOON._Shader_LoadFromStrings.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
LIB_MOON._Shader_LoadFromStrings.restype = ctypes.c_bool
LIB_MOON._Shader_GetCurrentTexture.argtypes = None
LIB_MOON._Shader_GetCurrentTexture.restype = ctypes.c_void_p

LIB_MOON._Shader_SetUniformInt.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_float]
LIB_MOON._Shader_SetUniformFloat.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_float]
LIB_MOON._Shader_SetUniformBool.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_bool]
LIB_MOON._Shader_SetUniformTexture.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_void_p]
LIB_MOON._Shader_SetUniformIntVector.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
LIB_MOON._Shader_SetUniformFloatVector.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_float, ctypes.c_float]
LIB_MOON._Shader_SetUniformColor.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]



def shaders_is_available() -> bool:
    """
    #### Проверяет доступность шейдеров в окружении

    ---

    :Return:
    - bool - True, если нативная библиотека сообщает о поддержке шейдеров

    ---

    :Example:
    ```python
    if shaders_is_available():
        print("Shaders supported")
    ```
    """
    return LIB_MOON._Shader_IsAvailable()


ShaderPtr = ctypes.c_void_p
TexturePtr = ctypes.c_void_p


def get_current_texture() -> TexturePtr:
    """
    #### Возвращает указатель на текущую активную текстуру

    ---

    :Return:
    - TexturePtr - Указатель на текущую текстуру из нативной библиотеки

    ---

    :Example:
    ```python
    tex_ptr = get_current_texture()
    ```
    """
    return LIB_MOON._Shader_GetCurrentTexture()


BASE_VERTEX_SOURCE = """
#version 130
void main()
{
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
    gl_TexCoord[0] = gl_TextureMatrix[0] * gl_MultiTexCoord0;
    gl_FrontColor = gl_Color;
}
"""

class Shader:
    """
    #### Обёртка для работы с шейдерами через PySGL.dll

    Класс предоставляет методы для загрузки шейдеров (из файлов и строк)
    и установки uniform-переменных различных типов.

    ---

    :Attributes:
    - __ptr - Внутренний указатель на нативный объект шейдера
    - __vertex_source - Код вершинного шейдера (строка)
    - __fragment_source - Код фрагментного шейдера (строка)

    ---

    :Example:
    ```python
    shader = Shader.LoadFromSources(vertex_code, fragment_code)
    ```
    """

    class SOURCE_TYPE(Enum):
        """Перечисление типов источников шейдера."""
        VERTEX = 0
        FRAGMENT = 1

    @classmethod
    def LoadFromSources(self, vertex: str, fragment: str) -> "Shader | None":
            """
            #### Создаёт Shader и загружает шейдеры из строк с исходным кодом

            ---

            :Args:
            - vertex - Строка с исходным кодом вершинного шейдера
            - fragment - Строка с исходным кодом фрагментного шейдера

            ---

            :Return:
            - Shader | None - Экземпляр Shader при успешной компиляции или None при ошибке

            ---

            :Example:
            ```python
            sh = Shader.LoadFromSources(vs_code, fs_code)
            ```
            """
            shader = Shader()
            shader._set_source(Shader.SOURCE_TYPE.VERTEX, vertex)
            shader._set_source(Shader.SOURCE_TYPE.FRAGMENT, fragment)
            result = shader._load_from_source()
            if result:
                print(f'[ {Fore.LIGHTBLUE_EX}ShaderLoader{Fore.RESET} ] [ {Fore.GREEN}succes{Fore.RESET} ] Shader from sources loaded')
                return shader
            else:
                print(f'[ {Fore.LIGHTBLUE_EX}ShaderLoader{Fore.RESET} ] [ {Fore.RED}error{Fore.RESET} ] Shader from sources not loaded')
                return None
            
    @classmethod
    def LoadFromFiles(self, vertex_path: str, fragment_path: str) -> "Shader | None":
        """
        #### Загружает и компилирует шейдеры из файлов

        ---

        :Args:
        - vertex_path - Путь к файлу вершинного шейдера
        - fragment_path - Путь к файлу фрагментного шейдера

        ---

        :Return:
        - Shader | None - Экземпляр Shader при успешной компиляции или None при ошибке (в данном коде при неудаче выполняется exit)

        ---

        :Example:
        ```python
        sh = Shader.LoadFromFiles("vertex.glsl", "fragment.glsl")
        ```
        """
        shader = Shader()
        print(f'[ {Fore.LIGHTBLUE_EX}ShaderLoader{Fore.RESET} ] [ {Fore.YELLOW}info{Fore.RESET} ] Loading shader from source files...')
        if os.path.exists(vertex_path):
            print(f'  {Fore.GREEN}+{Fore.RESET} Vertex Path: {Fore.LIGHTMAGENTA_EX}{vertex_path}{Fore.RESET}')
        else:
            print(f'  {Fore.RED}-{Fore.RESET} Vertex Path not found: {Fore.LIGHTMAGENTA_EX}{vertex_path}{Fore.RESET}')
        
        if os.path.exists(fragment_path):
            print(f'  {Fore.GREEN}+{Fore.RESET} Fragment Path: {Fore.LIGHTMAGENTA_EX}{fragment_path}{Fore.RESET}')
        else:
            print(f'  {Fore.RED}-{Fore.RESET} Fragment Path not found: {Fore.LIGHTMAGENTA_EX}{fragment_path}{Fore.RESET}')
        
        print(f'[ {Fore.LIGHTBLUE_EX}ShaderLoader{Fore.RESET} ] [ {Fore.YELLOW}info{Fore.RESET} ] Compiling shader...')

        result = LIB_MOON._Shader_LoadFromFile(shader.get_ptr(), vertex_path.encode('utf-8'), fragment_path.encode('utf-8'))
        if result:
            print(f'[ {Fore.LIGHTBLUE_EX}ShaderLoader{Fore.RESET} ] [ {Fore.GREEN}succes{Fore.RESET} ] Shader compiled successfully')
            return shader
        else:
            print(f'[ {Fore.LIGHTBLUE_EX}ShaderLoader{Fore.RESET} ] [ {Fore.RED}error{Fore.RESET} ] Shader compilation failed')
            exit(-1)
            return None

    @classmethod
    def LoadFragmentFromFile(self, path: str) -> "Shader | None":
        """
        #### Загружает фрагментный шейдер из файла, используя стандартный вершинный шейдер

        Метод читает указанный файл с кодом фрагментного шейдера и создает Shader,
        используя встроенный BASE_VERTEX_SOURCE в качестве вершинного шейдера.

        ---

        :Args:
        - path - Путь к файлу фрагментного шейдера

        ---

        :Return:
        - Shader | None - Экземпляр Shader при успешной загрузке/компиляции или None при ошибке

        ---

        :Example:
        ```python
        sh = Shader.LoadFragmentFromFile("fragment.glsl")
        ```
        """
        print(f'[ {Fore.LIGHTBLUE_EX}ShaderLoader{Fore.RESET} ] [ {Fore.YELLOW}info{Fore.RESET} ] Loading shader from source files...')
        print(f'  {Fore.GREEN}+{Fore.RESET} Fragment Path: {Fore.BLACK}used STANDART_VERTEX_SOURCE{Fore.RESET}')
        if os.path.exists(path):
            print(f'  {Fore.GREEN}+{Fore.RESET} Fragment Path: {Fore.LIGHTMAGENTA_EX}{path}{Fore.RESET}')
        else:
            print(f'  {Fore.RED}-{Fore.RESET} Fragment Path not found: {Fore.LIGHTMAGENTA_EX}{path}{Fore.RESET}')
            exit(-1)
        fragment_source = open(path, 'r', encoding='utf-8').read()
        shader = Shader().LoadFromSources(BASE_VERTEX_SOURCE, fragment_source)
        return shader
        


    def __init__(self):
        """
        #### Инициализация объекта Shader

        Создаёт внутренний нативный объект шейдера и инициализирует строки исходников.

        ---

        :Return:
        - None

        ---

        :Example:
        ```python
        shader = Shader()
        ```
        """
        self.__ptr = LIB_MOON._Shader_Create()

        self.__vertex_source = ""
        self.__fragment_source = ""

    def _set_source(self, source_type: SOURCE_TYPE, source: str):
        """
        #### Устанавливает исходный код для указанного типа шейдера

        ---

        :Args:
        - source_type - SOURCE_TYPE.VERTEX или SOURCE_TYPE.FRAGMENT
        - source - Строка с исходным кодом шейдера

        ---

        :Return:
        - None

        ---

        :Example:
        ```python
        shader._set_source(Shader.SOURCE_TYPE.VERTEX, vertex_code)
        ```
        """
        if source_type == Shader.SOURCE_TYPE.FRAGMENT:
            self.__fragment_source = source
        elif source_type == Shader.SOURCE_TYPE.VERTEX:
            self.__vertex_source = source
        else:
            raise ValueError("Invalid source type")
        

    def _load_from_source(self):
        """
        #### Компилирует шейдеры из установленных строк исходников

        Отправляет vertex и fragment source в нативную библиотеку для компиляции.

        ---

        :Return:
        - bool - True при успешной компиляции, False при ошибке

        ---

        :Example:
        ```python
        success = shader._load_from_source()
        ```
        """
        return LIB_MOON._Shader_LoadFromStrings(self.__ptr, self.__vertex_source.encode('utf-8'),
                                                            self.__fragment_source.encode('utf-8'))

    def get_ptr(self) -> ShaderPtr:
        """
        #### Возвращает внутренний указатель на нативный объект шейдера

        ---

        :Return:
        - ShaderPtr - Указатель на нативный объект шейдера

        ---

        :Example:
        ```python
        ptr = shader.get_ptr()
        ```
        """
        return self.__ptr
    
    def __del__(self):
        """
        #### Уничтожение объекта Shader и освобождение нативного ресурса

        ---

        :Return:
        - None

        ---

        :Example:
        ```python
        del shader
        ```
        """
        LIB_MOON._Shader_Delete(self.__ptr)
    
    def set_uniform(self, name: str, arg: Any):
        """
        #### Устанавливает uniform-переменную в шейдере по имени

        Поддерживаемые типы:
        - int
        - float
        - bool
        - Texture / RenderTexture (через get_ptr)
        - Vector2f / Vector2i
        - Color

        ---

        :Args:
        - name - Имя uniform-переменной в шейдере
        - arg - Значение или объект для установки (поддерживаемые типы см. выше)

        ---

        :Return:
        - None

        ---

        :Raises:
        - TypeError: Если тип arg не поддерживается

        ---

        :Example:
        ```python
        shader.set_uniform("u_time", 1.23)
        shader.set_uniform("u_color", Color(255,0,0))
        ```
        """
        if isinstance(arg, int):
            LIB_MOON._Shader_SetUniformInt(self.__ptr, name.encode('utf-8'), float(arg))
        elif isinstance(arg, float):
            LIB_MOON._Shader_SetUniformFloat(self.__ptr, name.encode('utf-8'), arg)
        elif isinstance(arg, bool):
            LIB_MOON._Shader_SetUniformBool(self.__ptr, name.encode('utf-8'), arg)
        elif arg.__class__.__name__ == 'Texture2D':
            LIB_MOON._Shader_SetUniformTexture(self.__ptr, name.encode('utf-8'), arg.get_ptr())
        elif arg.__class__.__name__ == 'RenderTexture2D':
            LIB_MOON._Shader_SetUniformTexture(self.__ptr, name.encode('utf-8'), arg.get_ptr())
        elif isinstance(arg, Vector2f):
            LIB_MOON._Shader_SetUniformFloatVector(self.__ptr, name.encode('utf-8'), arg.x, arg.y)
        elif isinstance(arg, Vector2i):
            LIB_MOON._Shader_SetUniformFloatVector(self.__ptr, name.encode('utf-8'), arg.x, arg.y)
        elif isinstance(arg, Color):
            LIB_MOON._Shader_SetUniformColor(self.__ptr, name.encode('utf-8'), arg.r, arg.g, arg.b, arg.a)
        else:
            raise TypeError(f'Unsupported uniform type: {type(arg)}')
