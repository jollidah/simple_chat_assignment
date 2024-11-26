#include <wx/frame.h>

class ChatFrame : public wxFrame
{
public:
  ChatFrame();

private:
  void OnHello(wxCommandEvent &evt);
  void OnExit(wxCommandEvent &evt);
  void OnAbout(wxCommandEvent &evt);
};
