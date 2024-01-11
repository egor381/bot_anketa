import os
import telebot
from telebot import types
from dotenv import load_dotenv
from questionnaires import *

load_dotenv()
token = os.getenv('TOKEN')
if not token:
    raise Exception('Не задана переменная окружения TOKEN')

bot = telebot.TeleBot(token)
questionnaires = Questionnaires()


def response_start(message):
    bot.send_message(message.chat.id,
                     text=f'Привет {message.from_user.first_name}, '
                          f'приступим к заполнению анкеты "{questionnaires.get_questionnaire_name()}"'
                     )

    start_questionnaire(message.chat.id)


def response_help(message):
    bot.send_message(message.chat.id,
                     parse_mode='MarkdownV2',
                     text='Для работы со мной вы можете использовать одну из команд:\n\n' +
                          commands_to_string()
                     )


def unknown_state(chat_id):
    bot.send_message(chat_id,
                     text='Сожалею, но что-то пошло не так. Попробуйте позже😢'
                     )


commands = [
    {
        'command': '/start',
        'description': 'начало заполнения анкеты',
        'keywords': ['start', 'старт', 'поехали'],
        'handler': response_start
    },
    {
        'command': '/help',
        'description': 'перечень поддерживаемых мной команд',
        'keywords': ['help', 'помощь', 'справка'],
        'handler': response_help
    },
]


def commands_to_string():
    result = ''
    for command in commands:
        if command['command'] and command['description']:
            result += f"*{command['command']}* \\- {command['description']}\n"
    return result


def process_command(message, text):
    is_processed = False
    for command in commands:
        handler = None
        if command['command'] == text.lower():
            handler = command['handler']
        else:
            keywords = command['keywords']
            for keyword in keywords:
                if keyword in text.lower():
                    handler = command['handler']
        if handler:
            handler(message)
            is_processed = True
    return is_processed


def process_answer(message, text):
    is_processed = questionnaires.process_answer(message.chat.id, text)
    if is_processed:
        next_question(message.chat.id)
    return is_processed


def create_question(chat_id):
    questionnaire = questionnaires.get_questionnaire(chat_id)
    if questionnaire:
        current_question = questionnaire.get_current_question()
        if current_question:
            markup = types.ReplyKeyboardRemove()
            if 'answers' in current_question:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                for answer in current_question['answers']:
                    markup.add(
                        types.KeyboardButton(answer['text'])
                    )

            bot.send_message(chat_id,
                             text=current_question['question'],
                             reply_markup=markup
                             )
    else:
        unknown_state(chat_id)


def create_result(chat_id):
    questionnaire = questionnaires.get_questionnaire(chat_id)
    if questionnaire:
        bot.send_message(chat_id,
                         text='Анкета заполнена, подсчитываю результаты',
                         reply_markup=types.ReplyKeyboardRemove()
                         )
        bot.send_message(chat_id, text=questionnaire.get_result_string())
        bot.send_photo(chat_id, photo=questionnaire.get_result_image())
    else:
        unknown_state(chat_id)


def start_questionnaire(chat_id):
    if questionnaires.start_questionnaire(chat_id):
        next_question(chat_id)
    else:
        unknown_state(chat_id)


def next_question(chat_id):
    if questionnaires.next_question(chat_id):
        create_question(chat_id)
    else:
        create_result(chat_id)
        questionnaires.finish_questionnaire(chat_id)


def process_message(message, text):
    if not process_command(message, text) and not process_answer(message, text):
        bot.send_message(message.chat.id,
                         parse_mode='MarkdownV2',
                         text=f'К сожалению я не понял вас, попробуйте уточнить свой запрос\n' +
                              'Я понимаю следующие команды:\n\n' +
                              commands_to_string()
                         )


@bot.message_handler(content_types=['text'])
def text_message(message):
    process_message(message, message.text)


@bot.message_handler(content_types=['sticker'])
def media_message(message):
    bot.send_message(message.chat.id, text='Классный стикер👍')


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    process_message(call.message, call.data)
    bot.answer_callback_query(call.id)


menu_commands = []
for command in commands:
    if command['command'] and command['description']:
        menu_commands.append(telebot.types.BotCommand(command['command'], command['description']))

try:
    bot.set_my_commands(menu_commands)
    bot.polling(non_stop=True)
except Exception as e:
    raise Exception(f'Ошибка обращения к Telegram, {e}')
