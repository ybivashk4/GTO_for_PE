import wx
import wx
import tempfile
import openpyxl
import pyperclip
from openpyxl.styles import Font, Alignment, PatternFill


"""
    TODO:
    * Сделать цвет у строчки с категорией+
    * Сделать Вывод верхней части таблицы+
    * Сделать Вывод нескольких таблиц+
    * Сделать Вывод остальных листов
"""

def to_roman(number:  int) -> str:
    roman_numbers = {'M': 1000, 'CM': 900, 'D': 500, 'CD': 400,
                 'C': 100, 'XC': 90, 'L': 50, 'XL': 40,
                 'X': 10, 'IX': 9, 'V': 5, 'IV': 4, 'I': 1}
    roman = ''
    for letter, value in roman_numbers.items():
        while number >= value:
            roman += letter
            number -= value
    return roman


def category_to_age(category: int) -> str:
    res = ''
    match category:
        case 2:
            res = '8-9'
        case 3:
            res = '10-11'
        case 4:
            res ='12-13'
        case 5:
            res = '14-15'
        case 6:
            res = '16-17'
        case 7:
            res = '18-19'
        case 8:
            res = '20-24'
        case 9:
            res = '25-29'
        case 10:
            res = '30-34'
        case 11:
            res = '35-39'
        case 12:
            res = '40-44'
        case 13:
            res = '45-49'
        case 14:
            res = '50-54'
        case 15:
            res = '55-59'
        case 16:
            res = '59-64'
        case 17:
            res = '65-69'
        case 18:                 
            res = '70+'                      
    return res

class Out_object():
    def __init__(self, place,surname, name, thirdname,date_of_borth : str, number, team, normatives : list, sum) -> None:
        self.name = name
        self.surname = surname
        self.thirdname = thirdname
        self.normatives = normatives
        self.sum = sum
        self.number = number
        self.team = team
        self.place = place
        self.date = date_of_borth
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
    def get_place(self):
        return self.place
    def get_date(self):
        return self.date
    # def calculate_sum(self):
    #     self.sum = 0
    #     for i in range(2, int(len(self.normatives)), 3):
    #         self.sum += self.normatives[i]
    #     return self.sum
    
class Out_category():
    def __init__(self, out_objects : list, category : int, sex: str) -> None:
        self.out_objects = out_objects    
        self.category = category
        self.sex = sex        
        
    def get_info(self):
        return self.out_objects
    
    def get_sex(self):
        return self.sex
    
    def get_category(self):
        return self.category
    
    def get_normatives(self):
        return self.out_objects[0].get_normatives()
    
    def get_normatives_without_results(self):
        return [self.out_objects[0].get_normatives()[i] for i in range(0, len(self.out_objects[0].get_normatives()), 3)]
    
def get_column_length(out_object : Out_object) -> int:
    name_len = 3
    sum_len = 1
    return int(len(out_object.get_normatives()) / 3 * 2 + 0.1) + 3 + sum_len + name_len


class Viewer(wx.Panel):
    def __init__(self, parent):
        
        # Объекты для вывода
        self.out_objects = []
        self.out_categories = []
        
        # begin wxGlade: Viewer.__init__
        super(Viewer, self).__init__(parent) 
        self.SetSize((600, 800))
        
        
        grid_sizer_1 = wx.FlexGridSizer(5, 1, 0, 0)
        
        self.choice_1 = wx.Choice(self, wx.ID_ANY, choices=[u"2 категория", u"3 категория", u"4 категория", u"5 категория", u"6 категория", u"7 категория", u"8 категория", u"9 категория", u"10 категория", u"11 категория", u"12 категория", u"13 категория", u"14 категория", u"15 категория", u"16 категория", u"17 категория", u"18 категория"])
        self.choice_1.SetSelection(0)
        grid_sizer_1.Add(self.choice_1, 0, 0, 0)

        self.radio_box_1 = wx.RadioBox(self, wx.ID_ANY, "", choices=[u"Мужской", u"Женский"], majorDimension=1, style=wx.RA_SPECIFY_COLS)
        self.radio_box_1.SetSelection(0)
        grid_sizer_1.Add(self.radio_box_1, 0, 0, 0)

        self.button_2 = wx.Button(self, wx.ID_ANY, "Подтвердить")
        grid_sizer_1.Add(self.button_2, 0, 0, 0)
        
        self.list_ctrl_1 = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
        self.list_ctrl_1.SetMinSize(wx.Size(10000, 600))
        self.list_ctrl_1.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.list_ctrl_1.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))
        
        grid_sizer_1.Add(self.list_ctrl_1, 1, wx.EXPAND, 0)
        self.button_1 = wx.Button(self, wx.ID_ANY, "Скопировать таблицу")
        grid_sizer_1.Add(self.button_1, 0, 0, 0)
        
        
        self.button_1.Bind(wx.EVT_BUTTON, self.copy_all_to_clipboard)
        self.button_2.Bind(wx.EVT_BUTTON, self.get_data)
        
        self.SetSizer(grid_sizer_1)

        self.Layout()
        # end wxGlade
    def builder(self):
        
        self.list_ctrl_1.AppendColumn("Место", format=wx.LIST_FORMAT_LEFT, width=100)
        self.list_ctrl_1.AppendColumn("ФИО", format=wx.LIST_FORMAT_LEFT, width=200)
        self.list_ctrl_1.AppendColumn("Дата рождения", format=wx.LIST_FORMAT_LEFT, width=200)
        self.list_ctrl_1.AppendColumn("Нагрудн. Номер", format=wx.LIST_FORMAT_LEFT, width=200)
        self.list_ctrl_1.AppendColumn("Команда", format=wx.LIST_FORMAT_LEFT, width=200)
        for j in range(0, len(self.out_objects[0].get_normatives()), 3):
            self.list_ctrl_1.AppendColumn(self.out_objects[0].get_normatives()[j] + " Результат", format=wx.LIST_FORMAT_LEFT, width=200)
            self.list_ctrl_1.AppendColumn(self.out_objects[0].get_normatives()[j] + " Баллы", format=wx.LIST_FORMAT_LEFT, width=200)
                
        self.list_ctrl_1.AppendColumn("Сумма очков", format=wx.LIST_FORMAT_LEFT, width=100)
        for out_category in self.out_categories:
            for i in range(len(out_category.get_info())):
                out = []
                out.append(str(out_category.get_info()[i].get_place()))
                out.append(out_category.get_info()[i].get_surname() + " " + out_category.get_info()[i].get_name() + " " + out_category.get_info()[i].get_thirdname())
                out.append(out_category.get_info()[i].get_date())
                out.append(out_category.get_info()[i].get_number())
                out.append(out_category.get_info()[i].get_team())
                for j in range(0, len(out_category.get_info()[i].get_normatives())):
                    if (j == 0 or j % 3 == 0):
                        continue
                    out.append(str(out_category.get_info()[i].get_normatives()[j]))
                out.append(str(out_category.get_info()[i].get_sum()))
                
                self.list_ctrl_1.Append(out)
            
            
    def copy_all_to_clipboard(self, event):
        # Создаем временный Excel файл
        wb = openpyxl.Workbook()
        ws = wb.active
        
        # Получаем количество строк и колонок
        col_count = self.list_ctrl_1.GetColumnCount()
        cur_row = 1
        
        # Вывод верхней шапки
        ws.append(["Фестиваль Всероссийского физкультурно-спортивного комплекса \"Готов к труду и обороне\""])
        ws.merge_cells(start_row=cur_row, start_column=1, end_row=cur_row, end_column=col_count)
        cur_row += 1
        ws.append(["Протокол соревнования"])
        ws.merge_cells(start_row=cur_row, start_column=1, end_row=cur_row, end_column=col_count)
        cur_row += 1
        ws.append([" Зачёт"])
        ws.merge_cells(start_row=cur_row, start_column=1, end_row=cur_row, end_column=col_count)
        cur_row += 1
        temp = ["Дата"]
        for i in range(1, int(col_count/2)):
            temp.append("")
        temp.append("Город")
        ws.append(temp)
        ws.merge_cells(start_row=cur_row, start_column=1, end_row=cur_row, end_column=int(col_count/2))
        ws.merge_cells(start_row=cur_row, start_column=int(col_count)/2+1, end_row=cur_row, end_column=col_count)
        cur_row += 1

        
        # Собираем заголовки колонок
        for out_category in self.out_categories:
            normatives_headers = []
            for i in out_category.get_normatives_without_results():
                normatives_headers.append(i + " Результат")
                normatives_headers.append(i + " Баллы")
            headers = ["Место", "ФИО","Дата рождения", "Нагрудн. Номер", "Команда" ] + normatives_headers + ["Сумма очков"]
            ws.append(headers)
            # Увеличение размера заголовков
            ws.row_dimensions[cur_row].height = 70
            
            cur_row += 1
            ws.append([f'({to_roman(out_category.get_category())} ступень)  {category_to_age(out_category.get_category())} лет {out_category.get_sex()}'])
            ws.merge_cells(start_row=cur_row, start_column=1, end_row=cur_row, end_column=col_count)
            
            # Подсветка цветом категории и возраста 
            ws[f'A{cur_row}'].fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type="solid")
            cur_row+=1

            # Собираем данные
            for i in range(len(out_category.get_info())):
                out = []
                out.append(str(out_category.get_info()[i].get_place()))
                out.append(out_category.get_info()[i].get_surname() + " " + out_category.get_info()[i].get_name() + " " + out_category.get_info()[i].get_thirdname())
                out.append(out_category.get_info()[i].get_date())
                out.append(out_category.get_info()[i].get_number())
                out.append(out_category.get_info()[i].get_team())
                for j in range(0, len(out_category.get_info()[i].get_normatives())):
                    if (j == 0 or j % 3 == 0):
                        continue
                    out.append(str(out_category.get_info()[i].get_normatives()[j]))
                out.append(str(out_category.get_info()[i].get_sum()))
                
                self.list_ctrl_1.Append(out)
                ws.append(out)
                cur_row += 1

        # Сохраняем файл во временной директории
        # temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
        # wb.save(temp_file.name)

        # Копируем данные в буфер обмена в текстовом формате
        # output = []
        # for row in ws.iter_rows(values_only=True):
        #     output.append('\t'.join(map(str, row)))
        
        # читаемый шрифт
        font_style = Font(name='Times New Roman', size=16, vertAlign='baseline')
        alignment= Alignment(horizontal='center', vertical='center', wrap_text=True)
        for row in ws.iter_rows():
            for cell in row:
                cell.font = font_style
                cell.alignment = alignment
        
        # Верхняя часть
        ws['A1'].font = Font(name='Times New Roman', size=28, vertAlign='baseline', bold=True)
        ws['A2'].font = Font(name='Times New Roman', size=28, vertAlign='baseline', bold=True)
        ws['A3'].font = Font(name='Times New Roman', size=28, vertAlign='baseline', bold=True)
        ws['A4'].font = Font(name='Times New Roman', size=28, vertAlign='baseline')
        ws['G4'].font = Font(name='Times New Roman', size=28, vertAlign='baseline')
        
        # Размеры ячеек
        ws.row_dimensions[1].height = 70
        ws.row_dimensions[2].height = 40
        ws.row_dimensions[3].height = 40
        ws.row_dimensions[4].height = 40
        
        for col in range(1, 1000):
            col_letter = openpyxl.utils.get_column_letter(col)
            ws.column_dimensions[col_letter].width = 20
        ws.column_dimensions['B'].width = 60
        ws.column_dimensions['E'].width = 70
        
        

        
        # # Сохранение файла таблицы
        # pyperclip.copy('\n'.join(output))
        wb.save('styled_document.xlsx')
        # Закрываем временный файл
        # temp_file.close()

        # Уведомляем пользователя
        wx.MessageBox("Данные скопированы в буфер обмена!", "Успех", wx.OK | wx.ICON_INFORMATION)  
                
    def get_data(self, event):
        #Удаление старых записей
        self.list_ctrl_1.DeleteAllColumns()
        self.list_ctrl_1.DeleteAllItems()
        
        # Для запроса в базу
        category = self.choice_1.GetSelection()+2
        sex =  self.radio_box_1.GetString(self.radio_box_1.GetSelection())
        self.out_objects.clear()
        # Пример формата получаемых данных
        self.out_objects.append(Out_object(1, "Beltyukov","Mikhail", "Olegovich", "20.09.2004", "1", "Сургут", ["Бег", 20, 5, "Плаванье", 10, 3, "Лыжи", 15, 4], 20))
        self.out_objects.append(Out_object(2, "Beltyukov2","Mikhail2",  "Olegovich2", "20.09.2000", "2", "НеСургут", ["Бег", 202, 52, "Плаванье", 102, 32, "Лыжи", 152, 42], 10))
        self.out_categories.append(Out_category(self.out_objects, category, sex))
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
    
    app = MyApp(0)
    app.MainLoop()
 