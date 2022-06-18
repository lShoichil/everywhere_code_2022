# Задания для back-end
Ниже будут описаны запросы для различный частей back-end части
## Необходимо выполнить перед запуском
- Создать config.py в разделе Memes с написать следующий код:
```
import os

file_path = os.path.abspath(os.getcwd()) + "/mems.db"
SECRET_KEY = 'thisissecret'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + file_path
SQLALCHEMY_TRACK_MODIFICATIONS = True
```
Этот файл содержит секретный ключ, поэтому я не стал его выкладывать.
- Создать виртуальное окружение:

Установить библиотеку virtualenv для python командой:
```
pip install virtualenv 
```
Создать окружение командой:
```
py -m venv venv  
```
Зайти в него командой (для windows):
```
.\venv\Scripts\activate
```
- Импортировать зависимость с помощью requirements.txt командой:
```
pip install -r .\requirements.txt
```

## Запуск
- Необходимо прописть команду:
```
 py .\run.py  
```
Может возникнуть ошибка в библиотеке vk:
```
ImportError: cannot import name 'Iterable' from 'collections'
```
[Решение](https://stackoverflow.com/questions/35762077/creating-a-new-object-returns-attributeerror-list-object-has-no-attribute-s)

## Запросы для первого задания
Текст задания:

Загрузите все мемы в вашу базу (или просто скачайте их локально, используя API ВКонтакте). 
Выведите в консоль информацию о полученных мемах — их авторов и количество лайков.

Запросы тестировал через Postman.
### Загрузка мемов (требуется логин, пароль, url)на интересующий альбом)
- Сразу после успешной загрузки будет redirect на url с запросом на вывод всех мемов, т.е. будет вывод всех мемов

![image](https://user-images.githubusercontent.com/78679833/174426797-eee245cc-8ef5-41c1-9b85-e1c9f77a7006.png)
- В случае неправильного логина или пароль, будет получено следующее сообщение

![image](https://user-images.githubusercontent.com/78679833/174426826-e80cf1b4-0d42-474a-995d-5d2855a9b200.png)

### Получение всех мемов
- Если база мемов не пуста, то выведется следующее
![image](https://user-images.githubusercontent.com/78679833/174426843-c3df938e-a6bf-4fdd-84a7-1a8d12dd890c.png)

- Если база пуста, то выведется соответствующее сообщение:
![image](https://user-images.githubusercontent.com/78679833/174427223-dfc4293e-5ffe-45ab-a16b-be885352b6a7.png)

### Удаление всех мемов
- В случае если база была не пуста, то мемы будут удалено и будет выведено соответствующее сообщение
![image](https://user-images.githubusercontent.com/78679833/174427112-8a816112-2f25-43ad-b7a2-2f473c9a9d11.png)

- В случае если база пуста, то будет выведено соответствующее сообщение
![image](https://user-images.githubusercontent.com/78679833/174427131-a09de029-b5c0-4b24-a23e-3c30d9d9d08d.png)
