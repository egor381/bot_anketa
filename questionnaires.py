from info import get_questionnaire_name, get_questions, get_answers_categories
import matplotlib as mpl
import matplotlib.pyplot as plt
from io import BytesIO
import json

mpl.use('agg')


class Questionnaire:
    def __init__(self):
        self.question_index = -1
        self.person_answers = {}

    def get_state(self):
        return {
            'question_index': self.question_index,
            'person_answers': self.person_answers
        }

    def set_state(self, state):
        if 'question_index' in state:
            self.question_index = state['question_index']
        if 'person_answers' in state:
            self.person_answers = state['person_answers']

    def next_question(self):
        questions = get_questions()
        if -1 <= self.question_index < len(questions) - 1:
            self.question_index += 1
            return questions[self.question_index]
        else:
            return None

    def get_current_question(self):
        questions = get_questions()
        if 0 <= self.question_index <= len(questions) - 1:
            return questions[self.question_index]
        else:
            return None

    def clear(self):
        self.question_index = -1
        self.person_answers = {}

    def add_result(self, category, rating):
        if category not in self.person_answers:
            self.person_answers[category] = 0
        self.person_answers[category] += rating

    def get_result_string(self):
        result = ''
        for category, rating in self.person_answers.items():
            if result:
                result += '\n'
            result += get_answers_categories()[category] + ': ' + str(rating)
        result = f'Оценка прохождения анкеты "{get_questionnaire_name()}", в баллах\n' + result
        return result

    def get_result_image(self):
        data_names = []
        data_values = []
        for category, rating in self.person_answers.items():
            data_names.append(get_answers_categories()[category])
            data_values.append(rating)

        dpi = 80
        plt.figure(dpi=dpi, figsize=(640 / dpi, 480 / dpi))
        mpl.rcParams.update({'font.size': 9})

        plt.title(f'Оценка прохождения анкеты "{get_questionnaire_name()}", в процентах')
        plt.pie(
            data_values,
            autopct='%.1f',
            radius=1.1,
            explode=[0.01 for _ in range(len(data_names))]
        )
        plt.legend(
            loc='lower left',
            bbox_to_anchor=(-0.25, 0.0),
            labels=data_names
        )

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()
        image = buffer.getvalue()
        buffer.close()

        return image


class Questionnaires:
    def __init__(self):
        self.questionnaires = {}
        self.load_state()

    @staticmethod
    def get_questionnaire_name():
        return get_questionnaire_name()

    def start_questionnaire(self, chat_id):
        if chat_id not in self.questionnaires:
            self.questionnaires[chat_id] = Questionnaire()
        self.questionnaires[chat_id].clear()
        self.save_state()
        return self.questionnaires[chat_id]

    def finish_questionnaire(self, chat_id):
        if chat_id in self.questionnaires:
            del self.questionnaires[chat_id]
        self.save_state()

    def get_questionnaire(self, chat_id):
        if chat_id in self.questionnaires:
            return self.questionnaires[chat_id]
        else:
            return None

    def next_question(self, chat_id):
        question = None
        questionnaire = self.get_questionnaire(chat_id)
        if questionnaire:
            question = questionnaire.next_question()
            self.save_state()
        return question

    def process_answer(self, chat_id, text):
        is_processed = False

        questionnaire = self.get_questionnaire(chat_id)
        if questionnaire:
            current_question = questionnaire.get_current_question()
            if current_question:
                for answer in current_question['answers']:
                    if answer['text'].lower() == text.lower():
                        for estimate in answer['estimates']:
                            questionnaire.add_result(estimate['category'], estimate['rating'])
                        is_processed = True

        return is_processed

    def load_state(self):
        state = None
        try:
            with open('storage.json', 'r') as f:
                state = json.load(f)
        except (IOError, json.decoder.JSONDecodeError) as e:
            print(f'Ошибка восстановлении состояния анкет, {e}')

        if state:
            print('load_state: ' + str(state))
            for item in state:
                chat_id = item['chat_id']
                if chat_id not in self.questionnaires:
                    self.questionnaires[chat_id] = Questionnaire()
                self.questionnaires[chat_id].set_state(item['questionnaire'])

    def save_state(self):
        state = []
        for chat_id in self.questionnaires:
            questionnaire = self.questionnaires[chat_id]
            state.append({
                'chat_id': chat_id,
                'questionnaire': questionnaire.get_state()
            })
        print('save_state: ' + str(state))

        try:
            with open('storage.json', 'w') as f:
                json.dump(state, f)
        except IOError as e:
            print(f'Ошибка сохранения состояния анкеты, {e}')
