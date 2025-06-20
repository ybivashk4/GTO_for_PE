import wx
from registration import Registration
from viewver import Viewer
from inputer import Inputer
from deleter import Deleter
from team_viewver import Team_viewer
from all_particepants_viewver import Participants_viewver

"""Класс, отвечающий за хранение всех страниц
ОПИСАНИЕ:
    Класс хранит в себе все классы для отображения в этом приложении
"""
class MainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        
        # Задание размеров и название
        self.SetSize((1000, 900))
        self.SetTitle("Помощник ГТО")

        # Создание разметки верхнего уровня
        grid_sizer_1 = wx.FlexGridSizer(1, 1, 10, 10)

        # Создание контейнера для остальных классов
        self.notebook_1 = wx.Notebook(self, wx.ID_ANY, style= wx.NB_TOP)
        grid_sizer_1.Add(self.notebook_1, 1, wx.EXPAND, 0)
        
        # Добавление классов внутрь контейнера
        self.notebook_1.AddPage(Registration(self.notebook_1), u"Регистрация")
        self.notebook_1.AddPage(Participants_viewver(self.notebook_1), u"Участники")
        self.notebook_1.AddPage(Inputer(self.notebook_1), u"Ввод")
        self.notebook_1.AddPage(Viewer(self.notebook_1), u"Личный зачет")
        self.notebook_1.AddPage(Team_viewer(self.notebook_1), u"Командный зачет")
        self.notebook_1.AddPage(Deleter(self.notebook_1), u"Удаление")

        self.SetSizer(grid_sizer_1)

        self.Layout()

# Класс для запуска приложения
class MyApp(wx.App):
    def OnInit(self):
        # Основное окно приложения
        self.frame = MainFrame(None, wx.ID_ANY, "")
        # Добавление приложению иконки
        self.frame.SetIcon(wx.Icon("GTO.png"))
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
