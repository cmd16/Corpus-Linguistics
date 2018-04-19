import wx
import os
debug = True


class nlp_gui_class(wx.Frame):
    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(nlp_gui_class, self).__init__(*args, **kw)
        self.file_menu = wx.Menu()
        self.setting_menu = wx.Menu()
        self.menubar = None
        self.filenames = []
        self.text_bodies = {}  # for text input directly from a textbox or clipboard. Map a "filename" to its text.

        self.open_file_item = None
        self.open_file_dialog = None
        self.open_dir_item = None
        self.open_dir_dialog = None
        self.open_clipboard_item = None
        self.close_files_item = None
        self.checklistframe = None
        self.checklistbox = None
        self.close_all_files_item = None
        self.save_item = None
        self.about_item = None

        self.createFileMenu()

        self.global_settings_item = None
        self.tool_settings_item = None

        self.createSettingMenu()
        self.createMenuBar()

        self.CreateStatusBar()
        self.SetStatusText("Corpus linguistics in Python")

    def createFileMenu(self):
        self.open_file_item = self.file_menu.Append(wx.ID_ANY, "Open File(s)", "Open file(s)")
        self.open_dir_item = self.file_menu.Append(wx.ID_ANY, "Open Dir", "Open directory")
        self.open_clipboard_item = self.file_menu.Append(wx.ID_ANY, "Open From Clipboard", "Open from clipboard")
        self.file_menu.AppendSeparator()
        self.close_files_item = self.file_menu.Append(wx.ID_ANY, "Close Selected File(s)", "Close selected file(s)")
        self.close_all_files_item = self.file_menu.Append(wx.ID_ANY, "Close All Files", "Close all files")
        self.file_menu.AppendSeparator()
        self.save_item = self.file_menu.Append(wx.ID_ANY, "Save Results", "Save results of current tab")
        self.about_item = self.file_menu.Append(wx.ID_ABOUT, "About", "About")
        self.file_menu.Append(wx.ID_EXIT, "Exit", "Close")

        self.Bind(wx.EVT_MENU, self.open_files, self.open_file_item)
        self.Bind(wx.EVT_MENU, self.open_dir, self.open_dir_item)
        self.Bind(wx.EVT_MENU, self.open_clipboard, self.open_clipboard_item)
        self.Bind(wx.EVT_MENU, self.close_files, self.close_files_item)
        self.Bind(wx.EVT_MENU, self.close_all_files, self.close_all_files_item)
        self.Bind(wx.EVT_MENU, self.save_results, self.save_item)

    def createSettingMenu(self):
        self.global_settings_item = self.setting_menu.Append(wx.ID_ANY, "Global Settings", "Global settings")
        self.tool_settings_item = self.setting_menu.Append(wx.ID_ANY, "Tool Settings", "Tool settings")

        self.Bind(wx.EVT_MENU, self.open_global_settings, self.global_settings_item)
        self.Bind(wx.EVT_MENU, self.open_tool_settings, self.tool_settings_item)

    def createMenuBar(self):
        self.menuBar = wx.MenuBar()
        self.menuBar.Append(self.file_menu, "File")  # Adding the "file_menu" to the MenuBar
        self.menuBar.Append(self.setting_menu, "Settings")
        self.SetMenuBar(self.menuBar)  # Adding the MenuBar to the Frame content.

    def open_files(self, event=None):
        self.open_file_dialog = wx.FileDialog(self, message="Choose corpus files", style=
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE)
        if self.open_file_dialog.ShowModal() == wx.ID_OK:
            self.filenames.extend(self.open_file_dialog.GetPaths())
        self.open_file_dialog.Destroy()
        if debug:
            print(self.get_filenames())

    def open_dir(self, event=None):
        self.open_dir_dialog = wx.DirDialog(self, message="Choose directory containing corpus files",
                  style=wx.DD_DIR_MUST_EXIST)
        if self.open_dir_dialog.ShowModal() == wx.ID_OK:
            path = self.open_dir_dialog.GetPath()
            for filename in os.listdir(path):
                self.filenames.append(os.path.join(path, filename))
        self.open_dir_dialog.Destroy()
        if debug:
            print(self.get_filenames())

    def open_clipboard(self, event=None):
        text_data = wx.TextDataObject()
        if wx.TheClipboard.Open():
            success = wx.TheClipboard.GetData(text_data)
            wx.TheClipboard.Close()
            if success:
                text = text_data.GetText()
                name = "Clipboard (%s...)" % (text[:10])
                while name in self.text_bodies:  # if another clipboard text with those same characters is stored
                    name += "1"
                self.text_bodies[name] = text
        if debug:
            self.view_text()

    def close_files(self, event=None):
        # TODO: fix
        self.checklistframe = wx.Frame(parent=self, name="Select file(s) to close")
        self.checklistbox = wx.CheckListBox(self.checklistframe, id=wx.ID_ANY, choices=self.filenames, name="Select files to close")
        if self.checklistframe._initCheckBoxes() == wx.ID_OK:
            self.filenames = [name for name in self.filenames if name not in self.checklistbox.GetCheckedStrings()]
        self.checklistbox.Destroy()
        if debug:
            print(self.get_filenames())

    def close_all_files(self, event=None):
        """Clear out all the files and bodies of text"""
        self.filenames = []
        self.text_bodies = {}

    def save_results(self, event=None):
        # TODO: write this
        raise NotImplementedError

    def open_global_settings(self, event=None):
        # character encoding?
        # files
        #     show full pathname
        #     default extension to use with OpenDir
        # token definition
        #     positive/negative letter (uppercase lowercase)
        #     number
        #     punctuation
        #     whitespace
        #     regex
        #     valid words
        #     stop words
        #     select all
        #     deselect all
        #     case sensitive
        pass

    def open_tool_settings(self, event=None):
        # concordance
        #     hit number
        #     KWIC display
        # ngrams
        #     display options
        #         rank
        #         frequency
        #     other options
        #         case sensitive
        #         replace line breaks
        # word list
        #     display options
        #         rank
        #         frequency
        #         word
        #     other options
        #         treat all data as lowercase
        #     target corpus
        #         use raw file(s)
        #         use word list(s) (warning: can only do wordlist and keyword analysis)
        # keyword list
        #     display options
        #         rank
        #         frequency
        #         keyness
        #         keyword
        #     other options
        #         treat all data as lowercase
        #     keyness values
        #         keyword statistic
        #         keyword statistic threshold
        #     reference corpus
        #         use raw file(s)
        #         use word list(s)
        pass

    def get_corpus(self, event=None):
        """
        Debugging method to see all the filenames and the 
        :param event:
        :return:
        """

    def get_filenames(self):
        return self.filenames

    def view_text(self):
        for item in self.text_bodies:
            print(item)
            print(self.text_bodies[item])

if __name__ == '__main__':
    app = wx.App()
    # Setting up the menu.
    frame = nlp_gui_class(None, -1, 'nlp_gui')
    frame.SetSize(0, 0, 200, 50)
    # Creating the menubar.
    frame.Show()
    app.MainLoop()