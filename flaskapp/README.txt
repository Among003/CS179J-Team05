#Start EC2 Instance

#Open AWS
#Running [ Ubuntu Server 16.04 LTS (HVM, SSD Volume Type - ami-43a15f3e ]
#Ports http 80 , TCP 22

#Install apache2 , libapache2-mod-wsgi , python , pip , flask

#Create Directory & Symlink
#mkdir ~/flaskapp
# sudo ln -s ~/flaskapp /var/www/html/flaskapp

#Create App
/file/

#Create .wsgi file
#path to /var/www/html/flaskapp
#Edit File in path /etc/apache2/sites-enabled/000-default.conf
# Insert - 
WSGIDaemonProcess flaskapp threads=5
WSGIScriptAlias / /var/www/html/flaskapp/flaskapp.wsgi

<Directory flaskapp>
    WSGIProcessGroup flaskapp
    WSGIApplicationGroup %{GLOBAL}
    Order deny,allow
    Allow from all
</Directory>
#

#Restart Server
#sudo service apache2 restart



