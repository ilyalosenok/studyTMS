# Веб-приложение на Python (Flask)

Простое приложение с приветственной страницей и калькулятором (функция суммы).

## Подготовка (venv)

Из корня проекта создайте и активируйте виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
# или: venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

Дальнейшие команды выполняйте с активированным venv.

## Запуск приложения

```bash
flask --app app run
```

или:

```bash
python app.py
```

Откройте в браузере:
- Главная: http://127.0.0.1:5000/
- Сумма: http://127.0.0.1:5000/calculator/sum?a=1&b=2
- Swagger UI: http://127.0.0.1:5000/apidocs

## Запуск тестов

```bash
pytest tests/ -v
```
