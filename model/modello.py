import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._allGenes = DAO.get_all_genes()
        self._idMapGenes = {}
        for g in self._allGenes:
            self._idMapGenes[g.GeneID] = g

    def getCromosomi(self):
        return DAO.getCromosomi()

    def buildGraph(self, cMin, cMax):
        self._graph.clear()
        nodes = DAO.getNodes(cMin, cMax)
        self._graph.add_nodes_from(nodes)
        self.addEdges(cMin, cMax)

    def addEdges(self, cMin, cMax):
        allEdges = DAO.getEdges(cMin, cMax)
        for arco in allEdges:
            self._graph.add_edge(arco.Gene1, arco.Gene2, weith=arco.peso)
            if arco.Chrom1 == arco.Chrom2:
                self._graph.add_edge(arco.Gene2, arco.Gene1, weith=arco.peso)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

