# main.py

import flet as ft
from wifi_screen import (
    WifiSplash,
    MonitorModeView,
    ScanNetworksView,
    CaptureHandshakeView,
    CrackMenuView,
    PasswordsView,
    WifiBottomAppBar
)

def main(page: ft.Page) -> None:
    page.title = "WiCrackFi GUI Control Panel"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # تحديد أحجام النافذة كما في التصميم المرجعي
    page.window.width = 400
    page.window.height = 760
    page.window.resizable = False
    page.padding = 0

    def router(route: str) -> None:
        print(f"تنقل الواجهة إلى المسار: {page.route}")
        page.views.clear()

        # بناء الواجهة المطلوبة بناءً على المسار الحالي
        if page.route == "/" or page.route == "/Splash":
            view = WifiSplash()
        elif page.route == "/monitor":
            view = MonitorModeView()
        elif page.route == "/scan":
            view = ScanNetworksView()
        elif page.route == "/capture":
            view = CaptureHandshakeView()
        elif page.route == "/crack":
            view = CrackMenuView()
        elif page.route == "/passwords":
            view = PasswordsView()
        else:
            view = WifiSplash()

        # استبعاد شريط التنقل السفلي من شاشة الترحيب فقط وإرفاقه بباقي النوافذ
        if page.route != "/" and page.route != "/Splash":
            view.bottom_appbar = WifiBottomAppBar(page)

        page.views.append(view)
        page.update()

    def view_pop(view):
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)

    page.on_route_change = router
    page.on_view_pop = view_pop
    
    # التوجيه الافتراضي لبدء العمل بصفحة الفلاش الترحيبية
    page.go("/Splash")

if __name__ == "__main__":
    ft.app(target=main)



