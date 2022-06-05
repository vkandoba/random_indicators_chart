import os
from pathlib import Path
from datetime import datetime

import asyncio

import json
import logging

import uvicorn
from fastapi import FastAPI

from price_service import PriceService
from instrument_service import InstrumentService
from random_price_shift_provider import RandomPriceShiftProvider
from generate_price_service import GeneratePriceService
from generate_price_service_api import GeneratePriceServiceApi


def load_config(env: str, location: str) -> dict:
    return json.loads((location / f"generate_price_service_config_{env}.json").read_text())


def configure_logger(env: str, location: str) -> None:
    logs_filename = f"{location.name}_{datetime.now().strftime('%%d-%m-%Y-%H-%M-%S')}.log"
    logs_location = location.parent / "logs" / logs_filename
    log_level_name = "INFO" if env == 'prod' else "DEBUG"
    logging.basicConfig(filename=logs_location,
                        format="%(levelname)s|%(asctime)s|%(name)s|%(message)s",
                        datefmt='%%d-%m-%Y %H:%M:%S',
                        encoding='utf-8',
                        level=logging.getLevelName(log_level_name))


def create_service_api(main_event_loop, config: dict) -> GeneratePriceServiceApi:
    shift_provider = RandomPriceShiftProvider(config['random_init_state'])
    instrument_service = InstrumentService(config['instrument_count'])
    price_service = PriceService(instrument_service, shift_provider, config['init_price'])
    generate_price_service = GeneratePriceService(price_service, instrument_service, config['update_interval'])
    return GeneratePriceServiceApi(main_event_loop, generate_price_service)


def create_server(main_event_loop, application: FastAPI, endpoint: dict) -> uvicorn.Server:
    return uvicorn.Server(config=(uvicorn.Config(app=application,
                                                 loop=main_event_loop,
                                                 host=endpoint['host'],
                                                 port=endpoint['port'])))


if __name__ == '__main__':
    main_loop = asyncio.new_event_loop()

    server_env = os.environ['SERVER_ENV']
    service_location = Path(__file__).parent
    configure_logger(server_env, service_location)
    app_config = load_config(server_env, service_location)

    service_api = create_service_api(main_loop, app_config)

    server = create_server(main_loop, service_api.fastapi_app, app_config['endpoint'])

    main_loop.run_until_complete(server.serve())
