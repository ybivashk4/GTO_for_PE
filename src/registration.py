import wx
import wx.adv
import datetime
import registerParticipant as reg_api

"""класс обёртка над DatePickerCtrl и GenericCalendarCtrl

Описание:
    Обеспечивает возможность выбора даты как в календаре, так и в поле с датой
"""
class Date_selector(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # Краткий выбор даты 
        self.date_picker = wx.adv.DatePickerCtrl(self, style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
        self.sizer.Add(self.date_picker, 0, wx.ALL | wx.EXPAND, 5)

        # Подробный календарь
        self.calendar = wx.adv.GenericCalendarCtrl(self)
        self.sizer.Add(self.calendar, 0, wx.ALL | wx.EXPAND, 5)


        self.SetSizer(self.sizer)

        # Синхронизация дат
        self.calendar.Bind(wx.adv.EVT_CALENDAR_SEL_CHANGED, self.sync_from_calendar)
        self.date_picker.Bind(wx.adv.EVT_DATE_CHANGED, self.sync_from_picker)
    
    def sync_from_calendar(self, event):
        self.date_picker.SetValue(self.calendar.GetDate())

    def sync_from_picker(self, event):
        self.calendar.SetDate(self.date_picker.GetValue())

    def GetDate(self):
        return self.date_picker.GetValue()

    """Класс для хранения данных о регистрируемом человеке

    
    """
class User():
    # Конструктор
    def __init__(self, name : str, surname : str, thirdname : str, sex: str, borth : datetime, number : str, team : str) -> None:
        self.name = name
        self.surname = surname
        self.thirdname = thirdname
        self.sex = sex
        self.borth = borth
        self.number = number
        self.team = team
        pass
    
    # Геттеры начало
    def get_name(self):
        return self.name
    def get_surname(self):
        return self.surname
    def get_third_name(self):
        return self.thirdname
    def get_sex(self):
        return self.sex
    def get_bortrh(self):
        return self.borth
    def get_num(self):
        return self.number
    def get_team(self):
        return self.team
    # Геттеры конец
    
    
    # Преобразование объекта класса в строку
    def __str__(self) -> str:
        return self.name + " " + self.sex + " " + str(self.borth)
    
    # фабричный конструктор
    def create_user(name : str, surname : str, thirdname : str, sex: str, borth : str, number : str, team : str):
        return User(name,surname,thirdname, sex, borth, number, team)

    """Класс, отвечающий за страницу регестрация
    ОПИСАНИЕ:
        Класс создаёт все виджеты на странице, отвечает за подтягивание данных с базы данных,
        Также отвечает за вывод ошибок в случае неправильной работы с приложением
    """
class Registration(wx.Panel):
    
    # Конструктор, принимающий родительский класс
    def __init__(self, parent):
        # вызов конструктора наследника с указанием того-же родителя, что и у класса Registration
        super(Registration, self).__init__(parent) 
        
        # Задача размеров окна
        self.SetSize((400, 700 ))
        # Установка цвета для фона приложения
        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        # Задание стандартного шрифта
        self.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "MS Reference Sans Serif"))

        # Создание разметки 1го уроовеня
        grid_sizer_1 = wx.FlexGridSizer(6, 1, 2, 2)

        # Создание разметки 2го уровня
        sizer_4 = wx.FlexGridSizer(10, 1, 0, 0)
        
        # Добавлление в разметку 1го уровня разметку второго уровня
        grid_sizer_1.Add(sizer_4, 1, wx.ALIGN_CENTER, 0)

        # Создание текстового поля Фамилия
        label_3 = wx.StaticText(self, wx.ID_ANY, u"Фамилия")
        label_3.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW))

        sizer_4.Add(label_3, 0, 0, 0)
        
        # Создание поля для ввода фамилии
        self.text_ctrl_1 = wx.TextCtrl(self, wx.ID_ANY, u"", style=wx.TE_PROCESS_ENTER)
        self.text_ctrl_1.SetMinSize((300, 35))
        self.text_ctrl_1.SetFont(wx.Font(16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        sizer_4.Add(self.text_ctrl_1, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)


        # Создание текстового поля Имя
        label_4 = wx.StaticText(self, wx.ID_ANY, u"Имя")
        label_4.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW))
        sizer_4.Add(label_4, 0, 0, 0)

        # Создание поля для ввода Имени
        self.text_ctrl_2 = wx.TextCtrl(self, wx.ID_ANY, u"", style=wx.TE_PROCESS_ENTER)
        self.text_ctrl_2.SetMinSize((300, 35))
        self.text_ctrl_2.SetFont(wx.Font(16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        sizer_4.Add(self.text_ctrl_2, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)


        
        label_5 = wx.StaticText(self, wx.ID_ANY, u"Отчество")
        label_5.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW))
        sizer_4.Add(label_5, 0, 0, 0)
        
        # Создание поля для ввода Отчества
        self.text_ctrl_3 = wx.TextCtrl(self, wx.ID_ANY, u"", style=wx.TE_PROCESS_ENTER)
        self.text_ctrl_3.SetMinSize((300, 35))
        self.text_ctrl_3.SetFont(wx.Font(16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        sizer_4.Add(self.text_ctrl_3, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)        
        
        
        # Создание текстового поля Номер 
        label_6 = wx.StaticText(self, wx.ID_ANY, u"Номер")
        label_6.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW))
        sizer_4.Add(label_6, 0, 0, 0)

        # Создание поля для ввода номера
        self.text_ctrl_4 = wx.TextCtrl(self, wx.ID_ANY, u"", style=wx.TE_PROCESS_ENTER)
        self.text_ctrl_4.SetMinSize((300, 35))
        self.text_ctrl_4.SetFont(wx.Font(16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        sizer_4.Add(self.text_ctrl_4, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)

        
        # Создание текстового поля Команда
        label_7 = wx.StaticText(self, wx.ID_ANY, u"Команда")
        label_7.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW))
        sizer_4.Add(label_7, 0, 0, 0)
        
        # Создание поля для ввода Команды
        self.text_ctrl_5 = wx.TextCtrl(self, wx.ID_ANY, u"", style=wx.TE_PROCESS_ENTER)
        self.text_ctrl_5.SetMinSize((300, 35))
        self.text_ctrl_5.SetFont(wx.Font(16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        sizer_4.Add(self.text_ctrl_5, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)
        
        #  Создание текстового пол Пол
        label_1 = wx.StaticText(self, wx.ID_ANY, u"Пол")
        label_1.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW))
        label_1.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "MS Reference Sans Serif"))
        grid_sizer_1.Add(label_1, 0, wx.ALIGN_CENTER, 0)

        # Создание разметки для отступов
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_1.Add(sizer_1, 1, wx.ALIGN_CENTER | wx.ALL, 10)

        # Создание двух исключающих кнопок для выбора пола
        self.radio_box_1 = wx.RadioBox(self, wx.ID_ANY, "", choices=[u"Мужской", u"Женский"], majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.radio_box_1.SetSelection(0)
        sizer_1.Add(self.radio_box_1, 0, 0, 0)

        
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_1.Add(sizer_2, 1, wx.ALIGN_CENTER | wx.ALL, 10)

        # Создание текстового поля Дата рождения
        label_2 = wx.StaticText(self, wx.ID_ANY, u"Дата рождения", style=wx.ALIGN_CENTER_HORIZONTAL)
        label_2.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW))
        label_2.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "MS Reference Sans Serif"))
        sizer_2.Add(label_2, 0, 0, 0)

        # Создание виджета класса Date_selector 
        self.generic_calendar_ctrl_1 = Date_selector(self)
        self.generic_calendar_ctrl_1.SetFont(wx.Font(9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "MS Reference Sans Serif"))
        self.generic_calendar_ctrl_1.SetMinSize(wx.Size(200, 30))
        grid_sizer_1.Add(self.generic_calendar_ctrl_1, 2, wx.ALIGN_CENTER | wx.ALL, 10)

        
        # Создание кнопки для отправкм данных
        self.button_1 = wx.Button(self, wx.ID_ADD, u"Подтвердить")
        self.button_1.SetBackgroundColour(wx.Colour(204, 50, 50))
        self.button_1.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))
        self.button_1.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "MS Reference Sans Serif"))
        grid_sizer_1.Add(self.button_1, 2, wx.ALIGN_CENTER | wx.ALL, 10)

        grid_sizer_1.AddGrowableCol(0)
        self.SetSizer(grid_sizer_1)
        
        # Привязка событий
        self.button_1.Bind(wx.EVT_BUTTON, self.on_confirm)
        
        self.Layout()

    def on_confirm(self, event):
        # Оставляем от имени только буквы, создаём шаблон для записи, где первая буква - заглавная, остальные маленькие
        surname = self.text_ctrl_1.GetValue().strip().capitalize()
        name = self.text_ctrl_2.GetValue().strip().capitalize()
        thirdname = self.text_ctrl_3.GetValue().strip().capitalize()
        
        # Проверка - заполнены ли поля фамилия и имя
        if (len(name) == 0 or len(surname) == 0):
            wx.MessageBox("Есть пустое поле в ФИО", "Ошибка", wx.ICON_ERROR)
            return
        
        # Проверка, что человеку, который регистрируется больше 8 лет
        if ( (datetime.date.today().year -  self.generic_calendar_ctrl_1.GetDate().year - (
            datetime.date.today().month < self.generic_calendar_ctrl_1.GetDate().month+1 or (
                datetime.date.today().month == self.generic_calendar_ctrl_1.GetDate().month+1 and 
                datetime.date.today().day < self.generic_calendar_ctrl_1.GetDate().day
            )
            )) < 8):
            wx.MessageBox("Соревнования доступны от 8 лет", "Ошибка", wx.ICON_ERROR)
            return

        # Получение пола
        sex = "Мужской" if self.radio_box_1.GetSelection() == 0 else "Женский"
    
        # Получение даты, номера, команды
        birth_date = self.generic_calendar_ctrl_1.GetDate()
        birth_str = birth_date.FormatISODate()  # Преобразуем в строку YYYY-MM-DD
        number = self.text_ctrl_4.GetValue()
        team = self.text_ctrl_5.GetValue() 
        
        # создание пользователя
        user = User.create_user(name, surname, thirdname, sex, birth_str, number, team)

        # Проверка создания пользователя
        if user:
            # Отправка данных в БД
            reg_api.register(user.get_surname(), user.get_name(), user.get_third_name(), user.get_sex(), user.get_bortrh(), user.get_num(), user.get_team())
            wx.MessageBox(f"Пользователь создан: {user}", "Успех", wx.ICON_INFORMATION)
            
            # Сброс полей 
            self.text_ctrl_1.SetValue("")
            self.text_ctrl_2.SetValue("")
            self.text_ctrl_3.SetValue("")
            self.text_ctrl_4.SetValue("")
            self.text_ctrl_5.SetValue("")
            
        else:
            wx.MessageBox("Ошибка ввода данных", "Ошибка", wx.ICON_ERROR)
# end of class Registration

