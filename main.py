import uvloop
from aiohttp.web import run_app

from bot import setup
from utils import make_logger
from utils import read_config
from web import make_app


def main():
    config_path = 'config.ini'
    required_fields = ['BotToken', 'WebHookUrl']
    config = read_config(config_path, required_fields)

    token = config.get(config.default_section, 'BotToken')
    web_hook_url = config.get(config.default_section, 'WebHookUrl')
    debug = config.getboolean(config.default_section, 'Debug')

    logger = make_logger(debug, name='BotLogger')
    dispatcher = setup(token, web_hook_url, logger)

    run_app(make_app(dispatcher))


if __name__ == '__main__':
    uvloop.install()
    main()
