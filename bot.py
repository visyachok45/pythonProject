import logging
from aiogram import Bot, Dispatcher, executor, types
import aiogram.dispatcher.filters as filters
import json
import os.path


bot = Bot(token="5212658093:AAFJRwcIchnRJBUkS5JgoX7PavZ94B9uQ8Q")
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

users = {} # Хранит состояние пользователей

diary = {} # переменная для зранения дневников
# Дневники хранятся в виде
# {'1012736210': {
# 	{'24.04.2022': {
# 		'Провел день - ': 'Отлично!', 
# 		'Чем занимался - ': 'Занимался спортом',
#       'Сон - ': 'Бессонница',
# 		'Описание дня - ': 'Пробежал 1000 км'}
# 	}
# }}


mood = ["Супер", "Хорошо", "Так себе", "Плохо", "Ужасно"]
step = ["Учился", "Занимался спортом", "Работал", "Мучал людей", "Отдыхал"]
sleep = ["Хороший сон"]
look = ["Посмотреть дневник",]


def add_note(user_id,note_date):
    user = diary.get(user_id)
    if user == None:
        diary[str(user_id)] = {}
    today_note = diary[str(user_id)].get(note_date)
    if today_note == None:
        diary[str(user_id)][note_date] = {}


@dp.message_handler(filters.CommandStart())
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    users[str(user_id)] = {}
    users[str(user_id)]["state"] = "INPUT_DATE"
    print(user_id)
    await message.answer("Привет! Введи дату заметки в виде дд.мм.гггг", reply_markup=types.ReplyKeyboardRemove())


# Обработчик введеных дат    
IMAGE_REGEXP = r'(\d{2}).(\d{2}).(\d{4})'


@dp.message_handler(filters.Regexp(IMAGE_REGEXP))
async def input_date(message: types.Message):
    in_date = message.text
    user_id = message.from_user.id

    user = users.get(str(user_id))
    if user == None:
        state = "FINISH"
    else:
        state = user["state"]

    if state == "INPUT_DATE":
        add_note(str(user_id), in_date)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*mood)
        await message.answer("Привет! Как прошел твой день?", reply_markup=keyboard)
        users[str(user_id)]["state"] = "INPUT_DAY_SPENT"
        users[str(user_id)]["date"] = in_date
    elif state == "INPUT_DIARY_DATE":
        user_diary = diary.get(str(user_id))
        if user_diary == None:
            mess = "Нет записей в дневнике"
        else:
            user_diary_day = user_diary.get(in_date)
            if user_diary_day == None:
                mess = "Нет записи в дневнике на эту дату"
            else:
                mess = f"Дата {in_date} \n"
                for note in user_diary[in_date]:
                    mess += f"     {note}{user_diary[in_date][note]} \n"
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*look)
        keyboard.add("/start")
        await message.answer(mess, reply_markup=keyboard)
        users[str(user_id)]["state"] = "FINISH"
    else:
        await message.reply("Неверный ввод")
        return


@dp.message_handler(filters.Text(contains="Супер"))
async def fine(message: types.Message):
    user_id = message.from_user.id
    user = users.get(str(user_id))
    if user == None:
        state = "FINISH"
    else:
        state = user["state"]
    if state != "INPUT_DAY_SPENT":
        await message.reply("Неверный ввод")
        return
    diary[str(user_id)][user["date"]]["Провел день - "] = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*step)
    await message.reply("Я так рад за тебя! Выбери занятие, которое олицетворяет твой день:", reply_markup=keyboard)
    users[str(user_id)]["state"] = "INPUT_WHATDO"


@dp.message_handler(filters.Text(contains="Хорошо"))
async def good(message: types.Message):
    user_id = message.from_user.id
    user = users.get(str(user_id))
    if user == None:
        state = "FINISH"
    else:
        state = user['state']
    if state != "INPUT_DAY_SPENT":
        await message.reply("Неверный ввод")
        return
    diary[str(user_id)][user["date"]]["Провел день - "] = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*step)
    await message.reply("Это здорово! Выбери занятие, которое олицетворяет твой день:", reply_markup=keyboard)
    users[str(user_id)]["state"] = "INPUT_WHATDO"


@dp.message_handler(filters.Text(contains="Так себе"))
async def bad(message: types.Message):
    user_id = message.from_user.id
    user = users.get(str(user_id))
    if user == None:
        state = "FINISH"
    else:
        state = user['state']
    if state != "INPUT_DAY_SPENT":
        await message.reply("Неверный ввод")
        return
    diary[str(user_id)][user["date"]]["Провел день - "] = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*step)
    await message.reply("Не расстраивайся! Выбери занятие, которое олицетворяет твой день:", reply_markup=keyboard)
    users[str(user_id)]["state"] = "INPUT_WHATDO"


@dp.message_handler(filters.Text(contains="Плохо"))
async def good(message: types.Message):
    user_id = message.from_user.id
    user = users.get(str(user_id))
    if user == None:
        state = "FINISH"
    else:
        state = user['state']
    if state != "INPUT_DAY_SPENT":
        await message.reply("Неверный ввод")
        return
    diary[str(user_id)][user["date"]]["Провел день - "] = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*step)
    await message.reply("Не грусти сильно. Выбери занятие, которое олицетворяет твой день:", reply_markup=keyboard)
    users[str(user_id)]["state"] = "INPUT_WHATDO"


@dp.message_handler(filters.Text(contains="Ужасно"))
async def good(message: types.Message):
    user_id = message.from_user.id
    user = users.get(str(user_id))
    if user == None:
        state = "FINISH"
    else:
        state = user['state']
    if state != "INPUT_DAY_SPENT":
        await message.reply("Неверный ввод")
        return
    diary[str(user_id)][user["date"]]["Провел день - "] = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*step)
    await message.reply("Давай исправим твое состояние. Выбери занятие, которое олицетворяет твой день:", reply_markup=keyboard)
    users[str(user_id)]["state"] = "INPUT_WHATDO"


@dp.message_handler(filters.Text(equals=step))
async def learn(message: types.Message):
    user_id = message.from_user.id
    user = users.get(str(user_id))
    if user == None:
        state = "FINISH"
    else:
        state = user['state']
    if state != "INPUT_WHATDO":
        await message.reply("Неверный ввод")
        return
    diary[str(user_id)][user["date"]]["Чем занимался - "] = message.text
    await message.reply("Как тебе спалось?", reply_markup=types.ReplyKeyboardRemove())
    users[str(user_id)]["state"] = "INPUT_DAY_DESCR"


@dp.message_handler(filters.Text(contains="Хороший сон"))
async def good(message: types.Message):
    user_id = message.from_user.id
    user = users.get(str(user_id))
    if user == None:
        state = "FINISH"
    else:
        state = user['state']
    if state != "INPUT_DAY_SPENT":
        await message.reply("Неверный ввод")
        return
    diary[str(user_id)][user["date"]]["Сон - "] = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*sleep)
    await message.reply("Отлично! Какая сегодня была погодка?", reply_markup=keyboard)
    users[str(user_id)]["state"] = "INPUT_SLEEP"


@dp.message_handler(filters.Text(contains="весь"))
async def print_diary(message: types.Message):
    user_id = message.from_user.id
    user_diary = diary.get(str(user_id))
    if user_diary == None:
        mess = "Нет записей в дневнике"
    else:
        mess = ""
        for date in user_diary:
            mess += f"Дата {date} \n"
            for note in user_diary[date]:
                mess += f"     {note}{user_diary[date][note]} \n"
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*look)
    keyboard.add("/start")
    await message.answer(mess, reply_markup=keyboard)
    users[str(user_id)]["state"] = "FINISH"


@dp.message_handler(filters.Text(contains="Посмотреть дневник"))
async def look_diary(message: types.Message):
    user_id = message.from_user.id
    user = users.get(str(user_id))
    if user == None:
        state = "FINISH"
    else:
        state = user['state']
    if state != "FINISH":
        await message.reply("Неверный ввод")
        return
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.add("весь")
    await message.reply("Введи дату заметки в виде дд.мм.гггг)", reply_markup=keyboard)
    users[str(user_id)]["state"] = "INPUT_DIARY_DATE"


@dp.message_handler()
async def any_text_message(message: types.Message):
    user_id = message.from_user.id
    user = users.get(str(user_id))
    if user == None:
        state = "FINISH"
    else:
        state = user['state']
    if state != "INPUT_DAY_DESCR":
        await message.answer("Неверный ввод")
        return    
    diary[str(user_id)][user["date"]]["Описание дня - "] = message.text
    # Сохраняем дневники в формате json
    with open('diary.json', 'w') as outfile:
        json.dump(diary, outfile)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*look)
    keyboard.add("/start")
    await message.answer("Ваш день успешно добавлен в дневник! До скорых встреч)", reply_markup=keyboard)
    users[str(user_id)]["state"] = "FINISH"


if __name__ == "__main__":
    # Открываем файл с дневниками
    if os.path.exists('diary.json'): 
        with open('diary.json') as json_file:
            diary = json.load(json_file)
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)