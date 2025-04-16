import os
import flet as ft
from service.tarefa_service import listar_tarefas, atualizar_tarefa, deletar_tarefa, cadastrar_tarefa

UPLOAD_DIR = "uploads"

def render_tarefas_view(page: ft.Page, container: ft.Column):
    container.controls.clear()
    tarefas = listar_tarefas()

    descricao_input = ft.TextField(label="Nova Tarefa")
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
        try:
            cadastrar_tarefa(descricao_input.value, False, selected_file_path)
            descricao_input.value = ""
            page.snack_bar = ft.SnackBar(ft.Text("Tarefa cadastrada com sucesso!"), open=True)
            render_tarefas_view(page, container)
        except Exception as err:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao cadastrar: {err}"), open=True)
        page.update()

    def handle_editar(tarefa):
        descricao_edit = ft.TextField(label="Descrição", value=tarefa.descricao)
        concluida_edit = ft.Checkbox(label="Concluída", value=tarefa.concluida)

        def confirmar_edicao(e):
            try:
                atualizar_tarefa(tarefa.id, descricao_edit.value, concluida_edit.value)
                page.snack_bar = ft.SnackBar(ft.Text("Tarefa atualizada!"), open=True)
                render_tarefas_view(page, container)
            except Exception as err:
                page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {err}"), open=True)
            finally:
                page.dialog.open = False
                page.update()

        editar_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar Tarefa"),
            content=ft.Column([descricao_edit, concluida_edit]),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: setattr(page.dialog, "open", False)),
                ft.TextButton("Salvar", on_click=confirmar_edicao)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        page.dialog = editar_dialog
        page.dialog.open = True
        page.update()

    def handle_excluir(tarefa):
        def confirmar_exclusao(e):
            try:
                deletar_tarefa(tarefa.id)
                page.snack_bar = ft.SnackBar(ft.Text("Tarefa excluída."), open=True)
                render_tarefas_view(page, container)
            except Exception as err:
                page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {err}"), open=True)
            finally:
                page.dialog.open = False
                page.update()

        def cancelar_exclusao(e):
            page.dialog.open = False
            page.update()

        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmação"),
            content=ft.Text("Deseja realmente excluir esta tarefa?"),
            actions=[
                ft.TextButton("Não", on_click=cancelar_exclusao),
                ft.TextButton("Sim", on_click=confirmar_exclusao),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        page.dialog = confirm_dialog
        page.dialog.open = True
        page.update()

    def mostrar_anexo(caminho):
        if caminho:
            # Verifica se o arquivo existe no diretório de uploads
            caminho_completo = os.path.join(UPLOAD_DIR, caminho)
            if os.path.exists(caminho_completo):
                # Exibe o anexo em um diálogo
                dialog = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Anexo da Tarefa"),
                    content=ft.Image(src=caminho_completo, width=400, height=400, fit=ft.ImageFit.CONTAIN),
                    actions=[ft.TextButton("Fechar", on_click=lambda e: fechar_dialog())],
                    actions_alignment=ft.MainAxisAlignment.END
                )
                page.dialog = dialog
                page.dialog.open = True
                page.update()
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Arquivo não encontrado!"), open=True)
                page.update()

    def fechar_dialog():
        page.dialog.open = False
        page.update()

    # Formulário de cadastro
    container.controls.append(
        ft.Column([
            ft.Row([
                descricao_input,
                ft.IconButton(
                    icon=ft.icons.ATTACH_FILE,
                    tooltip="Anexar arquivo",
                    on_click=lambda _: anexo_picker.pick_files(allow_multiple=False)
                ),
                ft.ElevatedButton("Cadastrar", on_click=cadastrar)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ])
    )

    # Lista de tarefas
    for tarefa in tarefas:
        def bind_editar(t=tarefa): return lambda e: handle_editar(t)
        def bind_excluir(t=tarefa): return lambda e: handle_excluir(t)

        row = ft.Row([
            ft.Checkbox(
                label=tarefa.descricao,
                value=tarefa.concluida,
                on_change=lambda e, t=tarefa: atualizar_tarefa(t.id, t.descricao, e.control.value),
                expand=True
            ),
            ft.IconButton(icon=ft.icons.EDIT, tooltip="Editar", on_click=bind_editar()),
            ft.IconButton(icon=ft.icons.DELETE, tooltip="Excluir", on_click=bind_excluir()),
            ft.TextButton(
                "Ver Anexo",
                visible=bool(tarefa.arquivo),
                on_click=lambda e, url=tarefa.arquivo: mostrar_anexo(url)
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        container.controls.append(row)

    container.update()
    page.update()