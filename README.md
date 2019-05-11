# Введение
Этот проект позволяет вытащить ретроспективную информацю о погоде с сайта Gismeteo и положить их в базу данных MongoDB для последующей с ней работы на усмотрение пользователя. Также проект предоставляет простой HTTP API для получения погоды в определенный день в определенном городе.

# Требования
Для работы требуется Python 3.6+ и набор библиотек, перечисленый в `backend/requirements.txt`. Тажке неободим установленный и запущенный экземпляр MongoDB версии 3 и выше.

# Сбор данных
Сбор данных происходит скриптом `scripts/scrapping.py`. Запускать его следует с первым аргументом - ID населенного пункта, для которого делается выборка. Узнать его можно из адреса `https://www.gismeteo.ru/diary/4720/`, где `4720` - ID населенного пункта. Выберите ваш населенный пункт на сайте `gismeteo.ru` и возьмите ID оттуда. Пример запуска скрипта:

```bash
python scrapping.py 4720
```

# Запуск сервера
Запустите `backend/main.py` без дополнительных параметров, чтобы сервер "слушал" на порту `8080`. Запустите `backend/main.py` с аргументом, чтобы сервер "слушал" на заданном в первом аргументе порту. Например:
```bash
# python main.py
Started on localhost:8080 
```
```bash
# python main.py 8000
Started on localhost:8000 
```

# Запросы к API
## Формат запроса
Для получения погоды в вашем регионе должен быть выполнен запрос:
```http request
GET /api/history?cityID=:cityID&date=:date&years=1997[,1998,...]
```
* `cityID` - обязательный параметр - ID города, для которого нужно взять погоду;
* `date` - это дата в формате timestamp, из которой будет взят день (по умолчанию принимается за время сервера);
* `years` - перечисленные через запятую года, для которых нужно взять данные. По умолчанию бергутся все возможные года.

## Формат ответа
Ответ выглядит следующим образом:

```json
{
  "res": [
    {
      "temperature": {
        "n": -19,
        "d": -11
      },
      "month": 1,
      "year": 2018,
      "day": 5
    },
    {
      "temperature": {
        "n": -21,
        "d": -15
      },
      "month": 1,
      "year": 2017,
      "day": 5
    },
    {
      "temperature": {
        "n": -31,
        "d": -29
      },
      "month": 1,
      "year": 2016,
      "day": 5
    },[...]
  ]
}
```
Результаты упорядочены по убыванию лет.
