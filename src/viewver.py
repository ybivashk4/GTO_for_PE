import wx


class Out_object():
    def __init__(self, name, surname, thirdname, number, team, normatives : list, sum) -> None:
        self.name = name
        self.surname = surname
        self.thirdname = thirdname
        self.normatives = normatives
        self.sum = sum
        self.number = number
        self.team = team
            
    def get_normatives(self) -> list:
        return self.normatives
    def get_name(self):
        return self.name
    def get_surname(self):
        return self.surname
    def get_thirdname(self):
        return self.thirdname
    def get_sum(self):
        return self.sum
    def get_number(self):
        return self.number
    def get_team(self):
        return self.team
    # def calculate_sum(self):
    #     self.sum = 0
    #     for i in range(2, int(len(self.normatives)), 3):
    #         self.sum += self.normatives[i]
    #     return self.sum
        

def get_column_length(out_object : Out_object) -> int:
    name_len = 3
    sum_len = 1
    return int(len(out_object.get_normatives()) / 3 * 2 + 0.1) + 3 + sum_len + name_len


class Viewer(wx.Frame ):
    def __init__(self, *args, **kwds):
        # begin wxGlade: Viewer.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((600, 800))
        self.SetTitle("Просмоторщик")
        
        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        
        grid_sizer_1 = wx.FlexGridSizer(5, 1, 0, 0)
        sizer_1.Add(grid_sizer_1, 1, wx.EXPAND, 0)

        self.choice_1 = wx.Choice(self.panel_1, wx.ID_ANY, choices=[u"2 категория", u"3 категория", u"4 категория", u"5 категория", u"6 категория", u"7 категория", u"8 категория", u"9 категория", u"10 категория", u"11 категория", u"12 категория", u"13 категория", u"14 категория", u"15 категория", u"16 категория", u"17 категория", u"18 категория"])
        self.choice_1.SetSelection(0)
        grid_sizer_1.Add(self.choice_1, 0, 0, 0)

        self.radio_box_1 = wx.RadioBox(self.panel_1, wx.ID_ANY, "", choices=[u"Мужской", u"Женский"], majorDimension=1, style=wx.RA_SPECIFY_COLS)
        self.radio_box_1.SetSelection(0)
        grid_sizer_1.Add(self.radio_box_1, 0, 0, 0)

        self.button_2 = wx.Button(self.panel_1, wx.ID_ANY, "Подтвердить")
        grid_sizer_1.Add(self.button_2, 0, 0, 0)
        
        self.list_ctrl_1 = wx.ListCtrl(self.panel_1, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
        self.list_ctrl_1.SetMinSize(wx.Size(100000, 600))
        self.list_ctrl_1.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.list_ctrl_1.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))
        
        grid_sizer_1.Add(self.list_ctrl_1, 1, wx.EXPAND, 0)
        self.button_1 = wx.Button(self.panel_1, wx.ID_ANY, "Скопировать таблицу")
        grid_sizer_1.Add(self.button_1, 0, 0, 0)
        
        
        self.button_1.Bind(wx.EVT_BUTTON, self.copy_all_to_clipboard)
        self.button_2.Bind(wx.EVT_BUTTON, self.get_data)
        
        
        self.panel_1.SetSizer(sizer_1)

        self.Layout()
        # end wxGlade
    def builder(self):
        self.list_ctrl_1.AppendColumn("Фамилия", format=wx.LIST_FORMAT_LEFT, width=200)
        self.list_ctrl_1.AppendColumn("Имя", format=wx.LIST_FORMAT_LEFT, width=200)
        self.list_ctrl_1.AppendColumn("Отчество", format=wx.LIST_FORMAT_LEFT, width=200)
        self.list_ctrl_1.AppendColumn("Номер", format=wx.LIST_FORMAT_LEFT, width=200)
        self.list_ctrl_1.AppendColumn("Команда", format=wx.LIST_FORMAT_LEFT, width=200)
        for j in range(0, len(out_objects[0].get_normatives()), 3):
            self.list_ctrl_1.AppendColumn(out_objects[0].get_normatives()[j] + " Результат", format=wx.LIST_FORMAT_LEFT, width=200)
            self.list_ctrl_1.AppendColumn(out_objects[0].get_normatives()[j] + " Баллы", format=wx.LIST_FORMAT_LEFT, width=200)
                
        self.list_ctrl_1.AppendColumn("Сумма", format=wx.LIST_FORMAT_LEFT, width=100)
        for i in range(len(out_objects)):
            out = []
            out.append(out_objects[i].get_name())
            out.append(out_objects[i].get_surname())
            out.append(out_objects[i].get_thirdname())
            out.append(out_objects[i].get_number())
            out.append(out_objects[i].get_team())
            for j in range(0, len(out_objects[i].get_normatives())):
                if (j == 0 or j % 3 == 0):
                    continue
                out.append(str(out_objects[i].get_normatives()[j]))
            out.append(str(out_objects[i].get_sum()))
            self.list_ctrl_1.Append(out)
            
            
    def copy_all_to_clipboard(self, event):
        all_items = []
        
        # Получаем количество строк и колонок
        row_count = self.list_ctrl_1.GetItemCount()
        col_count = self.list_ctrl_1.GetColumnCount()
        
        # Собираем заголовки колонок
        headers = []
        for col in range(col_count):
            headers.append(self.list_ctrl_1.GetColumn(col).GetText())
        all_items.append("\t".join(headers))
        
        # Собираем данные
        for row in range(row_count):
            row_data = []
            for col in range(col_count):
                row_data.append(self.list_ctrl_1.GetItemText(row, col))
            all_items.append("\t".join(row_data))
        
        # Копируем в буфер обмена
        if all_items:
            clipboard_data = wx.TextDataObject()
            clipboard_data.SetText("\n".join(all_items))
            
            if wx.TheClipboard.Open():
                wx.TheClipboard.SetData(clipboard_data)
                wx.TheClipboard.Close()
                
                
    def get_data(self, event):
        # удаление данных прошлого запроса
        self.list_ctrl_1.DeleteAllItems()
        self.list_ctrl_1.DeleteAllColumns()
        
        # Для запроса в базу
        category = self.choice_1.GetSelection()+1
        sex =  self.radio_box_1.GetString(self.radio_box_1.GetSelection())
        
        # Пример формата получаемых данных
        out_objects.append(Out_object("Mikhail", "Beltyukov", "Olegovich", "1", "Сургут", ["Бег", 20, 5, "Плаванье", 10, 3, "Лыжи", 15, 4], 0))
        out_objects.append(Out_object("Mikhail2", "Beltyukov2", "Olegovich2", "2", "НеСургут", ["Бег", 202, 52, "Плаванье", 102, 32, "Лыжи", 152, 42], 0))
        # Строительство новых данных
        self.builder()
# end of class Viewer

class MyApp(wx.App):
    def OnInit(self):
        self.frame = Viewer(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

if __name__ == "__main__":
    out_objects = []
    app = MyApp(0)
    app.MainLoop()
 