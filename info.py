questionnaire_name = 'Какой ты программист?'

questions = [
    {
        'question': 'Ты гуляешь по выходным?',
        'answers': [
            {
                'text': 'Да',
                'estimates': [
                    {
                        'category': 'c1',
                        'rating': 2
                    },
                    {
                        'category': 'c4',
                        'rating': 2
                    },
                ],
            },
            {
                'text': 'Скорее да',
                'estimates': [
                    {
                        'category': 'c4',
                        'rating': 1
                    },
                ],
            },
            {
                'text': 'Затрудняюсь ответить',
                'estimates': []
            },
            {
                'text': 'Скорее нет',
                'estimates': [
                    {
                        'category': 'c2',
                        'rating': 1
                    },
                ],
            },
            {
                'text': 'Нет',
                'estimates': [
                    {
                        'category': 'c3',
                        'rating': 1
                    },
                    {
                        'category': 'c2',
                        'rating': 2
                    },
                ],
            },
        ],
    },
    {
        'question': 'У тебя есть график?',
        'answers': [
            {
                'text': 'Да',
                'estimates': [
                    {
                        'category': 'c4',
                        'rating': 2
                    },
                ],
            },
            {
                'text': 'Нет',
                'estimates': [
                    {
                        'category': 'c5',
                        'rating': 2
                    },
                    {
                        'category': 'c3',
                        'rating': 2
                    },
                    {
                        'category': 'c2',
                        'rating': 1
                    },
                ],
            },
        ],
    },
    {
        'question': 'Часто ли ты работаешь в команде?',
        'answers': [
            {
                'text': 'Часто',
                'estimates': [
                    {
                        'category': 'c4',
                        'rating': 2
                    },
                    {
                        'category': 'c1',
                        'rating': 2
                    },
                ],
            },
            {
                'text': 'Редко',
                'estimates': [
                    {
                        'category': 'c2',
                        'rating': 2
                    },
                ],
            },
        ],
    },
    {
        'question': 'Оставляешь ли ты работу на последний день?',
        'answers': [
            {
                'text': 'Оставляю',
                'estimates': [
                    {
                        'category': 'c5',
                        'rating': 2
                    },
                ],
            },
            {
                'text': 'Иногда',
                'estimates': [],
            },
            {
                'text': 'Никогда',
                'estimates': [
                    {
                        'category': 'c4',
                        'rating': 2
                    },
                ],
            },
        ],
    },
    {
        'question': 'Много ты уделяешь времени работе?',
        'answers': [
            {
                'text': 'Много',
                'estimates': [
                    {
                        'category': 'c3',
                        'rating': 2
                    },
                    {
                        'category': 'c1',
                        'rating': 2
                    },
                ],
            },
            {
                'text': 'Мало',
                'estimates': [],
            },
        ],
    },
]

answers_categories = {
    'c1': 'Общительный',
    'c2': 'Закрытый',
    'c3': 'Работаешь на износ',
    'c4': 'Распределяешь нагрузку',
    'c5': 'Делаешь всё в последний день',
}


def get_questionnaire_name():
    return questionnaire_name


def get_questions():
    return questions


def get_answers_categories():
    return answers_categories
