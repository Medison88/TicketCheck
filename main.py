
import flet as ft

def main(page: ft.Page):
    page.title = "Ticket Check Test"
    page.scroll = ft.ScrollMode.AUTO

    input_tab = ft.Column(
        controls=[
            ft.Text("Ticket Purchase", size=22),
            ft.TextField(label="Date", width=300),
            ft.TextField(label="Draw", width=300),
            ft.TextField(label="Number", width=300),
            ft.Dropdown(
                label="Prize",
                width=300,
                options=[
                    ft.dropdown.Option("First"),
                    ft.dropdown.Option("Second"),
                    ft.dropdown.Option("Third"),
                ],
                value="First",
            ),
            ft.ElevatedButton(
                text="Save Record",
                on_click=lambda e: page.add(
                    ft.Text("Save button works!")
                ),
            ),
        ],
        spacing=15,
        scroll=ft.ScrollMode.AUTO,
    )

    search_tab = ft.Column(
        controls=[
            ft.Text("Search & History", size=22),
            ft.TextField(label="Search keyword", width=300),
            ft.Dropdown(
                label="Filter Tag",
                width=300,
                options=[
                    ft.dropdown.Option("All"),
                    ft.dropdown.Option("S2"),
                    ft.dropdown.Option("Oakland"),
                ],
                value="All",
            ),
            ft.Text("Search page is working"),
        ],
        spacing=15,
    )

    page.add(
        tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        expand=True,
        tabs=[
            ft.Tab(
                text="Input",
                content=ft.Container(
                    content=input_tab,
                    padding=10,
                    expand=True,
                ),
            ),
            ft.Tab(
                text="Search",
                content=ft.Container(
                    content=search_tab,
                    padding=10,
                    expand=True,
                ),
            ),
        ],
    )

    page.add(
        ft.Container(
            content=tabs,
            expand=True,
        )
    )

ft.app(target=main)
