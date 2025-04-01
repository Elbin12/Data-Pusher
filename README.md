# Data-Pusher
A Django project deployed on AWS with PostgreSQL, Gunicorn, and Nginx.

## Prerequisites
- AWS EC2 instance (Ubuntu 22.04 recommended)
- SSH access to the instance
- PostgreSQL database setup
- Domain name (optional, for HTTPS)

---

## 1. Clone the Project
```bash
cd ~  # Move to home directory
git clone https://github.com/Elbin12/Data-Pusher.git
cd data_pusher
```

## 2. Set Up a Virtual Environment
```bash
sudo apt update && sudo apt install python3-venv python3-pip -y
python3 -m venv env
source env/bin/activate
```

## 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 4. Configure Environment Variables
Create a `.env` file in the project root:
```bash
SECRET_KEY=your-secret-key
POSTGRES_DB_NAME=datapusher
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

## 5. Configure PostgreSQL
Ensure PostgreSQL is installed and create a database:
```bash
sudo -u postgres psql
```
In the PostgreSQL shell, run:
```sql
CREATE DATABASE datapusher;
ALTER USER postgres SET PASSWORD 'your_db_password';
\q  # Exit PostgreSQL
```

## 6. Apply Migrations & Collect Static Files
```bash
python manage.py makemigrations
python manage.py migrate
```

## 7. Set Up Gunicorn
Create a Gunicorn systemd service file:
```bash
sudo nano /etc/systemd/system/gunicorn.service
```
Add:
```ini
[Unit]
Description=Gunicorn daemon for Django project
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/data_pusher
ExecStart=/home/ubuntu/data_pusher/env/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          data_pusher.wsgi:application

[Install]
WantedBy=multi-user.target
```
Create a Gunicorn systemd socket file:
```bash
sudo nano /etc/systemd/system/gunicorn.socket
```
Add:
```ini
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```


Save and exit. Then run:
```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

## 8. Set Up Nginx
Create an Nginx configuration file:
```bash
sudo nano /etc/nginx/sites-available/data-pusher
```
Add:
```nginx
server {
    listen 80;
    server_name your-domain.com ec2-your-ip.compute.amazonaws.com;

    location / {
        proxy_pass http://unix:/run/gunicorn.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
Save and exit. Then run:
```bash
sudo ln -s /etc/nginx/sites-available/data-pusher /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

## 9. Restart Services After Changes
After updating `.env`, restart services:
```bash
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

## 🎉 Done! Your Django project is now live on AWS.
Let me know if you have any issues! 🚀 