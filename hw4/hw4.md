В созданной ранее виртуальной машине настройте:
1. дату и время, часовой пояс. Проверьте hostname, при необходимости поменять. Установить в качестве сервера времени `0.pool.ntp.org 1.pool.ntp.org`. Проверить правильность настройки, пояснить почему Вы решили что все правильно.  

timedatectl проверяем дату, время и часовой пояс
sudo timedatectl set-timezone Europe/Minsk устанавливаем часовой пояс
timedatectl ещё раз проверяем
sudo hostnamectl проверяем hostname
systemctl status systemd-timesyncd проверяем включена ли синхронизация
sudo timedatectl set-ntp true включаем при необходимости
sudo nano /etc/systemd/timesyncd.conf открываем конфиг файл и добавляем в секцию добавляем в секцию Time 2 строки:
NTP=0.pool.ntp.org 1.pool.ntp.org 
FallbackNTP=ntp.ubuntu.com
sudo systemctl restart systemd-timesyncd перезагружаем сервис
sudo system ctk statustimedatectl проверяем, в строке NTP сервис должно быть active 


2. Статический ip-address, маршрут по умолчанию и днс сервер при помощи `netplan`.

ls /etc/netplan/ смотрим файл netplan
sudo nano /etc/netplan/50-cloud-init.yaml открываем файл и редактируем
network:
  version: 2
  renderer: networkd
  ethernets:
    enp0s3:
      dhcp4: false
      addresses:
        - 192.168.0.50/24
      routes:
        - to: default
          via: 192.168.0.1
      nameservers:
        addresses:
          - 1.1.1.1
          - 8.8.8.8
sudo netplan try  проверяем конфигурацию
3. 2 пользователей в разных группах. Выдайте группе права на обновление системы через настройку `sudo visudo`. Для одного из пользователей настройте права для использования `systemctl status`. Настройте доступ по ssh для новых пользователей через ssh ключи. Доступ по ssh по логину и паролю запретите.
sudo useradd -m -s /bin/bash -c "User1" user1 создаем первого пользователя
sudo passwd nuser1 задаем пароль первому пользователю
sudo useradd -m -s /bin/bash -c "User2" user2 создаем второго пользователя
sudo passwd user2 задаем пароль второму пользователю
sudo groupadd tms1 создаем первую группу
sudo groupadd tms2 создаем вторую группу
sudo usermod -aG tms1 user1 добавляем первого пользователя в первую группу
sudo usermod -aG tms2 user2 добавляем второго пользователя во вторую группу
sudo visudo редактируем /etc/sudoers
%tms1 ALL=(ALL) /usr/bin/apt update, /usr/bin/apt upgrade добавляем строку, после сохраняем изменения
sudo su user1 заходим под user1
sudo apt update пробуем выполнить команду 
%user2 ALL=(ALL) NOPASSWD: /usr/bin/systemctl status * добавлем строку в sudo visudo, сохраняем изменения
sudo su user2 заходим под user2
systemctl status проверяем выполнение команды
ssh-keygen -t ed25519 далее по очереди входим под пользователями user1 и user2 b генерируем ssh ключи
 ssh-copy-id user1@ilyalosenok копируем ключи для обоих пользователей
 ssh-copy-id user2@ilyalosenok 
 nano /etc/ssh/sshd_config открываем конфиг
 PasswordAuthentication ставим no
 sudo service ssh restart перезапускаем службу ssh
4.  каталог для работы группы людей, настройте что бы права во внутренних каталогах наследовались от  группы директории, а не основную группу пользователя. В ней создайте файл под одним из пользоватей разрешите доступ к нему только для владельца.
mkdir forg создаем каталог
chmod g+s ./forg/ делаем наследование от группы директории
ls -la проверяем, появляется s в правах на диркторию
touch test.me создаем файл в директории
chmod 700 test.me оставляем доступ только для владельца
5. сетевой доступ к виртуальной машине только по 22 и 80. Попробуйте подключиться по ssh. Установить nginx `sudo apt install nginx` посмотрите что доступно из браузера вашей основной машины при разрешенном трафике и запрещенном. Найдите информацию почему мы разрешали именно 80 порт, какие еще зарезервированные порты вы знаете?
В качесте результата домашнего задания мне нужен файл с командами для выполнения списка заданий и пояснением к ним + скриншоты выполненных действий.
sudo ufw status проверяем доступные порты
sudo ufw deny 43/tcp запрещаем доступ по порту
sudo ufw deny 53/tcp запрещаем доступ по порту
sudo ufw deny 53/tcp запрещаем доступ по порту
или sudo ufw default deny incoming запрещаем входящий трафик
sudo ufw allow 22/tcp разрешаем доступ по порту
sudo ufw allow 80/tcp разрешаем доступ по порту
sudo ufw enable
sudo ufw status

80 порт протокола http
443 порт протокола https
22 порт ssh