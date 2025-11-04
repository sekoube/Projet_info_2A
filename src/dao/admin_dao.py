import logging
from dao.db_connection import DBConnection
from business_object.evenement import Evenement
from utils.log_decorator import log

class AdminService:
    """Classe contenant les méthodes de service pour gérer les événements par un administrateur"""

    @log
    def creer(self, admin_pseudo, titre, description, lieu, date, capacite_max, tarif) -> Evenement:
        """Création d'un événement à partir des informations fournies"""
        try:
            evenement = Evenement(
                titre=titre,
                description=description,
                lieu=lieu,
                date=date,
                capacite_max=capacite_max,
                tarif=tarif,
                pseudo_createur=admin_pseudo,
            )

            # Appeler le DAO pour persister l'événement dans la base de données
            if AdminDAO().creer(evenement):
                return evenement
            return None
        except Exception as e:
            logging.error(f"Erreur lors de la création de l'événement: {e}")
            raise

    @log
    def lister_tous(self) -> list[Evenement]:
        """Lister tous les événements"""
        return AdminDAO().lister_tous()

    @log
    def trouver_par_id(self, id_event: int) -> Evenement:
        """Trouver un événement à partir de son ID"""
        return AdminDAO().trouver_par_id(id_event)

    @log
    def supprimer(self, evenement: Evenement) -> bool:
        """Supprimer un événement"""
        try:
            return AdminDAO().supprimer(evenement)
        except Exception as e:
            logging.error(f"Erreur lors de la suppression de l'événement {evenement.id_event}: {e}")
            return False



# from business_object.admin import Admin
# from dao.db_connection import DBConnection


# class AdminDao:
#     """Accès aux données pour les administrateurs. """

#     @staticmethod
#     def creer(administrateur: Admin) -> Admin:
#         """Insère un nouvel administrateur dans la base de données."""
#         query = """
#         INSERT INTO administrateur (id_utilisateur)
#         VALUES (%s)
#         RETURNING id_admin;
#         """

#         with DBConnection.connection as connection:
#             with connection.cursor() as cursor:
#                 cursor.execute(
#                     query,
#                     (
#                         administrateur.id_utilisateur
#                     ),
#                 )
#                 administrateur.id_admin = cursor.fetchone()["id_admin"]
#         return Admin
    
#     @staticmethod
#     def trouver_par_email(email: str) -> Admin | None:
#         """Recherche un administrateur par son email."""
#         query = "SELECT * FROM administrateur WHERE email = %s"
#         with DBConnection().connection as connection:
#             with connection.cursor as cursor:
#                 cursor.execute(query, (email,))
#                 row = cursor.fetchone()
#                 if row:
#                     return Admin.from_dict(row)
#                 return None
    
#     @staticmethod
#     def trouver_tous() -> list[Admin]:
#         """Retourne tous les administrateurs."""
#         query = "SELECT * FROM administrateur ORDER BY id_admin"
#         with DBConnection().connection as connection:
#             with connection.cursor() as cursor:
#                 cursor.execute(query)
#                 rows = cursor.fetchall()
#                 return [Admin.from_dict(row) for row in rows]
    
#     @staticmethod
#     def supprimer(id_admin: int) -> bool:
#         """Supprime un administrateur par son ID."""
#         query = "DELETE FROM administrateur WHERE id_admin = %s"
#         with DBConnection().connection as connection:
#             with connection.cursor as cursor:
#                 cursor.execute(query, (id_admin,))
#                 return cursor.rowcount > 0
