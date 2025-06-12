import wx
from outputResults import outputTeamsResults
class Team_viewer(wx.Panel):
    def __init__(self, parent):
        
        # Объекты для вывода
        self.out_objects = []
        self.out_categories = []
        
        # begin wxGlade: Viewer.__init__
        super(Team_viewer, self).__init__(parent) 
        self.SetSize((600, 800))
        self.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Segoe UI"))
        
        
        self.grid_sizer_1 = wx.FlexGridSizer(2, 1, 0, 0)
        
        self.button_1 = wx.Button(self, wx.ID_ANY, "Обновить")
        self.button_1.SetBackgroundColour(wx.Colour(204, 50, 50))
        self.button_1.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))
        self.button_1.SetMinSize((350, 25))
        self.grid_sizer_1.Add(self.button_1, 0, 0, 0)
        
        self.list_ctrl_1 = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
        self.list_ctrl_1.SetMinSize(wx.Size(10000, 350))
        self.list_ctrl_1.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.list_ctrl_1.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))
        self.grid_sizer_1.Add(self.list_ctrl_1, 1, wx.EXPAND, 0)
        
        self.button_1.Bind(wx.EVT_BUTTON, self.update_data)
        self.SetSizer(self.grid_sizer_1)

        self.Layout()
        # end wxGlade
    def update_data(self, event):
        self.list_ctrl_1.DeleteAllColumns()
        self.list_ctrl_1.DeleteAllItems()
        self.list_ctrl_1.AppendColumn("Место", format=wx.LIST_FORMAT_LEFT, width=100)
        self.list_ctrl_1.AppendColumn("Команда", format=wx.LIST_FORMAT_LEFT, width=200)
        self.list_ctrl_1.AppendColumn("Сумма очков", format=wx.LIST_FORMAT_LEFT, width=200)
        for i in outputTeamsResults():
            self.list_ctrl_1.Append(i)