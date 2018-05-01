import wx
import os
import nltk
import main
import operator

class NlpGuiClass(wx.Frame):
    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(NlpGuiClass, self).__init__(*args, **kw)
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
        self.global_file_vbox = None
        self.global_show_full_pathname_checkbox = None
        self.global_default_extension_label = None
        self.global_default_extension_txtctrl = None
        self.global_default_extension_hbox = None
        self.global_save_intermediate_hbox = None
        self.global_save_intermediate_choice = None
        self.global_save_intermediate_statictext = None
        self.global_save_intermediate_dirpick_button = None
        self.global_save_intermediate_txtctrl = None
        self.global_file_apply_button = None

        self.show_full_pathname = True
        self.global_default_extension = ".txt"
        self.global_save_intermediate = 0
        self.global_save_intermediate_dir = ""

        self.global_settings_token_window = None
        self.global_token_vbox = None
        self.global_regex_hbox = None
        self.global_regex_statictext = None
        self.global_regex_txtctrl = None
        self.global_case_sensitive_checkbox = None
        self.global_stop_words_hbox = None
        self.global_stop_words_statictext = None
        self.global_stop_words_txtctrl = None
        self.global_stop_words_file_button = None
        self.global_token_apply_button = None

        self.global_regex = "[a-zA-Z]+"
        self.global_case_sensitive = False
        self.global_stop_words = []
        self.global_stop_words_modified = False

        self.tool_settings_item = None
        self.tool_settings_frame = None
        self.tool_settings_listbook = None

        self.tool_settings_wordlist_window = None
        self.tool_wordlist_vbox = None
        self.tool_wordlist_case_choice = None
        self.tool_wordlist_regex_hbox = None
        self.tool_wordlist_regex_checkbox = None
        self.tool_wordlist_regex_txtctrl = None
        self.tool_wordlist_target_corpus_choice = None
        self.tool_load_wordlist_hbox = None
        self.tool_load_wordlist_button = None
        self.tool_wordlist_filename_txtctrl = None
        self.tool_wordlist_apply_button = None

        self.tool_wordlist_case = 0  # in this case means (match whatever global is)
        self.tool_wordlist_regex_checkval = True  # match whatever global is
        self.tool_wordlist_regex = ""
        self.tool_wordlist_target_corpus = 0  # everything
        self.tool_wordlist_wordlists = []

        self.tool_settings_concordance_window = None
        self.tool_concordance_vbox = None
        self.tool_concordance_target_corpus_choice = None
        self.tool_concordance_displaywindow_hbox = None
        self.tool_concordance_displaywindow_txt = None
        self.tool_concordance_displaywindow_spinctrl = None
        self.tool_concordance_apply_button = None

        self.tool_concordance_target_corpus = 0  # everything
        self.tool_concordance_case = 0  # same as global settings
        self.tool_concordance_win_length = 7

        self.tool_settings_ngram_window = None
        self.tool_ngram_vbox = None
        self.tool_ngram_case_choice = None
        self.tool_ngram_regex_hbox = None
        self.tool_ngram_regex_vbox = None
        self.tool_ngram_regex_checkbox = None
        self.tool_ngram_regex_button = None
        self.tool_ngram_regex_txtctrl = None
        self.tool_ngram_nontoken_hbox = None
        self.tool_ngram_nontoken_checkbox = None
        self.tool_ngram_nontoken_button = None
        self.tool_ngram_nontoken_txtctrl = None
        self.tool_ngram_stop_hbox = None
        self.tool_ngram_stop_checkbox = None
        self.tool_ngram_stop_button = None
        self.tool_ngram_stop_txtctrl = None
        self.tool_ngram_freq_hbox = None
        self.tool_ngram_freq_checkbox = None
        self.tool_ngram_freq_spinctrl = None
        self.tool_ngram_ufreq_checkbox = None
        self.tool_ngram_ufreq_spinctrl = None
        self.tool_ngram_newline_checkbox = None
        self.tool_ngram_precision_hbox = None
        self.tool_ngram_precision_txt = None
        self.tool_ngram_precision_spinctrl = None
        self.tool_ngram_2d_hbox = None
        self.tool_ngram_2d_txt = None
        self.tool_ngram_2d_choice = None
        self.tool_ngram_3d_hbox = None
        self.tool_ngram_3d_txt = None
        self.tool_ngram_3d_choice = None
        self.tool_ngram_4d_hbox = None
        self.tool_ngram_4d_txt = None
        self.tool_ngram_4d_choice = None
        self.tool_ngram_button = None

        self.tool_ngram_case = 0
        self.tool_ngram_regex_checkval = True  # match whatever global is
        self.tool_ngram_regex = ""
        self.tool_ngram_nontoken_checkval = True
        self.tool_ngram_nontokens = []
        self.tool_ngram_stop_checkval = True
        self.tool_ngram_stopwords = []
        self.tool_ngram_freq_checkval = False
        self.tool_ngram_freq = 1
        self.tool_ngram_ufreq_checkval = False
        self.tool_ngram_ufreq = 1
        self.tool_ngram_newline_checkval = True
        self.tool_ngram_precision = 6

        self.ngram_measures_2 = ["CHI phi", "CHI tscore", "CHI squared", "Dice dice", "Dice jaccard", "Fisher left",
                           "Fisher right",
                           "Fisher twotailed", "Mutual information log likelihood",
                           "Mutual information pointwise mutual information", "Mutual information poisson stirling",
                           "Mutual information true mutual information", "Odds"]
        self.ngram_measures_2_tups = []
        for measure in self.ngram_measures_2:
            if measure == "Odds":
                self.ngram_measures_2_tups.append((measure, "odds.pm"))
            elif measure == "CHI squared":
                self.ngram_measures_2_tups.append((measure, "x2.pm"))
            elif not measure.startswith("Mutual"):
                if "log" in measure:
                    self.ngram_measures_2_tups.append((measure, "ll.pm"))
                elif "pointwise" in measure:
                    self.ngram_measures_2_tups.append((measure, "pmi.pm"))
                elif "poisson" in measure:
                    self.ngram_measures_2_tups.append((measure, "ps.pm"))
                else:
                    self.ngram_measures_2_tups.append((measure, "tmi.pm"))
            else:
                self.ngram_measures_2_tups.append((measure, measure.split()[1] + ".pm"))
        self.tool_ngram_2d_idx = self.ngram_measures_2.index("Mutual information log likelihood")
        self.ngram_measures_3 = ["Mutual information log likelihood", "Mutual information pointwise mutual information",
                           "Mutual information poisson stirling", "Mutual information true mutual information"]
        self.ngram_measures_3_tups = []
        for measure in self.ngram_measures_3:
            if "log" in measure:
                self.ngram_measures_3_tups.append((measure, "ll.pm"))
            elif "pointwise" in measure:
                self.ngram_measures_3_tups.append((measure, "pmi.pm"))
            elif "poisson" in measure:
                self.ngram_measures_3_tups.append((measure, "ps.pm"))
            else:
                self.ngram_measures_3_tups.append((measure, "tmi.pm"))
        self.tool_ngram_3d_idx = self.ngram_measures_3.index("Mutual information log likelihood")
        self.ngram_measures_4 = ["Mutual information log likelihood"]
        self.ngram_measures_4_tups = [(self.ngram_measures_4[0], "ll.pm")]
        self.tool_ngram_4d_idx = 0

        self.tool_settings_keyword_window = None
        self.tool_keyword_vbox = None
        self.tool_keyword_p_choice = None
        self.tool_keyword_reference_choice = None
        self.tool_keyword_load_hbox = None
        self.tool_keyword_reference_button = None
        self.tool_keyword_swap_button = None
        self.tool_keyword_reference_txtctrl = None
        self.tool_keyword_button = None

        self.p_values = [0.05, 0.01, 0.001, 0.0001, 0]
        self.tool_keyword_p_choices = ["p = 0.05 (exclude keywords with log likelihood < 3.84)",
                                       "p = 0.01 (exclude keywords with log likelihood < 6.63)",
                                       "p = 0.001 (exclude keywords with log likelihood < 10.83",
                                       "p = 0.0001 (exclude keywords with log likelihood < 15.13",
                                       "include all keywords"]
        self.tool_keyword_p_idx = 1
        self.tool_keyword_reference_idx = 0
        self.tool_keyword_reference_filenames = []

        self.main_window = None
        self.main_listbook = None
        self.listbook_idx = 0

        self.main_wordlist_window = None
        self.main_wordlist_vbox = None
        self.main_wordlist_info_hbox = None
        self.main_wordlist_info_hbox = None
        self.main_wordlist_types_txt = None
        self.main_wordlist_tokens_txt = None
        self.main_wordlist_flexgrid = None
        self.main_wordlist_start_hbox = None
        self.main_wordlist_start_button = None
        self.main_wordlist_page_spinctrl = None
        self.main_wordlist_page_button = None
        self.main_wordlist_search_txt = None
        self.main_wordlist_search_hbox = None
        self.main_wordlist_search_term_txt = None
        self.main_wordlist_search_exact_checkbox = None
        self.main_wordlist_search_case = None
        self.main_wordlist_search_regex = None
        self.main_wordlist_searchbar_hbox = None
        self.main_wordlist_searchbar_txtctrl = None
        self.main_wordlist_searchbar_button = None
        self.main_wordlist_sort_hbox = None
        self.main_wordlist_sort_choice = None
        self.main_wordlist_sort_reverse_checkbox = None
        self.main_wordlist_sort_button = None

        self.freqdist = None
        self.wordlist_files_dirty = False  # tracks when a new freqdist needs to be made
        self.page_len = 20
        self.main_wordlist_boxes = []
        self.freqdist_pages = []

        self.main_concordance_window = None
        self.main_concordance_vbox = None
        self.main_concordance_hits_txt = None
        self.main_concordance_flexgrid = None
        self.main_concordance_page_hbox = None
        self.main_concordance_page_spinctrl = None
        self.main_concordance_page_button = None
        self.main_concordance_search_hbox = None
        self.main_concordance_search_term_txt = None
        self.main_concordance_search_regex = None
        self.main_concordance_search_exact_checkbox = None
        self.main_concordance_searchbar_hbox = None
        self.main_concordance_searchbar_txtctrl = None
        self.main_concordance_searchbar_button = None

        self.main_concordance_boxes = []
        self.concordance_pages = []

        self.main_ngram_window = None
        self.main_ngram_vbox = None
        self.main_ngram_info_hbox = None
        self.main_ngram_types_txt = None
        self.main_ngram_size_txt = None
        self.main_ngram_tokens_txt = None
        self.main_ngram_search_txt = None
        self.main_ngram_search_txt = None
        self.main_ngram_flexgrid = None
        self.main_ngram_size_spinctrl = None
        self.main_ngram_start_hbox = None
        self.main_ngram_start_button = None
        self.main_ngram_page_spinctrl = None
        self.main_ngram_page_button = None
        self.main_ngram_search_exact_checkbox = None
        self.main_ngram_search_hbox = None
        self.main_ngram_search_term_txt = None
        self.main_ngram_search_regex = None
        self.main_ngram_searchbar_hbox = None
        self.main_ngram_searchbar_txtctrl = None
        self.main_ngram_searchbar_button = None
        self.main_ngram_sort_hbox = None
        self.main_ngram_sort_choice = None
        self.main_ngram_sort_reverse_checkbox = None
        self.main_ngram_sort_button = None

        self.ngram_freqdist = None
        self.ngram_files_dirty = False
        self.main_ngram_boxes = []
        self.ngram_freqdist_pages = []

        self.main_keyword_window = None

        self.createSettingMenu()
        self.createMenuBar()

        self.CreateStatusBar()
        self.SetStatusText("Corpus linguistics in Python")

        self.createMainWindow()

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
            self.filenames.extend(open_file_dialog.GetPaths())
            self.wordlist_files_dirty = True
            self.ngram_files_dirty = True
        open_file_dialog.Destroy()

    def open_dir(self, event=None):
        open_dir_dialog = wx.DirDialog(self, message="Choose directory containing corpus files",
                  style=wx.DD_DIR_MUST_EXIST)
        if open_dir_dialog.ShowModal() == wx.ID_OK:
            path = self.open_dir_dialog.GetPath()
            for filename in os.listdir(path):
                if filename.endswith(self.global_default_extension):
                    self.filenames.append(os.path.join(path, filename))
            self.wordlist_files_dirty = True
            self.ngram_files_dirty = True
        open_dir_dialog.Destroy()

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
                self.wordlist_files_dirty = True
                self.ngram_files_dirty = True

    def open_text(self, event=None):
        open_text_dialog = wx.TextEntryDialog(self, message="Type in some words to add to your corpus",
                                        caption="Open from text box", style=wx.TextEntryDialogStyle | wx.TE_MULTILINE)
        if open_text_dialog.ShowModal() == wx.ID_OK:
            text = open_text_dialog.GetValue()
            name = "Textbox (%s...)" % text[:10]
            while name in self.text_bodies:  # if another textbox with those same characters is stored
                name += "1"
            self.text_bodies[name] = text
            self.wordlist_files_dirty = True
            self.ngram_files_dirty = True

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
            self.wordlist_files_dirty = True
            self.ngram_files_dirty = True
        close_file_dialog.Destroy()

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
            self.wordlist_files_dirty = True
            self.ngram_files_dirty = True

    def close_everything(self, event=None):
        """Clear out all the files and bodies of text"""
        self.filenames = []
        self.text_bodies = {}
        self.wordlist_files_dirty = True
        self.ngram_files_dirty = True

    def save_results(self, event=None):
        saveDialog = wx.FileDialog(self.main_wordlist_window, message="Save results", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if saveDialog.ShowModal() == wx.ID_OK:
            filename = saveDialog.GetPath()
            if self.listbook_idx == 0:
                main.freqdist_to_wordlistfile(self.freqdist, filename)
        saveDialog.Destroy()

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
        self.global_file_vbox = wx.BoxSizer(orient=wx.VERTICAL)

        self.global_show_full_pathname_checkbox = wx.CheckBox(self.global_settings_file_window, label="Show full pathname")
        self.global_show_full_pathname_checkbox.SetValue(self.show_full_pathname)
        self.global_file_vbox.Add(self.global_show_full_pathname_checkbox, proportion=0, flag=wx.ALIGN_CENTER)
        self.global_file_vbox.AddSpacer(10)

        self.global_default_extension_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.global_default_extension_label = wx.StaticText(self.global_settings_file_window, label="Default extension to use with Open Dir")
        self.global_default_extension_hbox.Add(self.global_default_extension_label, proportion=0)
        self.global_default_extension_hbox.AddSpacer(5)
        self.global_default_extension_txtctrl = wx.TextCtrl(self.global_settings_file_window, value=self.global_default_extension)
        self.global_default_extension_hbox.Add(self.global_default_extension_txtctrl, proportion=0)
        self.global_file_vbox.Add(self.global_default_extension_hbox, proportion=0, flag=wx.ALIGN_CENTER)
        self.global_file_vbox.AddSpacer(10)

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
        self.global_file_vbox.Add(self.global_save_intermediate_hbox, proportion=0, flag=wx.ALIGN_CENTER | wx.EXPAND)
        self.global_file_vbox.AddSpacer(10)

        self.global_file_apply_button = wx.Button(self.global_settings_file_window, label="Apply")
        self.global_file_vbox.Add(self.global_file_apply_button, proportion=0, flag=wx.ALIGN_CENTER)

        self.global_settings_file_window.SetSizer(self.global_file_vbox)
        self.global_settings_file_window.Bind(wx.EVT_CHOICE, self.global_save_intermediate_enable, self.global_save_intermediate_choice)
        self.global_settings_file_window.Bind(wx.EVT_BUTTON, self.global_save_intermediate_dirpick, self.global_save_intermediate_dirpick_button)
        self.global_settings_file_window.Bind(wx.EVT_BUTTON, self.apply_global_file_settings, self.global_file_apply_button)

        self.global_settings_listbook.InsertPage(0, self.global_settings_file_window, "Files")

        self.global_settings_token_window = wx.Panel(parent=self.global_settings_listbook)
        self.global_token_vbox = wx.BoxSizer(orient=wx.VERTICAL)

        self.global_regex_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.global_regex_statictext = wx.StaticText(self.global_settings_token_window, label="Regex")
        self.global_regex_hbox.Add(self.global_regex_statictext, proportion=0)
        self.global_regex_hbox.AddSpacer(5)
        self.global_regex_txtctrl = wx.TextCtrl(self.global_settings_token_window)
        self.global_regex_txtctrl.ChangeValue(self.global_regex)
        self.global_regex_hbox.Add(self.global_regex_txtctrl, proportion=2)
        self.global_token_vbox.Add(self.global_regex_hbox, proportion=0, flag=wx.ALIGN_CENTER)
        self.global_token_vbox.AddSpacer(10)

        self.global_case_sensitive_checkbox = wx.CheckBox(self.global_settings_token_window, label="Case sensitive")
        self.global_case_sensitive_checkbox.SetValue(self.global_case_sensitive)
        self.global_token_vbox.Add(self.global_case_sensitive_checkbox, proportion=0, flag=wx.ALIGN_CENTER)
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
        self.show_full_pathname = self.global_show_full_pathname_checkbox.IsChecked()
        self.global_default_extension = self.global_default_extension_txtctrl.GetValue()
        self.global_save_intermediate = self.global_save_intermediate_choice.GetSelection()
        if self.global_save_intermediate:
            self.global_save_intermediate_dir = self.global_save_intermediate_txtctrl.GetValue()

    def global_token_open_stoplist(self, event=wx.EVT_BUTTON):
        open_file_dialog = wx.FileDialog(self.global_settings_token_window, message="Choose corpus files", style=
                                                wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE)
        if open_file_dialog.ShowModal() == wx.ID_OK:
            for filename in open_file_dialog.GetPaths():
                f_in = open(filename)
                for line in f_in:
                    self.global_stop_words_txtctrl.write(line)
                f_in.close()
            self.global_stop_words_modify()
        open_file_dialog.Destroy()

    def global_token_stop_words_modify(self, event=wx.EVT_TEXT):
        self.global_stop_words_modified = True

    def apply_global_token_settings(self, event=None):
        if self.global_regex != self.global_regex_txtctrl.GetValue():
            self.global_regex = self.global_regex_txtctrl.GetValue()

        self.global_case_sensitive = self.global_case_sensitive_checkbox.GetValue()

        if self.global_stop_words_modified:
            self.global_stop_words = []
            for word in self.global_stop_words_txtctrl.GetValue().split("\n"):
                if word:  # empty strings don't count
                    self.global_stop_words.append(word)
        self.global_stop_words_modified = False

    def openToolSettings(self, event=None):
        self.tool_settings_frame = wx.Frame(parent=self, title="Tool Settings")
        self.tool_settings_frame.SetSize(0, 23, 700, 500)
        self.tool_settings_listbook = wx.Listbook(parent=self.tool_settings_frame, style=wx.LB_LEFT)

        self.tool_settings_wordlist_window = wx.Panel(parent=self.tool_settings_listbook)  # TODO: remember that stopwords are still counted, just not displayed
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

        self.tool_wordlist_regex_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.tool_wordlist_regex_checkbox = wx.CheckBox(self.tool_settings_wordlist_window, label="Use global token definition")
        self.tool_wordlist_regex_checkbox.SetValue(self.tool_wordlist_regex_checkval)
        self.tool_wordlist_regex_hbox.Add(self.tool_wordlist_regex_checkbox, proportion=0)
        self.tool_wordlist_regex_hbox.AddSpacer(5)
        self.tool_wordlist_regex_txtctrl = wx.TextCtrl(self.tool_settings_wordlist_window)
        if self.tool_wordlist_regex_checkval:
            self.tool_wordlist_regex_txtctrl.ChangeValue(self.global_regex)
        else:
            self.tool_wordlist_regex_txtctrl.ChangeValue(self.tool_wordlist_regex)
        if self.tool_wordlist_regex_checkval:  # if using global definition, don't allow regex to be modified
            self.tool_wordlist_regex_txtctrl.Enable(False)
        self.tool_wordlist_regex_hbox.Add(self.tool_wordlist_regex_txtctrl, proportion=2, flag=wx.EXPAND)
        self.tool_wordlist_vbox.Add(self.tool_wordlist_regex_hbox, proportion=0, flag=wx.ALIGN_CENTER)
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

        self.tool_settings_wordlist_window.Bind(wx.EVT_CHECKBOX, self.tool_wordlist_enable_regex, self.tool_wordlist_regex_checkbox)
        self.tool_settings_wordlist_window.Bind(wx.EVT_CHOICE, self.tool_wordlist_enable_target_corpus, self.tool_wordlist_target_corpus_choice)
        self.tool_settings_wordlist_window.Bind(wx.EVT_BUTTON, self.tool_wordlist_load_wordlist, self.tool_load_wordlist_button)
        self.tool_settings_wordlist_window.Bind(wx.EVT_BUTTON, self.apply_tool_wordlist_settings, self.tool_wordlist_apply_button)

        self.tool_settings_wordlist_window.SetSizer(self.tool_wordlist_vbox)
        self.tool_settings_listbook.InsertPage(0, self.tool_settings_wordlist_window, "Wordlist")

        self.tool_settings_concordance_window = wx.Panel(parent=self.tool_settings_listbook)
        self.tool_concordance_vbox = wx.BoxSizer(orient=wx.VERTICAL)
        self.tool_concordance_case_choice = wx.Choice(self.tool_settings_concordance_window,
                                                   choices=["Match global setting (%s)" % case_str, "Case sensitive",
                                                            "Case insensitive"])
        self.tool_concordance_case_choice.SetSelection(self.tool_concordance_case)
        self.tool_concordance_vbox.Add(self.tool_concordance_case_choice, proportion=0, flag=wx.ALIGN_CENTER)
        self.tool_concordance_vbox.AddSpacer(10)

        self.tool_concordance_target_corpus_choice = wx.Choice(self.tool_settings_concordance_window,
                                                            choices=["Use all (files and texts)", "Use files",
                                                                     "Use texts"])
        self.tool_concordance_target_corpus_choice.SetSelection(self.tool_concordance_target_corpus)
        self.tool_concordance_vbox.Add(self.tool_concordance_target_corpus_choice, proportion=0, flag=wx.ALIGN_CENTER)
        self.tool_concordance_vbox.AddSpacer(10)

        self.tool_concordance_displaywindow_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.tool_concordance_displaywindow_txt = wx.StaticText(self.tool_settings_concordance_window,
            label="Number of tokens to show before and after query")
        self.tool_concordance_displaywindow_hbox.Add(self.tool_concordance_displaywindow_txt, proportion=0)
        self.tool_concordance_displaywindow_hbox.AddSpacer(5)
        self.tool_concordance_displaywindow_spinctrl = wx.SpinCtrl(self.tool_settings_concordance_window, initial=7,
                                                                   min=1, max=10)
        self.tool_concordance_displaywindow_hbox.Add(self.tool_concordance_displaywindow_spinctrl, proportion=0)
        self.tool_concordance_vbox.Add(self.tool_concordance_displaywindow_hbox, proportion=0, flag=wx.ALIGN_CENTER)
        self.tool_concordance_vbox.AddSpacer(10)

        self.tool_concordance_apply_button = wx.Button(self.tool_settings_concordance_window, label="Apply")
        self.tool_concordance_vbox.Add(self.tool_concordance_apply_button, proportion=0, flag=wx.ALIGN_CENTER)

        self.tool_settings_concordance_window.Bind(wx.EVT_BUTTON, self.apply_tool_concordance_settings, self.tool_concordance_apply_button)

        self.tool_settings_concordance_window.SetSizer(self.tool_concordance_vbox)
        self.tool_settings_listbook.InsertPage(1, self.tool_settings_concordance_window, "Concordance")

        self.tool_settings_ngram_window = wx.Panel(parent=self.tool_settings_listbook)
        self.tool_ngram_vbox = wx.BoxSizer(orient=wx.VERTICAL)

        if self.global_case_sensitive:
            case_str = "Case sensitive"
        else:
            case_str = "Case insensitive"
        self.tool_ngram_case_choice = wx.Choice(self.tool_settings_ngram_window,
                                                   choices=["Match global setting (%s)" % case_str, "Case sensitive", "Case insensitive"])
        self.tool_ngram_case_choice.SetSelection(self.tool_ngram_case)
        self.tool_ngram_vbox.Add(self.tool_ngram_case_choice, proportion=0, flag=wx.ALIGN_CENTER)
        self.tool_ngram_vbox.AddSpacer(10)

        self.tool_ngram_regex_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.tool_ngram_regex_checkbox = wx.CheckBox(self.tool_settings_ngram_window,
                                                        label="Use global token definition")
        self.tool_ngram_regex_checkbox.SetValue(self.tool_ngram_regex_checkval)
        self.tool_ngram_regex_hbox.Add(self.tool_ngram_regex_checkbox, proportion=0)
        self.tool_ngram_regex_hbox.AddSpacer(5)
        self.tool_ngram_regex_button = wx.Button(self.tool_settings_ngram_window, label="Open file(s) with token regexes")
        self.tool_ngram_regex_hbox.Add(self.tool_ngram_regex_button)
        self.tool_ngram_vbox.Add(self.tool_ngram_regex_hbox, proportion=0, flag=wx.ALIGN_CENTER)

        self.tool_ngram_regex_txtctrl = wx.TextCtrl(self.tool_settings_ngram_window, style=wx.TE_MULTILINE)
        if self.tool_ngram_regex_checkval:
            self.tool_ngram_regex_txtctrl.ChangeValue(self.global_regex)
            self.tool_ngram_enable_regex()  # we need to disable the button and textbox
        else:
            self.tool_ngram_regex_txtctrl.ChangeValue(self.tool_ngram_regex)
        self.tool_ngram_vbox.Add(self.tool_ngram_regex_txtctrl, proportion=1, flag=wx.EXPAND)
        self.tool_ngram_vbox.AddSpacer(10)

        self.tool_ngram_nontoken_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.tool_ngram_nontoken_checkbox = wx.CheckBox(self.tool_settings_ngram_window, label="Use global stopwords as nontokens")
        self.tool_ngram_nontoken_checkbox.SetValue(self.tool_ngram_nontoken_checkval)
        self.tool_ngram_nontoken_hbox.Add(self.tool_ngram_nontoken_checkbox, proportion=0)
        self.tool_ngram_nontoken_hbox.AddSpacer(5)
        self.tool_ngram_nontoken_button = wx.Button(self.tool_settings_ngram_window, label="Open file(s) with nontoken regexes")
        self.tool_ngram_nontoken_hbox.Add(self.tool_ngram_nontoken_button, proportion=0)
        self.tool_ngram_vbox.Add(self.tool_ngram_nontoken_hbox, proportion=0, flag=wx.ALIGN_CENTER)

        self.tool_ngram_nontoken_txtctrl = wx.TextCtrl(self.tool_settings_ngram_window, style=wx.TE_MULTILINE)
        if self.tool_ngram_nontoken_checkval:
            for word in self.global_stop_words:
                self.tool_ngram_nontoken_txtctrl.write(word + "\n")
            self.tool_ngram_enable_nontoken()  # we need to disable the button and textbox
        else:
            for regex in self.tool_ngram_nontokens:
                self.tool_ngram_nontoken_txtctrl.write(regex + "\n")
        self.tool_ngram_vbox.Add(self.tool_ngram_nontoken_txtctrl, proportion=1, flag=wx.EXPAND)

        self.tool_ngram_vbox.AddSpacer(10)

        self.tool_ngram_stop_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.tool_ngram_stop_checkbox = wx.CheckBox(self.tool_settings_ngram_window,
                                                        label="Use global stopwords as stopwords")
        self.tool_ngram_stop_checkbox.SetValue(self.tool_ngram_stop_checkval)
        self.tool_ngram_stop_hbox.Add(self.tool_ngram_stop_checkbox, proportion=0)
        self.tool_ngram_stop_hbox.AddSpacer(5)
        self.tool_ngram_stop_button = wx.Button(self.tool_settings_ngram_window,
                                                    label="Open file(s) with stopword regexes")
        self.tool_ngram_stop_hbox.Add(self.tool_ngram_stop_button, proportion=0)
        self.tool_ngram_vbox.Add(self.tool_ngram_stop_hbox, proportion=0, flag=wx.ALIGN_CENTER)
        self.tool_ngram_stop_txtctrl = wx.TextCtrl(self.tool_settings_ngram_window, style=wx.TE_MULTILINE)
        if self.tool_ngram_stop_checkval:
            for word in self.global_stop_words:
                self.tool_ngram_stop_txtctrl.write(word + "\n")
            self.tool_ngram_enable_stop()  # we need to disable the button and textbox
        else:
            for regex in self.tool_ngram_stopwords:
                self.tool_ngram_stop_txtctrl.write(regex + "\n")
        self.tool_ngram_vbox.Add(self.tool_ngram_stop_txtctrl, proportion=1, flag=wx.EXPAND)
        self.tool_ngram_vbox.AddSpacer(10)

        self.tool_ngram_freq_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.tool_ngram_freq_checkbox = wx.CheckBox(self.tool_settings_ngram_window, label="Minimum frequency to display")
        self.tool_ngram_freq_checkbox.SetValue(self.tool_ngram_freq_checkval)
        self.tool_ngram_freq_hbox.Add(self.tool_ngram_freq_checkbox, proportion=0)
        self.tool_ngram_freq_spinctrl = wx.SpinCtrl(self.tool_settings_ngram_window, min=1, initial=self.tool_ngram_freq)
        if not self.tool_ngram_freq_checkval:
            self.tool_ngram_freq_spinctrl.Enable(False)
        self.tool_ngram_freq_hbox.Add(self.tool_ngram_freq_spinctrl)
        self.tool_ngram_freq_hbox.AddSpacer(5)
        self.tool_ngram_ufreq_checkbox = wx.CheckBox(self.tool_settings_ngram_window, label="Maximum frequency to display")
        self.tool_ngram_ufreq_checkbox.SetValue(self.tool_ngram_ufreq_checkval)
        self.tool_ngram_freq_hbox.Add(self.tool_ngram_ufreq_checkbox, proportion=0)
        self.tool_ngram_ufreq_spinctrl = wx.SpinCtrl(self.tool_settings_ngram_window, min=1, initial=self.tool_ngram_ufreq)
        if not self.tool_ngram_ufreq_checkval:
            self.tool_ngram_ufreq_spinctrl.Enable(False)
        self.tool_ngram_freq_hbox.Add(self.tool_ngram_ufreq_spinctrl)
        self.tool_ngram_vbox.Add(self.tool_ngram_freq_hbox, proportion=0, flag=wx.ALIGN_CENTER)
        self.tool_ngram_vbox.AddSpacer(10)

        self.tool_ngram_newline_checkbox = wx.CheckBox(self.tool_settings_ngram_window, label="Allow ngrams to span across lines")
        self.tool_ngram_newline_checkbox.SetValue(self.tool_ngram_newline_checkval)
        self.tool_ngram_vbox.Add(self.tool_ngram_newline_checkbox, proportion=0, flag=wx.ALIGN_CENTER)
        self.tool_ngram_vbox.AddSpacer(10)

        self.tool_ngram_precision_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.tool_ngram_precision_txt = wx.StaticText(self.tool_settings_ngram_window, label="Round score to this many decimal places")
        self.tool_ngram_precision_hbox.Add(self.tool_ngram_precision_txt, proportion=0)
        self.tool_ngram_precision_spinctrl = wx.SpinCtrl(self.tool_settings_ngram_window, min=0, initial=self.tool_ngram_precision)
        self.tool_ngram_precision_hbox.Add(self.tool_ngram_precision_spinctrl, proportion=0)
        self.tool_ngram_vbox.Add(self.tool_ngram_precision_hbox, proportion=0, flag=wx.ALIGN_CENTER)
        self.tool_ngram_vbox.AddSpacer(10)

        self.tool_ngram_2d_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.tool_ngram_2d_txt = wx.StaticText(self.tool_settings_ngram_window, label="Bigram measure")
        self.tool_ngram_2d_hbox.Add(self.tool_ngram_2d_txt, proportion=0)
        self.tool_ngram_2d_hbox.AddSpacer(5)
        self.tool_ngram_2d_choice = wx.Choice(self.tool_settings_ngram_window, choices=self.ngram_measures_2)
        self.tool_ngram_2d_choice.SetSelection(self.tool_ngram_2d_idx)
        self.tool_ngram_2d_hbox.Add(self.tool_ngram_2d_choice, proportion=0)
        self.tool_ngram_vbox.Add(self.tool_ngram_2d_hbox, proportion=0, flag=wx.ALIGN_CENTER)
        self.tool_ngram_vbox.AddSpacer(10)

        self.tool_ngram_3d_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.tool_ngram_3d_txt = wx.StaticText(self.tool_settings_ngram_window, label="Trigram measure")
        self.tool_ngram_3d_hbox.Add(self.tool_ngram_3d_txt, proportion=0)
        self.tool_ngram_3d_hbox.AddSpacer(5)
        self.tool_ngram_3d_choice = wx.Choice(self.tool_settings_ngram_window, choices=self.ngram_measures_3)
        self.tool_ngram_3d_choice.SetSelection(self.tool_ngram_3d_idx)
        self.tool_ngram_3d_hbox.Add(self.tool_ngram_3d_choice, proportion=0)
        self.tool_ngram_vbox.Add(self.tool_ngram_3d_hbox, proportion=0, flag=wx.ALIGN_CENTER)
        self.tool_ngram_vbox.AddSpacer(10)

        self.tool_ngram_4d_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.tool_ngram_4d_txt = wx.StaticText(self.tool_settings_ngram_window, label="Quadrigram measure")
        self.tool_ngram_4d_hbox.Add(self.tool_ngram_4d_txt, proportion=0)
        self.tool_ngram_4d_hbox.AddSpacer(5)
        self.tool_ngram_4d_choice = wx.Choice(self.tool_settings_ngram_window, choices=self.ngram_measures_4)
        self.tool_ngram_4d_hbox.Add(self.tool_ngram_4d_choice, proportion=0)
        self.tool_ngram_vbox.Add(self.tool_ngram_4d_hbox, proportion=0, flag=wx.ALIGN_CENTER)
        self.tool_ngram_vbox.AddSpacer(10)

        self.tool_ngram_button = wx.Button(self.tool_settings_ngram_window, label="Apply")
        self.tool_ngram_vbox.Add(self.tool_ngram_button, proportion=0, flag=wx.ALIGN_CENTER)

        self.tool_settings_ngram_window.Bind(wx.EVT_CHECKBOX, self.tool_ngram_enable_regex, self.tool_ngram_regex_checkbox)
        self.tool_settings_ngram_window.Bind(wx.EVT_BUTTON, self.tool_ngram_open_regex, self.tool_ngram_regex_button)
        self.tool_settings_ngram_window.Bind(wx.EVT_CHECKBOX, self.tool_ngram_enable_nontoken, self.tool_ngram_nontoken_checkbox)
        self.tool_settings_ngram_window.Bind(wx.EVT_BUTTON, self.tool_ngram_open_nontoken, self.tool_ngram_nontoken_button)
        self.tool_settings_ngram_window.Bind(wx.EVT_CHECKBOX, self.tool_ngram_enable_stop, self.tool_ngram_stop_checkbox)
        self.tool_settings_ngram_window.Bind(wx.EVT_BUTTON, self.tool_ngram_open_stop, self.tool_ngram_stop_button)
        self.tool_settings_ngram_window.Bind(wx.EVT_CHECKBOX, self.tool_ngram_enable_freq, self.tool_ngram_freq_checkbox)
        self.tool_settings_ngram_window.Bind(wx.EVT_SPINCTRL, self.tool_ngram_update_freq, self.tool_ngram_freq_spinctrl)
        self.tool_settings_ngram_window.Bind(wx.EVT_CHECKBOX, self.tool_ngram_enable_ufreq, self.tool_ngram_ufreq_checkbox)
        self.tool_settings_ngram_window.Bind(wx.EVT_SPINCTRL, self.tool_ngram_update_ufreq, self.tool_ngram_ufreq_spinctrl)
        self.tool_settings_ngram_window.Bind(wx.EVT_BUTTON, self.apply_tool_ngram_settings, self.tool_ngram_button)

        self.tool_settings_ngram_window.SetSizer(self.tool_ngram_vbox)
        self.tool_settings_listbook.InsertPage(2, self.tool_settings_ngram_window, "Ngrams")

        self.tool_settings_keyword_window = wx.Panel(parent=self.tool_settings_listbook)
        self.tool_keyword_vbox = wx.BoxSizer(orient=wx.VERTICAL)
        self.tool_keyword_p_choice = wx.Choice(self.tool_settings_keyword_window, choices=self.tool_keyword_p_choices)
        self.tool_keyword_p_choice.SetSelection(self.tool_keyword_p_idx)
        self.tool_keyword_vbox.Add(self.tool_keyword_p_choice, proportion=0, flag=wx.ALIGN_CENTER)
        self.tool_keyword_vbox.AddSpacer(10)

        self.tool_keyword_reference_choice = wx.Choice(self.tool_settings_keyword_window, choices=["Use raw file(s)", "Use wordlist"])
        self.tool_keyword_reference_choice.SetSelection(self.tool_keyword_reference_idx)
        self.tool_keyword_vbox.Add(self.tool_keyword_reference_choice, proportion=0, flag=wx.ALIGN_CENTER)
        self.tool_keyword_vbox.AddSpacer(5)

        self.tool_keyword_load_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.tool_keyword_reference_button = wx.Button(self.tool_settings_keyword_window, label="Load")
        self.tool_keyword_load_hbox.Add(self.tool_keyword_reference_button, proportion=0)
        self.tool_keyword_load_hbox.AddSpacer(5)
        self.tool_keyword_swap_button = wx.Button(self.tool_settings_keyword_window, label="Swap with target file(s)")
        self.tool_keyword_load_hbox.Add(self.tool_keyword_swap_button, proportion=0)
        self.tool_keyword_vbox.Add(self.tool_keyword_load_hbox, proportion=0, flag=wx.ALIGN_CENTER)

        self.tool_keyword_reference_txtctrl = wx.TextCtrl(self.tool_settings_keyword_window, style=wx.TE_READONLY)
        for filename in self.tool_keyword_reference_filenames:
            self.tool_keyword_reference_txtctrl.write(filename + "\n")
        self.tool_keyword_vbox.Add(self.tool_keyword_reference_txtctrl, proportion=1, flag=wx.ALIGN_CENTER | wx.EXPAND)
        self.tool_keyword_vbox.AddSpacer(10)

        self.tool_keyword_button = wx.Button(self.tool_settings_keyword_window, label="Apply")
        self.tool_keyword_vbox.Add(self.tool_keyword_button, proportion=0, flag=wx.ALIGN_CENTER)

        self.tool_settings_keyword_window.Bind(wx.EVT_CHOICE, lambda event: self.tool_keyword_reference_txtctrl.SetValue(""), self.tool_keyword_reference_choice)
        self.tool_settings_keyword_window.Bind(wx.EVT_BUTTON, self.tool_keyword_load, self.tool_keyword_reference_button)
        self.tool_settings_keyword_window.Bind(wx.EVT_BUTTON, self.tool_keyword_swap, self.tool_keyword_swap_button)
        self.tool_settings_keyword_window.Bind(wx.EVT_BUTTON, self.apply_tool_keyword_settings, self.tool_keyword_button)

        self.tool_settings_keyword_window.SetSizer(self.tool_keyword_vbox)
        self.tool_settings_listbook.InsertPage(3, self.tool_settings_keyword_window, "Keyword Analysis")

        self.tool_settings_frame.Show()

    def tool_wordlist_enable_regex(self, event=wx.EVT_CHECKBOX):
        if self.tool_wordlist_regex_checkbox.IsChecked():
            self.tool_wordlist_regex_txtctrl.Enable(False)
            self.tool_wordlist_regex_txtctrl.ChangeValue(self.global_regex)
        else:
            self.tool_wordlist_regex_txtctrl.Enable(True)

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
        self.tool_wordlist_regex_checkval = self.tool_wordlist_regex_checkbox.GetValue()
        self.tool_wordlist_regex = self.tool_wordlist_regex_txtctrl.GetValue()
        self.tool_wordlist_target_corpus = self.tool_wordlist_target_corpus_choice.GetSelection()
        if self.tool_wordlist_target_corpus == 3:
            self.tool_wordlist_wordlists = []
            for filename in self.tool_wordlist_filename_txtctrl.GetValue().split("\n"):
                if filename:
                    self.tool_wordlist_wordlists.append(filename)
            self.wordlist_files_dirty = True

    def apply_tool_concordance_settings(self, event=wx.EVT_BUTTON):
        self.tool_concordance_case = self.tool_concordance_case_choice.GetSelection()
        self.tool_concordance_target_corpus = self.tool_concordance_target_corpus_choice.GetSelection()
        self.tool_concordance_win_length = self.tool_concordance_displaywindow_spinctrl.GetValue()

    def tool_ngram_enable_regex(self, event=wx.EVT_CHECKBOX):
        if self.tool_ngram_regex_checkbox.IsChecked():
            self.tool_ngram_regex_txtctrl.Enable(False)
            self.tool_ngram_regex_button.Enable(False)
        else:
            self.tool_ngram_regex_txtctrl.Enable(True)
            self.tool_ngram_regex_button.Enable(True)

    def tool_ngram_open_regex(self, event=wx.EVT_BUTTON):
        fileDialog = wx.FileDialog(self.tool_settings_ngram_window, style=wx.FD_MULTIPLE)
        if fileDialog.ShowModal() == wx.ID_OK:
            text = ""
            filenames = fileDialog.GetPaths()
            for filename in filenames:
                with open(filename) as f_in:
                    for line in f_in:
                        if line.strip():  # if there is something left after removing whitespace
                            text += line
            self.tool_ngram_regex_txtctrl.write(text)
        fileDialog.Destroy()

    def tool_ngram_enable_nontoken(self, event=wx.EVT_CHECKBOX):
        if self.tool_ngram_nontoken_checkbox.IsChecked():
            self.tool_ngram_nontoken_txtctrl.Enable(False)
            self.tool_ngram_nontoken_button.Enable(False)
        else:
            self.tool_ngram_nontoken_txtctrl.Enable(True)
            self.tool_ngram_nontoken_button.Enable(True)

    def tool_ngram_open_nontoken(self, event=wx.EVT_BUTTON):
        fileDialog = wx.FileDialog(self.tool_settings_ngram_window, style=wx.FD_MULTIPLE)
        if fileDialog.ShowModal() == wx.ID_OK:
            text = ""
            filenames = fileDialog.GetPaths()
            for filename in filenames:
                with open(filename) as f_in:
                    for line in f_in:
                        if line.strip():  # if there is something left after removing whitespace
                            text += line
            self.tool_ngram_nontoken_txtctrl.write(text)
        fileDialog.Destroy()

    def tool_ngram_enable_stop(self, event=wx.EVT_CHECKBOX):
        if self.tool_ngram_stop_checkbox.IsChecked():
            self.tool_ngram_stop_txtctrl.Enable(False)
            self.tool_ngram_stop_button.Enable(False)
        else:
            self.tool_ngram_stop_txtctrl.Enable(True)
            self.tool_ngram_stop_button.Enable(True)

    def tool_ngram_open_stop(self, event=wx.EVT_BUTTON):
        fileDialog = wx.FileDialog(self.tool_settings_ngram_window, style=wx.FD_MULTIPLE)
        if fileDialog.ShowModal() == wx.ID_OK:
            text = ""
            filenames = fileDialog.GetPaths()
            for filename in filenames:
                with open(filename) as f_in:
                    for line in f_in:
                        if line.strip():  # if there is something left after removing whitespace
                            text += line
            self.tool_ngram_stop_txtctrl.write(text)
        fileDialog.Destroy()

    def tool_ngram_enable_freq(self, event=wx.EVT_CHECKBOX):
        if self.tool_ngram_freq_checkbox.IsChecked():
            self.tool_ngram_freq_spinctrl.Enable(True)
        else:
            self.tool_ngram_freq_spinctrl.Enable(False)

    def tool_ngram_enable_ufreq(self, event=wx.EVT_CHECKBOX):
        if self.tool_ngram_ufreq_checkbox.IsChecked():
            self.tool_ngram_ufreq_spinctrl.Enable(True)
        else:
            self.tool_ngram_ufreq_spinctrl.Enable(False)

    def tool_ngram_update_freq(self, event=wx.EVT_SPINCTRL):
        num = self.tool_ngram_freq_spinctrl.GetValue()
        self.tool_ngram_ufreq_spinctrl.SetMin(num)

    def tool_ngram_update_ufreq(self, event=wx.EVT_SPINCTRL):
        num = self.tool_ngram_ufreq_spinctrl.GetValue()
        self.tool_ngram_freq_spinctrl.SetMax(num)

    def apply_tool_ngram_settings(self, event=wx.EVT_BUTTON):
        self.tool_ngram_case = self.tool_ngram_case_choice.GetSelection()
        self.tool_ngram_regex_checkval = self.tool_ngram_regex_checkbox.GetValue()
        if not self.tool_ngram_regex_checkval:
            self.tool_ngram_regex = self.tool_ngram_regex_txtctrl.GetValue()
        self.tool_ngram_nontoken_checkval = self.tool_ngram_nontoken_checkbox.GetValue()
        if not self.tool_ngram_regex_checkval:
            self.tool_ngram_nontokens = self.tool_ngram_nontoken_txtctrl.GetValue().split("\n")
        self.tool_ngram_nontoken_checkval = self.tool_ngram_nontoken_checkbox.GetValue()
        if not self.tool_ngram_nontoken_checkval:
            self.tool_ngram_nontokens = self.tool_ngram_nontoken_txtctrl.GetValue().split("\n")
        self.tool_ngram_stop_checkval = self.tool_ngram_stop_checkbox.GetValue()
        if not self.tool_ngram_stop_checkval:
            self.tool_ngram_stopwords = self.tool_ngram_stop_txtctrl.GetValue().split("\n")
        self.tool_ngram_freq_checkval = self.tool_ngram_freq_checkbox.GetValue()
        if self.tool_ngram_freq_checkval:
            self.tool_ngram_freq = self.tool_ngram_freq_spinctrl.GetValue()
        self.tool_ngram_ufreq_checkval = self.tool_ngram_ufreq_checkbox.GetValue()
        if self.tool_ngram_ufreq_checkval:
            self.tool_ngram_ufreq = self.tool_ngram_ufreq_spinctrl.GetValue()
        self.tool_ngram_newline_checkval = self.tool_ngram_newline_checkbox.GetValue()
        self.tool_ngram_precision = self.tool_ngram_precision_spinctrl.GetValue()
        self.tool_ngram_2d_idx = self.tool_ngram_2d_choice.GetSelection()
        self.tool_ngram_3d_idx = self.tool_ngram_3d_choice.GetSelection()

    def tool_keyword_load(self, event=wx.EVT_BUTTON):
        if self.tool_keyword_reference_choice.GetSelection() == 0:  # use raw files
            style=wx.FD_MULTIPLE
        else:
            style=wx.FD_DEFAULT_STYLE
        fileDialog = wx.FileDialog(self.tool_settings_keyword_window, style=style)
        if fileDialog.ShowModal() == wx.ID_OK:
            if style == wx.FD_MULTIPLE:
                filenames = fileDialog.GetPaths()
            else:
                filenames = [fileDialog.GetPath()]
            for filename in filenames:
                self.tool_keyword_reference_txtctrl.write(filename + "\n")
        fileDialog.Destroy()

    def tool_keyword_swap(self, event=wx.EVT_BUTTON):
        if self.tool_wordlist_target_corpus == 3:
            self.tool_keyword_reference_choice.SetSelection(1)  # set to use wordlist
            key_filenames = self.tool_wordlist_wordlists[:]  # copy the list because we are about to modify it
        else:
            if self.tool_wordlist_target_corpus != 1 and self.text_bodies:
                confirm = wx.MessageDialog(self.tool_settings_keyword_window, message="Warning: texts cannot be copied over"
                        " and thus will be lost. Continue?", caption="Warning", style=wx.OK | wx.CANCEL)
                if confirm.ShowModal() != wx.ID_OK:
                    return
                confirm.Destroy()
            key_filenames = self.filenames[:]
            self.text_bodies = {}
        word_filenames = []
        for filename in self.tool_keyword_reference_txtctrl.GetValue().split("\n"):
            if filename.strip() != "":
                word_filenames.append(filename)
        # moving files from keyword to global
        self.filenames = word_filenames
        if self.tool_keyword_reference_idx:  # wordlist
            self.tool_wordlist_target_corpus = 3  # wordlist uses wordlist file
        else:
            self.tool_wordlist_target_corpus = 1  # wordlist uses files only
        # moving files from global to keyword
        self.tool_keyword_reference_txtctrl.SetValue("")
        for filename in key_filenames:
            self.tool_keyword_reference_txtctrl.write(filename + "\n")

    def apply_tool_keyword_settings(self, event=wx.EVT_BUTTON):
        self.tool_keyword_p_idx = self.tool_keyword_p_choice.GetSelection()
        self.tool_keyword_reference_idx = self.tool_keyword_reference_choice.GetSelection()
        self.tool_keyword_reference_filenames = []
        for filename in self.tool_keyword_reference_txtctrl.GetValue().split("\n"):
            if filename.strip() != "":
                self.tool_keyword_reference_filenames.append(filename)

    def createMainWindow(self):
        # TODO: implement word vs regex in search. Fix problem where empty search doesn't clear display. Figure out what's up with the IndexError.
        self.main_window = wx.Frame(self)
        self.main_window.SetSize(0, 23, 1200, 700)
        self.main_listbook = wx.Listbook(self.main_window, style=wx.LB_TOP)

        self.main_wordlist_window = wx.Panel(self.main_listbook)
        self.main_wordlist_vbox = wx.BoxSizer(orient=wx.VERTICAL)

        self.main_wordlist_info_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.main_wordlist_types_txt = wx.StaticText(self.main_wordlist_window, label="Types: 0")
        self.main_wordlist_info_hbox.Add(self.main_wordlist_types_txt, proportion=0)
        self.main_wordlist_info_hbox.AddSpacer(100)
        self.main_wordlist_tokens_txt = wx.StaticText(self.main_wordlist_window, label="Tokens: 0")
        self.main_wordlist_info_hbox.Add(self.main_wordlist_tokens_txt, proportion=0)
        self.main_wordlist_info_hbox.AddSpacer(100)
        self.main_wordlist_search_txt = wx.StaticText(self.main_wordlist_window, label="Search hits: 0")
        self.main_wordlist_info_hbox.Add(self.main_wordlist_search_txt, proportion=0)
        self.main_wordlist_vbox.Add(self.main_wordlist_info_hbox, proportion=0, flag=wx.ALIGN_CENTER)
        self.main_wordlist_vbox.AddSpacer(10)

        self.main_wordlist_flexgrid = wx.FlexGridSizer(cols=3, vgap=5, hgap=10)
        self.main_wordlist_flexgrid.Add(wx.StaticText(self.main_wordlist_window, label="Rank"), 0, 0)
        self.main_wordlist_flexgrid.Add(wx.StaticText(self.main_wordlist_window, label="Frequency"), 0, 1)
        self.main_wordlist_flexgrid.Add(wx.StaticText(self.main_wordlist_window, label="Word"), 0, 2)
        for row in range(1, self.page_len+1):
            self.main_wordlist_boxes.append([wx.StaticText(self.main_wordlist_window, label=str(row)),
                                               wx.StaticText(self.main_wordlist_window, label=""),
                                               wx.StaticText(self.main_wordlist_window, label="")])
            for i in range(3):
                self.main_wordlist_flexgrid.Add(self.main_wordlist_boxes[row-1][i], row, i)
        self.main_wordlist_vbox.Add(self.main_wordlist_flexgrid, proportion=1, flag=wx.EXPAND | wx.ALIGN_CENTER)
        self.main_wordlist_vbox.AddSpacer(10)

        self.main_wordlist_start_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.main_wordlist_start_button = wx.Button(self.main_wordlist_window, label="Start")
        self.main_wordlist_start_hbox.Add(self.main_wordlist_start_button, proportion=0)
        self.main_wordlist_start_hbox.AddSpacer(30)
        self.main_wordlist_page_spinctrl = wx.SpinCtrl(self.main_wordlist_window, min=0, initial=0)
        self.main_wordlist_start_hbox.Add(self.main_wordlist_page_spinctrl, proportion=0)
        self.main_wordlist_start_hbox.AddSpacer(5)
        self.main_wordlist_page_button = wx.Button(self.main_wordlist_window, label="Go")
        self.main_wordlist_start_hbox.Add(self.main_wordlist_page_button, proportion=0)
        self.main_wordlist_vbox.Add(self.main_wordlist_start_hbox, proportion=0, flag=wx.ALIGN_CENTER)
        self.main_wordlist_vbox.AddSpacer(10)

        self.main_wordlist_search_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.main_wordlist_search_term_txt = wx.StaticText(self.main_wordlist_window, label="Search term")
        self.main_wordlist_search_hbox.Add(self.main_wordlist_search_term_txt, proportion=0)
        self.main_wordlist_search_hbox.AddSpacer(5)
        self.main_wordlist_search_regex = wx.CheckBox(self.main_wordlist_window, label="Regex")
        self.main_wordlist_search_hbox.Add(self.main_wordlist_search_regex, proportion=0)
        self.main_wordlist_search_hbox.AddSpacer(5)
        self.main_wordlist_search_exact_checkbox = wx.CheckBox(self.main_wordlist_window, label="Exact")
        self.main_wordlist_search_hbox.Add(self.main_wordlist_search_exact_checkbox, proportion=0)
        self.main_wordlist_vbox.Add(self.main_wordlist_search_hbox, proportion=0, flag=wx.ALIGN_CENTER)
        self.main_wordlist_vbox.AddSpacer(10)

        self.main_wordlist_searchbar_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.main_wordlist_searchbar_txtctrl = wx.TextCtrl(self.main_wordlist_window)
        self.main_wordlist_searchbar_hbox.Add(self.main_wordlist_searchbar_txtctrl, proportion=0)
        self.main_wordlist_searchbar_hbox.AddSpacer(5)
        self.main_wordlist_searchbar_button = wx.Button(self.main_wordlist_window, label="Search")
        self.main_wordlist_searchbar_hbox.Add(self.main_wordlist_searchbar_button, proportion=0)
        self.main_wordlist_vbox.Add(self.main_wordlist_searchbar_hbox, proportion=0, flag=wx.ALIGN_CENTER)
        self.main_wordlist_vbox.AddSpacer(10)

        self.main_wordlist_sort_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.main_wordlist_sort_choice = wx.Choice(self.main_wordlist_window, choices=["Frequency", "Word"])
        self.main_wordlist_sort_reverse_checkbox = wx.CheckBox(self.main_wordlist_window, label="Descending")
        self.main_wordlist_sort_reverse_checkbox.SetValue(1)
        self.main_wordlist_sort_hbox.Add(self.main_wordlist_sort_reverse_checkbox, proportion=0)
        self.main_wordlist_sort_hbox.AddSpacer(5)
        self.main_wordlist_sort_hbox.Add(self.main_wordlist_sort_choice, proportion=0)
        self.main_wordlist_sort_hbox.AddSpacer(5)
        self.main_wordlist_sort_button = wx.Button(self.main_wordlist_window, label="Sort")
        self.main_wordlist_sort_hbox.Add(self.main_wordlist_sort_button, proportion=0)
        self.main_wordlist_vbox.Add(self.main_wordlist_sort_hbox, proportion=0, flag=wx.ALIGN_CENTER)

        self.main_wordlist_window.Bind(wx.EVT_BUTTON, self.main_wordlist_get_wordlist, self.main_wordlist_start_button)
        self.main_wordlist_window.Bind(wx.EVT_BUTTON, lambda event: self.main_wordlist_display_page(num=self.main_wordlist_page_spinctrl.GetValue(), event=event),
                                       self.main_wordlist_page_button)
        self.main_wordlist_window.Bind(wx.EVT_BUTTON, self.main_wordlist_search, self.main_wordlist_searchbar_button)
        self.main_wordlist_window.Bind(wx.EVT_BUTTON, self.main_wordlist_display_wordlist, self.main_wordlist_sort_button)

        self.main_wordlist_window.SetSizer(self.main_wordlist_vbox)
        self.main_listbook.InsertPage(0, self.main_wordlist_window, "Wordlist")

        self.main_concordance_window = wx.Panel(self.main_listbook)
        self.main_concordance_vbox = wx.BoxSizer(orient=wx.VERTICAL)
        self.main_concordance_hits_txt = wx.StaticText(self.main_concordance_window, label="Concordance hits: 0")
        self.main_concordance_vbox.Add(self.main_concordance_hits_txt, proportion=0, flag=wx.ALIGN_CENTER)
        self.main_concordance_vbox.AddSpacer(10)

        self.main_concordance_flexgrid = wx.FlexGridSizer(cols=3, vgap=5, hgap=10)
        self.main_concordance_flexgrid.AddGrowableCol(idx=0, proportion=0)
        self.main_concordance_flexgrid.AddGrowableCol(idx=1, proportion=2)
        self.main_concordance_flexgrid.AddGrowableCol(idx=2, proportion=1)
        self.main_concordance_flexgrid.Add(wx.StaticText(self.main_concordance_window, label="Rank"), 0, 0)
        self.main_concordance_flexgrid.Add(wx.StaticText(self.main_concordance_window, label="KWIC"), 0, 1)
        self.main_concordance_flexgrid.Add(wx.StaticText(self.main_concordance_window, label="Filename"), 0, 2)
        for row in range(1, self.page_len+1):
            self.main_concordance_boxes.append([wx.StaticText(self.main_concordance_window, label=str(row)),
                                               wx.StaticText(self.main_concordance_window, label=""),
                                               wx.StaticText(self.main_concordance_window, label="")])
            for i in range(3):
                self.main_concordance_flexgrid.Add(self.main_concordance_boxes[row-1][i], row, i)
        self.main_concordance_vbox.Add(self.main_concordance_flexgrid, proportion=1, flag=wx.EXPAND)
        self.main_concordance_vbox.AddSpacer(10)

        self.main_concordance_page_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.main_concordance_page_spinctrl = wx.SpinCtrl(self.main_concordance_window, min=0, initial=0)
        self.main_concordance_page_hbox.Add(self.main_concordance_page_spinctrl, proportion=0)
        self.main_concordance_page_hbox.AddSpacer(5)
        self.main_concordance_page_button = wx.Button(self.main_concordance_window, label="Go")
        self.main_concordance_page_hbox.Add(self.main_concordance_page_button, proportion=0)
        self.main_concordance_vbox.Add(self.main_concordance_page_hbox, proportion=0, flag=wx.ALIGN_CENTER)
        self.main_concordance_vbox.AddSpacer(10)

        self.main_concordance_search_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.main_concordance_search_term_txt = wx.StaticText(self.main_concordance_window, label="Search term")
        self.main_concordance_search_hbox.Add(self.main_concordance_search_term_txt, proportion=0)
        self.main_concordance_search_hbox.AddSpacer(5)
        self.main_concordance_search_regex = wx.CheckBox(self.main_concordance_window, label="Regex")
        self.main_concordance_search_hbox.Add(self.main_concordance_search_regex, proportion=0)
        self.main_concordance_search_hbox.AddSpacer(5)
        self.main_concordance_search_exact_checkbox = wx.CheckBox(self.main_concordance_window, label="Exact")
        self.main_concordance_search_hbox.Add(self.main_concordance_search_exact_checkbox, proportion=0)
        self.main_concordance_vbox.Add(self.main_concordance_search_hbox, proportion=0, flag=wx.ALIGN_CENTER)
        self.main_concordance_vbox.AddSpacer(10)

        self.main_concordance_searchbar_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.main_concordance_searchbar_txtctrl = wx.TextCtrl(self.main_concordance_window)
        self.main_concordance_searchbar_hbox.Add(self.main_concordance_searchbar_txtctrl, proportion=0)
        self.main_concordance_searchbar_hbox.AddSpacer(5)
        self.main_concordance_searchbar_button = wx.Button(self.main_concordance_window, label="Search")
        self.main_concordance_searchbar_hbox.Add(self.main_concordance_searchbar_button, proportion=0)
        self.main_concordance_vbox.Add(self.main_concordance_searchbar_hbox, proportion=0, flag=wx.ALIGN_CENTER)
        self.main_concordance_vbox.AddSpacer(10)

        self.main_concordance_window.Bind(wx.EVT_BUTTON, lambda event: self.main_concordance_display_page(
            num=self.main_concordance_page_spinctrl.GetValue(), event=event),
                                       self.main_concordance_page_button)
        self.main_concordance_window.Bind(wx.EVT_BUTTON, self.main_concordance_search, self.main_concordance_searchbar_button)

        self.main_concordance_window.SetSizer(self.main_concordance_vbox)
        self.main_listbook.InsertPage(1, self.main_concordance_window, "Concordance")

        self.main_ngram_window = wx.Panel(self.main_listbook)
        self.main_ngram_vbox = wx.BoxSizer(orient=wx.VERTICAL)

        self.main_ngram_info_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.main_ngram_types_txt = wx.StaticText(self.main_ngram_window, label="Types: 0")
        self.main_ngram_info_hbox.Add(self.main_ngram_types_txt, proportion=0)
        self.main_ngram_info_hbox.AddSpacer(100)
        self.main_ngram_tokens_txt = wx.StaticText(self.main_ngram_window, label="Tokens: 0")
        self.main_ngram_info_hbox.Add(self.main_ngram_tokens_txt, proportion=0)
        self.main_ngram_info_hbox.AddSpacer(100)
        self.main_ngram_search_txt = wx.StaticText(self.main_ngram_window, label="Search hits: 0")
        self.main_ngram_info_hbox.Add(self.main_ngram_search_txt, proportion=0)
        self.main_ngram_vbox.Add(self.main_ngram_info_hbox, proportion=0, flag=wx.ALIGN_CENTER)
        self.main_ngram_vbox.AddSpacer(10)

        self.main_ngram_flexgrid = wx.FlexGridSizer(cols=8, vgap=5, hgap=10)
        self.main_ngram_flexgrid.AddGrowableCol(idx=7, proportion=1)
        self.main_ngram_flexgrid.Add(wx.StaticText(self.main_ngram_window, label="Rank"), 0, 0)
        self.main_ngram_flexgrid.Add(wx.StaticText(self.main_ngram_window, label="Statistic"), 0, 1)
        self.main_ngram_flexgrid.Add(wx.StaticText(self.main_ngram_window, label="Frequency"), 0, 2)
        self.main_ngram_flexgrid.Add(wx.StaticText(self.main_ngram_window, label="Frequency 0"), 0, 3)
        self.main_ngram_flexgrid.Add(wx.StaticText(self.main_ngram_window, label="Frequency 1"), 0, 4)
        self.main_ngram_flexgrid.Add(wx.StaticText(self.main_ngram_window, label="Frequency 2"), 0, 5)
        self.main_ngram_flexgrid.Add(wx.StaticText(self.main_ngram_window, label="Frequency 3"), 0, 6)
        self.main_ngram_flexgrid.Add(wx.StaticText(self.main_ngram_window, label="Ngram"), 0, 7)
        for row in range(1, self.page_len + 1):
            # TODO: make this a loop
            self.main_ngram_boxes.append([wx.StaticText(self.main_ngram_window, label=str(row)),
                wx.StaticText(self.main_ngram_window, label=""), wx.StaticText(self.main_ngram_window, label=""),
                wx.StaticText(self.main_ngram_window, label=""), wx.StaticText(self.main_ngram_window, label=""),
                wx.StaticText(self.main_ngram_window, label=""), wx.StaticText(self.main_ngram_window, label=""),
                wx.StaticText(self.main_ngram_window, label=""), wx.StaticText(self.main_ngram_window, label="")])
            for i in range(8):
                self.main_ngram_flexgrid.Add(self.main_ngram_boxes[row - 1][i], row, i)
        self.main_ngram_vbox.Add(self.main_ngram_flexgrid, proportion=1, flag=wx.EXPAND | wx.ALIGN_CENTER)
        self.main_ngram_vbox.AddSpacer(10)

        self.main_ngram_start_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.main_ngram_size_txt = wx.StaticText(self.main_ngram_window, label="Ngram size")
        self.main_ngram_start_hbox.Add(self.main_ngram_size_txt, proportion=0)
        self.main_ngram_start_hbox.AddSpacer(5)
        self.main_ngram_size_spinctrl = wx.SpinCtrl(self.main_ngram_window, initial=2, min=1, max=4)
        self.main_ngram_start_hbox.Add(self.main_ngram_size_spinctrl)
        self.main_ngram_start_hbox.AddSpacer(5)
        self.main_ngram_start_button = wx.Button(self.main_ngram_window, label="Start")
        self.main_ngram_start_hbox.Add(self.main_ngram_start_button, proportion=0)
        self.main_ngram_start_hbox.AddSpacer(30)
        self.main_ngram_page_spinctrl = wx.SpinCtrl(self.main_ngram_window, min=0, initial=0)
        self.main_ngram_start_hbox.Add(self.main_ngram_page_spinctrl, proportion=0)
        self.main_ngram_start_hbox.AddSpacer(5)
        self.main_ngram_page_button = wx.Button(self.main_ngram_window, label="Go")
        self.main_ngram_start_hbox.Add(self.main_ngram_page_button, proportion=0)
        self.main_ngram_vbox.Add(self.main_ngram_start_hbox, proportion=0, flag=wx.ALIGN_CENTER)
        self.main_ngram_vbox.AddSpacer(10)

        self.main_ngram_search_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.main_ngram_search_term_txt = wx.StaticText(self.main_ngram_window, label="Search term")
        self.main_ngram_search_hbox.Add(self.main_ngram_search_term_txt, proportion=0)
        self.main_ngram_search_hbox.AddSpacer(5)
        self.main_ngram_search_regex = wx.CheckBox(self.main_ngram_window, label="Regex")
        self.main_ngram_search_hbox.Add(self.main_ngram_search_regex, proportion=0)
        self.main_ngram_search_hbox.AddSpacer(5)
        self.main_ngram_search_exact_checkbox = wx.CheckBox(self.main_ngram_window, label="Exact")
        self.main_ngram_search_hbox.Add(self.main_ngram_search_exact_checkbox, proportion=0)
        self.main_ngram_vbox.Add(self.main_ngram_search_hbox, proportion=0, flag=wx.ALIGN_CENTER)
        self.main_ngram_vbox.AddSpacer(10)

        self.main_ngram_searchbar_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.main_ngram_searchbar_txtctrl = wx.TextCtrl(self.main_ngram_window)
        self.main_ngram_searchbar_hbox.Add(self.main_ngram_searchbar_txtctrl, proportion=0)
        self.main_ngram_searchbar_hbox.AddSpacer(5)
        self.main_ngram_searchbar_button = wx.Button(self.main_ngram_window, label="Search")
        self.main_ngram_searchbar_hbox.Add(self.main_ngram_searchbar_button, proportion=0)
        self.main_ngram_vbox.Add(self.main_ngram_searchbar_hbox, proportion=0, flag=wx.ALIGN_CENTER)
        self.main_ngram_vbox.AddSpacer(10)

        self.main_ngram_sort_hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.main_ngram_sort_choice = wx.Choice(self.main_ngram_window, choices=["Statistic", "Ngram frequency", "Token 0 frequency",
            "Token 1 frequency", "Token 2 frequency", "Token 3 frequency", "Ngram"])
        self.main_ngram_sort_reverse_checkbox = wx.CheckBox(self.main_ngram_window, label="Descending")
        self.main_ngram_sort_reverse_checkbox.SetValue(1)
        self.main_ngram_sort_hbox.Add(self.main_ngram_sort_reverse_checkbox, proportion=0)
        self.main_ngram_sort_hbox.AddSpacer(5)
        self.main_ngram_sort_hbox.Add(self.main_ngram_sort_choice, proportion=0)
        self.main_ngram_sort_hbox.AddSpacer(5)
        self.main_ngram_sort_button = wx.Button(self.main_ngram_window, label="Sort")
        self.main_ngram_sort_hbox.Add(self.main_ngram_sort_button, proportion=0)
        self.main_ngram_vbox.Add(self.main_ngram_sort_hbox, proportion=0, flag=wx.ALIGN_CENTER)

        self.main_ngram_window.Bind(wx.EVT_BUTTON, lambda event:
            self.main_ngram_get_ngrams(n=self.main_ngram_size_spinctrl.GetValue(), event=event), self.main_ngram_start_button)
        self.main_ngram_window.Bind(wx.EVT_BUTTON, lambda event: self.main_ngram_display_page(
            num=self.main_ngram_page_spinctrl.GetValue(), event=event),
                                       self.main_ngram_page_button)
        self.main_ngram_window.Bind(wx.EVT_BUTTON, self.main_ngram_search, self.main_ngram_searchbar_button)
        self.main_ngram_window.Bind(wx.EVT_BUTTON, self.main_ngram_display_ngram,
                                       self.main_ngram_sort_button)

        self.main_ngram_window.SetSizer(self.main_ngram_vbox)
        self.main_listbook.InsertPage(2, self.main_ngram_window, "Ngrams")

        self.main_keyword_window = wx.Panel(self.main_listbook)
        self.main_listbook.InsertPage(3, self.main_keyword_window, "Keyword")

        self.main_listbook.Bind(wx.EVT_LISTBOOK_PAGE_CHANGED, self.change_listbook_idx)

        self.main_window.Show()

    def main_wordlist_get_wordlist(self, event=wx.EVT_BUTTON):
        if not self.wordlist_files_dirty:
            return
        if self.tool_wordlist_target_corpus == 3:
            self.freqdist = main.wordlist_to_freqdist()
            self.main_wordlist_display_wordlist()
        else:
            self.freqdist = nltk.FreqDist()
            if not self.tool_wordlist_case:
                case = self.global_case_sensitive
            elif self.tool_wordlist_case == 1:
                case = True
            else:
                case = False
            if self.tool_wordlist_target_corpus == 0 or self.tool_wordlist_target_corpus == 1:
                for filename in self.filenames:
                    self.freqdist.update(main.freq_from_txt(filename, case_sensitive=case))
            if self.tool_wordlist_target_corpus == 0 or self.tool_wordlist_target_corpus == 2:
                for textbody in self.text_bodies:
                    self.freqdist.update(main.freq_from_str(self.text_bodies[textbody], case_sensitive=case))
        self.main_wordlist_types_txt.SetLabel("Types: " + str(len(self.freqdist)))
        self.main_wordlist_tokens_txt.SetLabel("Tokens: " + str(self.freqdist.N()))
        self.main_wordlist_display_wordlist()
        self.wordlist_files_dirty = False

    def main_wordlist_display_wordlist(self, event=wx.EVT_BUTTON):
        sortval = self.main_wordlist_sort_choice.GetSelection()
        if sortval == 0:  # frequency
            sortval = 1  # index 1
        else:
            sortval = 0
        values = [x for x in self.freqdist.items()]
        values.sort(key=operator.itemgetter(sortval), reverse=self.main_wordlist_sort_reverse_checkbox.IsChecked())
        row = 1  # row 0 is header
        self.freqdist_pages = list(main.divide_chunks(values, self.page_len))
        if len(self.freqdist_pages) > 0:
            self.main_wordlist_page_spinctrl.SetMax(len(self.freqdist_pages)-1)
        # print(self.freqdist_pages)
        self.main_wordlist_display_page(0)

    def main_wordlist_display_page(self, num=0, event=None):
        i = 0
        for value in self.freqdist_pages[num]:
            self.main_wordlist_boxes[i][0].SetLabel(str(num*self.page_len+i+1))
            self.main_wordlist_boxes[i][1].SetLabel(str(value[1]))  # frequency
            self.main_wordlist_boxes[i][2].SetLabel(value[0])  # word
            i += 1
        for x in range(i, self.page_len + 1):  # clear out the empty boxes. TODO: why isn't this working? This should be working
            self.main_wordlist_boxes[x][0].SetLabel(str(x+1))
            for idx in range(1, 3):
                self.main_wordlist_boxes[x][idx].SetLabel("")

    def main_wordlist_search(self, event=wx.EVT_BUTTON):
        query = self.main_wordlist_searchbar_txtctrl.GetValue()
        if query == "":
            self.main_wordlist_display_wordlist()
            return  # we're done here
        sortval = self.main_wordlist_sort_choice.GetSelection()
        if sortval == 0:  # frequency
            sortval = 1  # index 1
        else:
            sortval = 0
        values = [x for x in self.freqdist.items() if x[0] == query or (not self.main_wordlist_search_exact_checkbox.IsChecked() and query in x[0])]
        values.sort(key=operator.itemgetter(sortval), reverse=self.main_wordlist_sort_reverse_checkbox.IsChecked())
        self.main_wordlist_search_txt.SetLabel("Search hits: %d" % len(values))
        self.freqdist_pages = list(main.divide_chunks(values, self.page_len))
        if len(self.freqdist_pages) > 0:
            self.main_wordlist_page_spinctrl.SetMax(len(self.freqdist_pages) - 1)
        self.main_wordlist_display_page(0)

    def main_concordance_display_page(self, num=0, event=wx.EVT_BUTTON):
        # print(self.concordance_pages[num])
        i = 0
        for filename, values in self.concordance_pages[num]:
            self.main_concordance_boxes[i][0].SetLabel(str(num * self.page_len + i + 1))
            self.main_concordance_boxes[i][1].SetLabel(" ".join(values))  # words
            self.main_concordance_boxes[i][2].SetLabel(filename)  # filename
            i += 1
        for x in range(i,
                       self.page_len + 1):  # clear out the empty boxes. TODO: why isn't this working? This should be working
            self.main_concordance_boxes[x][0].SetLabel("")
            self.main_concordance_boxes[x][1].SetLabel("")
            self.main_concordance_boxes[x][2].SetLabel("")

    def main_concordance_search(self, event=wx.EVT_BUTTON):
        query = self.main_concordance_searchbar_txtctrl.GetValue()
        if query == "":
            return
        if not self.tool_concordance_case:
            case = self.global_case_sensitive
        elif self.tool_concordance_case == 1:
            case = True
        else:
            case = False
        full_values = []
        if self.tool_concordance_target_corpus == 0 or self.tool_concordance_target_corpus == 1:  # if we are inlcuding files
            for filename in self.filenames:
                with open(filename) as f_in:
                    # TODO: make this take the token definition into account
                    text = f_in.read()
                    if not case:
                        text = text.lower()
                tokens = [token for token in nltk.word_tokenize(text) if token.isalpha() or token.replace("'", "").isalpha()]
                for idx in range(len(tokens)):
                    token = tokens[idx]
                    if token == query or (not self.main_concordance_search_exact_checkbox.IsChecked() and query in token):
                        # use max and min to avoid IndexError (going out of range)
                        # TODO: do I want this in list like this or as a string?
                        full_values.append(
                            (filename, tokens[max(0, idx - self.tool_concordance_win_length):idx] + [token.replace(token, "<%s>" % token)] +
                             tokens[idx+1:min(len(tokens), idx + self.tool_concordance_win_length + 1)])
                        )
        if self.tool_concordance_target_corpus == 0 or self.tool_concordance_target_corpus == 2:  # if we are including texts
            for text_body in self.text_bodies:
                text = self.text_bodies[text_body]
                if not case:
                    text = text.lower()
                tokens = [token for token in nltk.word_tokenize(text) if
                          token.isalpha() or token.replace("'", "").isalpha()]
                for idx in range(len(tokens)):
                    token = tokens[idx]
                    if token == query or (
                        not self.main_concordance_search_exact_checkbox.IsChecked() and query in token):
                        # use max and min to avoid IndexError (going out of range)
                        # TODO: do I want this in list like this or as a string?
                        full_values.append(
                            (text_body, tokens[max(0, idx - self.tool_concordance_win_length):min(len(tokens),
                                                                                                  idx + self.tool_concordance_win_length)])
                        )
        self.concordance_pages = list(main.divide_chunks(full_values, self.page_len))
        if len(self.concordance_pages) > 0:
            self.main_concordance_page_spinctrl.SetMax(len(self.concordance_pages) - 1)
        self.main_concordance_hits_txt.SetLabel("Concordance hits: %d" % len(full_values))
        self.main_concordance_display_page(0)

    def main_ngram_get_ngrams(self, n=2, event=wx.EVT_BUTTON):
        if not self.ngram_files_dirty:
            return
        self.ngram_freqdist = nltk.FreqDist()
        if not self.tool_ngram_case:
            case = self.global_case_sensitive
        elif self.tool_ngram_case == 1:
            case = True
        else:
            case = False
        for filename in self.filenames:
            with open(filename) as f_in:
                text = f_in.read()
            if not case:
                text = text.lower()
            # TODO: customize to deal with nontokens and stopwords
            tokens = [token for token in nltk.word_tokenize(text) if token.isalpha() or token.replace("'", "").isalpha()]
            ngrams = nltk.ngrams(tokens, n)
            freqdist = nltk.FreqDist(ngrams)
            self.ngram_freqdist.update(freqdist)
        self.main_ngram_types_txt.SetLabel("Types: " + str(len(self.ngram_freqdist)))
        self.main_ngram_tokens_txt.SetLabel("Tokens: " + str(self.ngram_freqdist.N()))
        self.main_ngram_display_ngram()
        self.ngram_files_dirty = False

    def main_ngram_display_ngram(self, event=wx.EVT_BUTTON):
        sortval = self.main_ngram_sort_choice.GetSelection()
        values = []
        for ngram, freq in self.ngram_freqdist.items():
            stat = 0
            freqs = []
            for token in ngram:
                freqs.append(self.freqdist[token])
            for i in range(len(ngram), 4):
                freqs.append(0)  # blank spot
            item = [stat, freq]
            item.extend(freqs)
            item.append(ngram)
            values.append(item)
        values.sort(key=operator.itemgetter(sortval), reverse=self.main_ngram_sort_reverse_checkbox.IsChecked())
        self.ngram_freqdist_pages = list(main.divide_chunks(values, self.page_len))
        if len(self.ngram_freqdist_pages) > 0:
            self.main_ngram_page_spinctrl.SetMax(len(self.ngram_freqdist_pages) - 1)
        self.main_ngram_display_page(0)

    def main_ngram_display_page(self, num=0, event=wx.EVT_BUTTON):
        i = 0
        if len(self.ngram_freqdist_pages) >= num + 1:
            for value in self.ngram_freqdist_pages[num]:
                self.main_ngram_boxes[i][0].SetLabel(str(num * self.page_len + i + 1))  # rank
                for idx in range(0, 7):
                    self.main_ngram_boxes[i][idx+1].SetLabel(str(value[idx]))  # stat
                i += 1
        for x in range(i, self.page_len + 1):  # clear out the empty boxes. TODO: why isn't this working? This should be working
            self.main_ngram_boxes[x][0].SetLabel(str(x+1))
            for idx in range(1, 8):
                self.main_ngram_boxes[x][idx].SetLabel("")

    def main_ngram_search(self, event=wx.EVT_BUTTON):
        query = self.main_ngram_searchbar_txtctrl.GetValue()
        if query == "":
            self.main_ngram_display_ngram()
            return  # we're done here
        sortval = self.main_ngram_sort_choice.GetSelection()
        values = []
        for ngram, freq in self.ngram_freqdist.items():
            if query not in ngram:
                if not self.main_ngram_search_exact_checkbox.IsChecked():
                    valid = False  # possibly invalid, need to look at each ngram
                else:
                    continue  # definitely invalid
            else:
                valid = True
            stat = 0
            freqs = []
            for token in ngram:
                if not valid and query in token:
                    valid = True
                freqs.append(self.ngram_freqdist[token])
            if not valid:
                continue
            for i in range(len(ngram), 4):
                freqs.append(0)  # blank spot
            item = [stat, freq]
            item.extend(freqs)
            item.append(ngram)
            values.append(item)
        values.sort(key=operator.itemgetter(sortval), reverse=self.main_ngram_sort_reverse_checkbox.IsChecked())
        self.main_ngram_search_txt.SetLabel("Search hits: %d" % len(values))
        self.ngram_freqdist_pages = list(main.divide_chunks(values, self.page_len))
        if len(self.ngram_freqdist_pages) > 0:
            self.main_ngram_page_spinctrl.SetMax(len(self.ngram_freqdist_pages) - 1)
        self.main_ngram_display_page(0)

    def change_listbook_idx(self, event=wx.EVT_LISTBOOK_PAGE_CHANGED):
        self.listbook_idx = event.GetSelection()

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
    frame = NlpGuiClass(None, -1, 'nlp_gui')
    frame.SetSize(0, 0, 200, 50)
    # Creating the menubar.
    frame.Show()
    app.MainLoop()
