# Задания для back-end
Ниже будут описаны запросы для различный частей back-end части
## Необходимо выполнить перед запуском
- Создать config.py в разделе Memes с написать следующий код:
```
import os

file_path = os.path.abspath(os.getcwd()) + "/mems.db"
SECRET_KEY = '...'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + file_path
SQLALCHEMY_TRACK_MODIFICATIONS = True
access_token = '...'

```
Этот файл содержит секретный ключ и токен, поэтому я не стал его выкладывать. Свой секретный ключ токен нужно ввести вместо '...'
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

![image](https://user-images.githubusercontent.com/78679833/174429925-0fb53d16-9855-4456-8c13-8bbd5858c6df.png)

### Получение всех мемов
- Если база мемов не пуста, то выведется следующее
![image](https://user-images.githubusercontent.com/78679833/174429939-7aa823a6-2e17-4d8d-bcc4-8981ae3ee59a.png)

- Если база пуста, то выведется соответствующее сообщение:
![image](https://user-images.githubusercontent.com/78679833/174429953-138c0613-27b7-485f-b7e0-2d554163d595.png)

### Удаление всех мемов
- В случае если база была не пуста, то мемы будут удалено и будет выведено соответствующее сообщение
![image](https://user-images.githubusercontent.com/78679833/174427112-8a816112-2f25-43ad-b7a2-2f473c9a9d11.png)

- В случае если база пуста, то будет выведено соответствующее сообщение
![image](https://user-images.githubusercontent.com/78679833/174427131-a09de029-b5c0-4b24-a23e-3c30d9d9d08d.png)
