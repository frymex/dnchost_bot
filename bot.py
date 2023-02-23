import requests
from aiogram import Bot, Dispatcher, executor, types

__token__ = 'bot_token'

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ContentTypes

bot = Bot(token=__token__, parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands='start')
async def on_start(msg: types.Message):
    await msg.answer('🛡️ Добро пожаловать.\n\n'
                     'Мы позволим загрузить выши файлы на супер-защищенные сервера Discord без потери качества\n\n'
                     '<code>[FREE_LIMIT: 50 MB]</>\n\n'
                     '👇 Просто отправь файл любого формата из перечисленных и мы отправим вам ссылку \n'
                     '[.css, .js, .html, .py, .zip, .7z, .rar, .mp4, .jpg, .png]')


@dp.message_handler(content_types=ContentTypes.all())
async def upload_(msg: types.Message):

    if msg.content_type in ['document', 'photo', 'video']:
        if msg.content_type == 'photo':
            _url = await msg.photo[-1].get_url()
            _name = f'{msg.message_id}.jpg'
        elif msg.content_type == 'video':
            _url = await msg.video[-1].get_url()
            _name = f'{msg.message_id}.mp4'

        elif msg.content_type == 'document':
            _url = await msg.document.get_url()
            _name = msg.document.file_name

        message = await msg.reply('📖 Читаем ваш файл, и загружаем на наши сервера')
        _bytes = requests.get(_url).content
        await message.edit_text(
            '⌛ Загружаем ваш файл на наши сервера...'
        )

        _upload = requests.post(
            url='https://dnchost.cloud/api/v3/upload',
            files={'file': (_name, _bytes)},
            data={"decode_version": 1},
        ).json()
        if _upload.get('uploaded'):
            await message.edit_text(f'✅ Файл успешно загружен\n\n'
                                    f'{_upload["uploaded"]["download_url"]}')
        else:
            await msg.answer('Error')


if __name__ == '__main__':
    executor.start_polling(dp)
