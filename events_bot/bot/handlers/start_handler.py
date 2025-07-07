from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from events_bot.database.services import UserService
from events_bot.bot.states import UserStates
from events_bot.bot.keyboards import get_city_keyboard, get_main_keyboard
from events_bot.bot.utils import get_db_session

router = Router()

def register_start_handlers(dp: Router):
    """Регистрация обработчиков команды start"""
    dp.include_router(router)

@router.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    """Обработчик команды /start"""
    async with get_db_session() as db:
        # Регистрируем пользователя
        user = await UserService.register_user(
            db=db,
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name
        )
        
        # Проверяем, есть ли у пользователя город
        if not user.city:
            await message.answer(
                "👋 Добро пожаловать в Events Bot!\n\n"
                "Для начала работы выберите ваш город:",
                reply_markup=get_city_keyboard()
            )
            await state.set_state(UserStates.waiting_for_city)
        else:
            await message.answer(
                f"👋 С возвращением, {user.first_name or user.username or 'пользователь'}!\n\n"
                "Выберите действие:",
                reply_markup=get_main_keyboard()
            ) 