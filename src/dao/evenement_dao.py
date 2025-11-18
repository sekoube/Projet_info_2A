from typing import List, Optional
from dao.db_connection import DBConnection
from business_object.evenement import Evenement
from utils.singleton import Singleton


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
                            created_at, tarif
                        )
                        VALUES (%(titre)s, %(description_event)s, %(lieu)s, 
                                %(date_event)s, %(capacite_max)s, %(created_by)s,
                                %(created_at)s, %(tarif)s)
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
        """
        Liste tous les événements de la base de données.

        return: Liste d'objets Evenement
        ------
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT id_event, titre, description_event, lieu,
                               date_event, capacite_max, created_by,
                               created_at, tarif
                        FROM evenement
                        ORDER BY date_event DESC;
                        """
                    )
                    results = cursor.fetchall()
                    
                    evenements = []
                    for row in results:
                        evenement = Evenement(
                            id_event=row["id_event"],
                            titre=row["titre"],
                            description_event=row["description_event"],
                            lieu=row["lieu"],
                            date_event=row["date_event"],
                            capacite_max=row["capacite_max"],
                            created_by=row["created_by"],
                            created_at=row["created_at"],
                            tarif=float(row["tarif"]),
                        )
                        evenements.append(evenement)

                    return evenements
        except Exception as e:
            print(f"Erreur lors de la récupération des événements : {e}")
            return []

    def get_by_field(self, field: str, value) ->  Evenement | None:
        """Retourne un Evenement selon un champ donné."""

        # Sécurité : liste blanche des champs autorisés
        allowed_fields = {"id_event", "titre", "description_event", "lieu",
                               "date_event", "capacite_max", "created_by",
                               "created_at, tarif", "statut"}
        if field not in allowed_fields:
            raise ValueError(f"Champ non autorisé : {field}")

        query = f"SELECT * FROM evenement WHERE {field} = %s"

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (value,))
                row = cursor.fetchone()

                return Evenement.from_dict(row) if row else None

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
