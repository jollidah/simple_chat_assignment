add_executable(chatui WIN32 chatapp.cpp ui/ui.cpp ui/root.cpp)

find_package(wxWidgets REQUIRED COMPONENTS core base xrc xml html)

target_link_libraries(chatui wxWidgets::wxWidgets)

set_property(TARGET chatui PROPERTY
  MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")

set_property(TARGET chatui PROPERTY VS_DPI_AWARE "PerMonitor")

set_property(TARGET chatui PROPERTY CXX_STANDARD 14)