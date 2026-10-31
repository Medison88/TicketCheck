
import flet as ft
from datetime import datetime


def main(page: ft.Page):
    page.title = "Ticket Purchase & 4D Analysis"
    page.scroll = ft.ScrollMode.AUTO

    date_field = ft.TextField(
        label="Date (DD/MM/YYYY)",
        value=datetime.now().strftime("%d/%m/%Y"),
        width=200,
    )

    draw_field = ft.TextField(
        label="Draw",
        hint_text="例如: 442/26",
        width=200,
    )

    number_field = ft.TextField(
        label="Number (4 digits)",
        hint_text="7338",
        width=150,
    )

    prize_dropdown = ft.Dropdown(
        label="Prize Type",
        options=[
            ft.dropdown.Option("First"),
            ft.dropdown.Option("Second"),
            ft.dropdown.Option("Third"),
            ft.dropdown.Option("Special"),
            ft.dropdown.Option("Consolation"),
        ],
        value="First",
        width=150,
    )

    location_dropdown = ft.Dropdown(
        label="Location / Tag",
        options=[
            ft.dropdown.Option("S2"),
            ft.dropdown.Option("Oakland"),
        ],
        value="S2",
        width=150,
    )

    bcn_fields = [
        ft.TextField(label=f"BCN {i+1}", width=95)
        for i in range(9)
    ]

    serial_field = ft.TextField(
        label="Serial",
        hint_text="流水号...",
        width=300,
    )

    status_text = ft.Text(
        "当前为本地离线模式运行",
        color=ft.colors.GREEN,
    )

    input_tab = ft.Column(
        [
            ft.Text("Ticket Purchase & Calculator", size=20),
            ft.Row([date_field, draw_field]),
            ft.Row([
                number_field,
                prize_dropdown,
                location_dropdown,
            ], wrap=True),
            ft.Text("BCN Numbers (Multi-groups):"),
            ft.Row(bcn_fields[:5], wrap=True),
            ft.Row(bcn_fields[5:], wrap=True),
            serial_field,
            ft.ElevatedButton(
                text="Save Record",
            ),
            status_text,
        ],
        scroll=ft.ScrollMode.AUTO,
    )

    search_input = ft.TextField(
        label="Search keyword",
        hint_text="搜索...",
        expand=True,
    )

    filter_location = ft.Dropdown(
        label="Filter Tag",
        options=[
            ft.dropdown.Option("All"),
            ft.dropdown.Option("S2"),
            ft.dropdown.Option("Oakland"),
        ],
        value="All",
        width=150,
    )

    search_tab = ft.Column(
        [
            ft.Text("Search & History Window", size=20),
            ft.Row([search_input, filter_location]),
            ft.Text("这里暂时不显示记录"),
        ],
    )

    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Input",
                content=ft.Container(input_tab, padding=10),
            ),
            ft.Tab(
                text="Search",
                content=ft.Container(search_tab, padding=10),
            ),
        ],
        expand=True,
    )

    page.add(tabs)


ft.app(target=main)
