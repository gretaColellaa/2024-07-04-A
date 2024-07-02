from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        pass

    def get_years(self):
        return DAO.get_years()

    def get_shapes_year(self, year: int):
        return DAO.get_shapes_year(year)