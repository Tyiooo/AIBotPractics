from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from app.generators import gptTurbo
from aiogram.fsm.context import FSMContext

router = Router()

class Generate(StatesGroup):
    text = State()
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(f'Привет, {message.from_user.first_name}. Напиши свой запрос')
    await state.clear()

@router.message(F.text)
async def generate(message: Message, state: FSMContext):
    await state.set_state(Generate.text)
    response = await gptTurbo(message.text)
    await message.answer(response.choices[0].message.content)
    await state.clear()

@router.message(Generate.text)
async def generate_error(message: Message):
    await message.answer('Подождите, ваше сообщение все еще генерируется...')



# @router.message(F.text == 'Как дела?')
# async def how_are_you(message: Message):
#     await message.answer('Good!')
#
# @router.message(F.photo)
# async def how_are_you(message: Message):
#     await message.answer(f'ID фото: {message.photo[-1].file_id}')
#
# @router.message(Command('get_photo'))
# async def how_are_you(message: Message):
#     await message.answer_photo(photo='AgACAgIAAxkBAAMTZpEJTbQc2Xf_encxsRH8y5m6oV8AAljlMRvcvIlItm1dFsBjnW4BAAMCAAN4AAM1BA',
#                                caption='Это кнопка загрузки')
#
# @router.callback_query(F.data == 'catalog')
# async def catalog(callback: CallbackQuery):
#     await callback.answer('Вы выбрали каталог!', show_alert=True)
#     await callback.message.edit_text('Hello!', reply_markup=await kb.inline_cars())
