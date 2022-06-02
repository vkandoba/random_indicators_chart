set FLASK_ENV=prod
python -m waitress --listen=127.0.0.1:8080 --call web_service_main:create_server
