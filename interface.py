import sys
import pandas as pd
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QApplication, QVBoxLayout, QWidget,
    QMainWindow, QLabel, QGridLayout, QPushButton,
    QFileDialog, QTextEdit, QListWidget, QListWidgetItem,
    QTableView, QTableWidgetItem, QTableWidget,
    QStackedLayout, QHBoxLayout, QVBoxLayout,
    QLineEdit, QSpacerItem, QSizePolicy
)

from engine import (
    load_files_engine,
    LLM_input_engine,
    table_columns_engine,
    update_table_columns_engine,
    control_table_columns_engine,
    table_file_preview_engine,
    create_file_engine
)


#-----------------------------------------------------------------------------------------------------------------------------
# Основной код интерфейса
#-----------------------------------------------------------------------------------------------------------------------------


class HomeLayout(QWidget):
    '''
    Класс вкладки меню Home 
    '''
    def __init__(self):
        super().__init__()

        # Объявляем макеты
        self.page_layout = QGridLayout(self)
        self.page_layout.setContentsMargins(40, 0, 40, 40)
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(40, 0, 40, 0)

        image_path_1 = 'images/gazprom_logo.jpg'
        image_path_2 = 'images/fkn_logo.jpg'

        # Создаем виджеты
        self.label1 = QLabel("Home page")
        self.image_label_1 = QLabel()
        self.image_label_2 = QLabel()
        self.pixmap_1 = QPixmap(image_path_1)
        self.image_label_1.setPixmap(self.pixmap_1)
        self.pixmap_2 = QPixmap(image_path_2)
        self.image_label_2.setPixmap(self.pixmap_2)


        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding)

        # Устанавливаем фиксированные размеры для виджетов   
        self.image_label_1.setScaledContents(True)
        self.image_label_1.setFixedSize(275, 150)
        self.image_label_2.setScaledContents(True)
        self.image_label_2.setFixedSize(275, 150)

        # Устанавливаем цвет фона виджета
        self.color_widget_1 = QWidget()
        self.color_widget_1.setStyleSheet("background-color: #ffffff;")
        
        # Добавляем виджеты в сетку
        # self.page_layout.setSpacing(20)
        # self.page_layout.addWidget(self.label1, 0, 0)
        # self.page_layout.setSpacing(20)

        self.page_layout.addLayout(self.grid_layout, 1, 0)
        self.grid_layout.addWidget(self.color_widget_1, 0, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout.addWidget(self.image_label_1, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        self.grid_layout.addWidget(self.image_label_2, 0, 1, alignment=Qt.AlignmentFlag.AlignRight) 

        self.page_layout.addItem(spacer, 2, 0)  

        # Устанавливаем stretch-факторы
        self.grid_layout.setRowStretch(0, 0)
        self.grid_layout.setRowStretch(1, 0)
        self.grid_layout.setColumnStretch(0, 0)
        self.grid_layout.setColumnStretch(1, 1)

        # Создаем вспомогательный виджет для второго фона в QVBoxLayout
        self.page_layout.addWidget(self.color_widget_1, 1, 0)


class UploadLayout(QWidget):
    '''
    Класс вкладки меню Загрузка файлов 
    '''
    def __init__(self):
        super().__init__()
        
        # Объявляем макеты
        self.page_layout = QGridLayout(self)
        self.page_layout.setContentsMargins(40, 40, 40, 40)
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(40, 40, 40, 40)
       
        # Создаем виджеты
        self.label1 = QLabel("Загрузка файлов")
        self.file_list_widget = QListWidget()
        self.button1 = QPushButton("Добавить файлы")
        self.button2 = QPushButton("Удалить файл")
        self.button3 = QPushButton("Загрузить файлы в систему")
        self.label2 = QLabel("Выбранные файлы: ")

        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        # Устанавливаем минимальные размеры для кнопок   
        self.button1.setMinimumSize(200, 50)
        self.button2.setMinimumSize(200, 50)
        self.button3.setMinimumSize(200, 50)
        self.file_list_widget.setMinimumSize(200, 400)
        
        # Устанавливаем цвет фона виджета
        self.color_widget = QWidget()
        self.color_widget.setStyleSheet("background-color: #32363F;")       
        
        # Добавляем виджеты в сетку
        self.page_layout.setSpacing(20)
        self.page_layout.addWidget(self.label1, 0, 0)
        # self.page_layout.setSpacing(20)
        
        self.page_layout.addLayout(self.grid_layout, 1, 0)
        self.grid_layout.addWidget(self.color_widget, 0, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout.addWidget(self.label2, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout.addWidget(self.file_list_widget, 1, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout.addWidget(self.button1, 2, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout.addWidget(self.button2, 2, 1, alignment=Qt.AlignmentFlag.AlignTop)
        # self.page_layout.setSpacing(100)
        self.page_layout.addWidget(self.button3, 2, 0)

        self.page_layout.addItem(spacer, 2, 0)      

        # Устанавливаем stretch-факторы
        self.grid_layout.setRowStretch(0, 0)
        self.grid_layout.setRowStretch(1, 0)
        self.grid_layout.setRowStretch(2, 1)
        self.grid_layout.setColumnStretch(0, 0)
        self.grid_layout.setColumnStretch(1, 0)

        # Подключаем сигнал нажатия на кнопки
        self.button1.clicked.connect(self.add_file)
        self.button2.clicked.connect(self.remove_file)
        self.button3.clicked.connect(self.load_file)
        # Создаем вспомогательный виджет для второго фона в QVBoxLayout
        self.page_layout.addWidget(self.color_widget, 1, 0)


        # Список загружаемых файлов
        self.files_list = []

    def add_file(self):
        # Открываем диалоговое окно для выбора файла
        file_names, _ = QFileDialog.getOpenFileNames(self, "Открыть файлы", "", "Все файлы (*);;Текстовые файлы (*.txt)")
        if file_names:
            for name in file_names:
                if name not in self.files_list:
                    self.files_list.append(name)
                    self.file_list_widget.addItem(name)                       

    

    def remove_file(self):
        # Удаляем выбранный файл из списка
        selected_items = self.file_list_widget.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            self.files_list.remove(item.text())
            self.file_list_widget.takeItem(self.file_list_widget.row(item))                         
    

    def load_file(self):
        # Загружаем файлы в engine.py
        load_files_engine(self.files_list)              # TODO <- Функция загрузки из engine.py


class SettingsLayout(QWidget):
    '''
    Класс вкладки меню Настройка запроса 
    '''
    def __init__(self):
        super().__init__()

        # Объявляем макеты
        self.page_layout = QGridLayout(self)
        self.page_layout.setContentsMargins(40, 40, 40, 40)
        self.grid_layout_1 = QGridLayout()
        self.grid_layout_1.setContentsMargins(40, 40, 40, 40)
        self.grid_layout_2 = QGridLayout()
        self.grid_layout_2.setContentsMargins(40, 40, 40, 40)

        # Создаем виджеты
        self.label1 = QLabel("Настройка запроса")
        self.label2 = QLabel("Таблица контроля выбранных столбцов")
        self.check_table = QTableWidget()
        self.columns_df = table_columns_engine()                        # TODO <- Функция загрузки из engine.py
        self.check_table.setRowCount(len(self.columns_df))
        self.check_table.setColumnCount(len(self.columns_df.columns))
        self.check_table.setHorizontalHeaderLabels(self.columns_df.columns)

        self.label3 = QLabel("Запрос с применением LLM")
        self.label4 = QLabel("Введите текст")
        self.text_input = QLineEdit()
        self.button1 = QPushButton("Запуск LLM")

        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        # Устанавливаем фиксированные размеры для виджетов   
        self.button1.setMinimumSize(200, 50)
        self.text_input.setMinimumSize(200, 50)
        self.check_table.setMinimumSize(200, 200)

        # Устанавливаем цвет фона виджета
        self.color_widget_1 = QWidget()
        self.color_widget_1.setStyleSheet("background-color: #32363F;")
        self.color_widget_2 = QWidget()
        self.color_widget_2.setStyleSheet("background-color: #32363F;")   

        # Добавляем виджеты в сетку
        self.page_layout.setSpacing(20)
        self.page_layout.addWidget(self.label1, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignTop)
        self.page_layout.setSpacing(20)

        self.page_layout.addLayout(self.grid_layout_1, 1, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout_1.addWidget(self.color_widget_1, 0, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout_1.addWidget(self.label2, 1, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout_1.addWidget(self.check_table, 2, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignTop)

        self.page_layout.addWidget(self.label3, 2, 0, 1, 2)

        self.page_layout.addLayout(self.grid_layout_2, 3, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout_2.addWidget(self.color_widget_2, 0, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout_2.addWidget(self.label4, 1, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout_2.addWidget(self.text_input, 2, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout_2.addWidget(self.button1, 3, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignTop)

        self.page_layout.addItem(spacer, 4, 0, 1, 2)

        # Устанавливаем stretch-факторы
        self.page_layout.setRowStretch(0, 0)
        self.grid_layout_1.setRowStretch(0, 0)
        self.grid_layout_1.setRowStretch(1, 0)
        self.grid_layout_1.setRowStretch(2, 0)
        self.page_layout.setRowStretch(1, 0)
        self.grid_layout_2.setRowStretch(0, 0)
        self.grid_layout_2.setRowStretch(1, 0)
        self.grid_layout_2.setRowStretch(2, 0)
        self.grid_layout_2.setRowStretch(3, 0)
        self.grid_layout_1.setColumnStretch(0, 1)
        self.grid_layout_2.setColumnStretch(0, 1)

        # Создаем вспомогательный виджет для второго фона в QVBoxLayout
        self.page_layout.addWidget(self.color_widget_1, 1, 0)
        self.page_layout.addWidget(self.color_widget_2, 3, 0)

        # Заполнение таблицы данными из DataFrame 
        for row in range(len(self.columns_df)):
            for col in range(len(self.columns_df.columns)):
                self.check_table.setItem(row, col, QTableWidgetItem(str(self.columns_df.iloc[row, col])))

        # Установить ширину столбцов и высоту строк
        for col in range(len(self.columns_df.columns)):
            self.check_table.setColumnWidth(col, 730)

        # Подключение сигнала изменения ячейки к обработчику
        self.check_table.cellChanged.connect(self.update_data)

        # Подключаем сигнал нажатия на кнопки запуска LLM
        self.button1.pressed.connect(self.LLM_input)

        # Задаем пустое начальное значение ввода для LLM
        self.LLM_input_text = ""

    def update_data(self, row, col):
        # Обновление DataFrame при изменении данных в таблице
        new_value = self.check_table.item(row, col).text()
        self.columns_df.iloc[row, col] = new_value
        update_table_columns_engine(self.columns_df, row, col, new_value)      # TODO <- Функция загрузки из engine.py

    def LLM_input(self):
        self.LLM_input_text = self.text_input.text()
        LLM_input_engine(self.LLM_input_text)                    # TODO <- Функция загрузки из engine.py
     

class ControlLayout(QWidget):
    '''
    Класс вкладки меню Контроль вывода 
    '''
    def __init__(self):
        super().__init__()

        # Объявляем макеты
        self.page_layout = QGridLayout(self)
        self.page_layout.setContentsMargins(40, 40, 40, 40)
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(40, 40, 40, 40)

        # Создаем виджеты
        self.label1 = QLabel("Контроль вывода")
        self.label2 = QLabel("Таблица контроля выбранных столбцов")
        self.check_table = QTableWidget()
        self.columns_settings_df = control_table_columns_engine()                        # TODO <- Функция загрузки из engine.py
        self.check_table.setRowCount(len(self.columns_settings_df))
        self.check_table.setColumnCount(len(self.columns_settings_df.columns))
        self.check_table.setHorizontalHeaderLabels(self.columns_settings_df.columns)
        
        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        # Устанавливаем фиксированные размеры для виджетов   
        self.check_table.setMinimumSize(200, 500)

        # Устанавливаем цвет фона виджета
        self.color_widget = QWidget()
        self.color_widget.setStyleSheet("background-color: #32363F;")

        # Добавляем виджеты в сетку
        self.page_layout.setSpacing(20)
        self.page_layout.addWidget(self.label1, 0, 0, 1, 2)
        self.page_layout.setSpacing(20)

        self.page_layout.addLayout(self.grid_layout, 1, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout.addWidget(self.color_widget, 0, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout.addWidget(self.label2, 1, 0, 1, 2)
        self.grid_layout.addWidget(self.check_table, 2, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignTop)
        
        self.page_layout.addItem(spacer, 2, 0)

        # Устанавливаем stretch-факторы
        self.grid_layout.setRowStretch(0, 0)
        self.grid_layout.setRowStretch(1, 0)
        self.grid_layout.setRowStretch(2, 1)
        self.grid_layout.setColumnStretch(0, 0)
        self.grid_layout.setColumnStretch(1, 1)

        # Заполнение таблицы данными из DataFrame 
        for row in range(len(self.columns_settings_df)):
            for col in range(len(self.columns_settings_df.columns)):
                self.check_table.setItem(row, col, QTableWidgetItem(str(self.columns_settings_df.iloc[row, col])))

        # Подключение сигнала изменения ячейки к обработчику
        self.check_table.cellChanged.connect(self.update_data)

        # Создаем вспомогательный виджет для второго фона в QVBoxLayout
        self.page_layout.addWidget(self.color_widget, 1, 0)

    def update_data(self, row, col):
        # Обновление DataFrame при изменении данных в таблице
        new_value = self.check_table.item(row, col).text()
        self.columns_settings_df.iloc[row, col] = new_value
        update_table_columns_engine(self.columns_settings_df, row, col, new_value)      # TODO <- Функция загрузки из engine.py


class ResultLayout(QWidget):
    '''
    Класс вкладки меню Выгрузка результата 
    '''
    def __init__(self):
        super().__init__()

        # Объявляем макеты
        self.page_layout = QGridLayout(self)
        self.page_layout.setContentsMargins(40, 40, 40, 40)
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(40, 40, 40, 40)

        # Создаем виджеты
        self.label1 = QLabel("Выгрузка результата")
        self.label2 = QLabel("Предварительный просмотр итоговой таблицы")
        self.check_table = QTableWidget()
        self.table_preview_df = table_file_preview_engine()                        # TODO <- Функция загрузки из engine.py
        self.check_table.setRowCount(len(self.table_preview_df))
        self.check_table.setColumnCount(len(self.table_preview_df.columns))
        self.check_table.setHorizontalHeaderLabels(self.table_preview_df.columns)
        self.button1 = QPushButton("Создать файл Excel")

        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        # Устанавливаем фиксированные размеры для виджетов   
        self.check_table.setMinimumSize(200, 500)
        self.button1.setMinimumSize(200, 50)

        # Устанавливаем цвет фона виджета
        self.color_widget = QWidget()
        self.color_widget.setStyleSheet("background-color: #32363F;")

        # Добавляем виджеты в сетку
        self.page_layout.setSpacing(20)
        self.page_layout.addWidget(self.label1)
        self.page_layout.setSpacing(20)

        self.page_layout.addLayout(self.grid_layout, 1, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout.addWidget(self.color_widget, 0, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout.addWidget(self.label2, 1, 0, 1, 2)
        self.grid_layout.addWidget(self.check_table, 2, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout.addWidget(self.button1, 3, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignTop)

        self.page_layout.addItem(spacer, 2, 0)

        # Устанавливаем stretch-факторы
        self.grid_layout.setRowStretch(0, 0)
        self.grid_layout.setRowStretch(1, 0)
        self.grid_layout.setRowStretch(2, 0)
        self.grid_layout.setRowStretch(3, 1)
        self.grid_layout.setColumnStretch(0, 0)
        self.grid_layout.setColumnStretch(1, 1)

        # Заполнение таблицы данными из DataFrame 
        for row in range(len(self.table_preview_df)):
            for col in range(len(self.table_preview_df.columns)):
                self.check_table.setItem(row, col, QTableWidgetItem(str(self.table_preview_df.iloc[row, col])))
        
        # Создаем вспомогательный виджет для второго фона в QVBoxLayout
        self.page_layout.addWidget(self.color_widget, 1, 0)

        # Подключаем сигнал нажатия на кнопки
        self.button1.clicked.connect(self.create_file)

    # Функция запуска создания файла
    def create_file(self):
        create_file_engine(self.table_preview_df)               # TODO <- Функция загрузки из engine.py


class MainWindow(QMainWindow):
    '''
    Класс главного окна
    '''
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Uranium table unifier")

        # Устанавливаем начальный размер окна
        self.resize(1300, 700)

        image_path = 'images/logo_uranium.jpg'

        widget = QWidget()
        self.setCentralWidget(widget)

        main_layout = QGridLayout(widget)
        main_layout.setContentsMargins(10, 0, 0, 0)
        menu_layout = QVBoxLayout()
        self.stack_layout = QStackedLayout()

        # Создаем виджеты
        self.image_label = QLabel()
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap)

        self.button0 = QPushButton("Home")
        self.button1 = QPushButton("Загрузка файлов")
        self.button2 = QPushButton("Настройка запроса")
        self.button3 = QPushButton("Контроль вывода")
        self.button4 = QPushButton("Выгрузка результата")
        self.button_close = QPushButton("Выход")          

        # Устанавливаем фиксированные размеры для виджетов    
        self.button0.setMinimumSize(230, 50)
        self.button1.setMinimumSize(230, 50)
        self.button2.setMinimumSize(230, 50)
        self.button3.setMinimumSize(230, 50)
        self.button4.setMinimumSize(230, 50)
        self.button_close.setMinimumSize(200, 50)

        self.image_label.setScaledContents(True)
        self.image_label.setFixedSize(150, 150)

        # Устанавливаем разные цвета фона для разных ячеек
        cell_widget_1 = QWidget()
        cell_widget_1.setStyleSheet("background-color: #32363F;")

        cell_widget_2 = QWidget()
        cell_widget_2.setStyleSheet('background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #252932, stop:1 #2A2D34);')

        main_layout.addLayout(menu_layout, 0, 0, alignment=Qt.AlignmentFlag.AlignTop)
        main_layout.addLayout(self.stack_layout, 0, 1, alignment=Qt.AlignmentFlag.AlignTop)
        main_layout.addWidget(cell_widget_1, 0, 0)
        main_layout.addWidget(cell_widget_2, 0, 1)


        # Добавляем виджеты в сетку
        menu_layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter) 
        menu_layout.addWidget(self.button0)
        menu_layout.addWidget(self.button1)
        menu_layout.addWidget(self.button2)
        menu_layout.addWidget(self.button3)
        menu_layout.addWidget(self.button4)
        menu_layout.addStretch()
        menu_layout.addWidget(self.button_close)
        menu_layout.addSpacing(20)   
                
        # Создаем экземпляры слоев и добавляем их в QStackedLayout
        self.home_layout = HomeLayout()
        self.stack_layout.addWidget(self.home_layout)
        
        self.start_layout = UploadLayout()
        self.stack_layout.addWidget(self.start_layout)

        self.settings_layout = SettingsLayout()
        self.stack_layout.addWidget(self.settings_layout)

        self.control_layout = ControlLayout()
        self.stack_layout.addWidget(self.control_layout)

        self.result_layout = ResultLayout()
        self.stack_layout.addWidget(self.result_layout)

        # Подключаем сигнал нажатия на кнопки
        self.button0.pressed.connect(lambda: self.activate_tab(0))
        self.button1.pressed.connect(lambda: self.activate_tab(1))
        self.button2.pressed.connect(lambda: self.activate_tab(2))
        self.button3.pressed.connect(lambda: self.activate_tab(3))
        self.button4.pressed.connect(lambda: self.activate_tab(4))
        self.button_close.pressed.connect(self.close)

        # Устанавливаем общий цвет фона окна
        self.setStyleSheet("""
            QMainWindow {
                background-color: #32363F; /* Устанавливаем цвет фона окна */
            }
            QPushButton {
                background-color: #32363F;
                color: white;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #252932;
                color: #00B5FF;
            }
            QLabel {
                color: #f0f0f0;
                font-size: 12px;
            }
        """)

    def activate_tab(self, index):
        # Функция активации вкладки меню
        self.stack_layout.setCurrentIndex(index)

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
