import pathlib

from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler

from db.queries import add_user
from db.queries import delete_user

REGISTERED_HANDLERS = []


def register(handler, **options):
    def decorator(function):
        options.update({
            'callback': function
        })
        h = handler(**options)
        REGISTERED_HANDLERS.append(h)

        def wrapper(*args, **kwargs):
            return function(*args, **kwargs)

        return wrapper

    return decorator


@register(CommandHandler, **{'command': 'start'})
def start(update, context):
    db = context.bot.db
    user_data = update.effective_user.to_dict()
    add_user(db, user_data)
    update.message.reply_text('Welcome!')


@register(CommandHandler, **{'command': 'stop'})
def stop(update, context):
    db = context.bot.db
    delete_user(db, update.effective_user.id)
    update.message.reply_text('Stop!')


@register(MessageHandler, **{'filters': (Filters.document.image | Filters.photo)})
def echo(update, context):
    try:
        instance = update.message.photo[-1]
    except IndexError:
        instance = update.message.document

    file = context.bot.getFile(instance.file_id)
    suffix = pathlib.Path(file.file_path).suffix
    file.download(f'file{suffix}')
    update.message.reply_text('Image!')
