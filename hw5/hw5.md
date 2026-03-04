
## Для начинающих


1. Напишите скрипт `~/bin/hello.sh`, который:
   - принимает один аргумент (имя пользователя);
   - если аргумент не передан — использует значение по умолчанию (например, текущего пользователя из `$USER`);
   - выводит приветствие вида: `Здравствуйте, <имя>. Скрипт запущен: <дата и время>. Количество переданных аргументов: N.`
   - в начале скрипта укажите shebang и комментарий с описанием назначения скрипта.
# Скрипт   
 nano ~/bin/hello.sh
 #!/bin/bash
 # Скрипт принимает один аргумент
 # Если аргумент не передан - использует значение по умолчанию (имя текущего пользователя)
 # Выводит приветствие
 NAME="${1:-$USER}"
 NOW=$(date '+%Y-%m-%d %H:%M:%S')
 ARGS=$#
 echo "Здравствуйте, $NAME. Скрипт запущен: #NOW. Количество переданных аргументов: $ARGS."
2. Сделайте скрипт исполняемым и запустите его: без аргументов, с одним аргументом. Приложите вывод.
chmod +x ~/bin/hello.sh
3. Добавьте в скрипт проверку кода возврата последней команды (`$?`) после вывода и выведите сообщение «Завершено успешно» или «Завершено с ошибкой» в зависимости от значения.
 if [ $? -eq 0 ]; then
     echo "Завершено успешно"
 else
     echo "Завершено с ошибкой"
 fi
4. Напишите скрипт настройки виртуальной машины из предыдущего задания
 nano ~/bin/hello.sh
 #!/bin/bash
 # Настройка ВМ из hw4
 # Пункт 1
 echo "Настройка даты, времени, часового пояса и сервера NTP."
 sudo timedatectl set-timezone Europe/Minsk
 sudo sed -i 's/#NTP=/NTP=0.pool.ntp.org 1.pool.ntp.org/' /etc/systemd/timesyncd.conf
 sudo sed -i 's/#FallbackNTP=/FallbackNTP=2.pool.ntp.org 3.pool.ntp.org/' /etc/systemd/timesyncd.conf
 sudo systemctl restart systemd-timesyncd
 echo "Серверы NTP настроены."
 # Пункт 2
 echo "Настройка статического ip-address, маршрут по умолчанию и днс сервер при помощи netplan"
 sudo tee $(ls /etc/netplan/50-cloud-init.yaml) <<EOF
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
 EOF
 echo "Изменения внесены."
 sudo netplan apply
 echo "Изменения применены."
 # Пункт 3
 echo "Создание 2 пользователей в разных группах и выдача прав"
 sudo groupadd tms1
 sudo groupadd tms2
 sudo useradd -m -G tms1 -s /bin/bash -c "User1" user1
 sudo useradd -m -G tms2 -s /bin/bash -c "User2" user2
 sudo passwd user1
 sudo passwd user2
 echo "User1:password" | sudo chpasswd
 echo "User2:password" | sudo chpasswd
 echo "Пользователи созданы"
 echo "%tms1 ALL=(ALL:ALL) /usr/bin/apt update, /usr/bin/apt upgrade" | sudo EDITOR='tee -a' visudo
 echo "Права на обновление системы выданы группе tms1."
 echo "user2 ALL=(ALL) NOPASSWD: /usr/bin/systemctl status *" | sudo EDITOR='tee -a' visudo
 echo "Права на systemctl status пользователю user2 выданы."
 # Пункт 4
 echo "Создание каталога для наследования от группы директории и файла в нем с правами только у владельца"
 sudo mkdir forg
 sudo chown -R root:tms1 forg
 sudo chmod g+s ./forg/
 sudo touch test.me
 sudo chmod 700 test.me
 echo "Директория и файл с правами только у владельца созданы"
 # Пункт 5
 echo "Настройка сетевого доступа по 22 и 80 порту"
 sudo apt update
 sudo apt install ufw nginx -y
 sudo ufw allow 22/tcp 
 sudo ufw allow 80/tcp
 sudo ufw default deny incoming 
 sudo ufw enable
 echo "Настройка выполнена"




