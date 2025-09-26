# PyType - Автоматизация заметок в Anytype  
(PyType - Automating notes in Anytype)  
  
PyType - это инструмент для выполнения Python скриптов, хранящихся в заметках Anytype.  
(PyType is a tool for executing Python scripts stored in Anytype notes.)  

Проект позволяет создавать исполняемые скрипты прямо в вашем пространстве знаний Anytype и запускать их через Local API.  
(The project allows you to create executable scripts directly in your Anytype knowledge space and run them via the Local API.)  
  
## Возможности  
(Features)  
  
- 🐍 Выполнение Python кода из заметок Anytype  
  (Execute Python code from Anytype notes)  
- 🔗 Система модулей с поддержкой `include` для связывания скриптов  
  (Module system with `include` support for linking scripts)  
- 🏠 Автоматический выбор рабочего пространства  
  (Automatic workspace selection)  
- 🔐 Безопасное хранение API токенов  
  (Secure storage of API tokens)  
- 📦 Песочница для изолированного выполнения кода  
  (Sandbox for isolated code execution)  
  
## Требования  
(Requirements)  
  
- Python 3.8+  
- Anytype с включенным Local API  
  (Anytype with Local API enabled)  
- Доступ к Local API Anytype (обычно `http://127.0.0.1:31009`)  
  (Access to Anytype Local API, usually `http://127.0.0.1:31009`)  
  
## Установка  
(Installation)  
  
1. **Клонируйте репозиторий**  
   (Clone the repository)  
```bash  
git clone https://github.com/she1kopr9d/Pytype.git  
cd Pytype
```

2. **Создайте виртуальное окружение**
    (Create a virtual environment)
```bash
python -m venv venv
```

3. **Активируйте виртуальное окружение**
    (Activate the virtual environment)
    
    На Linux/macOS:
    (On Linux/macOS:)

```bash
source venv/bin/activate
```

    На Windows:
    (On Windows:)

```bash
venv\Scripts\activate
```

4. **Установите зависимости (если есть requirements.txt)**
    (Install dependencies if requirements.txt exists)
```bash
pip install -r requirements.txt
```

## Использование (Usage)

### Базовый запуск (Basic run)
```bash
python main.py
```

При первом запуске вам потребуется:
(On first run you will need to:)

1. Ввести API-ключ из Local API Anytype
    (Enter the API key from Anytype Local API)
2. Выбрать рабочее пространство
    (Select a workspace)


### Быстрый запуск с сохраненным токеном (Quick run with saved token)

```bash
python main.py --token <номер-пространства>
```

## Настройка Anytype (Anytype setup)
1. Включите Local API в настройках Anytype
    (Enable Local API in Anytype settings)
2. Создайте объекты типа "pyrun" в вашем пространстве
    (Create objects of type “pyrun” in your space)
3. Добавьте Python код в markdown блоки внутри этих объектов
    (Add Python code into markdown blocks inside these objects)
4. Используйте # script_name в начале кода для именования скриптов
    (Use # script_name at the beginning of the code to name scripts)


## Система модулей (Module system)
PyType поддерживает простую систему модулей:
(PyType supports a simple module system:)
**Пример использования (Example usage)**

1. Скрипт начала (все скрипты начала должны называться __main__)
(Initialization script, all entry scripts must be named __main__)
![](docs/img/init_script.png)

2. Скрипт, который показывает работу include/ classes
(Script showing usage of include/classes)
![](docs/img/classes_script.png)

3. Скрипт, в котором испльзуется класс из classes и переменные из __main__
(Script using a class from classes and variables from __main__)
![](docs/img/analitic_script.png)

4. Вывод в консоле
(Console output)
![](docs/img/console.png)


## Структура проекта (Project structure)

Pytype/  
├── main.py              # Точка входа приложения (Application entry point)  
├── anytype/             # Основной пакет (Main package)  
│   ├── __init__.py      # Конфигурация API (API configuration)  
│   ├── macros.py        # Основная логика выполнения (Execution logic)  
│   ├── token.py         # Управление токенами (Token management)  
│   ├── queryes.py       # API запросы к Anytype (Anytype API requests)  
│   ├── utils.py         # Вспомогательные функции (Helper functions)  
│   ├── sandbox.py       # Песочница для выполнения (Execution sandbox)  
│   └── space.py         # Работа с пространствами (Workspace management)  
└── README.md  
