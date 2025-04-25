import os
import datetime
import flet as ft
from service.tarefa_service import listar_tarefas, atualizar_tarefa, deletar_tarefa, cadastrar_tarefa, editar_tarefa
from model.tarefa_model import Tarefa

UPLOAD_DIR = "uploads"

def render_tarefas_view(page: ft.Page, container: ft.Column):
    """Função para listar as tarefas no container."""
    container.controls.clear()  # Limpar controles do container antes de renderizar

    tarefas = listar_tarefas()  # Pega a lista de tarefas (do banco de dados ou do serviço)

    if not tarefas:
        container.controls.append(ft.Text("Nenhuma tarefa encontrada.", size=18))
    else:
        for tarefa in tarefas:
            tarefa_container = ft.Container(
                content=ft.Column([
                    ft.Text(f"Descrição: {tarefa.descricao}", weight=ft.FontWeight.BOLD),
                    ft.Text(f"Tipo: {tarefa.tipo}"),
                    ft.Text(f"Cadastrado em: {tarefa.data_hora}"),
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                tooltip="Editar",
                                on_click=lambda e, t=tarefa: editar_tarefa_com_dialogo(t, page, container)  # Corrigido
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                tooltip="Excluir",
                                on_click=lambda e, t=tarefa: excluir_tarefa_com_dialogo(t, page, container)
                            ),
                            ft.TextButton(
                                "Ver Anexo",
                                visible=bool(tarefa.arquivo),
                                on_click=lambda e, url=tarefa.arquivo: mostrar_anexo(url, page)
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,  # Centraliza os botões horizontalmente
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,  # Centraliza os botões verticalmente
                        spacing=10  # Adiciona espaçamento entre os botões
                    )
                ]),
                padding=10,
                border=ft.border.all(1, ft.Colors.GREY),
                border_radius=5,
                margin=5
            )
            container.controls.append(tarefa_container)

    # Adiciona o botão "Voltar ao Início"
    voltar_button = ft.ElevatedButton(
        text="Voltar ao Início",
        icon=ft.Icons.HOME,
        on_click=lambda e: __voltar_ao_inicio(page)
    )
    container.controls.append(voltar_button)

    container.update()
    page.update()
def __voltar_ao_inicio(page: ft.Page):
    from view.home import render_home  # Importação local para evitar ciclo
    render_home(page)

def __voltar_ao_inicio(page: ft.Page):
    from view.home import render_home  # Importação local para evitar ciclo
    render_home(page)

def mostrar_anexo(caminho, page: ft.Page):
    """Função para exibir o anexo de uma tarefa."""
    if caminho:
        caminho_completo = os.path.join(UPLOAD_DIR, caminho)
        if os.path.exists(caminho_completo):
            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Anexo da Tarefa"),
                content=ft.Image(src=caminho_completo, width=400, height=400, fit=ft.ImageFit.CONTAIN),
                actions=[
                    ft.TextButton("Fechar", on_click=lambda e: fechar_dialogo(dialog, page))
                ],
                actions_alignment=ft.MainAxisAlignment.END
            )
            page.dialog = dialog
            dialog.open = True
            page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Arquivo não encontrado!"), open=True)
            page.update()

    def fechar_dialogo(dialog, page: ft.Page):
        """Função para fechar o diálogo."""
        dialog.open = False
        page.update()# Remove o diálogo da página para evitar duplicação

          # Adiciona o diálogo à página para garantir que ele seja exibido corretamente
    page.add(dialog)
      # Adiciona o diálogo à página para garantir que ele seja exibido corretamente
def excluir_tarefa_com_dialogo(tarefa, page: ft.Page, container: ft.Column):
    """Função para exibir um diálogo modal antes de excluir uma tarefa."""

    def confirmar_exclusao(e):
        try:
            # Chama a função para excluir a tarefa do banco de dados
            deletar_tarefa(tarefa.id)
            
            # Atualiza a lista de tarefas no container
            render_tarefas_view(page, container)
            
            # Exibe uma mensagem de sucesso
            page.snack_bar = ft.SnackBar(ft.Text("Tarefa excluída com sucesso!"), open=True)
        except Exception as err:
            # Exibe uma mensagem de erro, caso ocorra
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao excluir tarefa: {err}"), open=True)
        finally:
            # Fecha o diálogo
            dialog.open = False
            page.update()

    def cancelar_exclusao(e):
        # Fecha o diálogo sem realizar a exclusão
        dialog.open = False
        page.update()

    # Criação do diálogo modal
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar Exclusão"),
        content=ft.Text(f"Tem certeza que deseja excluir a tarefa '{tarefa.descricao}'?"),
        actions=[
            ft.TextButton("Sim", on_click=confirmar_exclusao),
            ft.TextButton("Não", on_click=cancelar_exclusao),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Atribui e abre o diálogo
    page.dialog = dialog
    dialog.open = True
    page.update()
    page.add(dialog)  # Adiciona o diálogo à página para garantir que ele seja exibido corretamente
    
def cadastrar_tarefa_page(page: ft.Page, tarefas_container: ft.Column):
    """Função para exibir o formulário de cadastro de tarefas."""
    descricao_input = ft.TextField(label="Descrição da Tarefa", expand=True)
    tipo_dropdown = ft.Dropdown(
        label="Tipo de Atividade",
        options=[
            ft.dropdown.Option("Tarefa do Lar"),
            ft.dropdown.Option("Atividade de Casa"),
            ft.dropdown.Option("Trabalho"),
            ft.dropdown.Option("Outro"),
        ],
        value="Outro"
    )
    anexo_picker = ft.FilePicker()
    selected_file_path = ""

    def on_file_selected(e: ft.FilePickerResultEvent):
        nonlocal selected_file_path
        if e.files:
            selected_file_path = e.files[0].path
        else:
            selected_file_path = ""

    anexo_picker.on_result = on_file_selected
    page.overlay.append(anexo_picker)

    def cadastrar(e):
        if descricao_input.value.strip():
            try:
                tipo = tipo_dropdown.value
                data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cadastrar_tarefa(descricao_input.value, False, selected_file_path, tipo, data_hora)
                descricao_input.value = ""
            
            # Exibe a mensagem de sucesso no SnackBar
                page.snack_bar = ft.SnackBar(ft.Text("Tarefa cadastrada com sucesso!"), open=True)
            
            # Exibe a mensagem no console
                print("Tarefa cadastrada com sucesso!")

            # Atualiza a lista de tarefas no container existente
                render_tarefas_view(page, tarefas_container)

            except Exception as err:
            # Exibe a mensagem de erro no SnackBar
                page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao cadastrar: {err}"), open=True)
            
            # Exibe a mensagem de erro no console
            print(f"Erro ao cadastrar: {err}")
        else:
        # Exibe a mensagem de validação no SnackBar
            page.snack_bar = ft.SnackBar(ft.Text("A descrição da tarefa não pode estar vazia!"), open=True)
        
        # Exibe a mensagem de validação no console
        print("A descrição da tarefa não pode estar vazia!")

    page.add(
        ft.Column([
            ft.Text("Cadastrar Nova Tarefa", size=24, weight=ft.FontWeight.BOLD),
            descricao_input,
            tipo_dropdown,
            ft.IconButton(
                icon=ft.Icons.ATTACH_FILE,
                tooltip="Anexar arquivo",
                on_click=lambda _: anexo_picker.pick_files(allow_multiple=False)
            ),
            ft.ElevatedButton("Cadastrar", on_click=cadastrar),
            
        ])
    )
def editar_tarefa_com_dialogo(tarefa: Tarefa, page: ft.Page, container: ft.Column):
    """Função para exibir um pop-up de edição de uma tarefa."""
    descricao_input = ft.TextField(label="Descrição da Tarefa", value=tarefa.descricao, expand=True)
    tipo_dropdown = ft.Dropdown(
        label="Tipo de Atividade",
        options=[
            ft.dropdown.Option("Tarefa do Lar"),
            ft.dropdown.Option("Atividade de Casa"),
            ft.dropdown.Option("Trabalho"),
            ft.dropdown.Option("Outro"),
        ],
        value=tarefa.tipo
    )
    anexo_picker = ft.FilePicker()
    selected_file_path = tarefa.arquivo or ""

    def on_file_selected(e: ft.FilePickerResultEvent):
        nonlocal selected_file_path
        if e.files:
            selected_file_path = e.files[0].path
        else:
            selected_file_path = ""

    anexo_picker.on_result = on_file_selected
    page.overlay.append(anexo_picker)

    def salvar_edicao(e):
        try:
            # Atualiza a tarefa no banco de dados
            editar_tarefa(
                tarefa_id=tarefa.id,
                descricao=descricao_input.value,
                tipo=tipo_dropdown.value,
                arquivo=selected_file_path
            )
            # Exibe mensagem de sucesso
            page.snack_bar = ft.SnackBar(ft.Text("Tarefa editada com sucesso!"), open=True)
            print("Tarefa editada com sucesso!")
            # Atualiza a lista de tarefas
            render_tarefas_view(page, container)
        except ValueError as err:
            # Exibe mensagem de erro
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao editar tarefa: {err}"), open=True)
            print(f"Erro ao editar tarefa: {err}")
        finally:
            # Fecha o diálogo
            dialog.open = False
            page.update()

    def cancelar_edicao(e):
        # Fecha o diálogo sem salvar alterações
        dialog.open = False
        page.update()

    # Criação do diálogo modal
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Editar Tarefa"),
        content=ft.Column([
            descricao_input,
            tipo_dropdown,
            ft.Checkbox(
                label="Concluída",
                value=tarefa.concluida,
                on_change=lambda e: atualizar_tarefa(tarefa.id, tarefa.descricao, e.control.value)
            ),
            ft.Text("Anexo: " + (selected_file_path if selected_file_path else "Nenhum arquivo selecionado")),
            ft.IconButton(
                icon=ft.Icons.ATTACH_FILE,
                tooltip="Anexar arquivo",
                on_click=lambda _: anexo_picker.pick_files(allow_multiple=False)
            ),
        ]),
        actions=[
            ft.TextButton("Salvar", on_click=salvar_edicao),
            ft.TextButton("Cancelar", on_click=cancelar_edicao),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Atribui e abre o diálogo
    page.dialog = dialog
    dialog.open = True
    page.update()
    
    page.add(
        ft.Column([
        ft.Text("Editar Tarefa", size=24, weight=ft.FontWeight.BOLD),
        descricao_input,
        tipo_dropdown,
        ft.Checkbox(
            label="Concluída",
            value=tarefa.concluida,
            on_change=lambda e: atualizar_tarefa(tarefa.id, tarefa.descricao, e.control.value)
        ),
        ft.IconButton(
            icon=ft.Icons.ATTACH_FILE,
            tooltip="Anexar arquivo",
            on_click=lambda _: anexo_picker.pick_files(allow_multiple=False)
        ),
        ft.Row([
            ft.ElevatedButton("Salvar", on_click=salvar_edicao),
            ft.ElevatedButton("Cancelar", on_click=lambda e: render_tarefas_view(page, container)),
        ], alignment=ft.MainAxisAlignment.END)
    ])
)
    page.update()
    page.add(dialog)  # Adiciona o diálogo à página para garantir que ele seja exibido corretamente

    page.update()