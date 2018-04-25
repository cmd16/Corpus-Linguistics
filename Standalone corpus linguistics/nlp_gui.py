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

        self.open_dir_item = None

        self.open_clipboard_item = None

        self.open_text_item = None

        self.close_files_item = None

        self.close_text_item = None

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
        self.global_save_intermediate_hbox = None
        self.global_save_intermediate_choice = None
        self.global_save_intermediate_statictext = None
        self.global_save_intermediate_dirpick_button = None
        self.global_save_intermediate_txtctrl = None
        self.global_file_apply_button = None

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
        self.global_token_check_hbox = None
        self.global_token_checkboxes = None
        self.global_token_checkall_button = None
        self.global_token_uncheckall_button = None
        self.global_regex_hbox = None
        self.global_regex_statictext = None
        self.global_regex_txtctrl = None
        self.global_case_sensitive_checkbox = None
        self.global_stop_words_hbox = None
        self.global_stop_words_statictext = None
        self.global_stop_words_txtctrl = None
        self.global_stop_words_file_button = None
        self.global_token_apply_button = None

        self.show_full_pathname = True
        self.global_default_extension = ".txt"
        self.global_save_intermediate = 0
        self.global_save_intermediate_dir = ""

        self.global_letter_lower = True
        self.global_letter_upper = True
        self.global_number = False
        self.global_middle_punctuation = False
        self.global_end_punctuation = False
        self.global_quotation = False
        self.global_apostrophe = False
        self.global_bracket = False
        self.global_space = False
        self.global_tab = False
        self.global_newline = False
        self.global_regex = "[a-zA-Z]+"
        self.global_case_sensitive = False
        self.global_regex_set = False
        self.global_stop_words = []
        self.global_stop_words_modified = False

        self.tool_settings_item = None
        self.tool_settings_frame = None
        self.tool_settings_listbook = None

        self.tool_settings_wordlist_window = None
        self.tool_wordlist_vbox = None
        self.tool_wordlist_case_choice = None
        self.tool_wordlist_target_corpus_choice = None
        self.tool_load_wordlist_hbox = None
        self.tool_load_wordlist_button = None
        self.tool_wordlist_filename_txtctrl = None
        self.tool_wordlist_apply_button = None

        self.tool_settings_concordance_window = None
        self.tool_settings_ngram_window = None
        self.tool_settings_keyword_window = None

        self.tool_wordlist_case = 0  # in this case means (match whatever global is)
        self.tool_wordlist_target_corpus = 0  # everything
        self.tool_wordlist_wordlists = []

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
        self.Bind(wx.EVT_MENU, self.openGlobalSettings, self.global_settings_item)
        self.Bind(wx.EVT_MENU, self.openToolSettings, self.tool_settings_item)

    def createMenuBar(self):
        self.menubar = wx.MenuBar()
        self.menubar.Append(self.file_menu, "File")  # Adding the "file_menu" to the MenuBar
        self.menubar.Append(self.setting_menu, "Settings")
        self.SetMenuBar(self.menubar)  # Adding the MenuBar to the Frame content.

    def open_files(self, event=None):
        open_file_dialog = wx.FileDialog(self, message="Choose corpus files", style=
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE)
        if open_file_dialog.ShowModal() == wx.ID_OK:
            self.filenames.extend(self.open_file_dialog.GetPaths())
        open_file_dialog.Destroy()
        if debug:
            print(self.get_filenames())

    def open_dir(self, event=None):
        open_dir_dialog = wx.DirDialog(self, message="Choose directory containing corpus files",
                  style=wx.DD_DIR_MUST_EXIST)
        if open_dir_dialog.ShowModal() == wx.ID_OK:
            path = self.open_dir_dialog.GetPath()
            for filename in os.listdir(path):
                if filename.endswith(self.global_default_extension):
                    self.filenames.append(os.path.join(path, filename))
        open_dir_dialog.Destroy()
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
        open_text_dialog = wx.TextEntryDialog(self, message="Type in some words to add to your corpus",
                                        caption="Open from text box", style=wx.TextEntryDialogStyle | wx.TE_MULTILINE)
        if open_text_dialog.ShowModal() == wx.ID_OK:
            text = open_text_dialog.GetValue()
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
        close_file_dialog = wx.MultiChoiceDialog(self, message="Select file(s) to close", caption="Close file(s)",
                                                      choices=self.filenames)
        if close_file_dialog.ShowModal() == wx.ID_OK:
            to_remove = [self.filenames[i] for i in close_file_dialog.GetSelections()]
            self.filenames = [name for name in self.filenames if name not in to_remove]
        close_file_dialog.Destroy()
        if debug:
            print(self.get_filenames())

    def close_text(self, event=None):
        """
        Allow user to select 1 or more texts (e.g., from Clipboard or text box) to remove.
        :param event:
        :return:
        """
        keys = [x for x in self.text_bodies.keys()]  # calculate list ahead of time to ensure correct order
        close_text_dialog = wx.MultiChoiceDialog(self, message="Select text(s) to close", caption="Close text(s)",
                                                      choices=keys)
        if close_text_dialog.ShowModal() == wx.ID_OK:
            to_remove = [keys[i] for i in close_text_dialog.GetSelections()]
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

    def openGlobalSettings(self, event=None):
        """
        Open the global settings menu
        :param event:
        :return:
        """
        self.global_settings_frame = wx.Frame(parent=self, title="Global Settings")
        self.global_settings_frame.SetSize(0, 23, 800, 500)  # this looks good on my 13in MacBook Pro, but idk how it looks other places
        self.global_settings_listbook = wx.Listbook(parent=self.global_settings_frame, style=wx.LB_LEFT)

        self.global_settings_file_window = wx.Panel(parent=self.global_settings_listbook)
        self.global_settings_file_box = wx.BoxSizer(orient=wx.VERTICAL)

        self.show_full_pathname_checkbox = wx.CheckBox(self.global_settings_file_window, label="Show full pathname")
        self.show_full_pathname_checkbox.SetValue(self.show_full_pathname)
        self.global_settings_file_box.Add(self.show_full_pathname_checkbox, proportion=0, flag=wx.ALIGN_CENTER)
        self.global_settings_file_box.AddSpacer(10)

        self.global_default_extension_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.global_default_extension_label = wx.StaticText(self.global_settings_file_window, label="Default extension to use with Open Dir")
        self.global_default_extension_hbox.Add(self.global_default_extension_label, proportion=0)
        self.global_default_extension_hbox.AddSpacer(5)
        self.global_default_extension_txtctrl = wx.TextCtrl(self.global_settings_file_window, value=self.global_default_extension)
        self.global_default_extension_hbox.Add(self.global_default_extension_txtctrl, proportion=0)
        self.global_settings_file_box.Add(self.global_default_extension_hbox, proportion=0, flag=wx.ALIGN_CENTER)
        self.global_settings_file_box.AddSpacer(10)

        self.global_save_intermediate_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.global_save_intermediate_statictext = wx.StaticText(self.global_settings_file_window, label="Sometimes, to process data, the system creates intermediate files."
                                                                 " Do you want to delete them, keep them, or have the system ask first?")
        self.global_save_intermediate_statictext.Wrap(150)
        self.global_save_intermediate_hbox.Add(self.global_save_intermediate_statictext, proportion=0)
        self.global_save_intermediate_hbox.AddSpacer(5)
        self.global_save_intermediate_choice = wx.Choice(self.global_settings_file_window, choices=["delete", "keep", "ask"])
        self.global_save_intermediate_choice.SetSelection(self.global_save_intermediate)  # set to the int
        self.global_save_intermediate_hbox.Add(self.global_save_intermediate_choice, proportion=0)
        self.global_save_intermediate_hbox.AddSpacer(5)
        self.global_save_intermediate_dirpick_button = wx.Button(self.global_settings_file_window, label="Choose dir to save in")
        self.global_save_intermediate_hbox.Add(self.global_save_intermediate_dirpick_button, proportion=0)
        self.global_save_intermediate_hbox.AddSpacer(5)
        self.global_save_intermediate_txtctrl = wx.TextCtrl(self.global_settings_file_window, style=wx.TE_READONLY)
        self.global_save_intermediate_txtctrl.ChangeValue(self.global_save_intermediate_dir)
        self.global_save_intermediate_hbox.Add(self.global_save_intermediate_txtctrl, proportion=3)
        if not self.global_save_intermediate:  # if the variable is 0 for delete
            self.global_save_intermediate_dirpick_button.Enable(False)
        self.global_settings_file_box.Add(self.global_save_intermediate_hbox, proportion=0, flag=wx.ALIGN_CENTER | wx.EXPAND)
        self.global_settings_file_box.AddSpacer(10)

        self.global_file_apply_button = wx.Button(self.global_settings_file_window, label="Apply")
        self.global_settings_file_box.Add(self.global_file_apply_button, proportion=0, flag=wx.ALIGN_CENTER)

        self.global_settings_file_window.SetSizer(self.global_settings_file_box)
        self.global_settings_file_window.Bind(wx.EVT_CHOICE, self.global_save_intermediate_enable, self.global_save_intermediate_choice)
        self.global_settings_file_window.Bind(wx.EVT_BUTTON, self.global_save_intermediate_dirpick, self.global_save_intermediate_dirpick_button)
        self.global_settings_file_window.Bind(wx.EVT_BUTTON, self.apply_global_file_settings, self.global_file_apply_button)

        self.global_settings_listbook.InsertPage(0, self.global_settings_file_window, "Files")

        self.global_settings_token_window = wx.Panel(parent=self.global_settings_listbook)
        self.global_token_vbox = wx.BoxSizer(orient=wx.VERTICAL)

        self.global_letter_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.global_letter_lower_checkbox = wx.CheckBox(self.global_settings_token_window, label="lowercase letters")
        self.global_letter_lower_checkbox.SetValue(self.global_letter_lower)
        self.global_letter_hbox.Add(self.global_letter_lower_checkbox, proportion=0)
        self.global_letter_hbox.AddSpacer(5)
        self.global_letter_upper_checkbox = wx.CheckBox(self.global_settings_token_window, label="uppercase letters")
        self.global_letter_upper_checkbox.SetValue(self.global_letter_upper)
        self.global_letter_hbox.Add(self.global_letter_upper_checkbox, proportion=0)
        self.global_letter_hbox.AddSpacer(5)
        self.global_token_vbox.Add(self.global_letter_hbox, proportion=0)
        self.global_token_vbox.AddSpacer(5)

        self.global_number_checkbox = wx.CheckBox(self.global_settings_token_window, label="numbers")
        self.global_number_checkbox.SetValue(self.global_number)
        self.global_token_vbox.Add(self.global_number_checkbox, proportion=0)
        self.global_token_vbox.AddSpacer(5)

        self.global_punctuation_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.global_middle_punctuation_checkbox = wx.CheckBox(self.global_settings_token_window, label="middle punctuation :,-")
        self.global_middle_punctuation_checkbox.SetValue(self.global_middle_punctuation)
        self.global_punctuation_hbox.Add(self.global_middle_punctuation_checkbox, proportion=0)
        self.global_punctuation_hbox.AddSpacer(5)
        self.global_end_punctuation_checkbox = wx.CheckBox(self.global_settings_token_window, label="end punctuation .?!")
        self.global_end_punctuation_checkbox.SetValue(self.global_end_punctuation)
        self.global_punctuation_hbox.Add(self.global_end_punctuation_checkbox, proportion=0)
        self.global_punctuation_hbox.AddSpacer(5)
        self.global_quotation_checkbox = wx.CheckBox(self.global_settings_token_window, label="quotation \"")
        self.global_quotation_checkbox.SetValue(self.global_quotation)
        self.global_punctuation_hbox.Add(self.global_quotation_checkbox, proportion=0)
        self.global_punctuation_hbox.AddSpacer(5)
        self.global_apostrophe_checkbox = wx.CheckBox(self.global_settings_token_window, label="apostrophe '")
        self.global_apostrophe_checkbox.SetValue(self.global_apostrophe)
        self.global_punctuation_hbox.Add(self.global_apostrophe_checkbox, proportion=0)
        self.global_punctuation_hbox.AddSpacer(5)
        self.global_bracket_checkbox = wx.CheckBox(self.global_settings_token_window, label="bracket (){}[]")
        self.global_bracket_checkbox.SetValue(self.global_bracket)
        self.global_punctuation_hbox.Add(self.global_bracket_checkbox, proportion=0)
        self.global_token_vbox.Add(self.global_punctuation_hbox, proportion=0)
        self.global_token_vbox.AddSpacer(5)

        self.global_whitespace_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.global_space_checkbox = wx.CheckBox(self.global_settings_token_window, label="space")
        self.global_quotation_checkbox.SetValue(self.global_space)
        self.global_whitespace_hbox.Add(self.global_space_checkbox, proportion=0)
        self.global_whitespace_hbox.AddSpacer(5)
        self.global_tab_checkbox = wx.CheckBox(self.global_settings_token_window, label="tab")
        self.global_tab_checkbox.SetValue(self.global_tab)
        self.global_whitespace_hbox.Add(self.global_tab_checkbox, proportion=0)
        self.global_whitespace_hbox.AddSpacer(5)
        self.global_newline_checkbox = wx.CheckBox(self.global_settings_token_window, label="newline")
        self.global_newline_checkbox.SetValue(self.global_newline)
        self.global_whitespace_hbox.Add(self.global_newline_checkbox, proportion=0)
        self.global_token_vbox.Add(self.global_whitespace_hbox, proportion=0)
        self.global_token_vbox.AddSpacer(10)

        self.global_token_check_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.global_token_checkall_button = wx.Button(self.global_settings_token_window, label="Select all")
        self.global_token_check_hbox.Add(self.global_token_checkall_button, proportion=0)
        self.global_token_check_hbox.AddSpacer(10)
        self.global_token_uncheckall_button = wx.Button(self.global_settings_token_window, label="Deselect all")
        self.global_token_check_hbox.Add(self.global_token_uncheckall_button, proportion=0)
        self.global_token_vbox.Add(self.global_token_check_hbox, proportion=0, flag=wx.ALIGN_CENTER)
        self.global_token_vbox.AddSpacer(10)
        self.global_token_checkboxes = [self.global_letter_lower_checkbox, self.global_letter_upper_checkbox,
                                        self.global_number_checkbox, self.global_middle_punctuation_checkbox,
                                        self.global_end_punctuation_checkbox, self.global_quotation_checkbox,
                                        self.global_apostrophe_checkbox, self.global_bracket_checkbox,
                                        self.global_space_checkbox, self.global_tab_checkbox, self.global_newline_checkbox]

        self.global_regex_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.global_regex_statictext = wx.StaticText(self.global_settings_token_window, label="Regex")
        self.global_regex_hbox.Add(self.global_regex_statictext, proportion=0)
        self.global_regex_hbox.AddSpacer(5)
        self.global_regex_txtctrl = wx.TextCtrl(self.global_settings_token_window)
        self.global_regex_txtctrl.ChangeValue(self.global_regex)
        self.global_regex_hbox.Add(self.global_regex_txtctrl, proportion=2)
        self.global_token_vbox.Add(self.global_regex_hbox, 0, wx.ALIGN_CENTER)
        self.global_token_vbox.AddSpacer(10)

        self.global_case_sensitive_checkbox = wx.CheckBox(self.global_settings_token_window, label="Case sensitive")
        self.global_case_sensitive_checkbox.SetValue(self.global_case_sensitive)
        self.global_token_vbox.Add(self.global_case_sensitive_checkbox, proportion=0)
        self.global_token_vbox.AddSpacer(15)

        self.global_stop_words_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.global_stop_words_statictext = wx.StaticText(self.global_settings_token_window, label="stop words /regexes/")
        self.global_stop_words_hbox.Add(self.global_stop_words_statictext, proportion=0)
        self.global_stop_words_hbox.AddSpacer(5)
        self.global_stop_words_txtctrl = wx.TextCtrl(self.global_settings_token_window, style=wx.TE_MULTILINE)
        text = ""
        for word in self.global_stop_words:
            text += "%s\n" % word
        self.global_stop_words_txtctrl.ChangeValue(text)
        del text  # don't need the extra data cluttering up the memory
        self.global_stop_words_hbox.Add(self.global_stop_words_txtctrl, proportion=3, flag=wx.EXPAND)
        self.global_stop_words_hbox.AddSpacer(5)
        self.global_stop_words_file_button = wx.Button(self.global_settings_token_window, label="Open file")
        self.global_stop_words_hbox.Add(self.global_stop_words_file_button, proportion=1)
        self.global_token_vbox.Add(self.global_stop_words_hbox, proportion=1, flag=wx.ALIGN_CENTER)
        self.global_token_vbox.AddSpacer(10)

        self.global_token_apply_button = wx.Button(self.global_settings_token_window, label="Apply")
        self.global_token_vbox.Add(self.global_token_apply_button, proportion=0, flag=wx.ALIGN_CENTER)

        self.global_settings_token_window.SetSizer(self.global_token_vbox)

        self.global_settings_token_window.Bind(wx.EVT_TEXT, self.global_set_regex, self.global_regex_txtctrl)
        self.global_settings_token_window.Bind(wx.EVT_BUTTON, self.global_token_checkall, self.global_token_checkall_button)
        self.global_settings_token_window.Bind(wx.EVT_BUTTON, self.global_token_uncheckall, self.global_token_uncheckall_button)
        self.global_settings_token_window.Bind(wx.EVT_CHECKBOX, self.global_token_checkbox_mark)
        self.global_case_sensitive_checkbox.Bind(wx.EVT_CHECKBOX, lambda *args, **kwargs: None)  # make sure that case_sensitive doesn't disable regex
        self.global_settings_token_window.Bind(wx.EVT_BUTTON, self.global_token_open_stoplist, self.global_stop_words_file_button)
        self.global_settings_token_window.Bind(wx.EVT_TEXT, self.global_token_stop_words_modify, self.global_stop_words_txtctrl)
        self.global_settings_token_window.Bind(wx.EVT_BUTTON, self.apply_global_token_settings, self.global_token_apply_button)

        self.global_settings_listbook.InsertPage(1, self.global_settings_token_window, "Token Defnition")
        self.global_settings_frame.Show()

    def global_save_intermediate_enable(self, event=wx.EVT_CHOICE):
        if self.global_save_intermediate_choice.GetSelection():
            self.global_save_intermediate_dirpick_button.Enable(True)
        else:
            self.global_save_intermediate_dirpick_button.Enable(False)

    def global_save_intermediate_dirpick(self, event=wx.EVT_BUTTON):
        open_dir_dialog = wx.DirDialog(self.global_settings_file_window, message="Pick a directory to save intermediate files in",
                                       style=wx.DD_DIR_MUST_EXIST)
        if open_dir_dialog.ShowModal() == wx.ID_OK:
            self.global_save_intermediate_txtctrl.SetValue(open_dir_dialog.GetPath())
        open_dir_dialog.Destroy()

    def apply_global_file_settings(self, event=wx.EVT_BUTTON):
        self.show_full_pathname = self.show_full_pathname_checkbox.IsChecked()
        self.global_default_extension = self.global_default_extension_txtctrl.GetValue()
        self.global_save_intermediate = self.global_save_intermediate_choice.GetSelection()
        if self.global_save_intermediate:
            self.global_save_intermediate_dir = self.global_save_intermediate_txtctrl.GetValue()

    def global_set_regex(self, event=wx.EVT_TEXT):
        if self.global_regex_txtctrl.GetValue() != self.global_regex:
            for checkbox in self.global_token_checkboxes:
                checkbox.Enable(False)
            self.global_token_checkall_button.Enable(False)
            self.global_token_uncheckall_button.Enable(False)
        else:
            for checkbox in self.global_token_checkboxes:
                checkbox.Enable(True)
            self.global_token_checkall_button.Enable(True)
            self.global_token_uncheckall_button.Enable(True)

    def global_token_checkall(self, event=wx.EVT_BUTTON):
        for checkbox in self.global_token_checkboxes:
            checkbox.SetValue(1)
        self.global_token_checkbox_mark()

    def global_token_uncheckall(self, event=wx.EVT_BUTTON):
        for checkbox in self.global_token_checkboxes:
            checkbox.SetValue(0)
        self.global_token_checkbox_mark()

    def global_token_checkbox_mark(self, event=wx.EVT_CHECKBOX):
        value_tups = [(self.global_letter_lower, self.global_letter_lower_checkbox),
                    (self.global_letter_upper, self.global_letter_upper_checkbox),
                    (self.global_number, self.global_number_checkbox),
                    (self.global_middle_punctuation, self.global_middle_punctuation_checkbox),
                    (self.global_end_punctuation, self.global_end_punctuation_checkbox),
                    (self.global_quotation, self.global_quotation_checkbox),
                    (self.global_apostrophe, self.global_apostrophe_checkbox),
                    (self.global_bracket, self.global_bracket_checkbox),
                    (self.global_space, self.global_space_checkbox),
                    (self.global_tab, self.global_tab_checkbox),
                    (self.global_newline, self.global_newline_checkbox)]
        for tup in value_tups:
            if tup[0] != tup[1].GetValue():
                self.global_regex_txtctrl.Enable(False)  # turn off the regex txtctrl to avoid conflicts
                break
        else:
            self.global_regex_txtctrl.Enable(True)

    def global_token_open_stoplist(self, event=wx.EVT_BUTTON):
        open_file_dialog = wx.FileDialog(self.global_settings_token_window, message="Choose corpus files", style=
                                                wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE)
        if open_file_dialog.ShowModal() == wx.ID_OK:
            for filename in open_file_dialog.GetPaths():
                f_in = open(filename)
                for line in f_in:
                    self.global_stop_words_txtctrl.write(line)
                f_in.close()
            self.global_stop_words_txtctrl.SetModified(True)
        open_file_dialog.Destroy()

    def global_token_stop_words_modify(self, event=wx.EVT_TEXT):
        self.global_stop_words_modified = True

    def apply_global_token_settings(self, event=None):
        if self.global_regex != self.global_regex_txtctrl.GetValue():
            self.global_regex = self.global_regex_txtctrl.GetValue()
        else:
            self.global_letter_lower = self.global_letter_lower_checkbox.GetValue()
            self.global_letter_upper = self.global_letter_upper_checkbox.GetValue()
            self.global_number = self.global_number_checkbox.GetValue()
            self.global_middle_punctuation = self.global_middle_punctuation_checkbox.GetValue()
            self.global_end_punctuation = self.global_end_punctuation_checkbox.GetValue()
            self.global_quotation = self.global_quotation_checkbox.GetValue()
            self.global_apostrophe = self.global_apostrophe_checkbox.GetValue()
            self.global_bracket = self.global_bracket_checkbox.GetValue()
            self.global_space = self.global_space_checkbox.GetValue()
            self.global_tab = self.global_tab_checkbox.GetValue()
            self.global_newline = self.global_newline_checkbox.GetValue()
        self.global_regex_txtctrl.Enable(True)
        for checkbox in self.global_token_checkboxes:
            checkbox.Enable(True)
        self.global_case_sensitive = self.global_case_sensitive_checkbox.GetValue()
        if self.global_stop_words_modified:
            self.global_stop_words = []
            for word in self.global_stop_words_txtctrl.GetValue().split("\n"):
                if word:  # empty strings don't count
                    self.global_stop_words.append(word)
        self.global_stop_words_modified = False

    def openToolSettings(self, event=None):
        # concordance?
        # ngrams
        #     display options
        #         rank
        #         frequency
        #     other options
        #         token definition
        #         case sensitive
        #         replace line breaks
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
        self.tool_settings_frame = wx.Frame(parent=self, title="Global Settings", name="Global Settings")
        self.tool_settings_frame.SetSize(0, 23, 600, 500)
        self.tool_settings_listbook = wx.Listbook(parent=self.tool_settings_frame, style=wx.LB_LEFT)

        self.tool_settings_wordlist_window = wx.Panel(parent=self.tool_settings_listbook)
        self.tool_wordlist_vbox = wx.BoxSizer(orient=wx.VERTICAL)

        if self.global_case_sensitive:
            case_str = "Case sensitive"
        else:
            case_str = "Case insensitive"
        self.tool_wordlist_case_choice = wx.Choice(self.tool_settings_wordlist_window,
                                                   choices=["Match global setting (%s)" % case_str, "Case sensitive", "Case insensitive"])
        self.tool_wordlist_case_choice.SetSelection(self.tool_wordlist_case)
        self.tool_wordlist_vbox.Add(self.tool_wordlist_case_choice, proportion=0, flag=wx.ALIGN_CENTER)
        self.tool_wordlist_vbox.AddSpacer(10)

        self.tool_wordlist_target_corpus_choice = wx.Choice(self.tool_settings_wordlist_window,
                                                            choices=["Use all (files and texts)", "Use files", "Use texts", "Use wordlist(s)"])
        self.tool_wordlist_target_corpus_choice.SetSelection(self.tool_wordlist_target_corpus)
        self.tool_wordlist_vbox.Add(self.tool_wordlist_target_corpus_choice, proportion=0, flag=wx.ALIGN_CENTER)
        self.tool_wordlist_vbox.AddSpacer(5)

        self.tool_load_wordlist_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.tool_load_wordlist_button = wx.Button(self.tool_settings_wordlist_window, label="Load wordlist(s)")
        if self.tool_wordlist_target_corpus != 3:  # 3 is the index of Use wordlist
            self.tool_load_wordlist_button.Enable(False)
        self.tool_load_wordlist_hbox.Add(self.tool_load_wordlist_button, proportion=0)
        self.tool_load_wordlist_hbox.AddSpacer(5)
        self.tool_wordlist_filename_txtctrl = wx.TextCtrl(self.tool_settings_wordlist_window, style=wx.TE_READONLY)  # TODO: figure out why TE_MULTILINE not working
        if self.tool_wordlist_target_corpus == 3:
            for filename in self.tool_wordlist_wordlists:
                self.tool_wordlist_filename_txtctrl.write("%s\n" % filename)
        self.tool_load_wordlist_hbox.Add(self.tool_wordlist_filename_txtctrl, proportion=3, flag=wx.EXPAND)
        self.tool_wordlist_vbox.Add(self.tool_load_wordlist_hbox, proportion=1, flag=wx.ALIGN_CENTER)
        self.tool_wordlist_vbox.AddSpacer(10)

        self.tool_wordlist_apply_button = wx.Button(self.tool_settings_wordlist_window, label="Apply")
        self.tool_wordlist_vbox.Add(self.tool_wordlist_apply_button, proportion=0, flag=wx.ALIGN_CENTER)

        self.tool_settings_wordlist_window.Bind(wx.EVT_CHOICE, self.tool_wordlist_enable_target_corpus, self.tool_wordlist_target_corpus_choice)
        self.tool_settings_wordlist_window.Bind(wx.EVT_BUTTON, self.tool_wordlist_load_wordlist, self.tool_load_wordlist_button)
        self.tool_settings_wordlist_window.Bind(wx.EVT_BUTTON, self.apply_tool_wordlist_settings, self.tool_wordlist_apply_button)

        self.tool_settings_wordlist_window.SetSizer(self.tool_wordlist_vbox)
        self.tool_settings_listbook.InsertPage(0, self.tool_settings_wordlist_window, "Wordlist")

        self.tool_settings_concordance_window = wx.Panel(parent=self.tool_settings_listbook)
        self.tool_settings_listbook.InsertPage(1, self.tool_settings_concordance_window, "Concordance")

        self.tool_settings_ngram_window = wx.Panel(parent=self.tool_settings_listbook)
        self.tool_settings_listbook.InsertPage(2, self.tool_settings_ngram_window, "Ngrams")

        self.tool_settings_keyword_window = wx.Panel(parent=self.tool_settings_listbook)
        self.tool_settings_listbook.InsertPage(3, self.tool_settings_keyword_window, "Keyword Analysis")

        self.tool_settings_frame.Show()

    def tool_wordlist_enable_target_corpus(self, event=wx.EVT_CHOICE):
        if self.tool_wordlist_target_corpus_choice.GetSelection() == 3:  # 3 is index of Use wordlist
            self.tool_load_wordlist_button.Enable(True)
        else:
            self.tool_load_wordlist_button.Enable(False)

    def tool_wordlist_load_wordlist(self, event=wx.EVT_BUTTON):
        file_dialog = wx.FileDialog(self.tool_settings_wordlist_window, style=wx.FD_MULTIPLE)
        if file_dialog.ShowModal() == wx.ID_OK:
            text = ""
            for filename in file_dialog.GetFilenames():
                text += "%s\n" % filename
            self.tool_wordlist_filename_txtctrl.write(text)
        file_dialog.Destroy()

    def apply_tool_wordlist_settings(self, event=wx.EVT_BUTTON):
        self.tool_wordlist_case = self.tool_wordlist_case_choice.GetSelection()
        self.tool_wordlist_target_corpus = self.tool_wordlist_target_corpus_choice.GetSelection()
        if self.tool_wordlist_target_corpus == 3:
            self.tool_wordlist_wordlists = []
            for filename in self.tool_wordlist_filename_txtctrl.GetValue().split("\n"):
                if filename:
                    self.tool_wordlist_wordlists.append(filename)

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