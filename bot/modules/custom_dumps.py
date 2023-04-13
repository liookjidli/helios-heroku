from bot.helper.telegram_helper.message_utils import sendMessage, sendMarkup, editMessage
from telegram.ext import CommandHandler
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.button_build import ButtonMaker
from bot import dispatcher, OWNER_ID, LOGGER, DUMP_DICT
from telegram.ext import CommandHandler, CallbackQueryHandler
from re import search as re_search
from urllib.parse import parse_qs, urlparse
from bot.helper.ext_utils.db_handler import DbManger




def add_dump(update, context):
    uid = update.message.from_user.id
    try:
        mus = update.message.text.split(" ", 1)[1]
    except:
        muus = f"send your Dump Channel IDs \n\nIf you want to add multiple IDs, seperate them with space."
        sendMessage(muus, context.bot, update.message)
        return
    need = mus
    iu = need.split(" ")
    if int(len(iu)) > 10:
        muuss = f"Maximum No. Of Dump Channels Allowed: 10 \n\nGiven: {len(iu)} "
        sendMessage(muuss, context.bot, update.message)
        return
    myl = DbManger().add_dumps(uid, iu)
    DUMP_DICT[uid] = iu
    sendMessage(f"Successfully added your Dump IDs \n\nID: <code>{iu}</code>. \n\n<b>Note:</b> Make Sure that @TheEdithXBot is Admin in Your Channel with Sufficient Rights.", context.bot, update.message)

def rm_dump(update, context):
    uid = update.message.from_user.id
    prev = DUMP_DICT[uid]
    myl = DbManger().rm_dumps(uid)
    del DUMP_DICT[uid]
    sendMessage(f"Removed Dump Channel IDs \n\n{prev}", context.bot, update.message)


add_dump_handler = CommandHandler("add_dump", add_dump, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(add_dump_handler)
rm_dump_handler = CommandHandler("rm_dump", rm_dump, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(rm_dump_handler)
