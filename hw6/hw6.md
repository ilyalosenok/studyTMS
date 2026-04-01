Выберите приложение которое будете "мучить на продолжении курса", можно два. Одно на компилируемом языке программирования, друшое - интерпритируемом. Просмотрите, что бы приложение писало логи в файл.

Я использовал предоставленное приложение на Python

1. Сделайте для него unit-файл и запустите его в виде демона.
создал директорию и скопировал приложение в неё
mkdir /home/user/app
cp -r /media/sf_same/. /home/user/app/
Использую виртуальное окружение:
cd /home/user/myapp
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Создал Unit файл и заполнил его:
sudo nano /etc/systemd/system/app.service
[Unit]
Description=My App Service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=root
Group=root
WorkingDirectory=/home/ilyalosenok/app
ExecStart=/home/ilyalosenok/app/venv/bin/python3 /home/ilyalosenok/app/app.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target

Затем выполняем команды:
sudo systemctl daemon-reload
sudo systemctl enable app
sudo systemctl start app
sudo systemctl status app
Видим что приложение работает

2. Проверьте пишуться ли логи в файл, просмотрите есть ли логи в journalctl
sudo journalctl -u myapp -f
3. Настройте ротацию логов через logrotate
sudo mkdir -p /var/log/app
sudo nano /etc/logrotate.d/app - создаем файл и заполняем:
/var/log/myapp/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 user user
    sharedscripts
    postrotate
        systemctl reload myapp.service > /dev/null 2>&1 || true
    endscript
}

Добавляем в Unit файл в секцию Service строки:
StandardOutput=file:/var/log/myapp/app.log
StandardError=file:/var/log/myapp/app-error.log

Перезапускаем сервисы:
sudo systemctl daemon-reload
sudo systemctl restart app.service
Проверяем на ошибки:
sudo logrotate -d /etc/logrotate.d/myapp
Выполняем ротацию:
sudo logrotate -f /etc/logrotate.d/myapp
Проверяем файлы логов:
ls -la /var/log/myapp/
4. Исследуйте прооцесс вашего приложения, от кого запущен какие параметры. Измените приоритет его выполнения.
sudo systemctl show app.service
можно сужать перечень параметров: через -p писать только нужные
top -p $1748
sudo renice -n 10 -p 1748

