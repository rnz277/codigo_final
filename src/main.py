import flet as ft
from view.home import render_home

if __name__ == "__main__":
    ft.app(target=render_home, view=ft.WEB_BROWSER, port=8550, assets_dir="assets")
