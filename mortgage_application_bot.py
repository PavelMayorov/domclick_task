import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import executor

API_TOKEN = '' # Введите ваш Токен

# Инициализируем бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)
loan_amount = 0


class LoanApplication(StatesGroup):
    LoanAmount = State()


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply(
        "Приветствую! Я бот для подачи заявки на ипотеку. "
        "Введите запрашиваемую сумму кредита:")


@dp.message_handler(regexp='^[0-9]+$')
async def process_loan_amount(message: types.Message, state: FSMContext):
    global loan_amount
    loan_amount = int(message.text)
    await message.reply("Введите сумму первоначального взноса:")
    await LoanApplication.LoanAmount.set()
    await bot.send_message(chat_id=message.chat.id,
                           text="Сумма первоначального взноса должна быть не "
                                "меньше 15% от запрашиваемой суммы кредита.")


@dp.message_handler(lambda message: message.text,
                    state=LoanApplication.LoanAmount)
async def process_down_payment(message: types.Message, state: FSMContext):
    global loan_amount
    if loan_amount * 0.15 > int(message.text):
        await message.reply("Необходимо указать бОльший первоначальный взнос.")
    else:
        await message.answer(
            "Вы можете подать онлайн-заявку на ипотеку на сайте "
            "https://domclick.ru/ipoteka/programs/onlajn-zayavka.")
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
