import wx
from outputResults import outputParticipants

"""Класс, отвечающий за страницу просмотра участников
ОПИСАНИЕ:
    Класс создаёт все виджеты на странице, отвечает за подтягивание данных с базы данных,
    Также отвечает за вывод ошибок в случае неправильной работы с приложением
"""
class Participants_viewver(wx.Panel):
    def __init__(self, parent):
        
        # вызов конструктора наследника с указанием того-же родителя, что и у класса Participants_viewver
        super(Participants_viewver, self).__init__(parent) 
        
        # Задание размера и стандартного шрифта
        self.SetSize((600, 800))
        self.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Segoe UI"))
        
        # Создание разметки верхнего уровня
        self.grid_sizer_1 = wx.FlexGridSizer(2, 1, 0, 0)
        
        # Кнопка обновить
        self.button_1 = wx.Button(self, wx.ID_ANY, "Обновить")
        self.button_1.SetBackgroundColour(wx.Colour(204, 50, 50))
        self.button_1.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))
        self.button_1.SetMinSize((350, 25))
        self.grid_sizer_1.Add(self.button_1, 0, 0, 0)
        
        # Поле для просмотра участников
        self.list_ctrl_1 = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
        self.list_ctrl_1.SetMinSize(wx.Size(10000, 775))
        self.list_ctrl_1.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.list_ctrl_1.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))
        self.grid_sizer_1.Add(self.list_ctrl_1, 1, wx.EXPAND, 0)
        
        # Привязка событий
        self.button_1.Bind(wx.EVT_BUTTON, self.update_data_api)
        
        
        self.SetSizer(self.grid_sizer_1)
        
        # Подтягивание данных при включении программы
        self.update_data()
        
        self.Layout()

    # Функция переходник, нужна, чтобы была возможность обновлять данные без эвента
    def update_data_api(self, event):
        self.update_data()
    
    def update_data(self):
        # Удаление старых данных
        self.list_ctrl_1.DeleteAllColumns()
        self.list_ctrl_1.DeleteAllItems()
        
        # Добавление нужных заголовков
        self.list_ctrl_1.AppendColumn("№ п/п", format=wx.LIST_FORMAT_LEFT, width=100)
        self.list_ctrl_1.AppendColumn("Фамилия", format=wx.LIST_FORMAT_LEFT, width=200)
        self.list_ctrl_1.AppendColumn("Имя", format=wx.LIST_FORMAT_LEFT, width=200)
        self.list_ctrl_1.AppendColumn("Отчество", format=wx.LIST_FORMAT_LEFT, width=200)
        self.list_ctrl_1.AppendColumn("Пол", format=wx.LIST_FORMAT_LEFT, width=200)
        self.list_ctrl_1.AppendColumn("Дата рождения", format=wx.LIST_FORMAT_LEFT, width=200)
        self.list_ctrl_1.AppendColumn("Нагруд. номер", format=wx.LIST_FORMAT_LEFT, width=200)
        self.list_ctrl_1.AppendColumn("Команда", format=wx.LIST_FORMAT_LEFT, width=200)
        self.list_ctrl_1.AppendColumn("Ступень", format=wx.LIST_FORMAT_LEFT, width=200)
        
        # Вывод данных из БД
        for i in outputParticipants():
            self.list_ctrl_1.Append(i)