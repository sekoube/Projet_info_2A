# dao/utilisateur_dao.py
from business_objet.utilisateur import Utilisateur
from dao.db_connection import DBConnection


class UtilisateurDAO:
    """Accès aux données pour les utilisateurs (CRUD)."""

    @staticmethod
    def creer(utilisateur: Utilisateur) -> Utilisateur:
        """Insère un nouvel utilisateur dans la base de données."""
        query = """
            INSERT INTO utilisateur (pseudo, nom, prenom, email, mot_de_passe, role, date_creation)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id_utilisateur;
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    query,
                    (
                        utilisateur.pseudo,
                        utilisateur.nom,
                        utilisateur.prenom,
                        utilisateur.email,
                        utilisateur.mot_de_passe,
                        utilisateur.role,
                        utilisateur.date_creation,
                    ),
                )
                utilisateur.id_utilisateur = cursor.fetchone()["id_utilisateur"]
        return utilisateur

    @staticmethod
    def trouver_par_email(email: str) -> Utilisateur | None:
        """Recherche un utilisateur par son e-mail."""
        query = "SELECT * FROM utilisateur WHERE email = %s"
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (email,))
                row = cursor.fetchone()
                if row:
                    return Utilisateur.from_dict(row)
                return None

    @staticmethod
    def trouver_tous() -> list[Utilisateur]:
        """Retourne tous les utilisateurs."""
        query = "SELECT * FROM utilisateur ORDER BY id_utilisateur"
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                return [Utilisateur.from_dict(row) for row in rows]

    @staticmethod
    def supprimer(id_utilisateur: int) -> bool:
        """Supprime un utilisateur par son ID."""
        query = "DELETE FROM utilisateur WHERE id_utilisateur = %s"
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (id_utilisateur,))
                return cursor.rowcount > 0
