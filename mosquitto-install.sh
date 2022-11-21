#!/bin/bash
#install mqtt server
#Usage: ./install.sh example.com username
domain=$1
username=$2
search='mqtt.example.com'
filename='default.conf'
sudo add-apt-repository ppa:certbot/certbot
sudo apt install certbot mosquitto mosquitto-clients acl
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 8883
sudo ufw allow 8083
sudo certbot certonly --standalone --preferred-challenges http -d $domain
sudo mosquitto_passwd -c /etc/mosquitto/passwd $username
if [[ $domain != "" ]]; then
sed -i "s/${search}/${domain}/g" $filename
fi
sudo cp default.conf /etc/mosquitto/conf.d/default.conf
sudo setfacl -R -m u:mosquitto:rX /etc/letsencrypt/{live,archive}
sudo systemctl restart mosquitto
sudo systemctl status mosquitto
sudo tail /var/log/mosquitto/mosquitto.log
sudo echo 'renew_hook = systemctl restart mosquitto' >> /etc/letsencrypt/renewal/$domain.conf
sudo certbot renew --dry-run

