import wx
from inputResult import inputResult
from getCompetitionNames import getCompetitionNamesNumber

# Класс для отправки данных о результате в БД
class Input_data():
    def __init__(self, number, sorev, result) -> None:
        self.number = number
        self.sorev = sorev
        self.result = result
    def get_number(self):
        return self.number
    
    def get_sorev(self):
        return self.sorev
    
    def get_result(self):
        return self.result
    
"""Класс, отвечающий за страницу ввода результатов соревнования
ОПИСАНИЕ:
    Класс создаёт все виджеты на странице, отвечает за подтягивание данных с базы данных,
    Также отвечает за вывод ошибок в случае неправильной работы с приложением
"""
class Inputer(wx.Panel):
    def __init__(self, parent):
        # вызов конструктора наследника с указанием того-же родителя, что и у класса Inputer
        super(Inputer, self).__init__(parent) 
        # Создание вспомогательных переменных
        self.number = 0
        
        # Задание размеров, цвета фона, цвета шрифта, шрифта
        self.SetSize((600, 550))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))
        self.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW))
        self.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Segoe UI"))

        # Создание разметки верхнего уровня
        grid_sizer_1 = wx.FlexGridSizer(3, 1, 30, 0)

        grid_sizer_2 = wx.FlexGridSizer(2, 1, 10, 0)
        grid_sizer_1.Add(grid_sizer_2, 1, wx.LEFT | wx.RIGHT, 30)

        # Создание надписи Номер участника
        label_1 = wx.StaticText(self, wx.ID_ANY, u"Номер участника", style=wx.ALIGN_CENTER_HORIZONTAL)
        grid_sizer_2.Add(label_1, 0, wx.ALIGN_CENTER | wx.TOP, 15)

        grid_sizer_5 = wx.FlexGridSizer(1, 3, 0, 0)
        grid_sizer_2.Add(grid_sizer_5, 1, 0, 0)

        # Создание поля для ввода номера участника
        self.text_ctrl_1 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER)
        self.text_ctrl_1.SetMinSize((300, 33))
        grid_sizer_5.Add(self.text_ctrl_1, 0, wx.ALIGN_CENTER | wx.BOTTOM | wx.RIGHT | wx.TOP, 5)

        
        # Создание кнопки Искать
        self.button_3 = wx.Button(self, wx.ID_ANY, u"Искать")
        self.button_3.SetMinSize((150, 50))
        self.button_3.SetBackgroundColour(wx.Colour(204, 50, 50))
        self.button_3.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))
        grid_sizer_5.Add(self.button_3, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        
        
        grid_sizer_3 = wx.FlexGridSizer(2, 1, 10, 0)
        grid_sizer_1.Add(grid_sizer_3, 1, wx.LEFT | wx.RIGHT, 30)


        grid_sizer_4 = wx.FlexGridSizer(5, 1, 10, 0)
        grid_sizer_1.Add(grid_sizer_4, 1, wx.LEFT | wx.RIGHT, 30)

        # Создание надписи Соревнования
        label_3 = wx.StaticText(self, wx.ID_ANY, u"Соревнования")
        grid_sizer_4.Add(label_3, 0, wx.ALIGN_CENTER, 0)

        # Создание объекта для выбора соревнования
        self.choice_4 = wx.Choice(self, wx.ID_ANY, choices=[])
        self.choice_4.SetMinSize((458, 33))
        grid_sizer_4.Add(self.choice_4, 0, wx.BOTTOM, 30)

        # Создание надписи результат
        label_4 = wx.StaticText(self, wx.ID_ANY, u"Результат")
        grid_sizer_4.Add(label_4, 0, wx.ALIGN_CENTER, 0)

        grid_sizer_7 = wx.FlexGridSizer(1, 2, 0, 0)
        grid_sizer_4.Add(grid_sizer_7, 1, wx.EXPAND | wx.RIGHT, 0)

        # Создание поля для ввода номера
        self.text_ctrl_2 = wx.TextCtrl(self, wx.ID_ANY, "")
        self.text_ctrl_2.SetMinSize((300, 33))
        self.text_ctrl_2.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DHIGHLIGHT))
        grid_sizer_7.Add(self.text_ctrl_2, 0, wx.ALIGN_CENTER | wx.BOTTOM | wx.RIGHT | wx.TOP, 5)

        # Создание поля для подсказки по шаблону ввода
        self.text_ctrl_3 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY | wx.NO_BORDER)
        self.text_ctrl_3.SetMinSize((300, 33))
        self.text_ctrl_3.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DHIGHLIGHT))
        grid_sizer_4.Add(self.text_ctrl_3, 0, wx.ALIGN_CENTER | wx.BOTTOM | wx.RIGHT | wx.TOP, 5)

        # Создание кнопки внести
        self.button_5 = wx.Button(self, wx.ID_ANY, u"Внести")
        self.button_5.SetMinSize((145, 50))
        self.button_5.SetBackgroundColour(wx.Colour(204, 50, 50))
        self.button_5.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))
        grid_sizer_7.Add(self.button_5, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        
        # Привязка событий
        self.button_3.Bind(wx.EVT_BUTTON, self.search_button)
        self.button_5.Bind(wx.EVT_BUTTON, self.input_button)
        self.choice_4.Bind(wx.EVT_CHOICE, self.set_format)
        
        self.SetSizer(grid_sizer_1)

        self.Layout()
        # end wxGlade
        
    # Функция для получения номера
    def search_button(self, event):
        try:
            # Попытка получить номер и преобразовать его в целое
            self.number = int(self.text_ctrl_1.GetValue().strip().replace(",", "."))
        except:
            wx.MessageBox("Введите численное значение в поле Номер участника", "Ошибка", wx.ICON_ERROR)
            return
        # Проеверка - существует ли участни с таким номером
        if (list(getCompetitionNamesNumber(self.number).keys()) == None):
            wx.MessageBox("Нет такого участника", "Информация", wx.ICON_INFORMATION)
            return
        # Добавление выбора соревнования
        self.choice_4.Set(list(getCompetitionNamesNumber(self.number).keys()))
        # подсказка по формату ввода
        self.text_ctrl_3.SetLabelText(f"Пример ввода: {getCompetitionNamesNumber(self.number)[list(getCompetitionNamesNumber(self.number).keys())[0]]}")
        
        self.choice_4.SetSelection(0)
        
    # Функция для отправки данных в БД
    def input_button(self, event):
        # Проверка - выбрано ли соревнование
        if (self.choice_4.GetSelection() == -1):
            wx.MessageBox("Выберите соревнование в поле соревнование", "Информация", wx.ICON_INFORMATION)
            return
        else:
            # отправка результата в БД
            inputResult(self.number, self.choice_4.GetStringSelection(), self.text_ctrl_2.GetValue())
            wx.MessageBox("Информация внесена", "Успех", wx.ICON_INFORMATION)
        
        # Сброс введённых данных
        self.text_ctrl_1.SetValue("")
        self.text_ctrl_2.SetValue("")
        self.choice_4.Set([])
        
    # Функция для обновления формата в случае изменения выбранного соревнования
    def set_format(self, event):
        self.text_ctrl_3.SetLabelText("Привер ввода: " + getCompetitionNamesNumber(self.number)[self.choice_4.GetStringSelection()])