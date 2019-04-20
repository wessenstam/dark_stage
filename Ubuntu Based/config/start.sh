cd /opt/stageworkshop
git pull
nohup /usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf 2>&1 