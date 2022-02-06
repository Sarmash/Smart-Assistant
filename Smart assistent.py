import webbrowser

from vosk import Model, KaldiRecognizer     # офлайн-распознование от Vosk
import speech_recognition       # распознавание пользовательской речи
import pyttsx3   # синтез речи
import wave     # создание и чтение аудиофайлов формата wav
import json     #  работа с json-файлами и json-строками
import os       # работа с файловой системой


class VoiceAssistant:
    """
    Настройки голосового ассистента, включающие имя, пол, язык речи
    """
    name = ''
    sex = ''
    speech_language = ''
    recoognition_language = ''


def setup_assistant_voice():
    """
    Установка голоса по умолчанию (индекс может менться в
    зависимости от настроек операционной системы)
    """
    voices = ttsEngine.getProperty('voices')

    if assistant.speech_language == 'en':
        assistant.recognition_language = 'en-US'
        if assistant.sex == 'female':
            # Microsoft Zira Desktop - English (United States)
            ttsEngine.setProperty('voice', voices[1].id)
        else:
            # Microsoft David Desktop - English (United States)
            ttsEngine.setProperty('voice', voices[2].id)
    else:
        assistant.recognition_language = 'ru-RU'
        # Microsoft Irina Desktop - Russian
        ttsEngine.setProperty('voice', voices[0].id)


def play_voice_assistant_speech(text_to_speech):
    """
    Проигрывание речи ответов голосового ассистента (без сохранения аудио)
    :param text_to_speech: текст, который нужно преобразовать в речь
    """
    ttsEngine.say(str(text_to_speech))
    ttsEngine.runAndWait()

def record_and_recognize_audio(*args: tuple):
    """
    Запись и распознавание аудио
    """
    with microphone:
        recognized_data = ""

        # регулирование уровня окружающего шума
        recognizer.adjust_for_ambient_noise(microphone, duration=2)

        try:
            print('Прослушивание...')
            audio = recognizer.listen(microphone, 5, 5)

            with open('micriphone-results.wav', 'wb') as file:
                file.write(audio.get_wav_data())

        except speech_recognition.WaitTimeoutError:
            print('Не могли бы вы проверить, включен ли ваш микрофон, пожалуйста?')
            return

        # использование online-распознавания через Google
        # (высокое качество распознования)
        try:
            print('Началось распознавание...')
            recognized_data = recognizer.recognize_google(audio, language='ru')

        except speech_recognition.UnknownValueError:
            pass

        # в случае проблем с доступом в Интернет происходит попытка
        # использовать offline-распознование через Vosk
        except speech_recognition.RequestError:
            print('Пытаюсь использовать автономное распознавание...')
            recognized_data = use_offline_recognition()

        return recognized_data


def use_offline_recognition():
    """
    Переключение га оффлайн-распознование речи
    :return: распознанная фраза
    """
    recognized_data = ""
    try:
        # проверка наличия модели на нужном языке в каталоге приложения
        if not os.path.exists('models/vosk-model-small-ru-0.4'):
            print("Пожалуйста, скачайте модель с:\n"
                  "https://alphacephei.com/vosk/models и распакуйте как 'модель' в текущей папке")
            exit(1)

        # анализ записанного в микрофон аудио (чтобы избежать повторов фразы)
        wave_audio_file = wave.open('micriphone-results.wav', 'rb')
        model = Model('models/vosk-model-small-ru-0.4')
        offline_reconizer = KaldiRecognizer(model, wave_audio_file.getframerate())

        data = wave_audio_file.readframes(wave_audio_file.getnframes())
        if len(data) > 0:
            if offline_reconizer.AcceptWaveform(data):
                recognized_data = offline_reconizer.Result()

                # получение данных распознанного текста из JSON-строки
                # (чтобы можно было выдать по ней ответ)
                recognized_data = json.loads(recognized_data)
                recognized_data = recognized_data['text']
    except:
        print('Извините, речевая служба недоступна. Попробуйте еще раз позже')

    return recognized_data

def play_greetings(*args: tuple):
    """
    Приветствие
    :param args: фраза приветствия
    """
    play_voice_assistant_speech('Здравствуйте, Николай Петрович')

def play_farewell_and_quit(*args: tuple):
    """
    Прощание
    :param args: фраза прощания
    :return: возвращает значение False для глобальной переменной program_operation
    """
    play_voice_assistant_speech('До свидания, Николай Петрович')
    global program_operation
    program_operation = False

def serch_for_term_on_yandex(*args: tuple):
    """
    Поиск информации в яндексе
    :param args: фраза поискового запроса
    """
    if not args[0]: return
    serch_term = ' '.join(args[0])
    url = 'https://www.yandex.ru/search/?text=' + serch_term
    webbrowser.get().open(url)

    # для мультиязычных голосовых ассистентов лучше создать
    # отдельный класс, который будет брать перевод из JSON-файла
    play_voice_assistant_speech("Вот что я нашла для" + serch_term + 'в яндексе')

def search_for_video_on_youtube(*args: tuple):
    """
    Поиск информации в YouTube
    :param args: фраза поискового запроса
    """
    if not args[0]: return
    serch_term = ' '.join(args[0])
    url = 'https://www.youtube.com/results?search_query=' + serch_term
    webbrowser.get().open(url)

    # для мультиязычных голосовых ассистентов лучше создать
    # отдельный класс, который будет брать перевод из JSON-файла
    play_voice_assistant_speech("Вот что я нашла для" + serch_term + 'в YouTube')


def search_for_definition_on_wikipedia(*args: tuple):
    """
    Поиск информации в YouTube
    :param args: фраза поискового запроса
    """
    if not args[0]: return
    serch_term = ' '.join(args[0])
    url = 'https://ru.wikipedia.org/wiki/' + serch_term
    webbrowser.get().open(url)

    # для мультиязычных голосовых ассистентов лучше создать
    # отдельный класс, который будет брать перевод из JSON-файла
    play_voice_assistant_speech("Вот что я нашла для" + serch_term + 'в википедии')

commands = {
    ('Привет', 'Здравствуй'): play_greetings,
    ('пока',): play_farewell_and_quit,
    ('найди'): serch_for_term_on_yandex,
    ('видео'): search_for_video_on_youtube,
    ('определение', 'Википедия'): search_for_definition_on_wikipedia
}

def execute_command_with_name(command_name: str, *args: list):
    """
    Выполнение заданной пользоателем команды с дополнительными аргументами
    :param command_name: название команды
    :param args: аргументы, которые будут переданы в функцию
    :return:
    """
    for key in commands.keys():
        if command_name in key:
            commands[key](*args)
        else:
            pass # print('Команда не найдена')




if __name__ == '__main__':

    # инициализация инструментов распознавания и ввода речи
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()

    # инициализация инструмента синтеза речи
    ttsEngine = pyttsx3.init()

    # настройка данных голосового помощника
    # настройка данных голосового помощника
    assistant = VoiceAssistant()
    assistant.name = 'Darya'
    assistant.sex = 'female'
    assistant.speech_language = 'ru'

    # установка голоса по умолчанию
    setup_assistant_voice()

    # присваеваем значение переменной True, изменяя значение на False мы сможем остановить цикл программы
    program_operation = True

    while program_operation:
        # старт записи речи с последующим выводом распознанной речи
        # и удаление записанного в микрофон аудио
        voice_input = record_and_recognize_audio()
        os.remove('micriphone-results.wav')
        print(voice_input)

        # отделение команд от дополнительной информации (аргументов)
        voice_input = voice_input.split(' ')
        command = voice_input[0]
        command_options = [str(input_part) for input_part in voice_input[1:len(voice_input)]]
        execute_command_with_name(command, command_options)