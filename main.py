from datetime import datetime
import flet as ft

# 暂时注释掉 gspread 相关内容，排除所有底层 C 库兼容性引起的段错误
# import gspread 


def get_bcn_string(r):
    bcn_val = r.get("bcn_list", [""] * 9)
    if isinstance(bcn_val, list):
        return "".join([str(b).strip() for b in bcn_val if str(b).strip()])
    return str(bcn_val).strip()


def load_data():
    # 暂时返回空或从本地存储加载，确保不触发网络底层崩溃
    return []


def main(page: ft.Page):
    page.title = "Ticket Purchase & 4D Analysis"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.scroll = ft.ScrollMode.AUTO

    records = load_data()

    date_field = ft.TextField(
        label="Date (DD/MM/YYYY)",
        value=datetime.now().strftime("%d/%m/%Y"),
        width=200,
    )
    draw_field = ft.TextField(label="Draw", hint_text="例如: 442/26", width=200)
    number_field = ft.TextField(label="Number (4 digits)", hint_text="7338", width=150)

    prize_dropdown = ft.Dropdown(
        label="Prize Type",
        options=[
            ft.dropdown.Option("First"),
            ft.dropdown.Option("Second"),
            ft.dropdown.Option("Third"),
            ft.dropdown.Option("Special"),
            ft.dropdown.Option("Consolation"),
            ft.dropdown.Option(" "),
        ],
        value="First",
        width=150,
    )

    location_dropdown = ft.Dropdown(
        label="Location / Tag",
        options=[ft.dropdown.Option("S2"), ft.dropdown.Option("Oakland")],
        value="S2",
        width=150,
    )

    bcn_fields = [ft.TextField(label=f"BCN {i+1}", width=95) for i in range(9)]
    serial_field = ft.TextField(label="Serial", hint_text="流水号...", width=300)

    status_text = ft.Text("当前为本地离线模式运行", color=ft.colors.GREEN)

    search_input = ft.TextField(label="Search keyword", hint_text="搜索...", expand=True)
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
    table_container = ft.Column()

    def refresh_table(filtered=None):
        table_container.controls.clear()
        data_to_show = filtered if filtered is not None else records

        rows = []
        for r in data_to_show:
            pct_str = str(r.get("percentage", "0%")).replace("%", "")
            try:
                pct_val = float(pct_str)
            except:
                pct_val = 0.0

            is_high = pct_val >= 50.0
            row_color = ft.colors.RED_50 if is_high else None
            text_color = ft.colors.RED_700 if is_high else ft.colors.BLACK
            weight = ft.FontWeight.BOLD if is_high else ft.FontWeight.NORMAL

            rows.append(
                ft.DataRow(
                    color=row_color,
                    cells=[
                        ft.DataCell(ft.Text(str(r["id"]), color=text_color, weight=weight)),
                        ft.DataCell(ft.Text(r["date"], color=text_color, weight=weight)),
                        ft.DataCell(ft.Text(r.get("source_location", "S2"), color=text_color, weight=weight)),
                        ft.DataCell(ft.Text(r["draw"], color=text_color, weight=weight)),
                        ft.DataCell(ft.Text(r["number"], color=text_color, weight=weight)),
                        ft.DataCell(ft.Text(r.get("prize_type", "-"), color=text_color, weight=weight)),
                        ft.DataCell(ft.Text(str(r["score"]), color=text_color, weight=weight)),
                        ft.DataCell(ft.Text(r.get("percentage", "0%"), color=text_color, weight=weight)),
                    ],
                )
            )

        dt = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Date")),
                ft.DataColumn(ft.Text("Tag")),
                ft.DataColumn(ft.Text("Draw")),
                ft.DataColumn(ft.Text("Number")),
                ft.DataColumn(ft.Text("Prize")),
                ft.DataColumn(ft.Text("Score")),
                ft.DataColumn(ft.Text("Percentage")),
            ],
            rows=rows,
        )
        table_container.controls.append(ft.Row([dt], scroll=ft.ScrollMode.ADAPTIVE))
        page.update()

    def save_clicked(e):
        nonlocal records
        date_str = date_field.value.strip()
        draw_val = draw_field.value.strip()
        number_val = number_field.value.strip()
        prize_type = prize_dropdown.value
        source_location = location_dropdown.value
        serial_val = serial_field.value.strip()

        draw_cleaned = draw_val.split("/")[0] if "/" in draw_val else draw_val
        bcn_combined = "".join([bf.value or "" for bf in bcn_fields])
        bcn_combined_clean = "".join(bcn_combined.split())
        combine_result = f"{bcn_combined_clean}{serial_val}{draw_cleaned}"

        total_len = len(combine_result)
        total_score = 0
        if number_val:
            for digit in number_val:
                if digit.isdigit():
                    total_score += combine_result.count(digit)

        percentage = (total_score / total_len * 100) if total_len > 0 else 0.0

        new_record = {
            "id": len(records) + 1,
            "date": date_str,
            "draw": draw_val,
            "number": number_val,
            "prize_type": prize_type,
            "bcn_list": [bf.value or "" for bf in bcn_fields],
            "serial": serial_val,
            "combine": combine_result,
            "score": total_score,
            "percentage": f"{percentage:.2f}%",
            "source_location": source_location,
        }

        records.append(new_record)
        status_text.value = f"保存成功！得分: {total_score} | Percentage: {percentage:.2f}%"
        status_text.color = ft.colors.GREEN
        refresh_table()
        page.update()

    def apply_search(e):
        q = search_input.value.strip().lower()
        loc = filter_location.value

        res = records
        if q:
            res = [
                r for r in res
                if q in str(r.get("combine", "")).lower()
                or q in str(r.get("number", "")).lower()
                or any(q in str(b).lower() for b in r.get("bcn_list", []))
                or q in str(r.get("serial", "")).lower()
                or q in str(r.get("prize_type", "")).lower()
            ]
        if loc != "All":
            res = [r for r in res if r.get("source_location", "S2") == loc]

        refresh_table(res)

    search_input.on_change = apply_search
    filter_location.on_change = apply_search

    save_btn = ft.ElevatedButton(
        text="📥 Save Record", on_click=save_clicked, color=ft.colors.WHITE, bgcolor=ft.colors.BLUE
    )

    input_tab = ft.Column(
        [
            ft.Text("Ticket Purchase & Calculator", size=20, weight=ft.FontWeight.BOLD),
            ft.Row([date_field, draw_field]),
            ft.Row([number_field, prize_dropdown, location_dropdown]),
            ft.Text("BCN Numbers (Multi-groups):"),
            ft.Row(bcn_fields[:5], wrap=True),
            ft.Row(bcn_fields[5:], wrap=True),
            serial_field,
            save_btn,
            status_text,
        ],
        scroll=ft.ScrollMode.AUTO,
    )

    search_tab = ft.Column(
        [
            ft.Text("Search & History Window", size=20, weight=ft.FontWeight.BOLD),
            ft.Row([search_input, filter_location]),
            table_container,
        ],
        scroll=ft.ScrollMode.AUTO,
    )

    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(text="📝 Input", content=ft.Container(input_tab, padding=10)),
            ft.Tab(text="🔍 Search", content=ft.Container(search_tab, padding=10)),
        ],
        expand=True,
    )

    page.add(tabs)
    refresh_table()

ft.app(target=main)
