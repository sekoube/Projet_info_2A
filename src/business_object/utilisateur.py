from datetime import datetime
from typing import Optional  # indiquer les types attendus pour les arguments, les attributs
import re  # pour vérifier la validité de l'adresse e-mail
from Projet_info_2A.utils.mdp import hash_password, verify_password


class Utilisateur:
    """
    Classe métier représentant un utilisateur de l'application (administrateur ou participant).
    Cette classe contient uniquement la logique métier et les attributs de l'entité.
    """

    def __init__(
        self,
        id_utilisateur: Optional[int] = None,
        pseudo: str = "",
        nom: str = "",
        prenom: str = "",
        email: str = "",
        mot_de_passe: str = "",
        role: bool = False,
        date_creation: Optional[datetime] = None
    ):
        """
        Constructeur de la classe Utilisateur.

        id_utilisateur: Identifiant unique de l'utilisateur (auto-incrémenté en base)
        pseudo: Pseudonyme choisi par l'utilisateur
        nom: Nom de famille
        prenom: Prénoms
        email: Adresse e-mail de l'utilisateur
        Mot de passe (hashé en base)
        role: Booléen indiquant si l'utilisateur est administrateur (True) ou participant (False)
        date_creation: Date de création du compte
        """

        self.id_utilisateur = id_utilisateur
        self.pseudo = pseudo
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.mot_de_passe = mot_de_passe
        self.role = role
        self.date_creation = date_creation or datetime.now()

        # ========================== VALIDATIONS ==========================
        if not pseudo or pseudo.strip() == "":
            raise ValueError("Le pseudo ne peut pas être vide")
        if not nom or nom.strip() == "":
            raise ValueError("Le nom ne peut pas être vide")
        if not prenom or prenom.strip() == "":
            raise ValueError("Le prénom ne peut pas être vide")

        # Validation de l'email - Format attendu : texte@texte.domaine
        if not email or not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            raise ValueError("L'adresse e-mail n'est pas valide")

        if not mot_de_passe or mot_de_passe.strip() == "":
            raise ValueError("Le mot de passe ne peut pas être vide")

        # =================================================================

    # ************************ Méthodes ***********************************************

    def identite(self) -> str:
        """
        Retourne une représentation de l'identité de l'utilisateur.
        utile pour héritage avec Administrateur

        return: str -> "Prénom Nom (pseudo)"
        ------
        """
        return f"{self.prenom} {self.nom} ({self.pseudo})"

    def is_admin(self):
        return self.role is True

    def set_password(self, plain_password: str) -> None:
        """Hache et stocke un mot de passe sécurisé."""
        # Déplacer la vérification dans validation
        if not plain_password or plain_password.strip() == "":
            raise ValueError("Le mot de passe ne peut pas être vide")
        self.mot_de_passe = hash_password(plain_password)

    def verify_password(self, plain_password: str) -> bool:
        """Vérifie qu'un mot de passe correspond au hash stocké."""
        return verify_password(plain_password, self.mot_de_passe)
     
    def __repr__(self):
        """Représentation texte"""
        role_str = "Admin" if self.role else "Participant"
        return f"<Utilisateur #{self.id_utilisateur} - {self.pseudo} ({role_str})>"

    def to_dict(self) -> dict:
        """
        On transforme l'objet en dict pour échange avec les autres couches (service/DAO/API).
        """
        return {
            "id_utilisateur": self.id_utilisateur,
            "pseudo": self.pseudo,
            "nom": self.nom,
            "prenom": self.prenom,
            "email": self.email,
            "mot_de_passe": self.mot_de_passe,  # hash attendu
            "role": self.role,
            "date_creation": self.date_creation.isoformat(),
        }

    @staticmethod
    def from_dict(data: dict) -> "Utilisateur":
        """Transformation d'un dict (provenant de la DAO ou de l'API) vers un objet métier."""
        date_value = data.get("date_creation", datetime.now())
        
        # Si la date est une chaîne ISO, on la retransforme en datetime
        if isinstance(date_value, str):
            try:
                date_value = datetime.fromisoformat(date_value)
            except ValueError:
                date_value = datetime.now()
        
        return Utilisateur(
            id_utilisateur=data.get("id_utilisateur"),
            pseudo=data.get("pseudo", ""),
            nom=data.get("nom", ""),
            prenom=data.get("prenom", ""),
            email=data.get("email", ""),
            mot_de_passe=data.get("mot_de_passe", ""),
            role=data.get("role", False),
            date_creation=date_value,
        )