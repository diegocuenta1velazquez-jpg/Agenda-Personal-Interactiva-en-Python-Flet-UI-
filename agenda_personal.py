import flet as ft

def main(page: ft.Page):
    page.title = "Agenda Personal"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 450
    page.window_height = 700
    page.window_resizable = False
    page.padding = 16
    page.bgcolor = "#F7FAFC"

    COLOR_PRIMARY = "#1565C0"
    COLOR_SECONDARY = "#2E7D32"
    COLOR_SUCCESS = "#2E7D32"
    COLOR_ERROR = "#C62828"
    COLOR_WHITE = "#FFFFFF"
    CARD_BG = "#FFFFFF"

    notes = []

    def show_message(text: str, color: str = COLOR_PRIMARY):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(text, color=COLOR_WHITE),
            bgcolor=color,
            open=True
        )
        page.update()

    # ---------- NAVIGATION ----------
    def go_to(screen):
        page.controls.clear()
        page.add(screen)
        page.update()

    # ---------- SCREENS ----------
    def home_screen():
        return ft.Column(
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("📘 Agenda Personal", size=30, weight=ft.FontWeight.BOLD, color=COLOR_PRIMARY),
                ft.Text("Gestiona tus notas fácilmente.", size=14, color="#444444"),

                ft.ElevatedButton(
                    text="📝 Agregar nota",
                    bgcolor=COLOR_PRIMARY,
                    color=COLOR_WHITE,
                    on_click=lambda e: go_to(add_note_screen())
                ),
                ft.ElevatedButton(
                    text="📚 Ver notas",
                    bgcolor=COLOR_SECONDARY,
                    color=COLOR_WHITE,
                    on_click=lambda e: go_to(list_notes_screen())
                )
            ]
        )

    title_input = ft.TextField(label="Título", width=380)
    content_input = ft.TextField(label="Contenido", multiline=True, min_lines=4, width=380)

    def add_note_screen():
        def on_save(e):
            title = title_input.value.strip()
            content = content_input.value.strip()
            if not title or not content:
                show_message("Completa todos los campos", COLOR_ERROR)
                return

            notes.append({"title": title, "content": content})
            title_input.value = ""
            content_input.value = ""

            show_message("Nota agregada correctamente", COLOR_SUCCESS)
            page.update()

        return ft.Column(
            spacing=15,
            controls=[
                ft.Row(
                    controls=[
                        ft.TextButton("⬅ Volver", on_click=lambda e: go_to(home_screen())),
                        ft.Text("Agregar nota", size=22, weight=ft.FontWeight.BOLD)
                    ]
                ),
                title_input,
                content_input,
                ft.ElevatedButton("💾 Guardar", bgcolor=COLOR_PRIMARY, color=COLOR_WHITE, on_click=on_save),
            ]
        )

    def list_notes_screen():
        items = []

        if not notes:
            items.append(ft.Text("No hay notas aún.", color="#666666"))
        else:
            for i, n in enumerate(notes):
                idx = i

                def delete_note(e, index=idx):
                    notes.pop(index)
                    show_message("Nota eliminada", COLOR_PRIMARY)
                    go_to(list_notes_screen())

                card = ft.Container(
                    bgcolor=CARD_BG,
                    padding=10,
                    border_radius=10,
                    content=ft.Column(
                        spacing=5,
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text("📄 " + n["title"], size=18, weight=ft.FontWeight.BOLD),
                                    ft.TextButton("🗑 Borrar", on_click=lambda e, index=idx: delete_note(e, index))
                                ]
                            ),
                            ft.Text(n["content"], size=14, color="#333333")
                        ]
                    )
                )
                items.append(card)

        return ft.Column(
            spacing=15,
            controls=[
                ft.Row(
                    controls=[
                        ft.TextButton("⬅ Volver", on_click=lambda e: go_to(home_screen())),
                        ft.Text("Notas Guardadas", size=22, weight=ft.FontWeight.BOLD)
                    ]
                ),
                ft.Column(items, spacing=12)
            ]
        )

    go_to(home_screen())


if __name__ == "__main__":
    ft.app(target=main)
