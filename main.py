from datetime import datetime
import json
import flet as ft
import gspread
import pandas as pd

SPREADSHEET_ID = "1j9R36vCXpSNPuQ8UuQU_k5gZm9xRPcIJ7RbN1hQrLq4"

# 服务账号凭证字典（直接硬编码内嵌，确保手机端离线打包也能直接免文件认证连接）
CREDS_DICT = {
    "type": "service_account",
    "project_id": "gen-lang-client-0777858623",
    "private_key_id": "ed7dfe9fea9f88a1ceb2a42961f54bf5e4de559b",
    "private_key": (
        "-----BEGIN PRIVATE"
        " KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC/+DYY320fYHfS\n+yxvthK1sSG//ZX7tZCRORJIqhrA8QJVd8ynG67d41fhUebvpy3WjtC3ofUmd1N2\n2WNwEVZPMKHMuaSY6aDRKspxYFn1GjfLLhz1CIPoNgAmoq/2rkrJ8Fg0PIr7qSFH\ns43sx9yg3L8IrJyBABVha31mQmnur+7xBBi0Z9BlmIBgHYK2Li3JgqfZAoGFnCw5\nnR5FXHkIaFPzVITFSHTO6a76vkSeIaAhLjavAxNcBX32lywi9zTaz8xR4GkIVoyA\nFspvbXx9QZIkhZVnIsok0gSGHG+Z2cfULVeK9Ltq4FaZ3OpyWw9kmPuFIpxJOGC2\nGMf1Xj87AgMBAAECggEABPdncuJI4PBueStdXXCA8GlqPZzSZgYu/MrUscOQ2KAD\nlvF3/nTFY+EvU1l6l4WkNnJQbQfIH1wj8SWzoGEacgcIkJLW8svMiMzKGv/KpAAv\nJFcHkcFMJFRNUbKQydl9ftb0eTl9wQABp+i5yb/r8c90M8W/cMjvRKtyvZQHSJEC\nGSZMBOpRk/osAb1SZgFISWVl5+HktD3dsmWESLCouX/rtXNVj4o5fj3Pci9dJfll\nsdVQCQLEVhk+8nMQ9ParXEOZi/t9Nj3YSPoeFZaZJWaEVkhpmmcOPPtU5Gf5Qr0I\IRajZBNWYvwb6BIaGKEdGewJNa5Bip5nwUSacTvalQKBgQD5Z1PBjyH/NjAPP2oT\nKUWmnB3yM2GbMaTs9+ctx12ZNz1RpnbDRrHKCKf2lk6c+56DmRsPbvxcBa6JooQG\nIYbDbaBYfZ6XKkzG0cNOUn7tAIKStTtWkL20v7enxk9piyNq3pBkGmdwx4hivmqb\nbJzcHNlFrwzNOxnufusfbqAnbwKBgQDFDAHZMIu5vMU59HzB3W7c/KwBed9R9kRp\RGVvhGvTL4N02BISSsGxkvNUSb1wUntPYTG/jE4UvlugzXeRznY1Cpik40ZlRa7M\nRpy0ZoLLlKcubBTjcTWASeokBHHz6CqRfC2tDAj01AmuhtEHRKxZUua4hXZ7pzqM\niWmk7V6e9QKBgDykKhJTOiHyzAa5FZKpI11aclGUurPgg0h3EofoBNMfQlKbFh9v\DgWgyy5C58R1zdoTnSfIhaXeX8zpbg6LklfsTOOXT7tTtq1VDZb6qg/4YsdHN7FZ\nqjbLst0hc+emxCrVCOi+Hs6mRXw07njyFMXUYeP2pzczmp+JzqOq41gTAoGAAtzB\nhyh3iabhMRSNADLDiw2MIPJ1AmTgyljTgJFaQGmk+R5w75vgfCC1SS48mqVMJZ4XJ\n6zZmi/aX7iYN7phJL0wQG5URmLcCawU7kYNLsxldtFbtlsA2Pr7UH+HQpfJha+uZ\n3kGmf6f03AwpTSm6NzH1GAkYR4OOXixA1Jx+G2ECgYA5G3tZVNWvMOEWIOulnQHz\nfeVe7hVjbtwkv3IirnX/xvzyyjRM984SWqZJdgd6x8Qz8Zg3AKtRzi7Yg+Nr2a8x\nC4kDcXwHbXuR3JwZF/LfE4AFNTxXvomyNQI3y7/0w/8Z0QUwrVaxGz+1loOD2woa\nOSEUBEJzYqBKhDWyfV3xkA==\n-----END"
        " PRIVATE KEY-----\n"
    ),
    "client_email": (
        "ticket-app-bot@gen-lang-client-0777858623.iam.gserviceaccount.com"
    ),
    "client_id": "105289009865180222878",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": (
        "https://www.googleapis.com/oauth2/v1/certs"
    ),
    "client_x509_cert_url": (
        "https://www.googleapis.com/robot/v1/metadata/x509/ticket-app-bot%40gen-lang-client-0777858623.iam.gserviceaccount.com"
    ),
    "universe_domain": "googleapis.com",
}


def init_gspread():
  try:
    gc = gspread.service_account_from_dict(CREDS_DICT)
    return gc.open_by_key(SPREADSHEET_ID).sheet1
  except Exception as e:
    print(f"Google Sheets 连接失败: {e}")
    return None


sheet = init_gspread()


def get_bcn_string(r):
  bcn_val = r.get("bcn_list", [""] * 9)
  if isinstance(bcn_val, list):
    return "".join([str(b).strip() for b in bcn_val if str(b).strip()])
  return str(bcn_val).strip()


def load_data():
  if sheet is None:
    return []
  try:
    rows = sheet.get_all_values()
    records = []
    if not rows:
      return []
    for row in rows:
      if not row or not row[0]:
        continue
      try:
        rid = int(row[0])
        bcn_raw = row[5] if len(row) > 5 else ""
        bcn_list = []
        if bcn_raw.startswith("["):
          try:
            bcn_list = json.loads(bcn_raw)
          except:
            bcn_list = []
        else:
          bcn_raw_clean = "".join(bcn_raw.split())
          bcn_list = [
              bcn_raw_clean[i : i + 5]
              for i in range(0, len(bcn_raw_clean), 5)
              if bcn_raw_clean[i : i + 5]
          ]
        while len(bcn_list) < 9:
          bcn_list.append("")
        bcn_list = bcn_list[:9]

        record = {
            "id": rid,
            "date": row[1] if len(row) > 1 else "",
            "draw": row[2] if len(row) > 2 else "",
            "number": row[3] if len(row) > 3 else "",
            "prize_type": row[4] if len(row) > 4 else "",
            "bcn_list": bcn_list,
            "serial": row[6] if len(row) > 6 else "",
            "combine": row[7] if len(row) > 7 else "",
            "score": int(row[8]) if len(row) > 8 and str(row[8]).isdigit() else 0,
            "percentage": row[9] if len(row) > 9 else "0.00%",
            "source_location": row[10] if len(row) > 10 else "S2",
        }
        records.append(record)
      except ValueError:
        continue
    return records
  except Exception as e:
    print(f"读取失败: {e}")
    return []


def save_data_all(records):
  if sheet is None:
    return False
  try:
    sheet.clear()
    headers = [
        "id",
        "date",
        "draw",
        "number",
        "prize_type",
        "bcn_list",
        "serial",
        "combine",
        "score",
        "percentage",
        "source_location",
    ]
    sheet.append_row(headers)
    data_to_write = []
    for r in records:
      row = [
          r.get("id"),
          r.get("date"),
          r.get("draw"),
          r.get("number"),
          r.get("prize_type", ""),
          get_bcn_string(r),
          r.get("serial", ""),
          r.get("combine", ""),
          r.get("score", 0),
          r.get("percentage", "0.00%"),
          r.get("source_location", "S2"),
      ]
      data_to_write.append(row)
    if data_to_write:
      sheet.append_rows(data_to_write)
    return True
  except Exception as e:
    print(f"保存失败: {e}")
    return False


def main(page: ft.Page):
  page.title = "Ticket Purchase & 4D Analysis"
  page.vertical_alignment = ft.MainAxisAlignment.START
  page.scroll = ft.ScrollMode.AUTO

  records = load_data()

  # 控件定义
  date_field = ft.TextField(
      label="Date (DD/MM/YYYY)",
      value=datetime.now().strftime("%d/%m/%Y"),
      width=200,
  )
  draw_field = ft.TextField(
      label="Draw", hint_text="例如: 442/26", width=200
  )
  number_field = ft.TextField(
      label="Number (4 digits)", hint_text="7338", width=150
  )

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

  status_text = ft.Text("", color=ft.colors.GREEN)

  # 搜索与历史记录表格容器
  search_input = ft.TextField(
      label="Search keyword", hint_text="搜索...", expand=True
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

      # 50%以上高亮红色
      is_high = pct_val >= 50.0
      row_color = ft.colors.RED_50 if is_high else None
      text_color = ft.colors.RED_700 if is_high else ft.colors.BLACK
      weight = (
          ft.FontWeight.BOLD if is_high else ft.FontWeight.NORMAL
      )

      rows.append(
          ft.DataRow(
              color=row_color,
              cells=[
                  ft.DataCell(
                      ft.Text(str(r["id"]), color=text_color, weight=weight)
                  ),
                  ft.DataCell(
                      ft.Text(r["date"], color=text_color, weight=weight)
                  ),
                  ft.DataCell(
                      ft.Text(
                          r.get("source_location", "S2"),
                          color=text_color,
                          weight=weight,
                      )
                  ),
                  ft.DataCell(
                      ft.Text(r["draw"], color=text_color, weight=weight)
                  ),
                  ft.DataCell(
                      ft.Text(r["number"], color=text_color, weight=weight)
                  ),
                  ft.DataCell(
                      ft.Text(
                          r.get("prize_type", "-"),
                          color=text_color,
                          weight=weight,
                      )
                  ),
                  ft.DataCell(
                      ft.Text(str(r["score"]), color=text_color, weight=weight)
                  ),
                  ft.DataCell(
                      ft.Text(
                          r.get("percentage", "0%"),
                          color=text_color,
                          weight=weight,
                      )
                  ),
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
    table_container.controls.append(
        ft.Row([dt], scroll=ft.ScrollMode.ADAPTIVE)
    )
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
    combine_result = (
        f"{bcn_combined_clean}{serial_val}{draw_cleaned}"
    )

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

    if sheet:
      row = [
          new_record["id"],
          new_record["date"],
          new_record["draw"],
          new_record["number"],
          new_record["prize_type"],
          get_bcn_string(new_record),
          new_record["serial"],
          new_record["combine"],
          new_record["score"],
          new_record["percentage"],
          new_record["source_location"],
      ]
      sheet.append_row(row)

    records.append(new_record)
    status_text.value = (
        f"保存成功！得分: {total_score} | Percentage: {percentage:.2f}%"
    )
    refresh_table()
    page.update()

  def apply_search(e):
    q = search_input.value.strip().lower()
    loc = filter_location.value

    res = records
    if q:
      res = [
          r
          for r in res
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

  # 选项卡布局
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