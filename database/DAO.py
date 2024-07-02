from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                    FROM state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * FROM 
                    sighting s 
                    ORDER BY `datetime` ASC """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_years():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT YEAR(datetime) as anno 
                FROM sighting s 
                ORDER BY anno DESC"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["anno"])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_shapes_year(anno: int):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT s.shape
                    FROM sighting s 
                    WHERE YEAR(s.datetime)=%s
                    ORDER BY shape ASC"""
            cursor.execute(query, (anno,))

            for row in cursor:
                if row["shape"] !="":
                    result.append(row["shape"])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_nodes(year: int, shape: str):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT *
                    FROM sighting s 
                    WHERE Year(s.datetime)=%s AND s.shape =%s
                    ORDER BY s.datetime  ASC"""
            cursor.execute(query, (year, shape,))

            for row in cursor:
                result.append(Sighting(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getEdges(year, shape, idMap):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select t1.id as id1, t1.datetime as d1, t2.id as id2, t2.datetime as d2
                        from (select * from sighting s  where YEAR(`datetime`) = %s  and shape = %s) t1 ,
                        (select * from sighting s where YEAR(`datetime`) = %s  and shape = %s) t2
                        where t1.state = t2.state and t1.datetime < t2.datetime"""
            cursor.execute(query, (year, shape, year, shape))

            for row in cursor:
                result.append((idMap[row['id1']], idMap[row['id2']]))

            cursor.close()
            cnx.close()
        return result