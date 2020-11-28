# основной файл бота
import settings
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, callback_query
from aiogram.utils import executor
from aiogram.utils.deep_linking import get_start_link, decode_payload
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import messages
import buttons
from models import User, Vacancy, create_tables, Candidate
from fuzzywuzzy import fuzz
from collections import OrderedDict
from operator import itemgetter
import parser_from_pdf
import json

bot = Bot(settings.token)
storage = MemoryStorage()  # внутреннее хранилище бота, позволяющее отслеживать FMS (Finite State Maschine)
dp = Dispatcher(bot, storage=storage)


class VacancyState(StatesGroup):
    name = State()
    specialization = State()
    description = State()
    key_skills = State()
    income = State()


class FindVacancy(StatesGroup):
    name = State()
    id = State()
    resume = State()


class AddTaskState(StatesGroup):
    vacancy_id = State()
    file = State()


class SendTaskSolution(StatesGroup):
    vacancy_id = State()
    candidate_id = State()
    file = State()

class CheckUsername(StatesGroup):
    user_id = State()
    payload = State()


@dp.message_handler(commands='start', state=VacancyState)
@dp.message_handler(commands='start', state=FindVacancy)
@dp.message_handler(commands='start', state=SendTaskSolution)
@dp.message_handler(commands='start', )
async def start_handler(message: types.Message, state: FSMContext):
    if state:
        await state.finish()
    text = message.text.split(' ')
    if len(text) > 1:
        payload = decode_payload(text[1])
        vacancy_id = int(payload)
        if not message.from_user.username:
            await CheckUsername.payload.set()
            await state.update_data(payload=vacancy_id)
            await state.update_data(user_id=message.from_user.id)
            await set_username(message.chat.id)
            return
        user = User.get_or_none(User.chat_id == message.chat.id)
        if not user:
            user = User(username=message.from_user.username,
                        first_name=message.from_user.first_name,
                        second_name=message.from_user.last_name,
                        chat_id=message.chat.id)
            user.save()
        # await FindVacancy.name.set()
        await show_vacancy_pure(message.chat.id, vacancy_id)
    else:
        user = User.get_or_none(User.chat_id == message.chat.id)
        if not user:
            user = User(username=message.from_user.username,
                        first_name=message.from_user.first_name,
                        second_name=message.from_user.last_name,
                        chat_id=message.chat.id)
            user.save()
            await message.answer(messages.start_message)

        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(buttons.create_vacancy, callback_data='create_vacancy'),
                     # InlineKeyboardButton(buttons.find_vacancies, callback_data='find_vacancies')
                     )
        vacancies = Vacancy.select().where(Vacancy.creator == User.get(User.chat_id == message.chat.id))
        if vacancies:
            keyboard.add(InlineKeyboardButton(buttons.placed_vacancies, callback_data='placed_vacancies'))

        candidate = Candidate.select().where(Candidate.user == User.get(User.chat_id == message.chat.id))
        for i in candidate:
            if i.status == 'Отправлено тестовое задание':
                keyboard.add(InlineKeyboardButton(buttons.test_task.format(i.vacancy.name),
                                                  callback_data=f'send_test_task_solution_{i.vacancy.id}'))

        await message.answer(messages.menu, reply_markup=keyboard)


async def set_username(chat_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(buttons.i_set, callback_data='i_set'))
    await bot.send_message(chat_id, messages.set_username, reply_markup=keyboard)

@dp.callback_query_handler(text='i_set', state=CheckUsername)
async def check_username(query: callback_query, state: FSMContext):
    async with state.proxy() as s:
        user = await bot.get_chat_member(query.message.chat.id, s['user_id'])
        if user.user.username:
            await query.message.answer(messages.username_set.format(await get_start_link(s['payload'], encode=True)))
        else:
            await set_username(query.message.chat.id)

@dp.callback_query_handler(text='menu', state=VacancyState)
@dp.callback_query_handler(text='menu', state=FindVacancy)
@dp.callback_query_handler(text='menu', state=SendTaskSolution)
@dp.callback_query_handler(text='menu')
async def menu(query: callback_query, state: FSMContext):
    if state:
        await state.finish()
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(buttons.create_vacancy, callback_data='create_vacancy'),
                 # InlineKeyboardButton(buttons.find_vacancies, callback_data='find_vacancies')
                 )
    vacancies = Vacancy.select().where(Vacancy.creator == User.get(User.chat_id == query.message.chat.id))
    if vacancies:
        keyboard.add(InlineKeyboardButton(buttons.placed_vacancies, callback_data='placed_vacancies'))

    candidate = Candidate.select().where(Candidate.user == User.get(User.chat_id == query.message.chat.id))
    for i in candidate:
        if i.status == 'Отправлено тестовое задание':
            keyboard.add(InlineKeyboardButton(f'Тестовое - {i.vacancy.name}',
                                              callback_data=f'send_test_task_solution_{i.vacancy.id}'))
    await query.message.answer(messages.menu, reply_markup=keyboard)


@dp.callback_query_handler(text='placed_vacancies')
async def placed_vacancies(query: callback_query):
    keyboard = InlineKeyboardMarkup()
    vacancies = Vacancy.select().where(Vacancy.creator == User.get(User.chat_id == query.message.chat.id))
    for i in vacancies:
        keyboard.add(InlineKeyboardButton(f'{i.name} - {i.income} руб.', callback_data=f'vacancy_my_{i.id}'))
    await query.message.answer(messages.placed_vacancies, reply_markup=keyboard)


@dp.callback_query_handler(text_contains=['vacancy_my_'])
async def vacancy_my(query: callback_query):
    vacancy_id = int(query.data.split('_')[2])
    keyboard = InlineKeyboardMarkup()
    vacancy = Vacancy.get(Vacancy.id == vacancy_id)
    keyboard.add(InlineKeyboardButton(buttons.delete_vacancy, callback_data=f'delete_vacancy_{vacancy_id}'))
    if not vacancy.test_task:
        keyboard.add(InlineKeyboardButton(buttons.back, callback_data='vacancy_myback'),
                     InlineKeyboardButton(buttons.add_tasks, callback_data=f'add_task_{vacancy_id}'))
    else:
        keyboard.add(InlineKeyboardButton(buttons.back, callback_data='vacancy_myback'))
    link = await get_start_link(str(vacancy_id), encode=True)
    await query.message.answer(messages.vacancy_template_with_deeplink.format(
                                                                vacancy.name,
                                                                vacancy.specialization,
                                                                vacancy.description,
                                                                vacancy.key_skills,
                                                                vacancy.income,
                                                                link),
                               reply_markup=keyboard)


@dp.callback_query_handler(text_contains=['delete_vacancy_'])
async def delete_vacancy(query: callback_query):
    vacancy_id = int(query.data.split('_')[2])
    Vacancy.delete_by_id(vacancy_id)
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(buttons.menu, callback_data='menu'))

    await query.message.answer(messages.deleted_vacancy, reply_markup=keyboard)

@dp.callback_query_handler(text_contains=['add_task_'])
async def add_task(query: callback_query, state: FSMContext):
    vacancy_id = int(query.data.split('_')[2])
    vacancy = Vacancy.get(Vacancy.id == vacancy_id)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(buttons.back, callback_data='vacancy_myback'))
    await AddTaskState.file.set()
    await state.update_data(vacancy_id=vacancy_id)
    await query.message.answer(messages.send_me_task, reply_markup=keyboard)


@dp.message_handler(content_types=types.ContentTypes.DOCUMENT, state=AddTaskState)
async def add_task_file(message: types.Message, state: FSMContext):
    await state.update_data(file=message.document.file_id)
    async with state.proxy() as s:
        vacancy = Vacancy.get(Vacancy.id == s['vacancy_id'])
        file_path = settings.tasks_path_base + str(s['vacancy_id']) + '_' + message.document.file_name
        await bot.download_file_by_id(s['file'], file_path)
        vacancy.test_task = file_path
        vacancy.save()
    await state.finish()
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(buttons.menu, callback_data='menu'))
    await message.answer(messages.saved_task, reply_markup=keyboard)


@dp.callback_query_handler(text='vacancy_myback')
async def vacancy_myback(query: callback_query, state: FSMContext):
    if state:
        await state.finish()
    await bot.delete_message(query.message.chat.id, query.message.message_id)


@dp.callback_query_handler(text='send_test_task_solutionback', state=SendTaskSolution)
async def send_test_task_solutionback(query: callback_query, state: FSMContext):
    if state:
        await state.finish()
    await bot.delete_message(query.message.chat.id, query.message.message_id)


@dp.callback_query_handler(text_contains=['send_test_task_solution_'])
async def send_test_task_solution(query: callback_query, state: FSMContext):
    vacancy_id = int(query.data.split('_')[4])
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(buttons.back, callback_data='send_test_task_solutionback'))
    await SendTaskSolution.file.set()
    await state.update_data(vacancy_id=vacancy_id)
    candidate = Candidate.select().where(Candidate.user == User.get(User.chat_id == query.message.chat.id)) \
        .where(Candidate.vacancy == Vacancy.get(Vacancy.id == vacancy_id)).where(
        Candidate.status == 'Отправлено тестовое задание').get()
    await state.update_data(candidate_id=candidate.id)
    await query.message.answer(messages.send_me_solution, reply_markup=keyboard)


@dp.message_handler(content_types=types.ContentTypes.DOCUMENT, state=SendTaskSolution)
async def test_task_solution(message: types.Message, state: FSMContext):
    await state.update_data(file=message.document.file_id)
    async with state.proxy() as s:
        file_path = settings.test_task_solution_path_base + str(s['vacancy_id']) + '_' + message.document.file_name
        await bot.download_file_by_id(s['file'], file_path)
        candidate = Candidate.get(Candidate.id == s['candidate_id'])
        candidate.test_task_solution = file_path
    await state.finish()
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(buttons.menu, callback_data='menu'))
    await message.answer(messages.test_task_solution_sent, reply_markup=keyboard)
    candidate.status = 'Выполнил тестовое задание'
    candidate.save()
    await bot.send_document(candidate.vacancy.creator.chat_id, open(file_path, 'rb'),
                            caption=messages.user_made_task.format(candidate.user.username, candidate.vacancy.name))


@dp.callback_query_handler(text='create_vacancy')
async def create_vacancy_handler(query: callback_query):
    await VacancyState.name.set()
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(buttons.menu, callback_data='menu'))
    await bot.send_message(query.message.chat.id, messages.enter_name_vacancy, reply_markup=keyboard)


@dp.message_handler(state=VacancyState.name)
async def vacancy_name_handler(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await VacancyState.next()
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(buttons.menu, callback_data='menu'))
    await message.answer(messages.enter_specialization, reply_markup=keyboard)


@dp.message_handler(state=VacancyState.specialization)
async def vacancy_specialization_handler(message: types.Message, state: FSMContext):
    await state.update_data(specialization=message.text)
    await VacancyState.next()
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(buttons.menu, callback_data='menu'))
    await message.answer(messages.enter_description, reply_markup=keyboard)


@dp.message_handler(state=VacancyState.description)
async def vacancy_description_handler(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await VacancyState.next()
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(buttons.menu, callback_data='menu'))
    await message.answer(messages.enter_key_skills, reply_markup=keyboard)


@dp.message_handler(state=VacancyState.key_skills)
async def vacancy_key_skills_handler(message: types.Message, state: FSMContext):
    await state.update_data(key_skills=message.text)
    await VacancyState.next()
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(buttons.menu, callback_data='menu'))
    await message.answer(messages.enter_income, reply_markup=keyboard)


@dp.message_handler(state=VacancyState.income)
async def vacancy_income_handler(message: types.Message, state: FSMContext):
    await state.update_data(income=message.text)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(buttons.no, callback_data='wrong_vacancy'),
                 InlineKeyboardButton(buttons.yes, callback_data='correct_vacancy'))
    async with state.proxy() as vacancy:
        await message.answer(messages.here_is_your_vacancy.format(vacancy['name'],
                                                                  vacancy['specialization'],
                                                                  vacancy['description'],
                                                                  vacancy['key_skills'],
                                                                  vacancy['income']),
                             reply_markup=keyboard)


@dp.callback_query_handler(text='correct_vacancy', state=VacancyState)
async def correct_vacancy(query: callback_query, state: FSMContext):
    async with state.proxy() as vacancy:
        user = User.get(User.chat_id == query.message.chat.id)
        vacancy_record = Vacancy(creator=user,
                                 name=vacancy['name'],
                                 specialization=vacancy['specialization'],
                                 description=vacancy['description'],
                                 key_skills=vacancy['key_skills'],
                                 income=vacancy['income'], test_task=None)
        vacancy_record.save()

    await state.finish()
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(buttons.menu, callback_data='menu'),
                 InlineKeyboardButton(buttons.create_vacancy, callback_data='create_vacancy'))
    await query.message.answer(messages.vacancy_created, reply_markup=keyboard)


@dp.callback_query_handler(text='wrong_vacancy', state=VacancyState)
async def wrong_vacancy(query: callback_query):
    await VacancyState.name.set()
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(buttons.menu, callback_data='menu'))
    await query.message.answer(messages.enter_name_vacancy, reply_markup=keyboard)


@dp.callback_query_handler(text='find_vacancies')
async def find_vacancies(query: callback_query):
    await FindVacancy.name.set()
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(buttons.menu, callback_data='menu'))
    await query.message.answer(messages.find_vacancies, reply_markup=keyboard)


@dp.message_handler(state=FindVacancy.name)
async def name_find_vacancies(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    async with state.proxy() as find_vacancies_:
        name = find_vacancies_['name']
        rations = {}
        vacanncies = Vacancy.select()
        for i in vacanncies:
            rations[i.id] = fuzz.token_sort_ratio(name, i.name)
    await FindVacancy.next()
    rations = OrderedDict(sorted(rations.items(), key=itemgetter(1), reverse=True))
    keyboard = InlineKeyboardMarkup()
    for i in rations:
        vacancy = Vacancy.get(Vacancy.id == i)
        keyboard.add(InlineKeyboardButton(f'{vacancy.name} - {vacancy.income} руб.',
                                          callback_data=f'vacancy_{i}'))
    await message.answer(messages.what_we_found, reply_markup=keyboard)


@dp.callback_query_handler(text_contains=['vacancy_'], state=FindVacancy)
async def show_vacancy(query: callback_query, state: FSMContext):
    vacancy_id = int(query.data.split('_')[1])
    vacancy = Vacancy.get(Vacancy.id == vacancy_id)
    await state.update_data(id=vacancy_id)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(buttons.additional_information, callback_data='additional_information'))
    keyboard.add(InlineKeyboardButton(buttons.back, callback_data='back_to_find_vacancies'),
                 InlineKeyboardButton(buttons.send_resume, callback_data=f'send_resume_{vacancy_id}'))
    await query.message.answer(messages.vacancy_template.format(vacancy.name,
                                                                vacancy.specialization,
                                                                vacancy.description,
                                                                vacancy.key_skills,
                                                                vacancy.income), reply_markup=keyboard)


async def show_vacancy_pure(chat_id, vacancy_id):
    vacancy = Vacancy.get(Vacancy.id == vacancy_id)
    keyboard = InlineKeyboardMarkup()
    await FindVacancy.id.set()

    keyboard.add(InlineKeyboardButton(buttons.additional_information, callback_data='additional_information'))
    keyboard.add(InlineKeyboardButton(buttons.send_resume, callback_data=f'send_resume_{vacancy_id}'))
    await bot.send_message(chat_id, messages.vacancy_template.format(vacancy.name,
                                                                vacancy.specialization,
                                                                vacancy.description,
                                                                vacancy.key_skills,
                                                                vacancy.income), reply_markup=keyboard)



@dp.callback_query_handler(text='back_to_find_vacancies', state=FindVacancy)
async def back_to_find_vacancies(query: callback_query):
    await bot.delete_message(query.message.chat.id, query.message.message_id)


@dp.callback_query_handler(text='additional_information', state=FindVacancy)
async def additional_information(query: callback_query, state: FSMContext):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(buttons.back, callback_data='additional_information_back'))
    await query.message.answer(messages.additional_information, reply_markup=keyboard)


@dp.callback_query_handler(text='additional_information_back', state=FindVacancy)
async def additional_information_back(query: callback_query, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)


@dp.callback_query_handler(text_contains=['send_resume_'], state=FindVacancy)
async def send_resume_handler(query: callback_query, state: FSMContext):
    vacancy_id = int(query.data.split('_')[2])
    await FindVacancy.next()
    await state.update_data(id=vacancy_id)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(buttons.back, callback_data='back_to_find_vacancies'))
    await query.message.answer(messages.send_me_your_resume, reply_markup=keyboard)


@dp.message_handler(content_types=types.ContentTypes.DOCUMENT, state=FindVacancy)
async def recieve_resume(message: types.Message, state: FSMContext):
    if message.document.mime_type == 'application/pdf':
        file_id = message.document.file_id
        file_path = settings.resumes_path_base + str(file_id) + '.pdf'
        await bot.download_file_by_id(file_id, file_path)
        text_pdf = parser_from_pdf.extract_text_from_pdf(file_path)
        json_obj = json.dumps(text_pdf)
        async with state.proxy() as s:
            vacancy_id = s['id']
        candidate = Candidate(user=User.get(User.chat_id == message.chat.id),
                              vacancy=Vacancy.get(Vacancy.id == vacancy_id),
                              resume_file_id=file_id,
                              resume_json=json_obj,
                              status='Резюме обрабатывается')
        candidate.save()
        await message.answer(messages.resume_in_treatment)
        treatment_result = await treatment_resume(candidate.id)
        if treatment_result:
            candidate.status = 'Резюме одобрено'
            candidate.save()
            await message.answer(messages.resume_is_good)
            vacancy = Vacancy.get(Vacancy.id == vacancy_id)
            if vacancy.test_task:
                keyboard = InlineKeyboardMarkup()
                keyboard.add(InlineKeyboardButton(buttons.menu, callback_data='menu'))
                await bot.send_document(message.chat.id, open(vacancy.test_task, 'rb'), caption=messages.here_is_task,
                                        reply_markup=keyboard)
                candidate.status = 'Отправлено тестовое задание'
                candidate.save()
                await state.finish()
            else:
                keyboard = InlineKeyboardMarkup()
                keyboard.add(InlineKeyboardButton(buttons.menu, callback_data='menu'))
                await message.answer(messages.there_is_no_task, reply_markup=keyboard)
                candidate.status = 'Контакты отправлены работодателю'
                candidate.save()
                # resume = json.loads(candidate.resume_json)['info']
                await bot.send_message(candidate.vacancy.creator.chat_id, messages.user_without_task.
                                       format(candidate.user.username, candidate.vacancy.name))
                await state.finish()
        else:
            candidate.status = 'Резюме отклонено'
            candidate.save()
            await message.answer(messages.resume_is_bad)
            await FindVacancy.id.set()

    else:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(buttons.back, callback_data='back_to_find_vacancies'))
        await message.answer(messages.something_wrong, reply_markup=keyboard)


async def treatment_resume(candidate_id):
    candidate = Candidate.get(Candidate.id == candidate_id)
    required_key_skills = candidate.vacancy.key_skills
    preformed_key_skills = json.loads(candidate.resume_json)['key_skills']['skills']
    ratio = fuzz.WRatio(required_key_skills, preformed_key_skills)
    if ratio > 50:
        return True
    return False


if __name__ == '__main__':
    create_tables()
    executor.start_polling(dp, skip_updates=False)
