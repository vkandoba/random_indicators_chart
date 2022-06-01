set FLASK_ENV=prod
python -m waitress --listen=127.0.0.1:7001 --call generate_price_service_main:create_flask_app
