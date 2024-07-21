import os
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from app.generators import gpt_turbo
from dotenv import load_dotenv
from app.generators import client

load_dotenv()
router = Router()

class Generate(StatesGroup):
    text = State()
    voice = State()

def text_to_speech(file_id, msg):
    response_audio = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=msg
    )
    response_audio.stream_to_file(f'bot_voices/{file_id}.mp3')

def transcribe_audio(audio_file_path):
    with open(audio_file_path, 'rb') as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcription.text


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.reply(f'Привет, {message.from_user.first_name}. Напиши свой запрос!')
    await state.clear()


@router.message(Generate.text)
async def generate_error(message: Message):
    await message.answer('Подождите, ваше сообщение все еще генерируется...')


@router.message(F.text)
async def generate(message: Message, state: FSMContext):
    await state.set_state(Generate.text)
    response = await gpt_turbo(message.text)
    await message.answer(response)
    await state.clear()


@router.message(F.voice)
async def get_audio(message: Message, bot: Bot, state: FSMContext):
    await state.set_state(Generate.voice)

    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    os.makedirs('user_voices', exist_ok=True)
    await bot.download_file(file_path, f'user_voices/{file_id}.mp3')

    result = transcribe_audio(f'user_voices/{file_id}.mp3')
    response = await gpt_turbo(result)

    text_to_speech(file_id, response)

    audio_file = FSInputFile(f'bot_voices/{file_id}.mp3')
    await bot.send_voice(message.from_user.id, voice=audio_file)

    os.remove(f'user_voices/{file_id}.mp3')
    os.remove(f'bot_voices/{file_id}.mp3')

    await state.clear()
