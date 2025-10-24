from business_object.admin import Admin
from dao.db_connection import DBConnection


class AdminDao:
    """Accès aux données pour les administrateurs. """

    @staticmethod
    def creer(administrateur: Admin) -> Admin:
        """Insère un nouvel administrateur dans la base de données."""
        query = """
        INSERT INTO administrateur (id_utilisateur)
        VALUES (%s)
        RETURNING id_admin;
        """

        with DBConnection.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    query,
                    (
                        administrateur.id_utilisateur
                    ),
                )
                administrateur.id_admin = cursor.fetchone()["id_admin"]
        return Admin
    
    @staticmethod
    def trouver_par_email(email: str) -> Admin | None:
        """Recherche un administrateur par son email."""
        query = "SELECT * FROM administrateur WHERE email = %s"
        with DBConnection().connection as connection:
            with connection.cursor as cursor:
                cursor.execute(query, (email,))
                row = cursor.fetchone()
                if row:
                    return Admin.from_dict(row)
                return None
    
    @staticmethod
    def trouver_tous() -> list[Admin]:
        """Retourne tous les administrateurs."""
        query = "SELECT * FROM administrateur ORDER BY id_admin"
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                return [Admin.from_dict(row) for row in rows]
    
    @staticmethod
    def supprimer(id_admin: int) -> bool:
        """Supprime un administrateur par son ID."""
        query = "DELETE FROM administrateur WHERE id_admin = %s"
        with DBConnection().connection as connection:
            with connection.cursor as cursor:
                cursor.execute(query, (id_admin,))
                return cursor.rowcount > 0
