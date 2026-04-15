import sys
import random
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.checkbox import CheckBox
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.clock import Clock
from kivy.metrics import dp, sp  # Добавлено для адаптивности

# Убираем фиксированный размер окна - пусть определяется автоматически
# Window.size = (360, 640)  # ЗАКОММЕНТИРОВАНО
Window.clearcolor = (0.1, 0.1, 0.15, 1)  # Тёмный фон

BASE = "images"

def img(name):
    return os.path.join(BASE, name)

# — ТЕСТ —
questions = [
    {"question": "К какой группе относится знак?",
     "image": img("1.png"),
     "options": ["Рельеф", "Сооружение", "Растительность"],
     "correct": ["Рельеф"]},
    {"question": "Как называется условный знак?",
     "image": img("kolodec.png"),
     "options": ["Родник", "Колодец", "Яма с водой"],
     "correct": ["Колодец"]},
    {"question": "Как называется условный знак?",
     "image": img("peresruchey.png"),
     "options": ["Непреодолимая река", "Ручей", "Пересыхающий ручей"],
     "correct": ["Пересыхающий ручей"]},
    {"question": "Как называется условный знак?",
     "image": img("controlpunct.png"),
     "options": ["Горка", "Финиш", "Контрольный путь"],
     "correct": ["Контрольный путь"]},
    {"question": "Какие условные знаки относятся к рельефу?",
     "image": img("usrelief.png"),
     "options": ["а", "б", "в", "г", "д", "е"],
     "correct": ["а", "е"]},
    {"question": "Какой знак — железная дорога?",
     "image": img("jd.png"),
     "options": ["а", "б", "в"],
     "correct": ["в"]},
    {"question": "Исключите лишний знак",
     "image": img("iscl.png"),
     "options": ["а", "б", "в", "г", "е"],
     "correct": ["г"]},
]

# — ИНТЕРЕСНЫЕ ФАКТЫ —
facts = [
    "Первые карты создавались ещё в древнем Вавилоне на глиняных табличках.",
    "На картах север чаще всего изображается сверху, но так было не всегда.",
    "Цвета на топографических картах стандартизированы для удобства чтения.",
    "Зелёный цвет на картах действительно обозначает лесную растительность.",
    "Коричневый цвет используется для рельефа, так как ассоциируется с землёй.",
    "Синий цвет на картах всегда обозначает водные объекты.",
    "Чёрным цветом обозначаются искусственные сооружения: дороги, здания.",
    "Горизонтали на карте помогают 'увидеть' высоту без 3D-изображения.",
    "Топографические карты используются не только туристами, но и военными.",
    "Масштаб карты показывает, во сколько раз уменьшено изображение местности."
]

# БОЛЬШЕ ВОПРОСОВ ДЛЯ РЕЖИМОВ
# Базовые вопросы для генерации новых
base_color_questions = [
    {"question": "Цвет леса?", "correct": ["Зелёный"], "incorrect": ["Синий", "Красный"]},
    {"question": "Цвет воды?", "correct": ["Синий"], "incorrect": ["Жёлтый", "Чёрный"]},
    {"question": "Цвет рельефа?", "correct": ["Коричневый"], "incorrect": ["Зелёный", "Синий"]},
    {"question": "Цвет дорог?", "correct": ["Чёрный"], "incorrect": ["Синий", "Жёлтый"]},
    {"question": "Цвет поля?", "correct": ["Жёлтый"], "incorrect": ["Синий", "Чёрный"]},
    {"question": "Цвет камней?", "correct": ["Чёрный"], "incorrect": ["Синий", "Зелёный"]},
    {"question": "Цвет болота?", "correct": ["Голубой"], "incorrect": ["Красный", "Чёрный"]},
    {"question": "Что показывают горизонтали?", "correct": ["Высоту"], "incorrect": ["Реки", "Дороги"]},
    {"question": "Цвет труднопроходимого леса?", "correct": ["Тёмно-зелёный"], "incorrect": ["Жёлтый", "Синий"]},
    {"question": "Как обозначается болото?", "correct": ["Голубым с штрихами"], "incorrect": ["Жёлтым", "Чёрным"]},
    {"question": "Цвет скал?", "correct": ["Чёрный"], "incorrect": ["Синий", "Зелёный"]},
    {"question": "Белый цвет обозначает?", "correct": ["Лес"], "incorrect": ["Поле", "Воду"]},
    {"question": "Жёлтый цвет — это?", "correct": ["Открытая местность"], "incorrect": ["Лес", "Горы"]},
    {"question": "Камни на карте — это?", "correct": ["Чёрные точки"], "incorrect": ["Синие линии", "Зелёные круги"]},
    {"question": "Цвет железных дорог?", "correct": ["Чёрный"], "incorrect": ["Красный", "Синий"]},
    {"question": "Цвет моста?", "correct": ["Чёрный"], "incorrect": ["Синий", "Зелёный"]},
    {"question": "Цвет здания?", "correct": ["Чёрный"], "incorrect": ["Красный", "Синий"]},
    {"question": "Цвет тропинки?", "correct": ["Чёрный"], "incorrect": ["Коричневый", "Зелёный"]},
    {"question": "Цвет реки?", "correct": ["Синий"], "incorrect": ["Зелёный", "Коричневый"]},
    {"question": "Цвет озера?", "correct": ["Синий"], "incorrect": ["Зелёный", "Жёлтый"]},
]

# Базовые утверждения для Верно/Неверно
base_true_false_statements = [
    {"statement": "Зелёный цвет обозначает лес.", "correct": True},
    {"statement": "Синий цвет — вода.", "correct": True},
    {"statement": "Жёлтый цвет — поле.", "correct": True},
    {"statement": "Чёрный цвет — рельеф.", "correct": False},
    {"statement": "Коричневый цвет — высоты.", "correct": True},
    {"statement": "Белый цвет — вода.", "correct": False},
    {"statement": "Дороги показываются синим.", "correct": False},
    {"statement": "Болото обозначается голубым.", "correct": True},
    {"statement": "Горизонтали показывают высоту.", "correct": True},
    {"statement": "Красный цвет используется для рельефа.", "correct": False},
    {"statement": "Тёмно-зелёный цвет — труднопроходимый лес.", "correct": True},
    {"statement": "Мосты обозначаются зелёным цветом.", "correct": False},
    {"statement": "Железные дороги обозначаются чёрным.", "correct": True},
    {"statement": "Реки обозначаются коричневым.", "correct": False},
    {"statement": "Здания обозначаются чёрным цветом.", "correct": True},
    {"statement": "Тропинки обозначаются синим.", "correct": False},
    {"statement": "Озера обозначаются голубым.", "correct": True},
    {"statement": "Поля обозначаются жёлтым.", "correct": True},
    {"statement": "Скалы обозначаются красным.", "correct": False},
    {"statement": "Камни обозначаются чёрными точками.", "correct": True},
]

# Функции для генерации вопросов
def generate_time_questions(count=20):
    """Генерация вопросов для режима 'На время'"""
    questions = []
    for i in range(count):
        base_q = random.choice(base_color_questions)
        options = [base_q["correct"][0]] + random.sample(base_q["incorrect"], 2)
        random.shuffle(options)
        questions.append({
            "question": base_q["question"],
            "options": options,
            "correct": base_q["correct"]
        })
    return questions

def generate_blitz_questions(count=20):
    """Генерация вопросов для режима 'Блиц'"""
    questions = []
    for i in range(count):
        base_q = random.choice(base_color_questions)
        options = [base_q["correct"][0]] + random.sample(base_q["incorrect"], 2)
        random.shuffle(options)
        questions.append({
            "question": base_q["question"],
            "options": options,
            "correct": base_q["correct"]
        })
    return questions

def generate_exam_questions(count=20):
    """Генерация вопросов для режима 'Экзамен'"""
    questions = []
    for i in range(count):
        base_q = random.choice(base_color_questions)
        options = [base_q["correct"][0]] + random.sample(base_q["incorrect"], 2)
        random.shuffle(options)
        questions.append({
            "question": base_q["question"],
            "options": options,
            "correct": base_q["correct"]
        })
    return questions

def generate_true_false_questions(count=20):
    """Генерация вопросов для режима 'Верно/Неверно'"""
    questions = []
    for i in range(count):
        statement = random.choice(base_true_false_statements)
        questions.append({
            "question": statement["statement"],
            "options": ["Верно", "Неверно"],
            "correct": ["Верно" if statement["correct"] else "Неверно"]
        })
    return questions

# — ЭКЗАМЕН (стартовый набор) —
exam_questions = generate_exam_questions(8)

# — НА ВРЕМЯ (стартовый набор) —
time_questions = generate_time_questions(8)

# — БЛИЦ (стартовый набор) —
blitz_questions = generate_blitz_questions(8)

# — ВЕРНО / НЕВЕРНО (стартовый набор) —
true_false_questions = generate_true_false_questions(8)

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Основной макет
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        
        # Заголовок
        title = Label(
            text="🌍 Тренажёр картографа",
            font_size=sp(28),
            bold=True,
            size_hint=(1, 0.2),
            color=[1, 1, 1, 1]
        )
        layout.add_widget(title)
        
        # Кнопки режимов
        modes_layout = BoxLayout(orientation='vertical', spacing=dp(15))
        modes = [
            ("📷 Тест по знакам", "quiz"),
            ("✅ Верно/Неверно", "tf"),
            ("⏱ На время", "time"),
            ("🎯 Экзамен", "exam"),
            ("⚡ Блиц", "blitz"),
        ]
        
        for text, mode in modes:
            btn = Button(
                text=text,
                size_hint=(1, None),
                height=dp(65),
                background_color=[0.12, 0.53, 0.9, 1],
                color=[1, 1, 1, 1],
                font_size=sp(18)
            )
            btn.mode = mode
            btn.bind(on_press=self.start_quiz)
            modes_layout.add_widget(btn)
        
        layout.add_widget(modes_layout)
        
        # Кнопка фактов
        fact_btn = Button(
            text="📖 Интересные факты",
            size_hint=(1, None),
            height=dp(65),
            background_color=[0.2, 0.6, 0.2, 1],
            color=[1, 1, 1, 1],
            font_size=sp(18)
        )
        fact_btn.bind(on_press=self.show_facts)
        layout.add_widget(fact_btn)
        
        self.add_widget(layout)
    
    def start_quiz(self, instance):
        # Сначала сбрасываем экран теста
        quiz_screen = self.manager.get_screen('quiz')
        quiz_screen.reset_screen()
        # Затем переключаемся и запускаем тест
        self.manager.current = 'quiz'
        quiz_screen.start_mode(instance.mode)
    
    def show_facts(self, instance):
        self.manager.current = 'facts'

class FactsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        
        # Заголовок
        title = Label(
            text="📖 Интересные факты",
            font_size=sp(26),
            bold=True,
            size_hint=(1, 0.1),
            color=[1, 1, 1, 1]
        )
        layout.add_widget(title)
        
        # Прокручиваемое окно для фактов
        scroll = ScrollView(size_hint=(1, 0.8))
        facts_layout = BoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=None)
        facts_layout.bind(minimum_height=facts_layout.setter('height'))
        
        self.fact_label = Label(
            text=random.choice(facts),
            font_size=sp(20),
            size_hint_y=None,
            height=dp(400),
            text_size=(Window.width - dp(40), None),
            halign='center',
            valign='center',
            color=[1, 1, 1, 1],
            markup=True
        )
        facts_layout.add_widget(self.fact_label)
        scroll.add_widget(facts_layout)
        layout.add_widget(scroll)
        
        # Кнопки
        buttons_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint=(1, 0.1))
        new_fact_btn = Button(
            text="Новый факт",
            background_color=[0.12, 0.53, 0.9, 1],
            color=[1, 1, 1, 1],
            font_size=sp(16)
        )
        new_fact_btn.bind(on_press=self.new_fact)
        
        back_btn = Button(
            text="Назад",
            background_color=[0.8, 0.2, 0.2, 1],
            color=[1, 1, 1, 1],
            font_size=sp(16)
        )
        back_btn.bind(on_press=self.go_back)
        
        buttons_layout.add_widget(new_fact_btn)
        buttons_layout.add_widget(back_btn)
        layout.add_widget(buttons_layout)
        
        self.add_widget(layout)
    
    def new_fact(self, instance):
        self.fact_label.text = random.choice(facts)
    
    def go_back(self, instance):
        self.manager.current = 'menu'

class QuizScreen(Screen):
    score = NumericProperty(0)
    count = NumericProperty(0)
    answered = NumericProperty(0)
    time_left = NumericProperty(15)  # Таймер для режима "На время"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Основной макет с прокруткой
        main_scroll = ScrollView()
        self.main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10), size_hint_y=None)
        self.main_layout.bind(minimum_height=self.main_layout.setter('height'))
        
        # Верхняя панель с информацией
        top_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(50), spacing=dp(10))
        
        # Панель счета и таймера
        info_layout = BoxLayout(orientation='horizontal', size_hint=(0.4, 1))
        self.score_label = Label(
            text="0/0",
            font_size=sp(18),
            color=[1, 1, 1, 1],
            size_hint=(0.5, 1)
        )
        self.timer_label = Label(
            text="15",
            font_size=sp(18),
            color=[1, 1, 1, 1],
            size_hint=(0.5, 1)
        )
        info_layout.add_widget(self.score_label)
        info_layout.add_widget(self.timer_label)
        top_layout.add_widget(info_layout)
        
        self.progress = ProgressBar(
            max=100,
            value=0,
            size_hint=(0.6, 1)
        )
        top_layout.add_widget(self.progress)
        self.main_layout.add_widget(top_layout)
        
        # Карточка с вопросом
        question_card = BoxLayout(orientation='vertical', size_hint=(1, None), height=dp(250), padding=dp(10), spacing=dp(10))
        
        # Контейнер для вопроса
        question_container = BoxLayout(orientation='vertical', size_hint=(1, None), height=dp(80))
        self.question_label = Label(
            text="",
            font_size=sp(22),
            size_hint_y=None,
            height=dp(80),
            text_size=(Window.width - dp(20), None),
            halign='center',
            valign='middle',
            color=[1, 1, 1, 1],
            markup=True
        )
        question_container.add_widget(self.question_label)
        question_card.add_widget(question_container)
        
        # Контейнер для изображения
        image_container = BoxLayout(orientation='vertical', size_hint=(1, None), height=dp(120))
        self.image_widget = Image(
            size_hint=(1, 1),
            allow_stretch=False,
            keep_ratio=True,
            fit_mode="contain"
        )
        image_container.add_widget(self.image_widget)
        question_card.add_widget(image_container)
        
        # Результат
        result_container = BoxLayout(orientation='vertical', size_hint=(1, None), height=dp(60))
        self.result_label = Label(
            text="",
            font_size=sp(18),
            size_hint_y=None,
            height=dp(60),
            text_size=(Window.width - dp(40), None),
            halign='center',
            valign='middle',
            color=[0, 1, 0, 1],
            markup=True
        )
        result_container.add_widget(self.result_label)
        question_card.add_widget(result_container)
        
        self.main_layout.add_widget(question_card)
        
        # Варианты ответов (чекбоксы)
        self.options_layout = BoxLayout(orientation='vertical', size_hint=(1, None), spacing=dp(5))
        self.options_layout.bind(minimum_height=self.options_layout.setter('height'))
        self.checkboxes = []
        
        for i in range(6):
            cb_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(55))
            checkbox = CheckBox(
                size_hint=(None, None),
                size=(dp(48), dp(48)),
                color=[1, 1, 1, 1]
            )
            self.checkboxes.append(checkbox)
            option_label = Label(
                text="",
                font_size=sp(18),
                size_hint=(0.8, 1),
                text_size=(Window.width - dp(100), None),
                valign='middle',
                color=[1, 1, 1, 1]
            )
            checkbox.label = option_label  # Привязываем метку к чекбоксу
            cb_layout.add_widget(checkbox)
            cb_layout.add_widget(option_label)
            self.options_layout.add_widget(cb_layout)
        
        self.main_layout.add_widget(self.options_layout)
        
        # Кнопки управления
        buttons_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(75), spacing=dp(10))
        self.confirm_btn = Button(
            text="Подтвердить",
            background_color=[0.12, 0.53, 0.9, 1],
            color=[1, 1, 1, 1],
            font_size=sp(18)
        )
        self.confirm_btn.bind(on_press=self.check_answer)
        
        self.next_btn = Button(
            text="Следующий",
            background_color=[0.2, 0.6, 0.2, 1],
            color=[1, 1, 1, 1],
            font_size=sp(18),
            disabled=True
        )
        self.next_btn.bind(on_press=self.next_question)
        
        self.back_btn = Button(
            text="Выход",
            background_color=[0.8, 0.2, 0.2, 1],
            color=[1, 1, 1, 1],
            font_size=sp(18)
        )
        self.back_btn.bind(on_press=self.exit_quiz)
        
        buttons_layout.add_widget(self.confirm_btn)
        buttons_layout.add_widget(self.next_btn)
        buttons_layout.add_widget(self.back_btn)
        self.main_layout.add_widget(buttons_layout)
        
        main_scroll.add_widget(self.main_layout)
        self.add_widget(main_scroll)
        
        # Инициализация таймера
        self.timer_event = None
    
    def reset_screen(self):
        """Сброс экрана перед началом нового теста"""
        # Останавливаем таймер если он работает
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None
        
        # Сбрасываем все виджеты к начальному состоянию
        self.clear_widgets()
        
        # Создаем заново основной макет
        main_scroll = ScrollView()
        self.main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10), size_hint_y=None)
        self.main_layout.bind(minimum_height=self.main_layout.setter('height'))
        
        # Верхняя панель с информацией
        top_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(50), spacing=dp(10))
        
        # Панель счета и таймера
        info_layout = BoxLayout(orientation='horizontal', size_hint=(0.4, 1))
        self.score_label = Label(
            text="0/0",
            font_size=sp(18),
            color=[1, 1, 1, 1],
            size_hint=(0.5, 1)
        )
        self.timer_label = Label(
            text="15",
            font_size=sp(18),
            color=[1, 1, 1, 1],
            size_hint=(0.5, 1)
        )
        info_layout.add_widget(self.score_label)
        info_layout.add_widget(self.timer_label)
        top_layout.add_widget(info_layout)
        
        self.progress = ProgressBar(
            max=100,
            value=0,
            size_hint=(0.6, 1)
        )
        top_layout.add_widget(self.progress)
        self.main_layout.add_widget(top_layout)
        
        # Карточка с вопросом
        question_card = BoxLayout(orientation='vertical', size_hint=(1, None), height=dp(250), padding=dp(10), spacing=dp(10))
        
        # Контейнер для вопроса
        question_container = BoxLayout(orientation='vertical', size_hint=(1, None), height=dp(80))
        self.question_label = Label(
            text="",
            font_size=sp(22),
            size_hint_y=None,
            height=dp(80),
            text_size=(Window.width - dp(20), None),
            halign='center',
            valign='middle',
            color=[1, 1, 1, 1],
            markup=True
        )
        question_container.add_widget(self.question_label)
        question_card.add_widget(question_container)
        
        # Контейнер для изображения
        image_container = BoxLayout(orientation='vertical', size_hint=(1, None), height=dp(120))
        self.image_widget = Image(
            size_hint=(1, 1),
            allow_stretch=False,
            keep_ratio=True,
            fit_mode="contain"
        )
        image_container.add_widget(self.image_widget)
        question_card.add_widget(image_container)
        
        # Результат
        result_container = BoxLayout(orientation='vertical', size_hint=(1, None), height=dp(60))
        self.result_label = Label(
            text="",
            font_size=sp(18),
            size_hint_y=None,
            height=dp(60),
            text_size=(Window.width - dp(40), None),
            halign='center',
            valign='middle',
            color=[0, 1, 0, 1],
            markup=True
        )
        result_container.add_widget(self.result_label)
        question_card.add_widget(result_container)
        
        self.main_layout.add_widget(question_card)
        
        # Варианты ответов
        self.options_layout = BoxLayout(orientation='vertical', size_hint=(1, None), spacing=dp(5))
        self.options_layout.bind(minimum_height=self.options_layout.setter('height'))
        self.checkboxes = []
        
        for i in range(6):
            cb_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(55))
            checkbox = CheckBox(
                size_hint=(None, None),
                size=(dp(48), dp(48)),
                color=[1, 1, 1, 1]
            )
            self.checkboxes.append(checkbox)
            option_label = Label(
                text="",
                font_size=sp(18),
                size_hint=(0.8, 1),
                text_size=(Window.width - dp(100), None),
                valign='middle',
                color=[1, 1, 1, 1]
            )
            checkbox.label = option_label
            cb_layout.add_widget(checkbox)
            cb_layout.add_widget(option_label)
            self.options_layout.add_widget(cb_layout)
        
        self.main_layout.add_widget(self.options_layout)
        
        # Кнопки управления
        buttons_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(75), spacing=dp(10))
        self.confirm_btn = Button(
            text="Подтвердить",
            background_color=[0.12, 0.53, 0.9, 1],
            color=[1, 1, 1, 1],
            font_size=sp(18)
        )
        self.confirm_btn.bind(on_press=self.check_answer)
        
        self.next_btn = Button(
            text="Следующий",
            background_color=[0.2, 0.6, 0.2, 1],
            color=[1, 1, 1, 1],
            font_size=sp(18),
            disabled=True
        )
        self.next_btn.bind(on_press=self.next_question)
        
        self.back_btn = Button(
            text="Выход",
            background_color=[0.8, 0.2, 0.2, 1],
            color=[1, 1, 1, 1],
            font_size=sp(18)
        )
        self.back_btn.bind(on_press=self.exit_quiz)
        
        buttons_layout.add_widget(self.confirm_btn)
        buttons_layout.add_widget(self.next_btn)
        buttons_layout.add_widget(self.back_btn)
        self.main_layout.add_widget(buttons_layout)
        
        main_scroll.add_widget(self.main_layout)
        self.add_widget(main_scroll)
    
    def start_mode(self, mode):
        self.mode = mode
        self.score = 0
        self.count = 0
        self.answered = 0
        self.time_left = 15  # Сбрасываем таймер
        
        # Генерируем новые вопросы каждый раз
        if mode == "exam":
            self.pool = generate_exam_questions(20)
        elif mode == "time":
            self.pool = generate_time_questions(20)
            self.start_timer()
        elif mode == "blitz":
            self.pool = generate_blitz_questions(20)
        elif mode == "tf":
            self.pool = generate_true_false_questions(20)
        else:
            self.pool = questions[:]  # Оригинальные вопросы с картинками
        
        random.shuffle(self.pool)
        self.load_question()
    
    def start_timer(self):
        """Запуск таймера для режима 'На время'"""
        if self.timer_event:
            self.timer_event.cancel()
        
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)
    
    def update_timer(self, dt):
        """Обновление таймера"""
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.text = str(self.time_left)
            
            # Меняем цвет таймера при малом времени
            if self.time_left <= 5:
                self.timer_label.color = [1, 0, 0, 1]  # Красный
            elif self.time_left <= 10:
                self.timer_label.color = [1, 1, 0, 1]  # Жёлтый
            else:
                self.timer_label.color = [1, 1, 1, 1]  # Белый
        else:
            # Время вышло - автоматически переходим к следующему вопросу
            self.auto_next_question()
    
    def auto_next_question(self):
        """Автоматический переход к следующему вопросу при окончании времени"""
        # Помечаем вопрос как неправильный если не успели ответить
        self.result_label.text = "Время вышло! ❌\nПравильный ответ не выбран"
        self.result_label.color = [1, 0, 0, 1]  # Красный
        
        # Отключаем чекбоксы
        for cb in self.checkboxes:
            if cb.parent.opacity == 1:
                cb.disabled = True
        
        # Обновляем статистику
        self.answered += 1
        self.score_label.text = f"{self.score}/{self.answered}"
        self.progress.value = (self.answered / 20) * 100
        
        # Кнопки
        self.confirm_btn.disabled = True
        self.next_btn.disabled = False
        
        # Перезапускаем таймер для следующего вопроса
        if self.pool:
            Clock.schedule_once(lambda dt: self.restart_timer(), 0.5)
        else:
            if self.timer_event:
                self.timer_event.cancel()
    
    def restart_timer(self):
        """Перезапуск таймера для следующего вопроса"""
        if self.pool:  # Проверяем, есть ли еще вопросы
            self.time_left = 15
            self.timer_label.text = str(self.time_left)
            self.timer_label.color = [1, 1, 1, 1]  # Белый
            self.timer_event = Clock.schedule_interval(self.update_timer, 1)
    
    def load_question(self):
        if not self.pool:
            self.finish()
            return
        
        self.current = self.pool.pop()
        self.question_label.text = self.current["question"]
        self.result_label.text = ""
        self.result_label.color = [0, 1, 0, 1]  # Зелёный по умолчанию
        
        # Показ изображения
        if self.mode == "quiz" and "image" in self.current:
            self.image_widget.source = self.current["image"]
            self.image_widget.opacity = 1
        else:
            self.image_widget.opacity = 0
        
        # Настройка вариантов ответов
        opts = self.current.get("options", ["Верно", "Неверно"])
        for i, cb in enumerate(self.checkboxes):
            if i < len(opts):
                cb.label.text = opts[i]
                cb.active = False
                cb.disabled = False
                cb.label.color = [1, 1, 1, 1]  # Белый цвет
                cb.parent.opacity = 1  # Показываем контейнер
                cb.parent.height = dp(55)  # Устанавливаем высоту
            else:
                cb.parent.opacity = 0  # Скрываем контейнер
                cb.parent.height = 0   # Устанавливаем нулевую высоту
        
        # Обновляем статистику
        self.score_label.text = f"{self.score}/{self.answered}"
        self.progress.value = (self.answered / 20) * 100
        
        # Кнопки
        self.confirm_btn.disabled = False
        self.next_btn.disabled = True
        
        # Если режим "На время", обновляем таймер
        if self.mode == "time":
            self.time_left = 15
            self.timer_label.text = str(self.time_left)
            self.timer_label.color = [1, 1, 1, 1]  # Белый
    
    def check_answer(self, instance):
        selected = []
        for cb in self.checkboxes:
            if cb.active and cb.parent.opacity == 1:
                selected.append(cb.label.text)
        
        correct = self.current["correct"]
        
        if set(selected) == set(correct):
            self.score += 1
            self.result_label.text = "Правильно! ✅"
            self.result_label.color = [0, 1, 0, 1]  # Зелёный
        else:
            self.result_label.text = f"Неправильно! ❌\nПравильный ответ: {', '.join(correct)}"
            self.result_label.color = [1, 0, 0, 1]  # Красный
        
        self.answered += 1
        
        # Отключаем чекбоксы после ответа
        for cb in self.checkboxes:
            if cb.parent.opacity == 1:
                cb.disabled = True
        
        # Обновляем статистику
        self.score_label.text