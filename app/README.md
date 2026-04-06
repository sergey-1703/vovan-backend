# Инструкция по запуску

1. Загрузить версию Python 3.14.3 - https://www.python.org/downloads/
2. При установке выбрать галочку "Add python to path"
3. Скачать проект
4. Настроить PostgreSQL (это должен здесь написать Платон)
5. После того, как настроили PostgreSQL, нужно перейти в терминале в корневую папку проекта и выполнить 
```
py -3.14.3 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```
6. После запуска открыть:

-   API: http://127.0.0.1:8000
-   Swagger UI: http://127.0.0.1:8000/docs

