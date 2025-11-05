from dao.db_connection import DBConnection

class InscriptionDAO:
    def compter_par_evenement(self, id_evenement: int) -> int:
        """
        Retourne le nombre d'inscriptions pour un événement donné.
        """
        with DBConnection().connection as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT COUNT(*) 
                FROM inscription 
                WHERE id_evenement = ?
                """,
                (id_evenement,)
            )
            resultat = cursor.fetchone()
            return resultat[0] if resultat else 0
