import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._anno = None

    def handle_graph(self, e):
        self._model.crea_grafo(self._view.ddshape.value, self._anno)
        self._view.txt_result1.controls.append(ft.Text(
            f"Il grafo contiene {self._model.getNumNodes()} nodi."))

        self._view.txt_result1.controls.append(ft.Text(
            f"Il grafo contiene {self._model.getNumEdges()} archi."))

        self._view.txt_result1.controls.append(ft.Text(
            f"Il grafo contiene {self._model.getConnesse()} componenti connesse."))

        maxConnessa, max = self._model.getMaxConnessa()
        self._view.txt_result1.controls.append(ft.Text(
            f"la componente connessa più grande è costituita da:"
            f" {max} nodi."))

        for n in maxConnessa:
            self._view.txt_result1.controls.append(ft.Text(
                f" {n.id} - {n.city} , {n.datetime}"))

        self._view.txt_result1.update()



    def handle_path(self, e):
        pass


    def fillDDanno(self):
        anni = self._model.getAnni()
        self._view.ddyear.options.clear()
        for a in anni:
            # print(n)
            self._view.ddyear.options.append(ft.dropdown.Option(a))

    def fillDDshape(self, e):
        self._anno = int(self._view.ddyear.value)
        self._view.ddshape.options.clear()
        self._view.ddshape.value = None

        shapes = self._model.getShape(self._anno)

        #print(shapes)
        for s in sorted(shapes):
            self._view.ddshape.options.append(ft.dropdown.Option(s))
        self._view.update_page()
