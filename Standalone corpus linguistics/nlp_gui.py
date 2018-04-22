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

        self.open_text_item = None
        self.open_text_dialog = None

        self.close_files_item = None
        self.close_file_dialog = None

        self.close_text_item = None
        self.close_text_dialog = None

        self.close_all_files_item = None

        self.save_item = None
        self.about_item = None

        self.createFileMenu()

        self.global_settings_item = None
        self.global_settings_frame = None
        self.global_settings_listbook = None
        self.global_settings_file_window = None
        self.global_settings_file_box = None
        self.show_full_pathname_checkbox = None
        self.global_default_extension_label = None
        self.global_default_extension_txtctrl = None
        self.global_default_extension_hbox = None
        self.global_file_button = None

        self.global_settings_token_window = None
        self.global_token_vbox = None
        self.global_letter_hbox = None
        self.global_letter_lower_checkbox = None
        self.global_letter_upper_checkbox = None
        self.global_number_checkbox = None
        self.global_punctuation_hbox = None
        self.global_middle_punctuation_checkbox = None
        self.global_end_punctuation_checkbox = None
        self.global_quotation_checkbox = None
        self.global_apostrophe_checkbox = None
        self.global_bracket_checkbox = None
        self.global_whitespace_hbox = None
        self.global_space_checkbox = None
        self.global_tab_checkbox = None
        self.global_newline_checkbox = None

        self.show_full_pathname = True
        self.global_default_extension = ".txt"

        self.tool_settings_item = None

        self.createSettingMenu()
        self.createMenuBar()

        self.CreateStatusBar()
        self.SetStatusText("Corpus linguistics in Python")

    def createFileMenu(self):
        self.open_file_item = self.file_menu.Append(wx.ID_ANY, "Open File(s)", "Open file(s)")
        self.open_dir_item = self.file_menu.Append(wx.ID_ANY, "Open Dir", "Open directory")
        self.open_clipboard_item = self.file_menu.Append(wx.ID_ANY, "Open From Clipboard", "Open from clipboard")
        self.open_text_item = self.file_menu.Append(wx.ID_ANY, "Open From Text Box", "Open from text box")
        self.file_menu.AppendSeparator()
        self.close_files_item = self.file_menu.Append(wx.ID_ANY, "Close File(s)", "Close file(s)")
        self.close_text_item = self.file_menu.Append(wx.ID_ANY, "Close text(s)", "Close text(s)")
        self.close_all_files_item = self.file_menu.Append(wx.ID_ANY, "Close All Files", "Close all files")
        self.file_menu.AppendSeparator()
        self.save_item = self.file_menu.Append(wx.ID_ANY, "Save Results", "Save results of current tab")
        self.about_item = self.file_menu.Append(wx.ID_ABOUT, "About", "About")
        self.file_menu.Append(wx.ID_EXIT, "Exit", "Close")

        self.Bind(wx.EVT_MENU, self.open_files, self.open_file_item)
        self.Bind(wx.EVT_MENU, self.open_dir, self.open_dir_item)
        self.Bind(wx.EVT_MENU, self.open_clipboard, self.open_clipboard_item)
        self.Bind(wx.EVT_MENU, self.open_text, self.open_text_item)
        self.Bind(wx.EVT_MENU, self.close_files, self.close_files_item)
        self.Bind(wx.EVT_MENU, self.close_text, self.close_text_item)
        self.Bind(wx.EVT_MENU, self.close_everything, self.close_all_files_item)
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
                name = "Clipboard (%s...)" % text[:10]
                while name in self.text_bodies:  # if another clipboard text with those same characters is stored
                    name += "1"
                self.text_bodies[name] = text
        if debug:
            self.view_text()

    def open_text(self, event=None):
        self.open_text_dialog = wx.TextEntryDialog(self, message="Type in some words to add to your corpus",
                                        caption="Open from text box", style=wx.TextEntryDialogStyle | wx.TE_MULTILINE)
        if self.open_text_dialog.ShowModal() == wx.ID_OK:
            text = self.open_text_dialog.GetValue()
            name = "Textbox (%s...)" % text[:10]
            while name in self.text_bodies:  # if another textbox with those same characters is stored
                name += "1"
            self.text_bodies[name] = text
        if debug:
            self.view_text()

    def close_files(self, event=None):
        """
        Allow user to select 1 or more files to close. Those files will be deleted from the filenames
        :param event:
        :return:
        """
        self.close_file_dialog = wx.MultiChoiceDialog(self, message="Select file(s) to close", caption="Close file(s)",
                                                      choices=self.filenames)
        if self.close_file_dialog.ShowModal() == wx.ID_OK:
            to_remove = [self.filenames[i] for i in self.close_file_dialog.GetSelections()]
            self.filenames = [name for name in self.filenames if name not in to_remove]
        self.close_file_dialog.Destroy()
        if debug:
            print(self.get_filenames())

    def close_text(self, event=None):
        """
        Allow user to select 1 or more texts (e.g., from Clipboard or text box) to remove.
        :param event:
        :return:
        """
        keys = [x for x in self.text_bodies.keys()]  # calculate list ahead of time to ensure correct order
        self.close_text_dialog = wx.MultiChoiceDialog(self, message="Select text(s) to close", caption="Close text(s)",
                                                      choices=keys)
        if self.close_text_dialog.ShowModal() == wx.ID_OK:
            to_remove = [keys[i] for i in self.close_text_dialog.GetSelections()]
            # TODO: fix
            for key in keys:  # don't loop through dict directly because that would cause problems
                if key in to_remove:
                    del self.text_bodies[key]  # remove the entry
        if debug:
            self.view_text()

    def close_everything(self, event=None):
        """Clear out all the files and bodies of text"""
        self.filenames = []
        self.text_bodies = {}
        if debug:
            print(self.filenames)
            print(self.text_bodies)

    def save_results(self, event=None):
        # TODO: write this
        raise NotImplementedError

    def open_global_settings(self, event=None):
        # token definition
        #     regex
        #     valid words
        #     stop words
        #     select all
        #     deselect all
        #     case sensitive
        self.global_settings_frame = wx.Frame(parent=self, title="Global Settings", name="Global Settings")
        self.global_settings_listbook = wx.Listbook(parent=self.global_settings_frame, style=wx.LB_LEFT)

        self.global_settings_file_window = wx.Panel(parent=self.global_settings_listbook)
        self.global_settings_file_box = wx.BoxSizer(orient=wx.VERTICAL)

        self.show_full_pathname_checkbox = wx.CheckBox(self.global_settings_file_window, label="Show full pathname")
        self.show_full_pathname_checkbox.SetValue(self.show_full_pathname)
        self.global_settings_file_box.Add(self.show_full_pathname_checkbox, proportion=1)

        self.global_default_extension_label = wx.StaticText(self.global_settings_file_window, label="Default extension to use with Open Dir")
        self.global_default_extension_txtctrl = wx.TextCtrl(self.global_settings_file_window, value=self.global_default_extension)
        self.global_default_extension_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.global_default_extension_hbox.Add(self.global_default_extension_label, proportion=0)
        self.global_default_extension_hbox.Add(self.global_default_extension_txtctrl, proportion=0)
        self.global_settings_file_box.Add(self.global_default_extension_hbox, proportion=0)

        self.global_file_button = wx.Button(self.global_settings_file_window, label="Apply")
        self.global_settings_file_box.Add(self.global_file_button, proportion=1)
        self.global_settings_file_window.SetSizer(self.global_settings_file_box)
        self.global_settings_file_window.Bind(wx.EVT_BUTTON, self.apply_global_file_settings, self.global_file_button)

        self.global_settings_token_window = wx.Panel(parent=self.global_settings_listbook)
        self.global_token_vbox = wx.BoxSizer(orient=wx.VERTICAL)

        self.global_letter_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.global_letter_lower_checkbox = wx.CheckBox(self.global_settings_token_window, label="lowercase letters")
        self.global_letter_hbox.Add(self.global_letter_lower_checkbox, proportion=1)
        self.global_letter_upper_checkbox = wx.CheckBox(self.global_settings_token_window, label="uppercase letters")
        self.global_letter_hbox.Add(self.global_letter_upper_checkbox, proportion=1)
        self.global_token_vbox.Add(self.global_letter_hbox, proportion=1)

        self.global_number_checkbox = wx.CheckBox(self.global_settings_token_window, label="numbers")
        self.global_token_vbox.Add(self.global_number_checkbox, proportion=1)

        self.global_punctuation_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.global_middle_punctuation_checkbox = wx.CheckBox(self.global_settings_token_window, label="middle punctuation :,-")
        self.global_punctuation_hbox.Add(self.global_middle_punctuation_checkbox, proportion=1)
        self.global_end_punctuation_checkbox = wx.CheckBox(self.global_settings_token_window, label="end punctuation .?!")
        self.global_punctuation_hbox.Add(self.global_end_punctuation_checkbox, proportion=1)
        self.global_quotation_checkbox = wx.CheckBox(self.global_settings_token_window, label="quotation \"")
        self.global_punctuation_hbox.Add(self.global_quotation_checkbox, proportion=1)
        self.global_apostrophe_checkbox = wx.CheckBox(self.global_settings_token_window, label="apostrophe '")
        self.global_punctuation_hbox.Add(self.global_apostrophe_checkbox, proportion=1)
        self.global_bracket_checkbox = wx.CheckBox(self.global_settings_token_window, label="bracket (){}[]")
        self.global_punctuation_hbox.Add(self.global_bracket_checkbox, proportion=1)
        self.global_token_vbox.Add(self.global_punctuation_hbox, proportion=1)

        self.global_whitespace_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.global_space_checkbox = wx.CheckBox(self.global_settings_token_window, label="space")
        self.global_whitespace_hbox.Add(self.global_space_checkbox, proportion=1)
        self.global_tab_checkbox = wx.CheckBox(self.global_settings_token_window, label="tab")
        self.global_whitespace_hbox.Add(self.global_tab_checkbox, proportion=1)
        self.global_newline_checkbox = wx.CheckBox(self.global_settings_token_window, label="newline")
        self.global_whitespace_hbox.Add(self.global_newline_checkbox, proportion=1)
        self.global_token_vbox.Add(self.global_whitespace_hbox, proportion=1)

        self.global_settings_token_window.SetSizer(self.global_token_vbox)

        self.global_settings_listbook.InsertPage(0, self.global_settings_file_window, "Files")
        self.global_settings_listbook.InsertPage(1, self.global_settings_token_window, "Token Defnition")
        self.global_settings_frame.Show()

    def apply_global_file_settings(self, event=wx.EVT_BUTTON):
        self.show_full_pathname = self.show_full_pathname_checkbox.IsChecked()
        self.global_default_extension = self.global_default_extension_txtctrl.GetLineText(0)

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