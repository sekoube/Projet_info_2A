from dao.db_connection import DBConnection
from typing import Optional, List
from business_object.inscription import Inscription

class InscriptionDAO:

    def creer(self, inscription: Inscription) -> Optional[Inscription]:
        """
        Crée un nouvel événement en base de données.
        
        evenement: Objet Evenement à insérer (sans id_event)
        
        return: Evenement avec son id_event généré, ou None si échec
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO inscription 
                        (code_reservation, boit, created_by, mode_paiement, 
                         id_event, id_bus_aller, id_bus_retour, created_at)
                        VALUES (%(code_reservation)s, %(boit)s, %(created_by)s, 
                                %(mode_paiement)s, %(id_event)s, 
                                %(id_bus_aller)s, %(id_bus_retour)s, %(created_at)s)
                        RETURNING code_reservation;
                        """,
                        {
                            "code_reservation": inscription.code_reservation,
                            "boit": inscription.boit,
                            "created_by": inscription.created_by,
                            "mode_paiement": inscription.mode_paiement,
                            "id_event": inscription.id_event,
                            "id_bus_aller": inscription.id_bus_aller,
                            "id_bus_retour": inscription.id_bus_retour,
                            "created_at": inscription.created_at,
                        },
                    )
                    code_reservation = cursor.fetchone()["code_reservation"]
                    inscription.code_reservation = code_reservation
                    return inscription

        except Exception as e:
            print(f"Erreur lors de la création de l'inscription : {e}")
            return None

    def get_by(self, column: str, value) -> list[Inscription]:
        # Liste blanche pour éviter les injections SQL via le nom de colonne
        allowed_columns = {
            "code_reservation",
            "boit",
            "created_by",
            "mode_paiement",
            "id_event",
            "id_bus_aller",
            "id_bus_retour",
            "created_at"
        }

        if column not in allowed_columns:
            raise ValueError(f"Colonne '{column}' non autorisée.")

        query = f"""
            SELECT code_reservation, boit, created_by, mode_paiement, 
                id_event, id_bus_aller, id_bus_retour, created_at
            FROM inscription
            WHERE {column} = %(value)s;
        """

        with DBConnection().connection.cursor() as cursor:
            cursor.execute(query, {"value": value})
            rows = cursor.fetchall()

        # Chaque ligne est convertie avec ton from_dict
        return [Inscription.from_dict(row) for row in rows]


    def lister_toutes(self) -> List[Inscription]:
        """
        Liste toutes les inscriptions en base de données.
        
        return: Liste de toutes les inscriptions
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT code_reservation, boit, created_by, mode_paiement,
                               id_event, id_bus_aller, id_bus_retour, created_at
                        FROM inscription;
                        """
                    )
                    rows = cursor.fetchall()
                    return [
                        Inscription(
                            code_reservation=row["code_reservation"],
                            boit=row["boit"],
                            created_by=row["created_by"],
                            mode_paiement=row["mode_paiement"],
                            id_event=row["id_event"],
                            id_bus_aller=row["id_bus_aller"],
                            id_bus_retour=row["id_bus_retour"],
                            created_at=row["created_at"]
                        )
                        for row in rows
                    ]
        except Exception as e:
            print(f"Erreur lors du listage des inscriptions : {e}")
            return []

    def compter_par_evenement(self, id_event: int) -> int:
        """
        Retourne le nombre d'inscriptions pour un événement donné.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT COUNT(*) as count
                        FROM inscription 
                        WHERE id_event = %(id_event)s;
                        """,
                        {"id_event": id_event}
                    )
                    resultat = cursor.fetchone()
                    return resultat["count"] if resultat else 0
        except Exception as e:
            print(f"Erreur lors du comptage des inscriptions : {e}")
            return 0

    def supprimer(self, inscription: Inscription) -> bool:
        """
        Supprime une inscription de la base de données.

        inscription : Objet Inscription à supprimer (doit contenir code_reservation)

        return : True si la suppression a réussi, False sinon.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        DELETE FROM inscription
                        WHERE code_reservation = %(code_reservation)s;
                        """,
                        {"code_reservation": inscription.code_reservation},
                    )
                    return cursor.rowcount > 0

        except Exception as e:
            print(f"Erreur lors de la suppression de l'inscription : {e}")
            return False

    def est_deja_inscrit(self, created_by: int, id_event: int) -> bool:
        """
        Vérifie si un utilisateur est déjà inscrit à un événement.

        created_by : ID de l'utilisateur
        id_event   : ID de l'événement

        return : True si l'utilisateur est déjà inscrit, False sinon
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT 1
                        FROM inscription
                        WHERE created_by = %(created_by)s
                        AND id_event = %(id_event)s
                        LIMIT 1;
                        """,
                        {"created_by": created_by, "id_event": id_event}
                    )
                    return cursor.fetchone() is not None

        except Exception as e:
            print(f"Erreur lors de la vérification de l'inscription : {e}")
            return False
