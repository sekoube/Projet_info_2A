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
            INSERT INTO projet.utilisateur (nom, prenom, email, mot_de_passe, role, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id_utilisateur;
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        query,
                        (
                            utilisateur.nom,
                            utilisateur.prenom,
                            utilisateur.email,
                            utilisateur.mot_de_passe,
                            utilisateur.role,
                            utilisateur.created_at,
                        ),
                    )
                    utilisateur.id_utilisateur = cursor.fetchone()["id_utilisateur"]
            return utilisateur
        except UniqueViolation as e:
            # Gestion des contraintes d'unicité
            if "utilisateur_email_key" in str(e):
                raise ValueError(f"Un utilisateur avec l'email '{utilisateur.email}' existe déjà")

    @staticmethod
    def lister_tous() -> List[Utilisateur]:
        query = "SELECT * FROM utilisateur ORDER BY id_utilisateur"
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                return [Utilisateur.from_dict(row) for row in rows]

    @staticmethod
    def supprimer(id_utilisateur: int) -> bool:
        query = "DELETE FROM utilisateur WHERE id_utilisateur = %s"
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (id_utilisateur,))
                return cursor.rowcount > 0

    def get_by_field(self, field: str, value) ->  Utilisateur | None:
        """Retourne un Utilisateur selon un champ donné."""

        # Sécurité : liste blanche des champs autorisés
        allowed_fields = {"nom", "prenom", "email", "mot_de_passe", "role", "created_at", "id_utilisateur"}
        if field not in allowed_fields:
            raise ValueError(f"Champ non autorisé : {field}")

        query = f"SELECT * FROM utilisateur WHERE {field} = %s"

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (value,))
                row = cursor.fetchone()

                return Utilisateur.from_dict(row) if row else None