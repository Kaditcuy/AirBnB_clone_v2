#!/usr/bin/env bash
# Script to set up web server for the deployment of web_static

# Installs Nginx if not installed
# Creates /data/ directory if it doesnt exist
# Creates /data/web_static/ if it doesnt already exist
# Creates /data/web_static/releases/ if it doesnt already exist
# Creates /data/web_static/shared/ if it doesnt already exist
# Creates /data/web_static/releases/test/ if it doesnt already exist
# Creates a fake html file /data/web_static/releases/test/index.html
#  (with simple content, to test Nginx Configuration)
# Creates a symbolic link /data/web_static/current linked to the /data/web_static/releases/test,
# Give ownership of the /data/ folder to the ubuntu user AND group
# Update Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static

# Update package list
sudo apt-get -y update

# Install nginx if it doesnt exist
[ ! -f /usr/sbin/nginx ] && sudo apt-get install -y nginx

# Shorthand for allowing traffic on port 80
sudo ufw allow 'Nginx HTTP'

[ ! -d /data/web_static/releases/test/ ] && sudo mkdir -p /data/web_static/releases/test/
[ ! -d /data/web_static/shared/ ] && sudo mkdir -p /data/web_static/shared/

# fake html file with simple content, to test your Nginx configuration
echo "<!DOCTYPE html>
<html>
	<head>
	</head>
	<body>
		<p>Hello World<p>
	</body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# if the symbolic link exits, delete it
# and recreated every time the script is ran
[ -f /data/web_static/current ] && sudo rm /data/web_static/current
sudo ln -sf /data/web_static/releases/test /data/web_static/current

# assign Recursive ownership of '/data/' to ubuntu USER and GROUP
sudo chown -R "ubuntu:ubuntu" /data/

# Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static
head_of_loc="location \/hbnb\_static\/ {"
content="alias \/data\/web\_static\/current\/;"
location="\n\t$head_of_loc\n\t\t$content\n\t}\n"
sudo sed -i "37s/$/$location/" /etc/nginx/sites-available/default

# Restart nginx without using systemctlt
sudo service nginx restart
