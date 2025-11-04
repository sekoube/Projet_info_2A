# dao/utilisateur_dao.py
from typing import Optional, List
from business_object.utilisateur import Utilisateur
from dao.db_connection import DBConnection


class UtilisateurDAO:
    """Accès aux données pour les utilisateurs (CRUD)."""

    @staticmethod
    def creer(utilisateur: Utilisateur) -> Utilisateur:
        """
        Insère un nouvel utilisateur dans la base de données.
        
        Args:
            utilisateur: Objet Utilisateur à créer
            
        Returns:
            Utilisateur avec son id_utilisateur généré
        """
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
    def trouver_par_id(id_utilisateur: int) -> Optional[Utilisateur]:
        """
        Recherche un utilisateur par son ID.
        
        Args:
            id_utilisateur: ID de l'utilisateur recherché
            
        Returns:
            Utilisateur trouvé ou None
        """
        query = "SELECT * FROM utilisateur WHERE id_utilisateur = %s"
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (id_utilisateur,))
                row = cursor.fetchone()
                if row:
                    return Utilisateur.from_dict(row)
                return None

    @staticmethod
    def trouver_par_email(email: str) -> Optional[Utilisateur]:
        """
        Recherche un utilisateur par son e-mail.
        
        Args:
            email: Email de l'utilisateur recherché
            
        Returns:
            Utilisateur trouvé ou None
        """
        query = "SELECT * FROM utilisateur WHERE email = %s"
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (email,))
                row = cursor.fetchone()
                if row:
                    return Utilisateur.from_dict(row)
                return None

    @staticmethod
    def trouver_par_pseudo(pseudo: str) -> Optional[Utilisateur]:
        """
        Recherche un utilisateur par son pseudo.
        
        Args:
            pseudo: Pseudo de l'utilisateur recherché
            
        Returns:
            Utilisateur trouvé ou None
        """
        query = "SELECT * FROM utilisateur WHERE pseudo = %s"
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (pseudo,))
                row = cursor.fetchone()
                if row:
                    return Utilisateur.from_dict(row)
                return None

    @staticmethod
    def trouver_tous() -> List[Utilisateur]:
        """
        Retourne tous les utilisateurs.
        
        Returns:
            Liste de tous les utilisateurs
        """
        query = "SELECT * FROM utilisateur ORDER BY id_utilisateur"
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                return [Utilisateur.from_dict(row) for row in rows]

    @staticmethod
    def trouver_par_role(role: str) -> List[Utilisateur]:
        """
        Recherche tous les utilisateurs ayant un rôle spécifique.
        
        Args:
            role: Rôle recherché (ex: 'admin', 'user')
            
        Returns:
            Liste des utilisateurs avec ce rôle
        """
        query = "SELECT * FROM utilisateur WHERE role = %s ORDER BY id_utilisateur"
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (role,))
                rows = cursor.fetchall()
                return [Utilisateur.from_dict(row) for row in rows]

    @staticmethod
    def modifier(utilisateur: Utilisateur) -> bool:
        """
        Met à jour un utilisateur existant dans la base de données.
        
        Args:
            utilisateur: Objet Utilisateur avec les nouvelles données
            
        Returns:
            True si la modification a réussi, False sinon
        """
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
        """
        Supprime un utilisateur par son ID.
        
        Args:
            id_utilisateur: ID de l'utilisateur à supprimer
            
        Returns:
            True si la suppression a réussi, False sinon
        """
        query = "DELETE FROM utilisateur WHERE id_utilisateur = %s"
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (id_utilisateur,))
                return cursor.rowcount > 0

    @staticmethod
    def email_existe(email: str) -> bool:
        """
        Vérifie si un email existe déjà dans la base de données.
        
        Args:
            email: Email à vérifier
            
        Returns:
            True si l'email existe déjà, False sinon
        """
        query = "SELECT COUNT(*) as count FROM utilisateur WHERE email = %s"
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (email,))
                result = cursor.fetchone()
                return result["count"] > 0

    @staticmethod
    def pseudo_existe(pseudo: str) -> bool:
        """
        Vérifie si un pseudo existe déjà dans la base de données.
        
        Args:
            pseudo: Pseudo à vérifier
            
        Returns:
            True si le pseudo existe déjà, False sinon
        """
        query = "SELECT COUNT(*) as count FROM utilisateur WHERE pseudo = %s"
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (pseudo,))
                result = cursor.fetchone()
                return result["count"] > 0