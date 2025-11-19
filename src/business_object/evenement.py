from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List


class Evenement:
    """
    Classe métier représentant un événement de l'application.
    Cette classe contient uniquement la logique métier et les attributs de l'entité.
    Les opérations de persistance et d'orchestration sont gérées par la couche service.
    """

    def __init__(
        self,
        date_event: date,
        titre: str = "",
        lieu: str = "",
        capacite_max: int = 0,
        created_by: Optional[int] = None,
        id_event: Optional[int] = None,
        description_event: str = "",
        created_at: Optional[datetime] = None,
        tarif: float = 0.00,
        statut : str = "en_cours"
    ):
        """
        Constructeur de la classe Evenement.

        titre: Titre de l'événement (max 100 caractères)
        lieu: Lieu de l'événement (max 100 caractères)
        date_event: Date de l'événement
        capacite_max: Capacité maximale de participants
        created_by: ID de l'utilisateur créateur (FK vers utilisateur)
        id_event: Identifiant unique de l'événement (auto-incrémenté en base)
        description_event: Description détaillée de l'événement
        created_at: Date de création de l'événement
        tarif: Tarif de participation à l'événement
        """

        # ========================== VALIDATIONS ==========================
        if not titre or titre.strip() == "":
            raise ValueError("Le titre ne peut pas être vide")
        if len(titre) > 100:
            raise ValueError("Le titre ne peut pas dépasser 100 caractères")

        if not lieu or lieu.strip() == "":
            raise ValueError("Le lieu ne peut pas être vide")
        if len(lieu) > 100:
            raise ValueError("Le lieu ne peut pas dépasser 100 caractères")

        if date_event is None:
            raise ValueError("La date de l'événement est obligatoire")
        if not isinstance(date_event, date):
            raise ValueError("La date de l'événement doit être un objet date")

        if capacite_max <= 0:
            raise ValueError("La capacité maximale doit être supérieure à 0")
        if not isinstance(capacite_max, int):
            raise ValueError("La capacité maximale doit être un entier")

        if created_by is None:
            raise ValueError("L'ID du créateur est obligatoire")
        if not isinstance(created_by, int) or created_by <= 0:
            raise ValueError("L'ID du créateur doit être un entier positif")

        # Conversion du tarif en nombre si c'est une chaîne (depuis from_dict)
        if isinstance(tarif, str):
            tarif = float(tarif)
        
        if tarif < 0:
            raise ValueError("Le tarif ne peut pas être négatif")

        if not statut in ["en_cours", "passe", "complet"]:
            raise ValueError("le satut doit être en_cours, passe ou complet")
        # =================================================================

        self.id_event = id_event
        self.titre = titre
        self.description_event = description_event
        self.lieu = lieu
        self.date_event = date_event
        self.capacite_max = capacite_max
        self.created_by = created_by
        self.created_at = datetime.now()
        # Quantize pour garantir exactement 2 décimales
        self.tarif = Decimal(str(tarif)).quantize(Decimal('0.01'))
        self.statut = statut

    # ************************ Méthodes ***********************************************


    def __str__(self) -> str:
        """
        Retourne un résumé textuel de l'événement.
        Utile pour affichage dans les listes ou interfaces.

        return: str -> "Titre - Date à Lieu (participants/capacité)"
        ------
        """
        # Formatage du tarif avec exactement 2 décimales
        tarif_str = f"{self.tarif:.2f}"
        return (
            f"{self.titre} - {self.date_event} à {self.lieu} - {tarif_str}€"
        )

    def __repr__(self):
        """Représentation technique de l'objet"""
        return (
            f"<Evenement #{self.id_event} - {self.titre} "
            f"({self.date_event} à {self.lieu})>"
        )

    def to_dict(self) -> dict:
        """
        Transforme l'objet en dictionnaire pour échange avec les autres couches.
        Utilisé pour la sérialisation (API, DAO, etc.)

        return: Dictionnaire contenant tous les attributs
        ------
        """
        return {
            "id_event": self.id_event,
            "titre": self.titre,
            "description_event": self.description_event,
            "lieu": self.lieu,
            "date_event": self.date_event.isoformat() if self.date_event else None,
            "capacite_max": self.capacite_max,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "tarif": f"{self.tarif:.2f}",  # Formatage avec exactement 2 décimales,
            "statut": self.statut
            }

    @staticmethod
    def from_dict(data: dict) -> "Evenement":
        """Transformation d'un dict (provenant de la DAO ou de l'API) vers un objet métier."""
        
        date_created_at = data.get("created_at", datetime.now())
        
        # Si la date est une chaîne ISO, on la retransforme en datetime
        if isinstance(date_created_at, str):
            try:
                date_created_at = datetime.fromisoformat(date_created_at)
            except ValueError:
                date_created_at = datetime.now()

        date_date_event = data.get("date_event")
        
        # Si la date est une chaîne ISO, on la retransforme en datetime
        if isinstance(date_date_event, str):
                date_date_event = datetime.fromisoformat(date_date_event)
        
        return Evenement(
            id_event=data.get("id_event"),
            titre=data.get("titre", ""),
            description_event=data.get("description_event", ""),
            lieu=data.get("lieu", ""),
            date_event=date_date_event,
            capacite_max=data.get("capacite_max", 0),
            created_at=date_created_at,
            created_by=data.get("created_by"),
            tarif=data.get("tarif", 0),
            statut=data.get("statut", "en_cours")
        )