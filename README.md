![image](https://user-images.githubusercontent.com/8759658/172070358-25171dd6-62a5-4344-a6a8-84e49d3b986a.png)

## Задача
Прототип сервиса по получению и предпросмотру торговых данных.

1. **Cервис данных**. Генерирует и возвращает цены для торговых инструментов.
- Торговые инструменты - искуственные, названия по шаблону:  
ticker_00, ticker_01, …, ticker_99.
- Интервал - раз в секунду
- Изменение цены по формуле:
```
movement = -1 if random() < 0.5 else 1
```
2. **Веб-сервис**. Визуализирует цены в режиме реального времени. 
- Селектор инструмента по имени - выпадающий список
- График цены от начального момента 

## Общая схема
![Untitled Diagram drawio (1)](https://user-images.githubusercontent.com/8759658/172102265-a1c735dc-50f3-4eef-912b-c083f7d54768.png)

## Веб-сервис
- [web_service_main.py](web_service/web_service_main.py) - точка входа и инициализация приложения
- [price_graph_page.py](web_service/price_graph_page.py) - основная страница с графиком, компоненты Dash и callback, который обновляет базовый график, когда пользователь меняет инструмент
- [update_store_callback.js](web_service/client_scripts/update_store_callback.js) - клиентский callback, который принимает сообщения и сохраняет новые цены
- [update_price_graph_callback.js](web_service/client_scripts/update_store_callback.js) - клиентский callback, который обновляет график

