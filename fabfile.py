from fabric import Connection

# Connect to the remote server
c = Connection('ubuntu@18.207.207.11')

# send the file to the remote server, as long as ssh is supported on the server
c.put("0-setup_web_static.sh")
# run the file on that server
#c.run("bash 0-setup_web_static.sh")
# But if the script needs superuser permission:
c.sudo("bash ./0-setup_web_static.sh")
#c.sudo("bash systemctl status nginx.service")
