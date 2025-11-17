# dao/utilisateur_dao.py
from typing import Optional, List
from psycopg2.errors import UniqueViolation
from business_object.utilisateur import Utilisateur
from dao.db_connection import DBConnection


class UtilisateurDAO:
    """Accès aux données pour les utilisateurs"""

    @staticmethod
    def creer(utilisateur: Utilisateur) -> Utilisateur:
        query = """
            INSERT INTO projet.utilisateur (pseudo, nom, prenom, email, mot_de_passe, role, date_creation)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id_utilisateur;
        """
        try:
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
        except UniqueViolation as e:
            # Gestion des contraintes d'unicité
            if "utilisateur_email_key" in str(e):
                raise ValueError(f"Un utilisateur avec l'email '{utilisateur.email}' existe déjà")
            elif "utilisateur_pseudo_key" in str(e):
                raise ValueError(f"Un utilisateur avec le pseudo '{utilisateur.pseudo}' existe déjà")
            else:
                raise

    @staticmethod
    def get_by_id(id_utilisateur: int) -> Optional[Utilisateur]:
        query = "SELECT * FROM utilisateur WHERE id_utilisateur = %s"
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (id_utilisateur,))
                row = cursor.fetchone()
                if row:
                    return Utilisateur.from_dict(row)
                return None

    @staticmethod
    def lister_tous() -> List[Utilisateur]:
        query = "SELECT * FROM utilisateur ORDER BY id_utilisateur"
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                return [Utilisateur.from_dict(row) for row in rows]

    @staticmethod
    def modifier(utilisateur: Utilisateur) -> bool:
        query = """
            UPDATE utilisateur
            SET pseudo = %s,
                nom = %s,
                prenom = %s,
                email = %s,
                mot_de_passe = %s,
                role = %s
            WHERE id_utilisateur = %s
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
                        utilisateur.id_utilisateur,
                    ),
                )
                return cursor.rowcount > 0

    @staticmethod
    def supprimer(id_utilisateur: int) -> bool:
        query = "DELETE FROM utilisateur WHERE id_utilisateur = %s"
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (id_utilisateur,))
                return cursor.rowcount > 0

    @staticmethod
    def email_existe(email: str) -> bool:
        query = "SELECT COUNT(*) as count FROM utilisateur WHERE email = %s"
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (email,))
                result = cursor.fetchone()
                return result["count"] > 0

    @staticmethod
    def pseudo_existe(pseudo: str) -> bool:
        query = "SELECT COUNT(*) as count FROM utilisateur WHERE pseudo = %s"
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (pseudo,))
                result = cursor.fetchone()
                return result["count"] > 0

    @staticmethod
    def trouver_par_email(email: str) -> Optional[Utilisateur]:
        query = "SELECT * FROM utilisateur WHERE email = %s"
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (email,))
                row = cursor.fetchone()
                if row:
                    return Utilisateur.from_dict(row)
                return None


