import wx


class nlp_gui_class(wx.Frame):
    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(nlp_gui_class, self).__init__(*args, **kw)
        self.file_menu = wx.Menu()
        self.setting_menu = wx.Menu()
        self.menubar = None
        self.filenames = []

        self.createFileMenu()
        self.createSettingMenu()
        self.createMenuBar()

        self.CreateStatusBar()
        self.SetStatusText("Corpus linguistics in Python")

    def createFileMenu(self):
        OPEN_FILE_ID = 101
        OPEN_DIR_ID = 102
        OPEN_CLIPBOARD_ID = 103
        DRAG_FILE_ID = 104
        CLOSE_FILE_ID = 105
        CLOSE_ALL_FILES_ID = 106
        SAVE_RESULTS_ID = 107
        open_file_item = self.file_menu.Append(OPEN_FILE_ID, "Open File(s)", "Open file(s)")
        open_dir_item = self.file_menu.Append(OPEN_DIR_ID, "Open Dir", "Open directory")
        open_clipboard_item = self.file_menu.Append(OPEN_CLIPBOARD_ID, "Open From Clipboard", "Open from clipboard")
        open_drag_item = self.file_menu.Append(DRAG_FILE_ID, "Drag File", "Drag file to open")
        self.file_menu.AppendSeparator()
        close_files_item = self.file_menu.Append(CLOSE_FILE_ID, "Close Selected File(s)", "Close selected file(s)")
        close_all_files_item = self.file_menu.Append(CLOSE_ALL_FILES_ID, "Close All Files", "Close all files")
        self.file_menu.AppendSeparator()
        save_item = self.file_menu.Append(SAVE_RESULTS_ID, "Save Results", "Save results of current tab")
        about_item = self.file_menu.Append(wx.ID_ABOUT, "About", "About")
        self.file_menu.Append(wx.ID_EXIT, "Exit", "Close")

        self.Bind(wx.EVT_MENU, self.open_files, open_file_item)

    def createSettingMenu(self):
        GLOBAL_SETTINGS_ID = 201
        TOOL_SETTINGS_ID = 202
        self.setting_menu.Append(GLOBAL_SETTINGS_ID, "Global Settings", "Global settings")
        self.setting_menu.Append(TOOL_SETTINGS_ID, "Tool Settings", "Tool settings")

    def createMenuBar(self):
        menuBar = wx.MenuBar()
        menuBar.Append(self.file_menu, "File")  # Adding the "file_menu" to the MenuBar
        menuBar.Append(self.setting_menu, "Settings")
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

    def open_files(self, event=None):
        openFileDialog = wx.FileDialog(frame, message="Choose corpus files", style=
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE)
        openFileDialog.ShowModal()
        self.filenames.extend(openFileDialog.GetPaths())
        openFileDialog.Destroy()

    def get_filenames(self):
        return self.filenames

if __name__ == '__main__':
    app = wx.App()
    # Setting up the menu.
    frame = nlp_gui_class(None, -1, 'nlp_gui')
    frame.SetSize(0, 0, 200, 50)
    # Creating the menubar.
    frame.Show()
    app.MainLoop()