from database.DB_connect import DBConnect
from model.arco import Arco
from model.gene import Gene
from model.interaction import Interaction


class DAO():

    @staticmethod
    def getCromosomi():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct(genes.Chromosome)
                            from genes 
                            order by genes.Chromosome asc"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["Chromosome"])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_genes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                    FROM genes"""
            cursor.execute(query)

            for row in cursor:
                result.append(Gene(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getNodes(cMin, cMax):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select *
                        from genes g
                        where g.Chromosome >= %s and g.Chromosome <= %s"""
            cursor.execute(query, (cMin, cMax))

            for row in cursor:
                result.append(Gene(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getEdges(cMin, cMax):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT c1.GeneID AS Gene1, g1.Chromosome AS Chrom1, c2.GeneID AS Gene2, g2.Chromosome AS Chrom2, i.Expression_Corr AS peso
                        FROM classification c1, classification c2, genes g1, genes g2, interactions i
                        WHERE c1.Localization = c2.Localization AND c1.GeneID != c2.GeneID 
                            AND ((i.GeneID1 = c1.GeneID AND i.GeneID2 = c2.GeneID) OR (i.GeneID2 = c1.GeneID AND i.GeneID1 = c2.GeneID))
                            AND g1.GeneID = c1.GeneID AND g2.GeneID = c2.GeneID
                            AND g1.Chromosome >= %s AND g1.Chromosome <= %s  
                            AND g2.Chromosome >= %s AND g2.Chromosome <= %s
                            AND (g1.Chromosome < g2.Chromosome OR (g1.Chromosome = g2.Chromosome AND c1.GeneID < c2.GeneID))"""
            cursor.execute(query, (cMin, cMax, cMin, cMax))

            for row in cursor:
                result.append(Arco(**row))

            cursor.close()
            cnx.close()
        return result





