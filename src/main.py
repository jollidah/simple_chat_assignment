import wx
import wx.xrc
import threading
import subprocess
import socket
import struct

from ui.chat_ui import chatUI
from server.server import create_server
from server.client import connect_to_server, join_server


import gettext
_ = gettext.gettext

class chatFrame ( wx.Frame ):

    def __init__( self, parent ):
        # Initialize the wx.Frame with a title and size
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 300,500 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        # Set minimum size hints for the window
        self.SetSizeHints( wx.Size( 300,500 ), wx.DefaultSize )

        # Create a vertical box sizer for the main layout
        bSizer5 = wx.BoxSizer( wx.VERTICAL )

        # Create a panel to hold other widgets
        self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer4 = wx.BoxSizer( wx.VERTICAL )

        # Add a static text label
        bSizer13 = wx.BoxSizer( wx.HORIZONTAL )
        self.m_staticText1 = wx.StaticText( self.m_panel2, wx.ID_ANY, _(u"Simple Chat\nSNS HW4"), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.m_staticText1.Wrap( -1 )
        self.m_staticText1.SetFont( wx.Font( 14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        bSizer13.Add( self.m_staticText1, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        bSizer4.Add( bSizer13, 1, wx.ALIGN_CENTER, 5 )

        # Add a horizontal box sizer for the new buttons
        bSizerButtons = wx.BoxSizer(wx.HORIZONTAL)

        # Add buttons for IP conversion functions
        self.m_btnInetPton = wx.Button(self.m_panel2, wx.ID_ANY, _(u"inet_pton()"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_btnInetNtop = wx.Button(self.m_panel2, wx.ID_ANY, _(u"inet_ntop()"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_btnHtonl = wx.Button(self.m_panel2, wx.ID_ANY, _(u"htonl()"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_btnNtohl = wx.Button(self.m_panel2, wx.ID_ANY, _(u"ntohl()"), wx.DefaultPosition, wx.DefaultSize, 0)

        # Add buttons to the sizer
        bSizerButtons.Add(self.m_btnInetPton, 0, wx.ALL, 5)
        bSizerButtons.Add(self.m_btnInetNtop, 0, wx.ALL, 5)
        bSizerButtons.Add(self.m_btnHtonl, 0, wx.ALL, 5)
        bSizerButtons.Add(self.m_btnNtohl, 0, wx.ALL, 5)

        # Add the button sizer to the main sizer
        bSizer4.Add(bSizerButtons, 0, wx.ALIGN_CENTER, 5)

        # Bind button events to handlers
        self.m_btnInetPton.Bind(wx.EVT_BUTTON, self.onInetPton)
        self.m_btnInetNtop.Bind(wx.EVT_BUTTON, self.onInetNtop)
        self.m_btnHtonl.Bind(wx.EVT_BUTTON, self.onHtonl)
        self.m_btnNtohl.Bind(wx.EVT_BUTTON, self.onNtohl)

        # Create a vertical box sizer for address input and buttons
        bSizer14 = wx.BoxSizer( wx.VERTICAL )
        bSizer14.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        # Add a button to show IP address
        self.m_btnShowIP = wx.Button( self.m_panel2, wx.ID_ANY, _(u"Show IP Address"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer4.Add( self.m_btnShowIP, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        # Bind the button click event to the handler
        self.m_btnShowIP.Bind(wx.EVT_BUTTON, self.showIPAddress)

        # Create a vertical box sizer for address input and buttons
        bSizer14 = wx.BoxSizer( wx.VERTICAL )

        # Text control for entering address
        self.m_txtAddr = wx.TextCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer14.Add( self.m_txtAddr, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        # Button to join as a client
        self.m_btnJoin = wx.Button( self.m_panel2, wx.ID_ANY, _(u"Join as a client"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer14.Add( self.m_btnJoin, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        # Bind the button click event to the handler
        self.m_btnJoin.Bind(wx.EVT_BUTTON, self.joinServer)

        # Button to start a server instance
        self.m_btnServer = wx.Button( self.m_panel2, wx.ID_ANY, _(u"Start a server instance"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer14.Add( self.m_btnServer, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        bSizer14.Add( ( 0, 0), 1, wx.EXPAND, 5 )
        bSizer4.Add( bSizer14, 1, wx.EXPAND, 5 )

        # Bind the button click event to the handler
        self.m_btnServer.Bind(wx.EVT_BUTTON, self.createServer)

        # Set the sizer for the panel and fit the layout
        self.m_panel2.SetSizer( bSizer4 )
        self.m_panel2.Layout()
        bSizer4.Fit( self.m_panel2 )
        bSizer5.Add( self.m_panel2, 1, wx.EXPAND |wx.ALL, 5 )

        # Set the sizer for the frame and layout
        self.SetSizer( bSizer5 )
        self.Layout()

        # Center the window on the screen
        self.Centre( wx.BOTH )

    def joinServer(self, event):
        port = int(self.m_txtAddr.GetValue())
        client_socket = connect_to_server("127.0.0.1", port)
        chat_ui_frame = chatUI(None, port, client_socket)
        threading.Thread(target=join_server, args=(chat_ui_frame.m_chatHistory, client_socket, chat_ui_frame.m_listUsers), daemon=True).start()
        chat_ui_frame.Show()

    def createServer(self, event):
        _, port = create_server()
        self.m_txtAddr.SetValue(str(port))
        self.joinServer(event)
    
    def showIPAddress(self, event):
        try:
            # Execute the command to get the public IP address
            ip_address = subprocess.check_output(['curl', 'ifconfig.me']).decode('utf-8').strip()
            wx.MessageBox(f"Your IP Address is: {ip_address}", "IP Address", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"Error retrieving IP address: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def onInetPton(self, event):
        try:
            ip = '127.0.0.1'
            packed_ip = socket.inet_pton(socket.AF_INET, ip)
            wx.MessageBox(f"{ip} -> {packed_ip}", "inet_pton()", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"Error: {e}", "inet_pton()", wx.OK | wx.ICON_ERROR)

    def onInetNtop(self, event):
        try:
            ip = b'\x7f\x00\x00\x01'
            packed_ip = socket.inet_ntop(socket.AF_INET, ip)
            wx.MessageBox(f"{ip} -> {packed_ip}", "inet_ntop()", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"Error: {e}", "inet_ntop()", wx.OK | wx.ICON_ERROR)

    def onHtonl(self, event):
        try:
            host_long = 12345
            network_long = socket.htonl(host_long)
            wx.MessageBox(f"{host_long} -> {network_long}", "htonl()", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"Error: {e}", "htonl()", wx.OK | wx.ICON_ERROR)

    def onNtohl(self, event):
        try:
            network_long = 12345
            host_long = socket.ntohl(network_long)
            wx.MessageBox(f"{network_long} -> {host_long}", "ntohl()", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"Error: {e}", "ntohl()", wx.OK | wx.ICON_ERROR)

    def showIPAddress(self, event):
        try:
            # Execute the command to get the public IP address
            ip_address = subprocess.check_output(['curl', 'ifconfig.me']).decode('utf-8').strip()
            wx.MessageBox(f"Your IP Address is: {ip_address}", "IP Address", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"Error retrieving IP address: {e}", "Error", wx.OK | wx.ICON_ERROR)


    def __del__( self ):
        pass

if __name__ == "__main__":
    app = wx.App()
    frame = chatFrame(None)
    frame.Show()
    app.MainLoop()
