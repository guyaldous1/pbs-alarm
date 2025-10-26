Run with 
gunicorn -w 1 -b 127.0.0.1:5000 player:app

Once player app is running, launch caddy with
caddy run