
import flet as ft

def main(page: ft.Page):
    page.title = "Flet Control Test"
    page.scroll = ft.ScrollMode.AUTO

    page.add(
        ft.Column(
            controls=[
                ft.Text("CONTROL TEST", size=25),

                ft.TextField(
                    label="Test TextField",
                    value="Hello",
                    width=300,
                ),

                ft.Dropdown(
                    label="Test Dropdown",
                    width=300,
                    options=[
                        ft.dropdown.Option("S2"),
                        ft.dropdown.Option("Oakland"),
                    ],
                    value="S2",
                ),

                ft.ElevatedButton(
                    text="Test Button",
                    on_click=lambda e: page.add(
                        ft.Text("Button works!")
                    ),
                ),

                ft.Text("End of test"),
            ],
            spacing=20,
        )
    )

ft.app(target=main)
