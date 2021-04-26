## Итоговый проект курса "Машинное обучение в бизнесе"

<b>Стек:</b><br>
ML: scikit-learn, numpy, pandas<br>
API: Flask <br>
Data: kaggle (https://www.kaggle.com/iabhishekofficial/mobile-price-classification) <br>

Задача: предсказать на основе 20 признаков, к какой ценовой категории (0-3) относится модель телефона. <br>

Преобразования признаков: StandartScaler()

Модель: LogisticRegression

1. Запуск сервера - run_server.py
2. Отправка случайного наблюдения, для выдачи предсказания - send_json.py
