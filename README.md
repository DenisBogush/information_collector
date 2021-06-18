"# information_collector" 

На вашем компьютере должен быть установлен Firefox 

Самый простой способ запустить данный код,- это установить его как пакет (все зависимости автомвтически будут установлены),
для этого нужно выполнить команду python.exe -m pip install git+https://github.com/DenisBogush/information_collector
после этого можно запустить командой python.exe -m information_collector

python -m information_collector --help
покажет какие опции доступны

Что бы запустить из репозитория, придется руками установить зависимости которые можно найти в setup.py

git clone https://github.com/DenisBogush/information_collector.git

cd information_collector

python main.py --help

Чтобы поменять почту нужно установить переменные окружения MY_MAIL и MY_MAIL_PASSWORD, или руками в коде

Тестовая почта: mailforrobotr2d2@gmail.com

Пароль: der_parol

На почте уже присутсвует итоговое письмо с вложенным эксель файлом. 
