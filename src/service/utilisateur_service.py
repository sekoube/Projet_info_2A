from business_object.utilisateur import Utilisateur
from dao.utilisateur_dao import UtilisateurDAO
from utils.mdp import hash_password


class UtilisateurService:
    """
    Couche service pour la gestion des utilisateurs.
    Elle orchestre la logique applicative autour des comptes :
    création, authentification, suppression, etc.
    """

    def __init__(self):
        self.utilisateur_dao = UtilisateurDAO()

    # ======================================================
    # === Création d'un compte utilisateur =================
    # ======================================================
    def creer_utilisateur(self, nom: str, prenom: str,
                    email: str, mot_de_passe: str, role: bool = False) -> Utilisateur | None:
        """
        Crée un nouvel utilisateur après vérifications.
        Vérifie que l'email n'est pas déjà pris,
        puis insère en base un utilisateur avec mot de passe hashé.

        return: Objet Utilisateur créé ou None si erreur
        """

        # Vérifier unicité e-mail
        if self.utilisateur_dao.email_existe(email):
            print("Cet email est déjà utilisé.")
            return None

        # Hachage du mot de passe
        mot_de_passe_hache = hash_password(mot_de_passe)

        # Création de l'objet métier
        nouvel_utilisateur = Utilisateur(
            nom=nom,
            prenom=prenom,
            email=email,
            mot_de_passe=mot_de_passe_hache,
            role=role
        )

        # Persistance en base
        utilisateur_cree = self.utilisateur_dao.creer(nouvel_utilisateur)

        if utilisateur_cree:
            print(f"Utilisateur '{prenom}', '{nom}' créé avec succès.")
            return utilisateur_cree
        else:
            print("Erreur lors de la création de l'utilisateur.")
            return None

    # ======================================================
    # === Authentification ================================
    # ======================================================
    def authentifier(self, email: str, mot_de_passe: str) -> Utilisateur | None:
        """
        Vérifie les identifiants d'un utilisateur.
        Compare le mot de passe fourni avec le hash stocké.

        return: Utilisateur si authentification réussie, None sinon
        """
        utilisateur = self.utilisateur_dao.trouver_par_email(email)
        if not utilisateur:
            print("Aucun compte trouvé avec cet email.")
            return None

        if not utilisateur.verify_password(mot_de_passe):
            print("Mot de passe incorrect.")
            return None

        print(f"Connexion réussie : {utilisateur.prenom}, {utilisateur.nom}")
        return utilisateur

    # ======================================================
    # === Liste des utilisateurs ===========================
    # ======================================================
    def lister_utilisateurs(self) -> list[Utilisateur]:
        """
        Retourne la liste de tous les utilisateurs enregistrés.
        """
        utilisateurs = self.utilisateur_dao.lister_tous()
        print(f"{len(utilisateurs)} utilisateur(s) trouvé(s).")
        return utilisateurs

    # ======================================================
    # === Suppression (admin uniquement) ===================
    # ======================================================
    def supprimer_utilisateur(self, admin: Utilisateur, id_utilisateur: int) -> bool:
        """
        Supprime un utilisateur, uniquement si l'action est effectuée par un admin.

        admin: objet Utilisateur qui effectue l'action
        id_utilisateur: ID de l'utilisateur à supprimer

        return: True si suppression réussie, False sinon
        """
        # Vérifier les droits d’accès
        if not admin.is_admin:
            print("Vous n'avez pas les droits pour supprimer un utilisateur.")
            return False

        # Vérifier l’existence de l’utilisateur à supprimer
        utilisateur_cible = self.utilisateur_dao.get_by_id(id_utilisateur)
        if not utilisateur_cible:
            print(f"Aucun utilisateur trouvé avec l'ID {id_utilisateur}.")
            return False


        # Suppression via la DAO
        suppression_ok = self.utilisateur_dao.supprimer(id_utilisateur)
        if suppression_ok:
            print(f"Utilisateur '{utilisateur_cible.prenom}', {utilisateur_cible.nom} supprimé avec succès.")
        else:
            print("Erreur lors de la suppression de l'utilisateur.")
        return suppression_ok

    def get_utilisateur_by_field(self, field: str, value) -> Optional[Utilisateur]:
        """
        Récupère un Utilisateur en fonction d'un champ et de sa valeur.

        Args:
            field (str): Le nom du champ de la table 'utilisateur' à rechercher.
                         La DAO gère la validation des champs autorisés.
            value: La valeur à comparer dans ce champ.

        Returns:
            Optional[Utilisateur]: L'objet Utilisateur trouvé ou None.
        
        Raises:
            ValueError: Si le champ fourni n'est pas autorisé par la DAO.
        """
        
        # 1. Logique métier (si nécessaire)
        # Par exemple, vérifier ici les permissions de l'utilisateur qui fait la requête.
        
        # 2. Délégation à la DAO
        try:
            # La DAO est responsable de l'exécution de la requête et de la validation
            # des champs autorisés (liste blanche).
            utilisateur = self.utilisateur_dao.get_by_field(field, value)
            
            # 3. Logique post-récupération (si nécessaire)
            # Par exemple, masquer le champ 'mot_de_passe' avant de retourner l'objet, 
            # bien que cela soit souvent géré par le modèle ou la couche API.
            
            return utilisateur
            
        except ValueError as e:
            # Capturer et propager l'erreur levée par la DAO si le champ n'est pas autorisé.
            # C'est important pour la sécurité.
            raise e