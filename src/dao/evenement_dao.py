from typing import List, Optional
from datetime import datetime, date

from dao.db_connection import DBConnection
from business_object.evenement import Evenement
from Projet_info_2A.utils.singleton import Singleton


class EvenementDao(metaclass=Singleton):
    """
    Classe DAO pour la gestion des événements en base de données.
    Gère toutes les opérations CRUD sur la table evenement.
    """

    def creer(self, evenement: Evenement) -> bool:
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
                            titre, description_evenement, lieu, 
                            date_evenement, capacite_max, created_by, 
                            created_at, tarif
                        )
                        VALUES (%(titre)s, %(description_evenement)s, %(lieu)s, 
                                %(date_evenement)s, %(capacite_max)s, %(created_by)s,
                                %(created_at)s, %(tarif)s)
                        RETURNING id_event;
                        """,
                        {
                            "titre": evenement.titre,
                            "description_evenement": evenement.description_evenement,
                            "lieu": evenement.lieu,
                            "date_evenement": evenement.date_evenement,
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
                        SELECT id_event, titre, description_evenement, lieu,
                               date_evenement, capacite_max, created_by,
                               created_at, tarif
                        FROM evenement
                        ORDER BY date_evenement DESC;
                        """
                    )
                    results = cursor.fetchall()
                    
                    evenements = []
                    for row in results:
                        evenement = Evenement(
                            id_event=row["id_event"],
                            titre=row["titre"],
                            description_evenement=row["description_evenement"],
                            lieu=row["lieu"],
                            date_evenement=row["date_evenement"],
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

    def get_by_id(self, id_event: int) -> Optional[Evenement]:
        """
        Trouve un événement par son identifiant.

        id_event: Identifiant de l'événement

        return: Instance d'Evenement ou None si non trouvé
        ------
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT id_event, titre, description_evenement, lieu,
                               date_evenement, capacite_max, created_by,
                               created_at, tarif
                        FROM evenement
                        WHERE id_event = %(id_event)s;
                        """,
                        {"id_event": id_event},
                    )
                    result = cursor.fetchone()
                    
                    if result:
                        return Evenement(
                            id_event=result["id_event"],
                            titre=result["titre"],
                            description_evenement=result["description_evenement"],
                            lieu=result["lieu"],
                            date_evenement=result["date_evenement"],
                            capacite_max=result["capacite_max"],
                            created_by=result["created_by"],
                            created_at=result["created_at"],
                            tarif=float(result["tarif"]),
                        )
                    return None
        except Exception as e:
            print(f"Erreur lors de la recherche de l'événement : {e}")
            return None

    def modifier(self, evenement: Evenement) -> bool:
        """
        Modifie un événement existant dans la base de données.

        evenement: Instance d'Evenement avec les nouvelles valeurs
        
        return: True si modification réussie, False sinon
        ------
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE evenement
                        SET titre = %(titre)s,
                            description_evenement = %(description_evenement)s,
                            lieu = %(lieu)s,
                            date_evenement = %(date_evenement)s,
                            capacite_max = %(capacite_max)s,
                            tarif = %(tarif)s
                        WHERE id_event = %(id_event)s;
                        """,
                        {
                            "id_event": evenement.id_event,
                            "titre": evenement.titre,
                            "description_evenement": evenement.description_evenement,
                            "lieu": evenement.lieu,
                            "date_evenement": evenement.date_evenement,
                            "capacite_max": evenement.capacite_max,
                            "tarif": float(evenement.tarif),
                        },
                    )
                    return cursor.rowcount > 0
        except Exception as e:
            print(f"Erreur lors de la modification de l'événement : {e}")
            return False

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

    def lister_par_createur(self, id_utilisateur: int) -> List[Evenement]:
        """
        Liste tous les événements créés par un utilisateur spécifique.

        id_utilisateur: ID de l'utilisateur créateur
        
        return: Liste d'objets Evenement
        ------
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT id_event, titre, description_evenement, lieu,
                               date_evenement, capacite_max, created_by,
                               created_at, tarif
                        FROM evenement
                        WHERE created_by = %(id_utilisateur)s
                        ORDER BY date_evenement DESC;
                        """,
                        {"id_utilisateur": id_utilisateur},
                    )
                    results = cursor.fetchall()
                    
                    evenements = []
                    for row in results:
                        evenement = Evenement(
                            id_event=row["id_event"],
                            titre=row["titre"],
                            description_evenement=row["description_evenement"],
                            lieu=row["lieu"],
                            date_evenement=row["date_evenement"],
                            capacite_max=row["capacite_max"],
                            created_by=row["created_by"],
                            created_at=row["created_at"],
                            tarif=float(row["tarif"]),
                        )
                        evenements.append(evenement)
                    
                    return evenements
        except Exception as e:
            print(f"Erreur lors de la récupération des événements par créateur : {e}")
            return []

    def lister_futurs(self) -> List[Evenement]:
        """
        Liste tous les événements futurs (date >= aujourd'hui).

        return: Liste d'objets Evenement
        ------
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT id_event, titre, description_evenement, lieu,
                               date_evenement, capacite_max, created_by,
                               created_at, tarif
                        FROM evenement
                        WHERE date_evenement >= CURRENT_DATE
                        ORDER BY date_evenement ASC;
                        """
                    )
                    results = cursor.fetchall()
                    
                    evenements = []
                    for row in results:
                        evenement = Evenement(
                            id_event=row["id_event"],
                            titre=row["titre"],
                            description_evenement=row["description_evenement"],
                            lieu=row["lieu"],
                            date_evenement=row["date_evenement"],
                            capacite_max=row["capacite_max"],
                            created_by=row["created_by"],
                            created_at=row["created_at"],
                            tarif=float(row["tarif"]),
                        )
                        evenements.append(evenement)
                    
                    return evenements
        except Exception as e:
            print(f"Erreur lors de la récupération des événements futurs : {e}")
            return []

    def lister_passes(self) -> List[Evenement]:
        """
        Liste tous les événements passés (date < aujourd'hui).

        return: Liste d'objets Evenement
        ------
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT id_event, titre, description_evenement, lieu,
                               date_evenement, capacite_max, created_by,
                               created_at, tarif
                        FROM evenement
                        WHERE date_evenement < CURRENT_DATE
                        ORDER BY date_evenement DESC;
                        """
                    )
                    results = cursor.fetchall()
                    
                    evenements = []
                    for row in results:
                        evenement = Evenement(
                            id_event=row["id_event"],
                            titre=row["titre"],
                            description_evenement=row["description_evenement"],
                            lieu=row["lieu"],
                            date_evenement=row["date_evenement"],
                            capacite_max=row["capacite_max"],
                            created_by=row["created_by"],
                            created_at=row["created_at"],
                            tarif=float(row["tarif"]),
                        )
                        evenements.append(evenement)
                    
                    return evenements
        except Exception as e:
            print(f"Erreur lors de la récupération des événements passés : {e}")
            return []