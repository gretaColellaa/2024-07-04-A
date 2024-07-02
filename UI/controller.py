import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        if self._view.ddyear.value is None:
            self._view.create_alert("Selezionare un anno!")
            return
        anno = int(self._view.ddyear.value)
        if self._view.ddshape.value is None:
            self._view.create_alert("Selezionare una shape!")
            return
        shape = self._view.ddshape.value
        self._view.txt_result1.controls.clear()

        self._model.create_graph_GA(anno, shape)
        self._view.txt_result1.controls.append(ft.Text("=======SOLUZIONE AV======"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di vertici: {self._model.get_num_of_nodes()}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di archi: {self._model.get_num_of_edges()}"))
        self._view.txt_result1.controls.append(
            ft.Text(f"Il grafo ha: {self._model.get_num_connesse()} componenti connesse"))
        connessa = self._model.get_largest_connessa()
        self._view.txt_result1.controls.append(ft.Text(f"La componente connessa più grande "
                                                       f"è costituita da {len(connessa)} nodi:"))

        self._model.create_graph(anno, shape)
        self._view.txt_result1.controls.append(ft.Text("=======SOLUZIONE CM======"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di vertici: {self._model.get_num_of_nodes()}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di archi: {self._model.get_num_of_edges()}"))

        self._view.txt_result1.controls.append(
            ft.Text(f"Il grafo ha: {self._model.get_num_connesse()} componenti connesse"))
        connessa = self._model.get_largest_connessa()
        self._view.txt_result1.controls.append(ft.Text(f"La componente connessa più grande "
                                                       f"è costituita da {len(connessa)} nodi:"))
        for c in connessa:
            self._view.txt_result1.controls.append(ft.Text(c))

        self._view.update_page()

    def handle_path(self, e):
        self._view.txt_result2.controls.clear()

        path = self._model.cammino_ottimo()
        self._view.txt_result2.controls.append(ft.Text(f"Il percorso ottimo è costituito da {len(path)} nodi:"))
        for p in path:
            self._view.txt_result2.controls.append(ft.Text(f"{p} - {p.duration}"))

        self._view.update_page()

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

