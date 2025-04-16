import os
import flet as ft
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from model.tarefa_model import Tarefa, create_tables

# Configuração do banco de dados
DATABASE_URL = "sqlite:///tarefas.db"  # Substitua pelo URL do seu banco de dados
engine = create_engine(DATABASE_URL, echo=True)
create_tables(engine)  # Cria as tabelas no banco de dados, se ainda não existirem

UPLOAD_DIR = "uploads"
IDIOMA_SELECIONADO = "Português"  # Variável global para salvar o idioma selecionado

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
        "attach_file": "Anexar Arquivo",
        "completed": "Concluída"
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
        "attach_file": "Attach File",
        "completed": "Completed"
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
        "attach_file": "Adjuntar Archivo",
        "completed": "Completada"
    }
}

# Componentes globais
welcome_text = ft.Text("", size=24, weight=ft.FontWeight.BOLD, color="white")
hint_text = ft.Text("", size=16, color="white")

def render_home(page: ft.Page):
    global IDIOMA_SELECIONADO
    estilo_gangster = False  # Variável para controlar o estilo gangster
    is_dark_mode = False  # Variável para controlar o tema

    # Limpa a interface antes de renderizar a página inicial
    page.clean()

    page.title = "Gerenciador de Tarefas"
    page.scroll = ft.ScrollMode.AUTO
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    background_image = ft.Image(
        src="", 
        fit=ft.ImageFit.COVER, 
        visible=True, 
        expand=True,  # Faz a imagem ocupar toda a tela
        opacity=0.8  # Define a opacidade da imagem de fundo
    )
    bg_picker = ft.FilePicker()

    def on_background_selected(e: ft.FilePickerResultEvent):
        if e.files:
            path = e.files[0].path
            background_image.src = path
            background_image.visible = True
            page.update()

    bg_picker.on_result = on_background_selected

    def atualizar_idioma(idioma, page):
        global IDIOMA_SELECIONADO
        IDIOMA_SELECIONADO = idioma  # Salva o idioma selecionado
        if idioma in traducoes:
            welcome_text.value = traducoes[idioma]["welcome"]
            hint_text.value = traducoes[idioma]["hint"]
            page.appbar.title = ft.Text(traducoes[idioma]["tasks"])
            page.update()

    idioma_dropdown = ft.Dropdown(
        value=IDIOMA_SELECIONADO,
        options=[ft.dropdown.Option("Português"), ft.dropdown.Option("Inglês"), ft.dropdown.Option("Espanhol")],
        on_change=lambda e: atualizar_idioma(e.control.value, page)
    )

    def aplicar_estilo_gangster(e):
        nonlocal estilo_gangster
        estilo_gangster = not estilo_gangster

        # Define a fonte com base no estado de estilo_gangster
        nova_fonte = "Old English Text MT" if estilo_gangster else None
        welcome_text.font_family = nova_fonte
        hint_text.font_family = nova_fonte

        # Mensagem de feedback para o usuário
        mensagem = "Estilo gangster aplicado!" if estilo_gangster else "Estilo padrão restaurado"
        page.snack_bar = ft.SnackBar(ft.Text(mensagem), open=True)

        # Atualiza a interface
        page.update()

    def abrir_tarefas_view(e):
        page.clean()  # Limpa a interface antes de renderizar a nova página
        descricao_input = ft.TextField(label=traducoes[IDIOMA_SELECIONADO]["register_task"], autofocus=True, width=300)
        file_picker = ft.FilePicker()
        file_picker_result = ft.Text(value="Nenhum arquivo anexado", size=12)

        def on_file_selected(e: ft.FilePickerResultEvent):
            if e.files:
                file_picker_result.value = f"Arquivo anexado: {e.files[0].name}"
                page.update()

        file_picker.on_result = on_file_selected

        cadastrar_btn = ft.ElevatedButton(
            traducoes[IDIOMA_SELECIONADO]["register_task"],
            on_click=lambda _: cadastrar_tarefa(descricao_input.value, file_picker_result.value)
        )
        voltar_btn = ft.ElevatedButton(traducoes[IDIOMA_SELECIONADO]["back_to_home"], on_click=lambda e: render_home(page))
        anexar_btn = ft.ElevatedButton(
            traducoes[IDIOMA_SELECIONADO]["attach_file"],
            on_click=lambda _: file_picker.pick_files(allow_multiple=False)
        )

        def cadastrar_tarefa(descricao, arquivo):
            if descricao.strip():
                try:
                    with Session(engine) as session:
                        nova_tarefa = Tarefa(descricao=descricao, arquivo=arquivo)
                        session.add(nova_tarefa)
                        session.commit()
                        page.snack_bar = ft.SnackBar(ft.Text("Sua tarefa foi cadastrada com sucesso!"), open=True)
                        page.update()
                except Exception as ex:
                    print(f"Erro ao cadastrar tarefa: {ex}")
                    page.snack_bar = ft.SnackBar(ft.Text("Erro ao cadastrar tarefa!"), open=True)
                    page.update()
            else:
                page.snack_bar = ft.SnackBar(ft.Text("A descrição da tarefa não pode estar vazia!"), open=True)
                page.update()

        page.appbar = ft.AppBar(title=ft.Text(traducoes[IDIOMA_SELECIONADO]["register_task"]))
        page.floating_action_button = None
        page.overlay.append(file_picker)
        page.add(voltar_btn, descricao_input, anexar_btn, file_picker_result, cadastrar_btn)
        page.update()

    def listar_tarefas_view(e):
        page.clean()  # Limpa a interface antes de renderizar a nova página
        voltar_btn = ft.ElevatedButton(traducoes[IDIOMA_SELECIONADO]["back_to_home"], on_click=lambda e: render_home(page))
        tarefas_container = ft.Column()

        # Busca as tarefas do banco de dados
        try:
            with Session(engine) as session:
                tarefas = session.query(Tarefa).all()  # Busca todas as tarefas
                for tarefa in tarefas:
                    tarefa_texto = f"{tarefa.id}: {tarefa.descricao}"
                    if tarefa.arquivo:
                        tarefa_texto += f" | Anexo: {tarefa.arquivo}"
                    if tarefa.concluida:
                        tarefa_texto += f" - {traducoes[IDIOMA_SELECIONADO]['completed']}"
                    tarefas_container.controls.append(ft.Text(tarefa_texto))
        except Exception as ex:
            print(f"Erro ao buscar tarefas: {ex}")
            tarefas_container.controls.append(ft.Text("Erro ao carregar tarefas."))

        page.appbar = ft.AppBar(title=ft.Text(traducoes[IDIOMA_SELECIONADO]["list_tasks"]))
        page.add(voltar_btn, tarefas_container)
        page.update()

    def abrir_configuracoes_view(e):
        page.clean()  # Limpa a interface antes de renderizar a nova página
        voltar_btn = ft.ElevatedButton(traducoes[IDIOMA_SELECIONADO]["back_to_home"], on_click=lambda e: render_home(page))

        def voltar_fonte_normal(e):
            nonlocal estilo_gangster
            estilo_gangster = False
            welcome_text.font_family = None
            hint_text.font_family = None
            page.snack_bar = ft.SnackBar(ft.Text("Fonte padrão restaurada!"), open=True)
            page.update()

        config_layout = ft.Column([
            ft.Text(traducoes[IDIOMA_SELECIONADO]["settings"], size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Text("Idioma"),
            idioma_dropdown,
            ft.ElevatedButton(traducoes[IDIOMA_SELECIONADO]["change_background"], on_click=lambda _: bg_picker.pick_files(allow_multiple=False)),
            ft.ElevatedButton("Aplicar Estilo Gangster", on_click=aplicar_estilo_gangster),
            ft.ElevatedButton("Voltar à Fonte Normal", on_click=voltar_fonte_normal),  # Botão para restaurar a fonte padrão
        ], spacing=10)

        page.appbar = ft.AppBar(title=ft.Text(traducoes[IDIOMA_SELECIONADO]["settings"]))
        page.overlay.append(bg_picker)
        page.floating_action_button = None
        page.add(voltar_btn, config_layout)
        page.update()

    def mudar_tema(e):
        nonlocal is_dark_mode
        is_dark_mode = not is_dark_mode
        page.theme_mode = ft.ThemeMode.DARK if is_dark_mode else ft.ThemeMode.LIGHT
        page.update()

    floating_button = ft.FloatingActionButton(
        icon=ft.icons.ADD,
        tooltip=traducoes[IDIOMA_SELECIONADO]["add_task"],
        on_click=abrir_tarefas_view,
        bgcolor=ft.colors.PRIMARY_CONTAINER
    )

    # Atualiza o AppBar para incluir o botão de Configurações e o menu
    page.appbar = ft.AppBar(
        title=ft.Text(traducoes[IDIOMA_SELECIONADO]["tasks"], size=20, weight=ft.FontWeight.BOLD),
        center_title=True,
        bgcolor=ft.colors.SURFACE_VARIANT,
        elevation=4,
        actions=[
            ft.IconButton(
                icon=ft.icons.WB_SUNNY_OUTLINED if not is_dark_mode else ft.icons.NIGHTLIGHT_ROUND,
                tooltip="Mudar Tema",
                on_click=mudar_tema
            ),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text=traducoes[IDIOMA_SELECIONADO]["settings"], on_click=abrir_configuracoes_view),
                    ft.PopupMenuItem(text=traducoes[IDIOMA_SELECIONADO]["list_tasks"], on_click=listar_tarefas_view),
                    ft.PopupMenuItem(text=traducoes[IDIOMA_SELECIONADO]["change_background"], on_click=lambda _: bg_picker.pick_files(allow_multiple=False)),
                    ft.PopupMenuItem(text=traducoes[IDIOMA_SELECIONADO]["exit"], on_click=lambda _: page.window_close()),
                ]
            ),
        ]
    )

    atualizar_idioma(IDIOMA_SELECIONADO, page)

    page.overlay.append(bg_picker)
    page.floating_action_button = floating_button

    # Usando Stack para sobrepor a imagem de fundo e os outros elementos
    content = ft.Stack([
        background_image,  # Imagem de fundo
        ft.Column([  # Conteúdo sobreposto
            ft.Container(
                content=ft.Column([welcome_text, hint_text],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                expand=True,
                alignment=ft.alignment.center
            ),
            ft.Divider()
        ])
    ])

    page.add(content)
    page.update()