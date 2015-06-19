#!/usr/bin/python
# Text Editor
# Author: Pranav Srinivas Kumar
# Date: 2015.02.24

import wx, sys, os
import wx.lib.flatnotebook as fnb

class Tab(wx.Panel):
    # Initialize Tab
    def __init__(self, parent):
        # Initialize wxPanel
        wx.Panel.__init__(self, parent=parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

        # Create text control in tab
        self.text_control = wx.TextCtrl(self, 1, style=wx.TE_MULTILINE|wx.TE_RICH2)
        # Set focus to text editor canvas
        wx.CallAfter(self.text_control.SetFocus)
        # Set font size & family
        self.font = wx.Font(15, 
                            wx.FONTFAMILY_DEFAULT,
                            wx.FONTWEIGHT_NORMAL, 
                            wx.FONTSTYLE_NORMAL)
        self.text_control.SetFont(self.font)
        self.sizer.Add(self.text_control, -1, wx.EXPAND)
        
        # Set text color to white
        self.text_control.SetForegroundColour(wx.WHITE)
        # Set background color to black
        self.text_control.SetBackgroundColour(wx.BLACK)
        
        # Filename of Tab
        self.filename = ""
        # Directory of Tab
        self.directory = ""

        # Is the tab file saved?
        self.saved = False
        # Contents from the last save point
        self.last_save = ""

class Frame(wx.Frame):
    # Initialize Frame
    def __init__(self, parent=None):
        # Initialize wxFrame
        wx.Frame.__init__(self, 
                          None, 
                          wx.ID_ANY, 
                          "Text Editor", 
                          size=(800, 600))

        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.sizer)
        # Create the notebook
        self.notebook = fnb.FlatNotebook(self.panel)
        self.notebook.SetFont(wx.Font(15, 
                                      wx.FONTFAMILY_DEFAULT,
                                      wx.FONTWEIGHT_NORMAL, 
                                      wx.FONTSTYLE_NORMAL))
        # Call the high-level setup function
        self.SetupEditor()

    # High-level setup function
    def SetupEditor(self):
        # Setup the default tab
        self.SetupDefaultTab()

        # Setup the menu bar
        self.SetupMenuBar()

        # Setup Toolbar
        self.SetupToolBar()

        # Setup Keyboard shortcuts
        self.SetupKeyboardShortcuts()   

        # Create the status bar
        self.CreateStatusBar()     

        # Open editor maximized
        self.Maximize()
        self.Layout()

    # Function to setup default tab
    def SetupDefaultTab(self):
        # Create the default tab
        self.default_tab = Tab(self.notebook)
        self.notebook.AddPage(self.default_tab, "Untitled")
        self.sizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL)        

    # Function to setup menubar
    def SetupMenuBar(self):
        # Create the menubar
        self.menubar = wx.MenuBar()
        self.menu_FILE = wx.Menu()
        
        self.menu_NEW = self.menu_FILE.Append(wx.ID_ANY, '&New\tCtrl+N', "Create a New Tab")
        self.menu_OPEN = self.menu_FILE.Append(wx.ID_OPEN, '&Open\tCtrl+O', "Open a File")
        self.menu_FILE.AppendSeparator()
        self.menu_SAVE = self.menu_FILE.Append(wx.ID_SAVE, '&Save\tCtrl+S', "Save a File")
        self.menu_SAVE_AS = self.menu_FILE.Append(wx.ID_SAVEAS, 'Save As...', "Save File As")
        self.menu_FILE.AppendSeparator()
        self.menu_EXIT = self.menu_FILE.Append(wx.ID_EXIT, '&Quit\tCtrl+Q', "Close the Editor")
        
        self.menubar.Append(self.menu_FILE, "&File")
        self.SetMenuBar(self.menubar)

        self.Bind(wx.EVT_MENU, self.OnNewTab, self.menu_NEW)
        self.Bind(wx.EVT_MENU, self.OnOpen, self.menu_OPEN)
        self.Bind(wx.EVT_MENU, self.OnSave, self.menu_SAVE)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, self.menu_SAVE_AS)
        self.Bind(wx.EVT_MENU, self.OnExit, self.menu_EXIT)

    # Function to setup keyboard shortcuts
    def SetupKeyboardShortcuts(self):
        # Setup Keyboard shortcuts
        self.keyboard_CLOSE_TAB = wx.NewId()
        self.Bind(wx.EVT_MENU, 
                  self.OnCloseTab, 
                  id = self.keyboard_CLOSE_TAB)

        self.accelerator_table = wx.AcceleratorTable([(wx.ACCEL_CTRL, 
                                                       ord('N'), 
                                                       self.menu_NEW.GetId()),
                                                      (wx.ACCEL_CTRL, 
                                                       ord('O'), 
                                                       self.menu_OPEN.GetId()),
                                                      (wx.ACCEL_CTRL, 
                                                       ord('S'), 
                                                       self.menu_SAVE.GetId()),
                                                      (wx.ACCEL_CTRL, 
                                                       ord('W'), 
                                                       self.keyboard_CLOSE_TAB),
                                                      (wx.ACCEL_CTRL,
                                                       ord('T'),
                                                       self.terminal.GetId())])
        self.SetAcceleratorTable(self.accelerator_table)

    # Function to setup toolbar
    def SetupToolBar(self):
        self.toolbar = self.CreateToolBar()
        self.file_NEW = self.toolbar.AddLabelTool(wx.ID_ANY, 
                                             'New', 
                                             wx.Bitmap('./icons/file_NEW.png'))
        self.file_OPEN = self.toolbar.AddLabelTool(wx.ID_ANY, 
                                              'Open', 
                                              wx.Bitmap('./icons/file_OPEN.png'))
        self.file_SAVE = self.toolbar.AddLabelTool(wx.ID_ANY, 
                                              'Save', 
                                              wx.Bitmap('./icons/file_SAVE.png'))
        self.file_SAVE_AS = self.toolbar.AddLabelTool(wx.ID_ANY, 
                                                 'Save As...', 
                                                 wx.Bitmap('./icons/file_SAVE_AS.png'))
        self.terminal = self.toolbar.AddLabelTool(wx.ID_ANY,
                                                  'Terminal',
                                                  wx.Bitmap('./icons/terminal.png'))
        self.editor_QUIT = self.toolbar.AddLabelTool(wx.ID_ANY, 
                                                'Quit', 
                                                wx.Bitmap('./icons/editor_QUIT.png'))
        self.toolbar.Realize()

        # Bind Toolbar Buttons to event handlers
        self.Bind(wx.EVT_TOOL, self.OnNewTab, self.file_NEW)
        self.Bind(wx.EVT_TOOL, self.OnOpen, self.file_OPEN)
        self.Bind(wx.EVT_TOOL, self.OnSave, self.file_SAVE)
        self.Bind(wx.EVT_TOOL, self.OnSaveAs, self.file_SAVE_AS)
        self.Bind(wx.EVT_TOOL, self.OnTerminal, self.terminal)
        self.Bind(wx.EVT_TOOL, self.OnExit, self.editor_QUIT)

    # Suppress all standard output
    def SuppressOutput(self):
        devnull = open(os.devnull, 'w')
        sys.stdout = devnull

    # Function to handle new tab
    def OnNewTab(self, e):
        new_tab = Tab(self.notebook)
        new_tab.SetFocus()
        self.notebook.AddPage(new_tab, "Untitled", select = True)

    def OnOpen(self, e):
        
        # Create a File Dialog asking for the file to open
        dialog = wx.FileDialog(self, 
                               "Choose a File", 
                               self.notebook.GetCurrentPage().directory, 
                               "", 
                               "*", 
                               wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            # Get the filename & directory
            filename = dialog.GetFilename()
            directory = dialog.GetDirectory()

            # Open the right file
            filehandle = open(os.path.join(directory, filename), 'r')
            # Check if a new tabe needs to be created to display contents of opened file
            if (self.notebook.GetPageCount() == 1 
                and self.notebook.GetCurrentPage().text_control.GetValue() == ""):
                self.notebook.GetCurrentPage().text_control.SetValue(filehandle.read())
                self.notebook.GetCurrentPage().filename = filename
                self.notebook.GetCurrentPage().directory = directory
                
                self.notebook.GetCurrentPage().last_save = self.notebook.GetCurrentPage().text_control.GetValue()
                
                self.notebook.GetCurrentPage().saved = True
            else:
                new_tab = Tab(self.notebook)
                new_tab.filename = filename
                new_tab.directory = directory
                self.notebook.AddPage(new_tab, "Untitled", select = True)
                wx.CallAfter(new_tab.SetFocus)
                # Populate the tab with file contents
                new_tab.text_control.SetValue(filehandle.read())
                new_tab.last_save = new_tab.text_control.GetValue()
                new_tab.saved = True
            # Set the tab name to be filename
            self.notebook.SetPageText(self.notebook.GetSelection(), filename)
            filehandle.close()
        dialog.Destroy()

    def OnSave(self, e):
        # Check if save is required
        if (self.notebook.GetCurrentPage().text_control.GetValue() 
            != self.notebook.GetCurrentPage().last_save):
            self.notebook.GetCurrentPage().saved = False

        # Check if Save should bring up FileDialog
        if (self.notebook.GetCurrentPage().saved == False 
            and self.notebook.GetCurrentPage().last_save == ""): 
            dialog = wx.FileDialog(self, 
                                   "Choose a file", 
                                   self.notebook.GetCurrentPage().directory, 
                                   "", 
                                   "*", 
                                   wx.SAVE | wx.OVERWRITE_PROMPT)
            if dialog.ShowModal() == wx.ID_OK:
                # Grab the content to be saved
                save_as_file_contents = self.notebook.GetCurrentPage().text_control.GetValue()

                # Open, Write & Close File
                save_as_name = dialog.GetFilename()
                save_as_directory = dialog.GetDirectory()    
                filehandle=open(os.path.join(save_as_directory, save_as_name), 'w')
                filehandle.write(save_as_file_contents)
                filehandle.close()
                self.notebook.SetPageText(self.notebook.GetSelection(), save_as_name)
                self.notebook.GetCurrentPage().filename = save_as_name
                self.notebook.GetCurrentPage().directory = save_as_directory
                self.notebook.GetCurrentPage().last_save = save_as_file_contents
                self.notebook.GetCurrentPage().saved = True
        else:
            # Grab the content to be saved
            save_as_file_contents = self.notebook.GetCurrentPage().text_control.GetValue()
            filehandle=open(os.path.join(self.notebook.GetCurrentPage().directory, 
                                         self.notebook.GetCurrentPage().filename), 'w')
            filehandle.write(save_as_file_contents)
            filehandle.close()
            self.notebook.GetCurrentPage().last_save = save_as_file_contents
            self.notebook.GetCurrentPage().saved = True

    def OnSaveAs(self, e):
        dialog = wx.FileDialog(self, 
                               "Choose a file", 
                               self.notebook.GetCurrentPage().directory, 
                               "", 
                               "*.*", 
                               wx.SAVE | wx.OVERWRITE_PROMPT)
        if dialog.ShowModal() == wx.ID_OK:
            # Grab the content to be saved
            save_as_file_contents = self.notebook.GetCurrentPage().text_control.GetValue()

            # Open, Write & Close File
            save_as_name = dialog.GetFilename()
            save_as_directory = dialog.GetDirectory()
            filehandle=open(os.path.join(save_as_directory, save_as_name), 'w')
            filehandle.write(save_as_file_contents)
            filehandle.close()
            self.notebook.SetPageText(self.notebook.GetSelection(), save_as_name)
            self.notebook.GetCurrentPage().filename = save_as_name
            self.notebook.GetCurrentPage().directory = save_as_directory
            self.notebook.GetCurrentPage().last_save = save_as_file_contents
            self.notebook.GetCurrentPage().saved = True
        dialog.Destroy()

    def OnCloseTab(self, e): 
        # Check if there is only 1 tab open
        if self.notebook.GetPageCount() == 1:
            self.notebook.SetPageText(self.notebook.GetSelection(), "Untitled")
            self.notebook.GetCurrentPage().filename = ""
            self.notebook.GetCurrentPage().directory = ""
            self.notebook.GetCurrentPage().last_save = ""
            self.notebook.GetCurrentPage().saved = False
            if self.notebook.GetCurrentPage().text_control != None:
                self.notebook.GetCurrentPage().text_control.SetValue("")
            # wx.CallAfter(self.notebook.GetCurrentPage().SetFocus)
        else:
            self.notebook.DeletePage(self.notebook.GetSelection())

    # Start a Maximized Terminal
    def OnTerminal(self, e):
        terminal_directory = self.notebook.GetCurrentPage().directory
        os.system("gnome-terminal --maximize --working-directory=" + terminal_directory)

    # Quit Application
    def OnExit(self, e):
        self.Close(True)

if __name__ == "__main__":
    # Create a wx App
    app = wx.App(False)
    # Create the editor frame
    frame = Frame()
    # Show the frame
    frame.Show()
    # Start the mainloop
    app.MainLoop()
