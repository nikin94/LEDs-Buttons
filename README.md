# Принцип работы: https://youtu.be/nWiyf43l0VQ
Проект на стадии разработки

Элементы, необходимые для работы проекта:
1) Код в данном репозитории
2) Плата, подключающаяся к Raspberry pi v2 B+ через программируемые пины, 
на которой находятся 8 светодиодов и 8 кнопок, каждая из которых соответствует своему светодиоду.
Для пояснения в данном репозитории имеется папка с визуальным подкреплением.

Программа имеет 3 режима работы:
1) Случайный. Загорается один из светодиодов, выбранный случайно, и ожидает нажатия соответствующей ему кнопки, после чего гаснет.
Пользователем задается количество повторений(по умолчанию - 5). Один светодиод не может включиться два раза подряд. 
2) Одиночный. Пользователь сам задает, какой из светодиодов загорится путем нажатия на соответствующую кнопку 
во встроенном в программу графическом интерфейсе. Невозможно включить более одного светодиода за раз.
3) Путь. Пользователем определяется, в каком порядке будут загораться светодиоды и количество попыток. Возможно зажечь один и тот же
светодиод более одного раза подряд(рекомендуется установить переменную pause>0 во избежание повторного "мгновенного" нажатия
одного и того же светодиода).

Невозможно включить более одного светодиода за раз.
Ведется статистика - время, потраченное на нажатие кнопки, общее время, самое быстрые и медленное нажатия, среднее время на одно нажатие.
Существует переменная pause - она отвечает за длительность паузы после выключения одного и включением следующего светодиода.
