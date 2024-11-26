/**
 * @file chatapp.cpp
 * @author your name (you@domain.com)
 * @brief Chat App enrty
 * @version 0.1
 * @date 2024-11-21
 *
 * @copyright Copyright (c) 2024
 *
 */

#include <wx/wxprec.h>
#ifndef WX_PRECOMP
#include <wx/wx.h>
#endif

#include <wx/xrc/xmlres.h>

enum
{
  ID_StartServer = wxID_LAST + 1,
  ID_JoinServer
};

class SimpleChatApp : public wxApp
{
public:
  virtual bool OnInit() override;

private:
  int showMainPage();
  int showChatUI();
};

int SimpleChatApp::showMainPage()
{
  // XRC
  wxXmlResource *xrc = wxXmlResource::Get();
  xrc->InitAllHandlers();

  bool loaded = xrc->Load("main.xrc");
  wxFrame *frame = xrc->LoadFrame(nullptr, "chatFrame");

  // Map objects and events from XRC
  wxButton *btnStartServer = XRCCTRL(*frame, "m_btnServer", wxButton);
  btnStartServer->Bind(wxEVT_COMMAND_BUTTON_CLICKED, [&frame](wxCommandEvent &)
                       { wxMessageBox("Feature not implemented!"); });

  wxButton *btnJoinServer = XRCCTRL(*frame, "m_btnJoin", wxButton);
  btnJoinServer->Bind(wxEVT_COMMAND_BUTTON_CLICKED, [&frame](wxCommandEvent &)
                      { wxMessageBox("Feature not implemented!"); return 2; });

  frame->CenterOnScreen();
  frame->Show();

  return 1;
}

int SimpleChatApp::showChatUI()
{
  // XRC
  wxXmlResource *xrc = wxXmlResource::Get();
  xrc->InitAllHandlers();

  bool loaded = xrc->Load("chatui.xrc");
  wxFrame *frame = xrc->LoadFrame(nullptr, "chatUI");

  // Map objects and events from XRC

  wxButton *btn = XRCCTRL(*frame, "m_btnSend", wxButton);
  wxTextCtrl *tb = XRCCTRL(*frame, "m_tbText", wxTextCtrl);
  wxTextCtrl *history = XRCCTRL(*frame, "m_chatHistory", wxTextCtrl);

  btn->Bind(wxEVT_COMMAND_BUTTON_CLICKED, [=](wxCommandEvent &)
            { if(tb->GetValue().length() < 1)
            {
              return;
            }
              history->SetValue(history->GetValue() + "\n" + tb->GetValue());
                                tb->Clear(); history->SetInsertionPoint(-1); });

  tb->Bind(wxEVT_COMMAND_TEXT_ENTER, [=](wxCommandEvent &)
           {wxCommandEvent evt(wxEVT_COMMAND_BUTTON_CLICKED, btn->GetId());
    wxPostEvent(btn, evt); });

  wxButton *filebtn = XRCCTRL(*frame, "m_bpBtnSendFile", wxButton);
  filebtn->Bind(wxEVT_COMMAND_BUTTON_CLICKED, [=](wxCommandEvent &)
                { wxFileDialog fileDlg(frame, "Select a file to send", "", "", wxString(wxFileSelectorDefaultWildcardStr), wxFD_OPEN | wxFD_FILE_MUST_EXIST); 
                fileDlg.ShowModal() ; });

  frame->CenterOnScreen();
  frame->Show();
  return 1;
}

wxIMPLEMENT_APP(SimpleChatApp);

bool SimpleChatApp::OnInit()
{
#ifdef _WIN32
  MSWEnableDarkMode();
#endif // _WIN32
  SetAppearance(Appearance::System);
  wxInitAllImageHandlers();

  this->SetAppName("SNS-HW3: Simple Chat");
  this->SetAppDisplayName("Simple Chat");

  showChatUI();

  switch (showMainPage())
  {
    // case 2:
    //   wxMessageBox("showMainPage()->2");
    //   break;
    // case 0:
    // case -1:
    // default:
    //   return true;
  }

#if 0

  wxSizer *rootSizer = new wxBoxSizer(wxVERTICAL);
  wxSizer *btnSizer = new wxBoxSizer(wxVERTICAL);
  wxFrame *myFrame = new wxFrame(nullptr, wxID_ANY, wxT("HW3: Simple Chat"));
  wxPanel *basePanel = new wxPanel(myFrame);
  wxTextCtrl *txtIP = new wxTextCtrl(myFrame, wxID_ANY);

  wxButton *btnStartServer = new wxButton(myFrame, ID_StartServer, wxT("Start a server instance"));
  wxButton *btnJoinServer = new wxButton(myFrame, ID_JoinServer, wxT("Join as a client"));
  // wxBitmap *Logo = new wxBitmap("Y:\\9q6080pqz9l91.png", wxBITMAP_TYPE_ANY);
  rootSizer->Add(basePanel);

  myFrame->SetSizer(rootSizer);

  btnSizer->AddStretchSpacer(1);
  btnSizer->Add(btnStartServer, 0, wxALIGN_CENTER | wxALL, 10);
  btnSizer->Add(btnJoinServer, 0, wxALIGN_CENTER | wxALL, 10);
  btnSizer->Add(txtIP, 0, wxALIGN_CENTER | wxALL, 10);
  btnSizer->AddStretchSpacer(1);

  rootSizer->Layout();
  rootSizer->Add(btnSizer, 1, wxEXPAND, 5);

  {
    wxSize size = myFrame->FromDIP(wxSize(240, 300));
    myFrame->SetMinSize(size);
    myFrame->SetSize(size);
    myFrame->Center();
  };

  myFrame->Show();

  // Map events
  Bind(wxEVT_COMMAND_BUTTON_CLICKED, [=](wxCommandEvent &)
       { wxMessageBox("Feature not implemented!", this->GetAppName(), wxICON_ERROR); }, ID_StartServer);

  Bind(wxEVT_COMMAND_BUTTON_CLICKED, [=](wxCommandEvent &)
       { if(txtIP->GetValue().length() < 1)
       {
         wxMessageBox("Server IP is empty.", this->GetAppDisplayName(), wxICON_ERROR);
         return;
       }
        wxMessageBox("Feature not implemented! : " + txtIP->GetValue(), this->GetAppName()); }, ID_JoinServer);

#endif

  return true;
}
