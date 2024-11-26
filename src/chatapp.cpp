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

  return true;
}
