import flet as ft
from flet import AppBar, Text, View
from flet.core.colors import Colors
from sqlalchemy import select

from models import *


def main(page: ft.Page):
    # Configurações
    page.title = "Exemplos de listas"
    page.theme_mode = ft.ThemeMode.DARK  # ou ft.ThemeMode.DARK
    page.window.width = 375
    page.window.height = 667

    def salvar_dados(e):
        if input_profissao.value == "" or input_salario.value == "" or input_nome.value == "":
            page.overlay.append(msg_erro)
            msg_erro.open = True
            page.update()

        else:
            obj_user = Usuario(
                Nome=input_nome.value,
                profissao=input_profissao.value,
                salario=int(input_salario.value),
            )

            obj_user.save()
            input_profissao.value = ""
            input_salario.value = ""
            input_nome.value = ""
            page.overlay.append(msg_sucesso)
            msg_sucesso.open = True
            page.update()

    def detalhes(nome, profissao, salario):
        txt_nome.value = nome
        txt_profissao.value = profissao
        txt_salario.value = salario
        page.update()
        page.go("/detalhes_usuario")

    def user(e):
        lv_dados.controls.clear()
        sql_usuario = select(Usuario)
        resultado_user = db_session.execute(sql_usuario).scalars()

        for usuario in resultado_user:
            lv_dados.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.PERSON),
                    title=ft.Text(f"Nome: {usuario.Nome}"),
                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.REMOVE_RED_EYE,
                        items=[
                            ft.PopupMenuItem(
                                text="Detalhes",
                                on_click=lambda _, u=usuario: detalhes(u.Nome, u.profissao, u.salario),
                            )
                        ]
                    )
                )
            )

    def gerencia_rotas(e):
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    AppBar(title=Text("Home"), bgcolor=Colors.PRIMARY_CONTAINER),
                    input_nome,
                    input_profissao,
                    input_salario,
                    ft.Button(
                        text='salvar',
                        on_click=lambda _: salvar_dados(e)
                    ),
                    ft.Button(
                        text='exibir lista',
                        on_click=lambda _: page.go("/lista_usuario"),
                    )
                ]
            )
        )
        if page.route == "/lista_usuario" or page.route == "/detalhes_usuario":
            user(e)
            page.views.append(
                View(
                    "/lista_usuario",
                    [
                        AppBar(title=Text("lista"), bgcolor=Colors.SECONDARY_CONTAINER),
                        lv_dados,
                    ]
                )
            )
        if page.route == "/detalhes_usuario":
            page.views.append(
                View(
                    "/detalhes_usuario",
                    [
                        AppBar(title=Text("Detalhes"), bgcolor=Colors.SECONDARY_CONTAINER),
                        txt_nome,
                        txt_profissao,
                        txt_salario,
                    ]
                )
            )
        page.update()

    def voltar(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    input_profissao = ft.TextField(label="Profissão", hint_text="Digite a profissão")
    input_salario = ft.TextField(label="Salário", hint_text="Digite o salario")
    input_nome = ft.TextField(label="Nome", hint_text="Digite o nome")

    # Componentes
    msg_sucesso = ft.SnackBar(
        content=ft.Text("Nome salvo com sucesso"),
        bgcolor=Colors.GREEN
    )

    msg_erro = ft.SnackBar(
        content=ft.Text("ERRO"),
        bgcolor=Colors.RED
    )

    btn_salvar = ft.Button(text="Salvar")
    lv_dados = ft.ListView(
        height=500
    )
    txt_nome = ft.Text()
    txt_profissao = ft.Text()
    txt_salario = ft.Text()

    # Eventos
    page.on_route_change = gerencia_rotas
    page.on_view_pop = voltar

    page.go(page.route)


# Comando que executa o aplicativo
# Deve estar sempre colado na linha
ft.app(main)
