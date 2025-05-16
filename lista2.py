import flet as ft
from flet import AppBar, Text, View
from flet.core.colors import Colors
from sqlalchemy import select
from models import Livro, db_session


def main(page: ft.Page):
    # Configurações
    page.title = "Exemplos de listas"
    page.theme_mode = ft.ThemeMode.DARK  # ou ft.ThemeMode.DARK
    page.window.width = 375
    page.window.height = 667

    # Funçõe
    def salvar_dados(e):
        if input_titulo.value == "" or input_autor.value == "" or input_descricao.value == "" or input_categoria.value == "":
            page.overlay.append(msg_erro)
            msg_erro.open = True
            page.update()
        else:
            obj_livro = Livro(
                titulo=input_titulo.value,
                descrisao=input_descricao.value,
                categoria=input_categoria.value,
                autor=input_autor.value,
            )
            obj_livro.save()
            input_titulo.value = ""
            input_descricao.value = ""
            input_categoria.value = ""
            input_autor.value = ""
            page.overlay.append(msg_sucesso)
            msg_sucesso.open = True
            page.update()

    def detalhes(titulo, descrisao, categoria, autor):
        txt_titulo.value = titulo
        txt_descricao.value = descrisao
        txt_categoria.value = categoria
        txt_autor.value = autor
        page.update()
        page.go("/detalhes_livro")

    def livros(e):
        lv.controls.clear()
        sql_livro = select(Livro)
        result = db_session.execute(sql_livro).scalars()

        for livro in result:
            lv.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.PERSON),
                    title=ft.Text(f"Nome: {livro.titulo}"),
                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.REMOVE_RED_EYE,
                        items=[
                            ft.PopupMenuItem(
                                text="Detalhes",
                                on_click=lambda _, u=livro: detalhes(u.titulo, u.descrisao, u.categoria, u.autor),
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
                    input_titulo,
                    input_descricao,
                    input_categoria,
                    input_autor,
                    ft.Button(
                        text='salvar',
                        on_click=lambda _: salvar_dados(e)
                    ),
                    ft.Button(
                        text='exibir lista',
                        on_click=lambda _: page.go("/lista_livro"),
                    )
                ],
            )
        )

        if page.route == "/lista_livro" or page.route == "/detalhes_livro":
            livros(e)
            page.views.append(
                View(
                    "/lista_livro",
                    [
                        AppBar(title=Text("Segunda tela"), bgcolor=Colors.SECONDARY_CONTAINER),
                        lv
                    ],
                )
            )
        if page.route == "/detalhes_livro":
            page.views.append(
                View(
                    "/detalhes_livro",
                    [
                        AppBar(title=Text("detalhes"), bgcolor=Colors.SECONDARY_CONTAINER),
                        txt_autor,
                        txt_descricao,
                        txt_categoria,
                        txt_titulo,
                    ],
                )
            )
        page.update()



    def voltar(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # Componentes
    msg_sucesso = ft.SnackBar(
        content=ft.Text("Nome salvo com sucesso"),
        bgcolor=Colors.GREEN
    )

    msg_erro = ft.SnackBar(
        content=ft.Text("ERRO"),
        bgcolor=Colors.RED
    )

    input_titulo = ft.TextField(label="titulo", hint_text="Digite o titulo")
    input_descricao = ft.TextField(label="descricao", hint_text="Digite a descricao")
    input_categoria = ft.TextField(label="categoria", hint_text="Digite a categoria")
    input_autor = ft.TextField(label="autor", hint_text="Digite o autor")
    btn_salvar = ft.Button(text="Salvar")
    lv = ft.ListView(
        height=500
    )
    txt_titulo = ft.Text()
    txt_descricao = ft.Text()
    txt_categoria = ft.Text()
    txt_autor = ft.Text()


    # Eventos
    page.on_route_change = gerencia_rotas
    page.on_view_pop = voltar

    page.go(page.route)


# Comando que executa o aplicativo
# Deve estar sempre colado na linha
ft.app(main)
