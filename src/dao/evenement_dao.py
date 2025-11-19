from typing import List, Optional
from dao.db_connection import DBConnection
from business_object.evenement import Evenement
from utils.singleton import Singleton
from datetime import datetime
from datetime import date

class EvenementDAO(metaclass=Singleton):
    """
    Classe DAO pour la gestion des événements en base de données.
    Gère toutes les opérations CRUD sur la table evenement.
    """

    def creer(self, evenement: Evenement) -> str:
        """
        Crée un nouvel événement dans la base de données.

        evenement: Instance d'Evenement à persister

        return: True si création réussie, False sinon
        ------
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO evenement (
                            titre, description_event, lieu, 
                            date_event, capacite_max, created_by, 
                            created_at, tarif, statut
                        )
                        VALUES (%(titre)s, %(description_event)s, %(lieu)s, 
                                %(date_event)s, %(capacite_max)s, %(created_by)s,
                                %(created_at)s, %(tarif)s, %(statut)s)
                        RETURNING id_event;
                        """,
                        {
                            "titre": evenement.titre,
                            "description_event": evenement.description_event,
                            "lieu": evenement.lieu,
                            "date_event": evenement.date_event,
                            "capacite_max": evenement.capacite_max,
                            "created_by": evenement.created_by,
                            "created_at": evenement.created_at,
                            "tarif": float(evenement.tarif),
                            "statut": evenement.statut,
                        },
                    )
                    result = cursor.fetchone()
                    if result:
                        evenement.id_event = result["id_event"]
                        return True
                    return False
        except Exception as e:
            print(f"Erreur lors de la création de l'événement : {e}")
            return False

    def lister_tous(self) -> List[Evenement]:
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT id_event, titre, description_event, lieu,
                            date_event, capacite_max, created_by,
                            created_at, tarif, statut
                        FROM evenement
                        ORDER BY date_event DESC;
                        """
                    )
                    rows = cursor.fetchall()

                    evenements = []
                    for row in rows:
                        # transformer chaque tuple SQL en dict
                        columns = [desc[0] for desc in cursor.description]
                        row_dict = dict(zip(columns, row))

                        # reconstruire proprement l'objet métier
                        evenements.append(Evenement.from_dict(row_dict))

                    return evenements

        except Exception as e:
            print(f"Erreur lors de la récupération des événements : {e}")
            return []

    def get_by(self, column: str, value) -> list[Evenement]:
        # Liste blanche pour éviter les injections SQL via le nom de colonne
        allowed_columns = {
            "id_event",
            "titre",
            "description_event",
            "lieu",
            "date_event",
            "capacite_max",
            "created_by",
            "created_at",
            "tarif",
            "statut"
        }

        if column not in allowed_columns:
            raise ValueError(f"Colonne '{column}' non autorisée.")

        query = f"""
            SELECT id_event, titre, description_event, lieu,
                date_event, capacite_max, created_by,
                created_at, tarif, statut
            FROM evenement
            WHERE {column} = %(value)s;
        """

        with DBConnection().connection.cursor() as cursor:
            cursor.execute(query, {"value": value})
            rows = cursor.fetchall()

        # Chaque ligne est convertie avec ton from_dict
        return [Evenement.from_dict(row) for row in rows]


    def supprimer(self, evenement: Evenement) -> bool:
        """
        Supprime un événement de la base de données.

        evenement: Instance d'Evenement à supprimer
        
        return: True si suppression réussie, False sinon
        ------
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        DELETE FROM evenement
                        WHERE id_event = %(id_event)s;
                        """,
                        {"id_event": evenement.id_event},
                    )
                    return cursor.rowcount > 0
        except Exception as e:
            print(f"Erreur lors de la suppression de l'événement : {e}")
            return False

    def modifier_statut(self, id_event: int, nouveau_statut: str) -> bool:
        """
        Met à jour uniquement le statut d'un événement dans la base de données.

        id_event : identifiant de l'événement
        nouveau_statut : chaîne ('en_cours', 'complet', 'passe')

        return : True si la mise à jour a réussi, False sinon
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE evenement
                        SET statut = %(statut)s
                        WHERE id_event = %(id_event)s;
                        """,
                        {
                            "statut": nouveau_statut,
                            "id_event": id_event
                        },
                    )
                    return cursor.rowcount > 0
        except Exception as e:
            print(f"Erreur lors de la mise à jour du statut : {e}")
            return False
