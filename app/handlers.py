from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from app.generators import gptTurbo
from aiogram.fsm.context import FSMContext
import whisper

router = Router()

class Generate(StatesGroup):
    text = State()
    voice = State()
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(f'Привет, {message.from_user.first_name}. Напиши свой запрос')
    await state.clear()
@router.message(Generate.text)
async def generate_error(message: Message):
    await message.answer('Подождите, ваше сообщение все еще генерируется...')

@router.message(F.text)
async def generate(message: Message, state: FSMContext):
    await state.set_state(Generate.text)
    response = await gptTurbo(message.text)
    await message.answer(response.choices[0].message.content)
    await state.clear()
@router.message(F.voice)
async def get_audio(message: Message, bot: Bot, state: FSMContext):
    await state.set_state(Generate.voice)

    model = whisper.load_model('base')

    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(file_path, f'userVoices/{file_id}.mp3')

    result = model.transcribe(f'userVoices/{file_id}.mp3', fp16=False)
    response = await gptTurbo(result['text'])
    await message.answer(response.choices[0].message.content)

    await state.clear()

