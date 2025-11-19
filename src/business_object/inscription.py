from datetime import datetime
from typing import Optional, List


class Inscription:

    """
    Classe métier représentant une inscription dans un évènement.
    Cette classe contient uniquement la logique métier et les attributs de l'entité.
    """

    def __init__(
        self,
        id_event: int,
        id_bus_aller: int,
        id_bus_retour: int,
        code_reservation: Optional[int] = None,
        boit: bool = False,
        mode_paiement: str = "",
        nom_event: str = "",
        created_by: Optional[int] = None
    ):
        """
        Constructeur de la classe Inscription.
        """
        # ========================== VALIDATIONS ==========================
        if not isinstance(code_reservation, int) or code_reservation <= 0:
            raise ValueError("Le code de réservation doit être un entier positif.")

        if not isinstance(boit, bool):
            raise TypeError("Le champ 'boit' doit être de type bool.")

        if created_by is None:
            raise ValueError("L'attribut 'id_utilisateur' (ID utilisateur) est obligatoire.")
        if not isinstance(created_by, int):
            raise TypeError("L'attribut 'id_utilisateur' doit être un entier.")

        if mode_paiement not in ("espece", "en ligne", ""):
            raise ValueError("Le mode de paiement doit être 'espece', 'en ligne' ou vide.")

        if not id_event or not isinstance(id_event, int):
            raise ValueError("L'ID de l'événement est obligatoire et doit être un entier.")
        if not isinstance(nom_event, str):
            raise ValueError("Le nom de l'événement doit être une chaîne.")

        if not isinstance(id_bus_aller, int):
            raise TypeError("L'identifiant du bus aller doit être un entier")
        if not isinstance(id_bus_retour, int):
            raise TypeError("L'identifiant du bus retour doit être un entier")
        # =================================================================

        # ========================== INITIALISATION ==========================
        self.code_reservation = code_reservation
        self.boit = boit
        self.mode_paiement = mode_paiement
        self.id_event = id_event
        self.nom_event = nom_event
        self.id_bus_aller = id_bus_aller
        self.id_bus_retour = id_bus_retour
        self.created_at = datetime.now()
        self.created_by = created_by
        # =================================================================

    # ************************ Méthodes ***********************************************
    def __str__(self) -> str:
        """
        Retourne un résumé textuel de l'inscription.
        Utile pour affichage dans les listes ou interfaces.

        return: str -> "code de reservation, nom_event, id_bus_aller, id_bus_retour"
        ------
        """
        return (
            f"{self.code_reservation} - {self.nom_event} - {self.id_bus_aller} - {self.id_bus_retour}"
        )

    def __repr__(self):
        """Représentation texte"""
        return f"<Inscription {self.created_by} - {self.nom_event}>"

    def to_dict(self) -> dict:
        """Convertit l'objet en dictionnaire"""
        return {
            "code_reservation": self.code_reservation,
            "boit": self.boit,
            "created_by": self.created_by,
            "mode_paiement": self.mode_paiement,
            "id_event": self.id_event,
            "nom_event": self.nom_event,
            "id_bus_aller": self.id_bus_aller,
            "id_bus_retour": self.id_bus_retour,
            "created_at": self.created_at.isoformat(),
        }

@staticmethod
def from_dict(data: dict) -> "Inscription":

    created_at = data.get("created_at")
    if isinstance(created_at, str):
        created_at = datetime.fromisoformat(created_at)

    return Inscription(
        code_reservation=data.get("code_reservation"),
        boit=data.get("boit", False),
        created_by=data.get("created_by"),
        mode_paiement=data.get("mode_paiement", ""),
        id_event=data.get("id_event", ""),
        nom_event=data.get("nom_event", ""),
        created_at=created_at,
        id_bus_aller=data.get("id_bus_aller", ""),
        id_bus_retour=data.get("id_bus_retour", ""),
    )