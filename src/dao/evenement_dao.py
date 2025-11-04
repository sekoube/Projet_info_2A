from typing import Optional, List
from datetime import date
from dao.db_connection import DBConnection
from business_object.evenement import Evenement
from utils.singleton import Singleton


class EvenementDAO(metaclass=Singleton):
    """
    Data Access Object pour gérer les opérations CRUD sur la table evenement.
    Utilise le pattern Singleton pour garantir une seule instance.
    """

    def creer(self, evenement: Evenement) -> Optional[Evenement]:
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
                        INSERT INTO evenement 
                        (titre, description_evenement, lieu, date_evenement, 
                         capacite_max, created_by, created_at, tarif)
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
                    id_event = cursor.fetchone()["id_event"]
                    evenement.id_event = id_event
                    return evenement

        except Exception as e:
            print(f"Erreur lors de la création de l'événement : {e}")
            return None

    def trouver_par_id(self, id_event: int) -> Optional[Evenement]:
        """
        Récupère un événement par son identifiant.
        
        id_event: Identifiant de l'événement
        
        return: Objet Evenement ou None si non trouvé
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
                    row = cursor.fetchone()
                    if row:
                        return Evenement.from_dict(row)
                    return None

        except Exception as e:
            print(f"Erreur lors de la recherche de l'événement : {e}")
            return None

    def lister_tous(self) -> List[Evenement]:
        """
        Récupère tous les événements de la base de données.
        
        return: Liste des événements (peut être vide)
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
                    rows = cursor.fetchall()
                    return [Evenement.from_dict(row) for row in rows]

        except Exception as e:
            print(f"Erreur lors de la récupération des événements : {e}")
            return []

    def lister_evenements_futurs(self) -> List[Evenement]:
        """
        Récupère tous les événements futurs (date >= aujourd'hui).
        
        return: Liste des événements futurs triés par date croissante
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
                    rows = cursor.fetchall()
                    return [Evenement.from_dict(row) for row in rows]

        except Exception as e:
            print(f"Erreur lors de la récupération des événements futurs : {e}")
            return []

    def lister_evenements_passes(self) -> List[Evenement]:
        """
        Récupère tous les événements passés (date < aujourd'hui).
        
        return: Liste des événements passés triés par date décroissante
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
                    rows = cursor.fetchall()
                    return [Evenement.from_dict(row) for row in rows]

        except Exception as e:
            print(f"Erreur lors de la récupération des événements passés : {e}")
            return []

    def lister_par_createur(self, created_by: int) -> List[Evenement]:
        """
        Récupère tous les événements créés par un utilisateur spécifique.
        
        created_by: ID de l'utilisateur créateur
        
        return: Liste des événements créés par cet utilisateur
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
                        WHERE created_by = %(created_by)s
                        ORDER BY date_evenement DESC;
                        """,
                        {"created_by": created_by},
                    )
                    rows = cursor.fetchall()
                    return [Evenement.from_dict(row) for row in rows]

        except Exception as e:
            print(f"Erreur lors de la récupération des événements du créateur : {e}")
            return []

    def mettre_a_jour(self, evenement: Evenement) -> bool:
        """
        Met à jour un événement existant en base de données.
        
        evenement: Objet Evenement avec les nouvelles valeurs
        
        return: True si la mise à jour a réussi, False sinon
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
            print(f"Erreur lors de la mise à jour de l'événement : {e}")
            return False

    def supprimer(self, id_event: int) -> bool:
        """
        Supprime un événement de la base de données.
        Attention : les contraintes de clé étrangère doivent être gérées
        (supprimer d'abord les inscriptions, bus, etc.)
        
        id_event: Identifiant de l'événement à supprimer
        
        return: True si la suppression a réussi, False sinon
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        DELETE FROM evenement
                        WHERE id_event = %(id_event)s;
                        """,
                        {"id_event": id_event},
                    )
                    return cursor.rowcount > 0

        except Exception as e:
            print(f"Erreur lors de la suppression de l'événement : {e}")
            return False

    def rechercher(self, 
                   titre: Optional[str] = None,
                   lieu: Optional[str] = None,
                   date_min: Optional[date] = None,
                   date_max: Optional[date] = None) -> List[Evenement]:
        """
        Recherche des événements selon différents critères (recherche flexible).
        
        titre: Recherche partielle dans le titre (insensible à la casse)
        lieu: Recherche partielle dans le lieu (insensible à la casse)
        date_min: Date minimum (inclusive)
        date_max: Date maximum (inclusive)
        
        return: Liste des événements correspondants aux critères
        """
        try:
            conditions = []
            params = {}

            if titre:
                conditions.append("LOWER(titre) LIKE LOWER(%(titre)s)")
                params["titre"] = f"%{titre}%"

            if lieu:
                conditions.append("LOWER(lieu) LIKE LOWER(%(lieu)s)")
                params["lieu"] = f"%{lieu}%"

            if date_min:
                conditions.append("date_evenement >= %(date_min)s")
                params["date_min"] = date_min

            if date_max:
                conditions.append("date_evenement <= %(date_max)s")
                params["date_max"] = date_max

            where_clause = " AND ".join(conditions) if conditions else "1=1"

            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"""
                        SELECT id_event, titre, description_evenement, lieu, 
                               date_evenement, capacite_max, created_by, 
                               created_at, tarif
                        FROM evenement
                        WHERE {where_clause}
                        ORDER BY date_evenement ASC;
                        """,
                        params,
                    )
                    rows = cursor.fetchall()
                    return [Evenement.from_dict(row) for row in rows]

        except Exception as e:
            print(f"Erreur lors de la recherche d'événements : {e}")
            return []

    def compter_participants(self, id_event: int) -> int:
        """
        Compte le nombre de participants inscrits à un événement.
        
        id_event: Identifiant de l'événement
        
        return: Nombre d'inscriptions (0 si aucune ou erreur)
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT COUNT(*) as nb_participants
                        FROM inscription
                        WHERE id_event = %(id_event)s;
                        """,
                        {"id_event": id_event},
                    )
                    result = cursor.fetchone()
                    return result["nb_participants"] if result else 0

        except Exception as e:
            print(f"Erreur lors du comptage des participants : {e}")
            return 0