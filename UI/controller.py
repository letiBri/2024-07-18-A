import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDCromosomi(self):
        cromosomi = self._model.getCromosomi()
        for c in cromosomi:
            self._view.dd_min_ch.options.append(ft.dropdown.Option(c))
            self._view.dd_max_ch.options.append(ft.dropdown.Option(c))
        self._view.update_page()

    def handle_graph(self, e):
        self._view.txt_result1.controls.clear()
        if self._view.dd_min_ch.value is None or self._view.dd_max_ch.value is None:
            self._view.create_alert("Attenzione: selezionare cromosoma minimo e cromosoma massimo!")
            self._view.update_page()
            return
        cMin = int(self._view.dd_min_ch.value)
        cMax = int(self._view.dd_max_ch.value)
        if cMin >= cMax:
            self._view.create_alert("Attenzione: il cromosoma minimo deve essere più basso del cromosoma massimo!")
            self._view.update_page()
            return

        self._model.buildGraph(cMin, cMax)
        numNodi, numArchi = self._model.getGraphDetails()
        self._view.txt_result1.controls.append(ft.Text(f"Creato grafo con {numNodi} nodi e {numArchi} archi"))
        self._view.txt_result1.controls.append(ft.Text(""))
        bestNodi = self._model.getBestNodiArchiUscenti()
        self._view.txt_result1.controls.append(ft.Text("I 5 nodi con il maggior numero di archi uscenti sono:"))
        for n in bestNodi:
            self._view.txt_result1.controls.append(ft.Text(f"{str(n[0])} | num. archi uscenti: {n[1]} | peso tot.: {n[2]}"))
        # self._view.dd_localization.disabled = False
        # self._view.btn_dettagli.disabled = False
        self._view.btn_path.disabled = False
        self._view.update_page()

    # def handle_dettagli(self, e):
    #     pass

    def handle_path(self, e):
        self._view.txt_result2.controls.clear()
        bestPath, bestScore = self._model.getOptimalPath()
        self._view.txt_result2.controls.append(ft.Text("Cammino ottimo trovato: "))
        self._view.txt_result2.controls.append(ft.Text(f"- Numero di nodi del cammino: {len(bestPath)}"))
        self._view.txt_result2.controls.append(ft.Text(f"- Peso totale del cammino: {bestScore}"))
        self._view.txt_result2.controls.append(ft.Text("- La sequenza dei nodi attraversati è:"))
        for n in bestPath:
            self._view.txt_result2.controls.append(ft.Text(n))
        self._view.update_page()


