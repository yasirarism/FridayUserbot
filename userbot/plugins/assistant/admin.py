from telethon import events, custom, Button
from telethon.tl.types import (
    Channel,
    Chat,
    User
)

import emoji
from googletrans import Translator
from userbot.utils import admin_cmd, edit_or_reply, sudo_cmd
from telethon.utils import get_display_name
from userbot.utils import admin_cmd, sudo_cmd
from userbot.uniborgConfig import Config
from telethon import events
from datetime import datetime
from userbot.utils import admin_cmd, edit_or_reply, sudo_cmd
import time
from userbot import Lastupdate, bot

from asyncio import sleep
from os import remove

from telethon.errors import (
    BadRequestError,
    ChatAdminRequiredError,
    ImageProcessFailedError,
    PhotoCropSizeSmallError,
    UserAdminInvalidError,
)
from telethon.errors.rpcerrorlist import MessageTooLongError, UserIdInvalidError
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChatAdminRights,
    ChatBannedRights,
    MessageEntityMentionName,
    MessageMediaPhoto,
)

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.utils import admin_cmd, errors_handler, register, sudo_cmd

# =================== CONSTANT ===================
PP_TOO_SMOL = "`The image is too small`"
PP_ERROR = "`Failure while processing the image`"
NO_ADMIN = "`I am not an admin nub nibba!`"
NO_PERM = (
    "`I don't have sufficient permissions! This is so sed. Alexa play Tera Baap Aaya`"
)
NO_SQL = "`Running on Non-SQL mode!`"

CHAT_PP_CHANGED = "`Chat Picture Changed`"
CHAT_PP_ERROR = (
    "`Some issue with updating the pic,`"
    "`maybe coz I'm not an admin,`"
    "`or don't have enough rights.`"
)
INVALID_MEDIA = "`Invalid Extension`"

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)

UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)





@tgbot.on(events.NewMessage(pattern="^/ban(?: |$)(.*)"))
async def ban(event):
    """ For .ban command, bans the replied/tagged person """
    # Here laying the sanity check
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await event.reply(NO_ADMIN)
        return

    user, reason = await get_user_from_event(event)
    if user:
        pass
    else:
        return

    # Announce that we're going to whack the pest
    await event.reply("`Whacking the pest!`")

    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS))
    except BadRequestError:
        await event.reply(NO_PERM)
        return
    # Helps ban group join spammers more easily
    try:
        reply = await event.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        await event.reply("`I dont have message nuking rights! But still he was banned!`")
        return
    # Delete message and then tell that the command
    # is done gracefully
    # Shout out the ID, so that fedadmins can fban later
    if reason:
        await event.reply(f"Loser `{str(user.id)}` was banned !!\nReason: {reason}")
    else:
        await event.reply(f"Bitch `{str(user.id)}` was banned !!")


@tgbot.on(events.NewMessage(pattern="^/ban(?: |$)(.*)"))
async def nothanos(event):
    """ For .unban command, unbans the replied/tagged person """
    # Here laying the sanity check
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Well
    if not admin and not creator:
        await event.reply(NO_ADMIN)
        return

    # If everything goes well...
    await event.reply("`Unbanning...`")

    user = await get_user_from_event(event)
    user = user[0]
    if user:
        pass
    else:
        return

    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS))
        await event.reply("```Unbanned Successfully. Granting another chance.```")
    except UserIdInvalidError:
        await event.reply("`Uh oh my unban logic broke!`")
