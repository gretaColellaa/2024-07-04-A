import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_scroll(self, e):
        print(e.x)
        self._view.txt_result1.scroll_to(e.x, e.y)

    def handle_graph(self, e):
        pass

    def handle_path(self, e):
        pass

    def fill_ddyear(self):
        years = self._model.get_years()
        self._view.ddyear.options.clear()
        for y in years:
            self._view.ddyear.options.append(ft.dropdown.Option(f"{y}"))

    def fill_ddshape(self, e):
        anno = int(self._view.ddyear.value)
        self._view.ddshape.options.clear()
        self._view.ddshape.value = None
        shapes = self._model.get_shapes_year(anno)
        for s in shapes:
            self._view.ddshape.options.append(ft.dropdown.Option(s))
        self._view.update_page()

