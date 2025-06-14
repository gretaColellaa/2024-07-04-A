import copy

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._avvistamenti = None
        self._nodes = []
        self._edges = []
        self._grafo = nx.DiGraph()
        pass


    def getAnni(self):

        self._avvistamenti = DAO.get_all_sightings()
        anni = []

        for a in self._avvistamenti:
            if a.datetime.year not in anni:
                anni.append(a.datetime.year)

        anni.reverse()

        return anni

    def getShape(self,a):
        shapes = []

        for avv in self._avvistamenti:
            if int(avv.datetime.year) == a:
                #print(a, avv.datetime.year)
                if avv.shape not in shapes:
                    shapes.append(avv.shape)

        return shapes

    def crea_grafo(self, shape, anno):


        for a in self._avvistamenti:
            if int(a.datetime.year)  == int(anno) and a.shape == shape:
                self._nodes.append(a)

        for a in self._nodes:
            for a2 in self._nodes:
                if a.datetime < a2.datetime:
                    if (a,a2) not in self._edges and a.state == a2.state:
                        self._edges.append((a,a2))

        self._grafo.add_nodes_from(self._nodes)
        self._grafo.add_edges_from(self._edges)

    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)

    def getConnesse(self): #componenti debolmente connesse
        self._debolmenteConnesse = list(nx.weakly_connected_components(self._grafo))
        return len(list(nx.weakly_connected_components(self._grafo)))


    def getMaxConnessa(self):
        max = 0
        maxConnessa = None

        for com in self._debolmenteConnesse:
            lista = list(com)
            if len(lista) > max:
                max = len(lista)
                maxConnessa = lista

        return maxConnessa,max

    def getPath(self):
        self._bestPath = []
        self._bestPunteggio = 0

        for nodo in self._grafo.nodes:
            self._ricorsionePunti([nodo], 0)
        print(self._bestPath, self._bestPunteggio)
        return self._bestPunteggio, self._bestPath

    def _ricorsionePunti(self, parziale, puntiParziale):
        self._stessomese = 1
        if puntiParziale > self._bestPunteggio:
            self._bestPunteggio = puntiParziale
            self._bestPath = copy.deepcopy(parziale)

        ultimo = parziale[-1]
        for succ in self._grafo.successors(ultimo):
            punteggio = 100
            if succ not in parziale:
                if len(parziale) == 1:
                    parziale.append(succ)
                    self._ricorsionePunti(parziale, puntiParziale + punteggio)
                    parziale.pop()

                elif parziale[-1].datetime.month == succ.datetime.month\
                        and self._stessomese<4:
                    punteggio = 200
                    parziale.append(succ)
                    self._stessomese+=1
                    self._ricorsionePunti(parziale, puntiParziale + punteggio)
                    parziale.pop()
                else:
                    parziale.append(succ)
                    self._stessomese = 1
                    self._ricorsionePunti(parziale, puntiParziale + punteggio)
                    parziale.pop()







