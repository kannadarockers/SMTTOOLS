from pyrogram import Client, filters, enums
from info import FILE_STORE_CHANNEL
from database.ia_filterdb import save_file

@Client.on_message(filters.chat(FILE_STORE_CHANNEL))
async def auto_index(client, message):

    if not message.media:
        return

    if message.media not in [
        enums.MessageMediaType.DOCUMENT,
        enums.MessageMediaType.VIDEO,
        enums.MessageMediaType.AUDIO
    ]:
        return

    media = getattr(message, message.media.value)

    if not media:
        return

    media.file_type = message.media.value
    media.caption = message.caption

    await save_file(media)
