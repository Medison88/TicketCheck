import flet as ft

def main(page: ft.Page):
    page.title = "Flet Android Test"
    page.add(
        ft.Text(
            "Flet Android Startup OK!",
            size=25
        )
    )

ft.app(target=main)
