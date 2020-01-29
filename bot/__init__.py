from logging import Logger
from queue import Queue
from threading import Thread

from telegram.bot import Bot
from telegram.ext import Dispatcher

from bot.handlers import REGISTERED_HANDLERS
from bot.utils import setup_web_hook


def setup(token: str,
          web_hook_url: str,
          logger: Logger) -> Dispatcher:
    bot = Bot(token)
    bot.logger = logger
    setup_web_hook(bot, web_hook_url)

    update_queue = Queue()

    dispatcher = Dispatcher(bot, update_queue, use_context=True)
    for handler in REGISTERED_HANDLERS:
        dispatcher.add_handler(handler)

    # Start the thread
    thread = Thread(target=dispatcher.start, name='dispatcher')
    thread.start()

    return dispatcher
