# Інструкція: Як запустити сканер секретів

Цей документ пояснює, як локально запустити `scripts/check_secrets.py`, що саме він шукає, та як інтерпретувати його результат.

Передумови
- Переконайтесь, що ви працюєте з кореня проекту `c:\Projects\ai-test-assistant` у терміналі.
- Має бути встановлений Python (версія 3.7+). Скрипт не потребує додаткових пакетів.

Чому ви отримали помилку `"'scripts' is not recognized as an internal or external command"`?
- Ви намагались виконати `scripts/check_secrets.py` без вказівки інтерпретатора. На Windows це інтерпретується як команда `scripts`, якої не існує. Потрібно запускати скрипт через `python` або вказати відносний шлях у PowerShell.

Кроки для запуску

1) У класичному CMD (Command Prompt):

```cmd
cd \Projects\ai-test-assistant
python scripts\check_secrets.py
```

або, якщо у вас встановлено кілька версій Python:

```cmd
py scripts\check_secrets.py
```

2) У PowerShell:

```powershell
Set-Location C:\Projects\ai-test-assistant
python .\scripts\check_secrets.py
# або
py .\scripts\check_secrets.py
```

3) У Bash / WSL / macOS / Linux:

```bash
cd /mnt/c/Projects/ai-test-assistant   # або відповідний шлях
python3 scripts/check_secrets.py
```

Перевірка коду виходу
- У CMD після завершення можна подивитись код виходу:

```cmd
echo %ERRORLEVEL%
```

- У PowerShell:

```powershell
$LASTEXITCODE
```

Що виводить скрипт
- Якщо не знайдено очевидних потенційних секретів, скрипт виведе:

```
No obvious secrets found by quick scan.
```

і завершиться з кодом `0`.

- Якщо знайдено потенційні секрети, скрипт виведе список у форматі:

```
Potential secrets found:
- C:\path\to\file.py:42 -> AWS Access Key ID (AKIA...) -- AKIA...EXAMPLE...
- C:\path\to\config.env:3 -> Private key block -- PRIVATE KEY HEADER

Please remove sensitive data and re-run the scanner before push.
```

і завершиться з кодом `1`.

> Примітка: якщо ви використовуєте у документації або прикладах буквальні маркери приватного ключа або AWS-ключа, сканер спрацює на них як на потенційний секрет. В таких випадках замініть приклади на описовий текст, наприклад `PRIVATE KEY HEADER`.

Що робити, якщо сканер щось знайшов
1. Не пуште такі файли у репозиторій.
2. Якщо це дійсно секрет (ключ, токен, приватний ключ) — відразу відкотіть/видаліть файл з локального staging (`git reset` / `git restore --staged`), видаліть значення і збережіть локально, або збережіть секрети у безпечному сховищі (env vars, Vault, Key Vault).
3. Якщо секрет вже потрапив в історію Git — потрібно виконати ротацію ключа (вендор/сервіс) та очищення історії (BFG Repo-Cleaner або `git filter-repo`).
4. Після видалення/редагування перезапустіть сканер і переконайтесь, що знахідки зникли.

Додаткові рекомендації
- Додайте цей скрипт у pre-commit або pre-push hook, щоб автоматизувати перевірку перед відправкою в origin.
- Для повноцінного захисту інтегруйте `detect-secrets` або `git-secrets` у CI та локальні хуки.
- Для витягів з Jira/Confluence: перед збереженням у репозиторій створюйте санітайзовані версії (редагуйте PII, заміняйте специфічні дані на маркери).

Якщо хочеш, я додам зараз `pre-commit` hook-шаблон, який запускає цей скрипт і блокує коміт при знахідках.

---
Файл: `scripts/check_secrets.py`
Розташування: `c:\Projects\ai-test-assistant\scripts\check_secrets.py`

Якщо після запуску у тебе все ще не виходить — скинь точну команду, яку ти виконав у терміналі, і я підкажу, чому виникає помилка.
