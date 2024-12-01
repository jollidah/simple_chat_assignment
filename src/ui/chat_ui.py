import wx
import wx.xrc

import gettext
from server.client import send_message, send_left_message

_ = gettext.gettext

class chatUI ( wx.Frame ):

    def __init__( self, parent, port: int, client_socket ):
        # Initialize the wx.Frame with a title and size
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Chat UI as Client: 127.0.0.1:"+str(port)), pos = wx.DefaultPosition, size = wx.Size( 900,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        # Set minimum size hints for the window
        self.SetSizeHints( wx.Size( 500, 300 ))

        # Create a vertical box sizer for the main layout
        bSizer7 = wx.BoxSizer( wx.VERTICAL )

        # Create a panel to hold other widgets
        self.m_panel3 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer8 = wx.BoxSizer( wx.VERTICAL )

        # Add a static text label
        bSizer111 = wx.BoxSizer( wx.VERTICAL )
        self.m_staticText2 = wx.StaticText( self.m_panel3, wx.ID_ANY, _(u"Simple Chat"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )
        bSizer111.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
        bSizer8.Add( bSizer111, 0, wx.EXPAND, 5 )

        # Create a horizontal box sizer for chat history and user list
        bSizer9 = wx.BoxSizer( wx.HORIZONTAL )

        # Text control for displaying chat history
        self.m_chatHistory = wx.TextCtrl( self.m_panel3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH2 )
        bSizer9.Add( self.m_chatHistory, 4, wx.ALL|wx.EXPAND, 5 )

        # List box for displaying users
        self.m_listUsers = wx.ListBox( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, [], 0 )
        bSizer9.Add( self.m_listUsers, 1, wx.ALL|wx.EXPAND, 5 )

        bSizer8.Add( bSizer9, 1, wx.EXPAND, 5 )

        # Add a horizontal line separator
        self.m_staticline1 = wx.StaticLine( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer8.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )

        # Create a vertical box sizer for text input and send button
        bSizer10 = wx.BoxSizer( wx.VERTICAL )
        bSizer11 = wx.BoxSizer( wx.HORIZONTAL )

        # Text control for entering messages
        self.m_tbText = wx.TextCtrl( self.m_panel3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        bSizer11.Add( self.m_tbText, 4, wx.ALL|wx.EXPAND, 5 )

        # Bind the Enter key event to the on_send_button_click method
        self.m_tbText.Bind(wx.EVT_TEXT_ENTER, self.on_send_button_click)

        # Button to send messages
        self.m_btnSend = wx.Button( self.m_panel3, wx.ID_ANY, _(u"Send"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer11.Add( self.m_btnSend, 1, wx.ALL|wx.EXPAND, 5 )

        # Bind the button click event to the on_send_button_click method
        self.m_btnSend.Bind(wx.EVT_BUTTON, self.on_send_button_click)

        bSizer10.Add( bSizer11, 1, wx.EXPAND|wx.TOP, 5 )
        bSizer10.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        # Create a vertical box sizer for file send button
        bSizer12 = wx.BoxSizer( wx.VERTICAL )

        # Bitmap button for sending files
        self.m_bpBtnSendFile = wx.BitmapButton( self.m_panel3, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
        self.m_bpBtnSendFile.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_FILE_OPEN,  ) )
        self.m_bpBtnSendFile.SetToolTip( _(u"Send a file...") )
        self.m_bpBtnSendFile.SetHelpText( _(u"Sen") )
        bSizer12.Add( self.m_bpBtnSendFile, 0, wx.BOTTOM, 5 )

        bSizer10.Add( bSizer12, 1, wx.EXPAND|wx.ALL, 5 )
        bSizer8.Add( bSizer10, 0, wx.EXPAND, 5 )

        # Set the sizer for the panel and fit the layout
        self.m_panel3.SetSizer( bSizer8 )
        self.m_panel3.Layout()
        bSizer8.Fit( self.m_panel3 )
        bSizer7.Add( self.m_panel3, 1, wx.EXPAND |wx.ALL, 5 )

        # Set the sizer for the frame and layout
        self.SetSizer( bSizer7 )
        self.Layout()

        # Create a status bar at the bottom of the window
        self.m_statusBar1 = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )

        # Center the window on the screen
        self.Centre( wx.BOTH )
        self.client_socket = client_socket

        # self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_send_button_click(self, event):
        message = self.m_tbText.GetValue()
        send_message(self.client_socket, message)
        self.m_tbText.SetValue("")
    
    def on_close(self, event):
        send_left_message(self.client_socket)
        self.client_socket.close()
        self.Destroy()
    
    def __del__( self ):
        pass


