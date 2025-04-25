import os
import flet as ft
from view.tarefa_view import render_tarefas_view, cadastrar_tarefa_page

UPLOAD_DIR = "uploads"
IDIOMA_SELECIONADO = "Português"

# Traduções
traducoes = {
    "Português": {
        "welcome": "Bem-vindo ao Gerenciador de Tarefas!",
        "hint": "Clique no botão '+' para adicionar uma nova tarefa.",
        "tasks": "Tarefas",
        "settings": "Configurações",
        "add_task": "Adicionar Tarefa",
        "change_background": "Alterar Fundo",
        "exit": "Sair",
        "register_task": "Cadastrar Tarefa",
        "back_to_home": "Voltar ao Início",
        "list_tasks": "Listar Tarefas",
        "attach_file": "Anexar Arquivo"
    },
    "Inglês": {
        "welcome": "Welcome to Task Manager!",
        "hint": "Click the '+' button to add a new task.",
        "tasks": "Tasks",
        "settings": "Settings",
        "add_task": "Add Task",
        "change_background": "Change Background",
        "exit": "Exit",
        "register_task": "Register Task",
        "back_to_home": "Back to Home",
        "list_tasks": "List Tasks",
        "attach_file": "Attach File"
    },
    "Espanhol": {
        "welcome": "¡Bienvenido al Gestor de Tareas!",
        "hint": "Haz clic en el botón '+' para añadir una nueva tarea.",
        "tasks": "Tareas",
        "settings": "Configuraciones",
        "add_task": "Añadir Tarea",
        "change_background": "Cambiar Fondo",
        "exit": "Salir",
        "register_task": "Registrar Tarea",
        "back_to_home": "Volver al Inicio",
        "list_tasks": "Listar Tareas",
        "attach_file": "Adjuntar Archivo"
    }
}

# Componentes globais
tarefas_container = ft.Column()  # Container global para listar tarefas
welcome_text = ft.Text("", size=24, weight=ft.FontWeight.BOLD, color="white")
hint_text = ft.Text("", size=16, color="white")

def render_home(page: ft.Page):
    global IDIOMA_SELECIONADO
    is_dark_mode = False
    background_image_path = ""

    page.clean()
    page.title = "Gerenciador de Tarefas"
    page.scroll = ft.ScrollMode.AUTO
    hint_text = ft.Text("", size=16, color="white", font_family="Arial")
    os.makedirs(UPLOAD_DIR, exist_ok=True)


    def on_background_selected(e: ft.FilePickerResultEvent):
        nonlocal background_image_path
        if e.files:
            file = e.files[0]
            filename = os.path.basename(file.path)
            novo_caminho = os.path.join(UPLOAD_DIR, filename)
            with open(file.path, "rb") as src, open(novo_caminho, "wb") as dst:
                dst.write(src.read())
            background_image_path = novo_caminho
            render_home(page)
            
            page.add()
            page.update()  # Recarrega a tela com a imagem

    bg_picker = ft.FilePicker(on_result=on_background_selected)

    def atualizar_idioma(idioma, page):
        global IDIOMA_SELECIONADO
        IDIOMA_SELECIONADO = idioma
        if idioma in traducoes:
            welcome_text.value = traducoes[idioma]["welcome"]
            hint_text.value = traducoes[idioma]["hint"]
            page.appbar.title = ft.Text(traducoes[idioma]["tasks"])
            page.update()

    
            

    idioma_dropdown = ft.Dropdown(
        value=IDIOMA_SELECIONADO,
        options=[ft.dropdown.Option(lang) for lang in traducoes],
        on_change=lambda e: atualizar_idioma(e.control.value, page)
    )

    def abrir_cadastro_view(e):
        page.clean()
        cadastrar_tarefa_page(page, tarefas_container)

    def abrir_listagem_view(e):
        page.clean()
        page.add(tarefas_container)
        render_tarefas_view(page, tarefas_container)

    def abrir_configuracoes_view(e):
        page.clean()

        def voltar_fonte_normal(e):
            welcome_text.font_family = None
            hint_text.font_family = None
            page.snack_bar = ft.SnackBar(ft.Text("Fonte padrão restaurada!"), open=True)
            page.update()

        config_layout = ft.Column([
            ft.Text(traducoes[IDIOMA_SELECIONADO]["settings"], size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Text("Idioma"),
            idioma_dropdown,
            ft.ElevatedButton(traducoes[IDIOMA_SELECIONADO]["change_background"], on_click=lambda _: bg_picker.pick_files(allow_multiple=False, allowed_extensions=["jpg", "jpeg", "png"])),
            ft.ElevatedButton("Voltar à Fonte Normal", on_click=voltar_fonte_normal),
            ft.ElevatedButton(traducoes[IDIOMA_SELECIONADO]["back_to_home"], on_click=lambda e: render_home(page))
        ], spacing=10)

        page.appbar = ft.AppBar(title=ft.Text(traducoes[IDIOMA_SELECIONADO]["settings"]))
        page.overlay.append(bg_picker)
        page.floating_action_button = None
        page.add(config_layout)
        page.update()

    def mudar_tema(e):
        nonlocal is_dark_mode
        is_dark_mode = not is_dark_mode
        page.theme_mode = ft.ThemeMode.DARK if is_dark_mode else ft.ThemeMode.LIGHT
        page.update()

    floating_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        tooltip=traducoes[IDIOMA_SELECIONADO]["add_task"],
        on_click=abrir_cadastro_view,
        bgcolor=ft.Colors.PRIMARY_CONTAINER
    )

    page.appbar = ft.AppBar(
        title=ft.Text(traducoes[IDIOMA_SELECIONADO]["tasks"], size=20, weight=ft.FontWeight.BOLD),
        center_title=True,
        bgcolor=ft.Colors.SURFACE,
        elevation=4,
        actions=[
            ft.IconButton(
                icon=ft.Icons.WB_SUNNY_OUTLINED if not is_dark_mode else ft.Icons.NIGHTLIGHT_ROUND,
                tooltip="Mudar Tema",
                on_click=mudar_tema
            ),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text=traducoes[IDIOMA_SELECIONADO]["settings"], on_click=abrir_configuracoes_view),
                    ft.PopupMenuItem(text=traducoes[IDIOMA_SELECIONADO]["list_tasks"], on_click=abrir_listagem_view),
                    ft.PopupMenuItem(text=traducoes[IDIOMA_SELECIONADO]["change_background"], on_click=lambda _: bg_picker.pick_files(allow_multiple=False, allowed_extensions=["jpg", "jpeg", "png"])),
                    ft.PopupMenuItem(text=traducoes[IDIOMA_SELECIONADO]["exit"], on_click=lambda _: page.close())
                ]
            ),
        ]
    )

    atualizar_idioma(IDIOMA_SELECIONADO, page)
    page.overlay.append(bg_picker)
    page.floating_action_button = floating_button

    background = ft.Stack([
        ft.Image(
            src=background_image_path,
            fit=ft.ImageFit.COVER,
            width=page.width,
            height=page.height
        ) if background_image_path else ft.Container(),
        ft.Container(
            expand=True,
            content=ft.Column([
                welcome_text,
                hint_text,
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        )
    ])

    page.add(background)
    page.update()