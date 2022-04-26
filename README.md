# simple-finance-bot

### 1. Описание проекта
Телеграм-бот для мониторинга финансов. Ведение расходов и доходов. Вывод статистики трат.
### 2. Функционал
* Запись расходов по категориям
* Запись доходов по категориям
* Удаление расходов
* Удаление доходов
* Вывод текстовой статистики за день/неделю/месяц/за все время
* Вывод графической статистики за день/неделю/месяц/за все время
### 3. Технологии
   1. Python
   2. Pandas, matplotlib
   3. SQLight3
   4. aiogram
   5. Docker 
### 4. Запуск на локальной машине.

Установить необходимые зависимости `pip install -r requirements.txt`

Создать файл `setenv.sh` (любое название). В нем заполнить переменные окружения:

   `export BOT_API_TOKEN=""` - Идентификатор бота

   `export MY_TELEGRAM_ID=""` - Идентификатор пользователя 

В виртуальном окружении выполнить команду `source setenv.sh`

Для запуска сервера - `python server.py`

### 5. Docker - подготовка и запуск

В `Dockerfile` заполнить переменные окружения

`ENV BOT_API_TOKEN=""` - Идентификатор бота

`ENV MY_TELEGRAM_ID=""` - Идентификатор пользователя 

``` 
docker build -t tgfinances ./
docker run --name tg-finance-bot -v /Users/andrewvolkov/Dev/simple-finance-bot/db/:/home/db tgfinances   
```
