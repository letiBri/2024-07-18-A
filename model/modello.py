import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._allGenes = DAO.get_all_genes()
        self._idMapGenes = {}
        for g in self._allGenes:  # la chiave del gene è la coppia id-fuction
            self._idMapGenes[(g.GeneID, g.Function)] = g

        self._bestPath = []
        self._bestScore = 0

    def getCromosomi(self):
        return DAO.getCromosomi()

    def buildGraph(self, cMin, cMax):
        self._graph.clear()
        nodes = DAO.getNodes(cMin, cMax)
        self._graph.add_nodes_from(nodes)
        self.addEdges(cMin, cMax)

    def addEdges(self, cMin, cMax):
        allEdges = DAO.getEdges(cMin, cMax, self._idMapGenes)
        for arco in allEdges:
            self._graph.add_edge(arco.Gene1, arco.Gene2, weight=arco.peso)
            if arco.Chrom1 == arco.Chrom2:
                self._graph.add_edge(arco.Gene2, arco.Gene1, weight=arco.peso)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getBestNodiArchiUscenti(self):
        diz = {}
        for node in self._graph.nodes:
            gradoUscente = self._graph.out_degree(node)
            diz[node] = gradoUscente
        dizSortato = sorted(diz.items(), key=lambda x: x[1], reverse=True)
        result = []
        for node, gradoUscente in dizSortato[:5]:
            pesoTot = 0.0
            for e in self._graph.out_edges(node, data=True):
                pesoTot += float(e[2]["weight"])
            result.append((node, gradoUscente, pesoTot))
        return result

    # cammino più lungo che minimizza la somma dei pesi
    def getOptimalPath(self):
        self._bestPath = []
        self._bestScore = 0

        for node in self._graph.nodes:
            parziale = [node]
            ammissibili = self.calcolaAmmissibili(node, parziale)
            self._ricorsione(parziale, ammissibili)
        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale, ammissibili):
        if len(ammissibili) == 0:
            if len(parziale) > len(self._bestPath) or (len(parziale) == len(self._bestPath) and self.getPeso(parziale) < self._bestScore):
                self._bestPath = copy.deepcopy(parziale)
                self._bestScore = self.getPeso(parziale)
        else:
            for node in ammissibili:
                parziale.append(node)
                nuovi_ammissibili = self.calcolaAmmissibili(node, parziale)
                self._ricorsione(parziale, nuovi_ammissibili)
                parziale.pop()

    def calcolaAmmissibili(self, node, parziale):
        result = []
        for succ in self._graph.successors(node):
            if succ not in parziale:
                if succ.Essential != node.Essential:
                    if len(parziale) == 1:
                        result.append(succ)
                    else:
                        if self._graph[node][succ]["weight"] >= self._graph[parziale[-2]][parziale[-1]]["weight"]:
                            result.append(succ)
        return result

    def getPeso(self, parziale):
        peso = 0.0
        if len(parziale) == 1:
            return peso
        for i in range(0, len(parziale) - 1):
            peso += float(self._graph[parziale[i]][parziale[i + 1]]["weight"])
        return peso





