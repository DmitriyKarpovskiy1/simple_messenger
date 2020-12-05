# Установка зависимостей

Версия python: `Python 3.7.3`
Установите зависимости при помощи `pipenv install` и зайти в оболочку `pipenv shell`

# Настройка базы данных

1. Исправить файл с конфиграцией БД `constants/detabase.json`, если это нужно. Пункты, которые идут далее, соответвуют стандартной конфигурации, если вы исправили данные в конфигурации, то также нужно исправить и информацию далее в соответсвии с новыми данными
2. Зайти в MySQL под root пользователем
3. Создать новую базу данных:
```
CREATE DATABASE simple_messenger;
```
4. Создать нового пользователя с root привелегиями для базы данных
```
GRANT ALL PRIVILEGES ON simple_messenger.* TO 'karpovskiy'@'localhost' IDENTIFIED BY 'pa$$w0rd';
GRANT ALL PRIVILEGES ON simple_messenger.* TO 'karpovskiy'@'%' IDENTIFIED BY 'pa$$w0rd';
```
5. Запустить `db_migrate.py` скрипт: `./db_migrate.py`

[Работающий пример](https://simple-messenger-server1.herokuapp.com/)
