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
    def getEdges(cMin, cMax, idMap):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinctrow g1.GeneID as Gene1, g1.Function as f1, g1.Chromosome as Chrom1, g2.GeneID as Gene2, g2.Function as f2, g2.Chromosome as Chrom2, i.Expression_Corr as peso
                        from genes g1, genes g2, classification c1, classification c2, interactions i 
                        where c1.Localization = c2.Localization 
                        and g1.GeneID = c1.GeneID and g2.GeneID = c2.GeneID and g1.GeneID <> g2.GeneID 
                        and g1.Chromosome >= %s and g1.Chromosome <= %s and g2.Chromosome >= %s and g2.Chromosome <= %s
                        and ((g1.GeneID = i.GeneID1 and g2.GeneID = i.GeneID2) or (g1.GeneID = i.GeneID2 and g2.GeneID = i.GeneID1))
                        and g1.Chromosome <= g2.Chromosome """
            cursor.execute(query, (cMin, cMax, cMin, cMax))

            for row in cursor:
                result.append(Arco(idMap[(row["Gene1"], row["f1"])], row["Chrom1"], idMap[(row["Gene2"], row["f2"])], row["Chrom2"], row["peso"]))

            cursor.close()
            cnx.close()
        return result





