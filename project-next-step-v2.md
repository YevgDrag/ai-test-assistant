# Наступний крок для MVP — v2

## Мета

Підготувати початковий робочий прототип, який можна швидко запустити та протестувати локально.

## Завдання

1. Запустити FastAPI прототип із `06-implementation/app.py`.
2. Надіслати приклад запиту до `/generate-test-plan`.
3. Перевірити відповідь: `plan_markdown`, `suggested_checks`, `qa_confirm_question`.

## Команди для запуску

```cmd
cd C:\Projects\ai-test-assistant\06-implementation
python -m pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

## Тестовий приклад

1. Створити `payload.json` у `06-implementation` з прикладом Jira-запиту.
2. Надіслати запит через `curl`.
3. Перевірити, що відповідь містить структурований тест-план.

## Що зробити після цього

- Уточнити, які поля Jira/Confluence потрібно додати до API.
- Зробити прототип генерації на основі LLM.
- Додати документацію для розгортання та інтеграції.
