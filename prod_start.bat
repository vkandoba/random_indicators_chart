set FLASK_ENV=production
python -m waitress --listen=127.0.0.1:7001 --call generate_price_service:generate_price_service_main
