
import flet as ft
from bidi.algorithm import get_display
import time
import asyncio
from home_screen import Splash,SplashFirst,PatientInfo,WelcomeScreen
from home_screen import Home,Home2,Settings,DoctorsView,ResultsView,MedicalAnalysisApp
import flet as ft
async def show_splash_sequence(page: ft.Page):
    page.views.append(SplashFirst())  # اعرض Splash مباشرة (الأزرار)
    page.update()
    await asyncio.sleep(3.0)  # انتظار اختياري
    page.views.clear()
    page.views.append(PatientInfo())  # ثم اعرض PatientInfo
    page.update()

def main(page: ft.Page) -> None:
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 380
    page.window.height = 750
    page.window.top = 0.5
    page.window.left = 898
    page.padding = 0
    async def router(route: str) -> None:
        print(f"Route changing to: {route}")
        page.views.clear()
        if page.route == "/":
            await show_splash_sequence(page) # يتم استدعاء show_splash_sequence عند "/"
        elif page.route == "/home":
            page.views.append(Home())
        elif page.route == "/Splash":
            
            page.views.append(Splash())
        elif page.route == "/doctors":
            page.views.append(DoctorsView())
        elif page.route == "/PatientInfo":
            page.views.append(PatientInfo())
        elif page.route == "/settings":
            page.views.append(Settings())
        elif page.route == "/home2":
            page.views.append(Home2())

            
        elif page.route == "/MedicalAnalysisApp":
            medical_app = MedicalAnalysisApp()
            page.views.clear()
            page.views.append(medical_app)
        elif page.route == "/results":

            if hasattr(page, 'results_data'):
                page.views.append(ResultsView(page.results_data))
            else:
                print("No results data found")
                page.go("/home")
        elif page.route == "/WelcomeScreen":
            if hasattr(page, 'results_data'):
                results_view = WelcomeScreen(page.results_data)
                page.views.append(results_view)
                page.update()
                await asyncio.sleep(9.0)  # انتظار 3 ثوانٍ
                page.views.clear()
                page.views.append(Splash())
                page.update()  # الانتقال إلى Splash (المسار "/")
            else:
                print("No results data found")
                
        page.update()
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    page.on_route_change = router
    page.on_view_pop = view_pop
    page.go("/")  # ابدأ بالمسار "/"
ft.app(target=main, assets_dir="assets")















# import flet as ft
# import asyncio  # Still needed for asyncio.sleep
# from home_screen import (
#     Splash,
#     SplashFirst,
#     PatientInfo,
#     WelcomeScreen,
#     Home,
#     Home2,
#     Settings,
#     DoctorsView,
#     ResultsView,
#     MedicalAnalysisApp,
# )
# async def show_splash_sequence(page: ft.Page):
#     page.views.append(SplashFirst())  
#     page.update()
#     await asyncio.sleep(3.0)  
#     page.views.clear()
#     page.views.append(PatientInfo()) 
#     page.update()


# async def long_initialization(page: ft.Page):
#   """Simulates a long initialization process."""
#   print("Starting long initialization...")
#   await asyncio.sleep(5)  # Simulate a long-running task
#   print("Long initialization complete.")


# def main(page: ft.Page) -> None:
#     page.theme_mode = ft.ThemeMode.LIGHT
#     page.window_width = 380
#     page.window_height = 750
#     page.window_top = 0.5
#     page.window_left = 898
#     page.padding = 0

#     async def router(route: str) -> None:
#         print(f"Route changing to: {route}")
#         page.views.clear()

#         if route == "/":
#             await show_splash_sequence(page)
#         elif route == "/home":
#             page.views.append(Home())
#         elif route == "/Splash":
#             page.views.append(Splash())
#         elif route == "/doctors":
#             page.views.append(DoctorsView())
#         elif route == "/PatientInfo":
#             page.views.append(PatientInfo())
#         elif route == "/settings":
#             page.views.append(Settings())
#         elif route == "/home2":
#             page.views.append(Home2())
#         elif route == "/MedicalAnalysisApp":
#             medical_app = MedicalAnalysisApp()
#             # No need to clear views here; MedicalAnalysisApp is appended.
#             page.views.append(medical_app)
#         elif route == "/results":
#             if hasattr(page, "results_data"):
#                 page.views.append(ResultsView(page.results_data))
#             else:
#                 print("No results data found")
#                 page.go("/home")  # Redirect to home if no data
#         elif route == "/WelcomeScreen":
#             if hasattr(page, "results_data"):
#                 results_view = WelcomeScreen(page.results_data)
#                 page.views.append(results_view)
#                 page.update()  # Ensure WelcomeScreen is displayed
#                 await asyncio.sleep(9.0)
#                 page.views.clear() # Clear views *after* the sleep
#                 page.go("/Splash") # Corrected: go to /Splash
#             else:
#                 print("No results data found")
#                 page.go("/home")

#         page.update()

#     def view_pop(e: ft.ViewPopEvent):  # Corrected type hint
#         page.views.pop()
#         if page.views:  # Check if views list is not empty
#             top_view = page.views[-1]
#             page.go(top_view.route)
#         else:  # Handle case where views list is empty (e.g., after popping the last view)
#             page.go("/")  # Go to the default route
#     page.on_route_change = router
#     page.on_view_pop = view_pop
#     # page.go("/") # Don't navigate here, do in task callback
#     page.run_task(long_initialization(page)) # Start the background task
#     page.go("/") # Call go *after* run_task, not before

# if __name__ == "__main__":
#     ft.app(target=main, assets_dir="assets")








