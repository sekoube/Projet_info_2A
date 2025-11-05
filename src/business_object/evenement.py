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
        titre: str = "",
        lieu: str = "",
        date_evenement: Optional[date] = None,
        capacite_max: int = 0,
        created_by: Optional[int] = None,
        id_event: Optional[int] = None,
        description_evenement: str = "",
        created_at: Optional[datetime] = None,
        tarif: float = 0.00
    ):
        """
        Constructeur de la classe Evenement.

        titre: Titre de l'événement (max 100 caractères)
        lieu: Lieu de l'événement (max 100 caractères)
        date_evenement: Date de l'événement
        capacite_max: Capacité maximale de participants
        created_by: ID de l'utilisateur créateur (FK vers utilisateur)
        id_event: Identifiant unique de l'événement (auto-incrémenté en base)
        description_evenement: Description détaillée de l'événement
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

        if date_evenement is None:
            raise ValueError("La date de l'événement est obligatoire")
        if not isinstance(date_evenement, date):
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
        # =================================================================

        self.id_event = id_event
        self.titre = titre
        self.description_evenement = description_evenement
        self.lieu = lieu
        self.date_evenement = date_evenement
        self.capacite_max = capacite_max
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
        # Quantize pour garantir exactement 2 décimales
        self.tarif = Decimal(str(tarif)).quantize(Decimal('0.01'))

        # Relations (non persistées directement en DB, gérées via tables de liaison)
        self.inscriptions: List = []  # Liste des objets Inscription
        self.bus_aller = None  # Objet Bus (sens=True)
        self.bus_retour = None  # Objet Bus (sens=False)
        self.createur = None  # Objet Utilisateur (si chargé depuis la DB)

    # ************************ Méthodes ***********************************************

    def places_disponibles(self) -> int:
        """
        Retourne le nombre de places disponibles.

        return: Nombre de places restantes
        ------
        """
        return self.capacite_max - len(self.inscriptions)

    def est_complet(self) -> bool:
        """
        Vérifie si l'événement est complet.

        return: True si aucune place disponible
        ------
        """
        return len(self.inscriptions) >= self.capacite_max

    def taux_remplissage(self) -> float:
        """
        Calcule le taux de remplissage de l'événement en pourcentage.

        return: Pourcentage de places occupées (0.0 à 100.0)
        ------
        """
        if self.capacite_max == 0:
            return 0.0
        return (len(self.inscriptions) / self.capacite_max) * 100

    def est_passe(self) -> bool:
        """
        Vérifie si l'événement est déjà passé.

        return: True si la date de l'événement est antérieure à aujourd'hui
        ------
        """
        return self.date_evenement < date.today()

    def resume(self) -> str:
        """
        Retourne un résumé textuel de l'événement.
        Utile pour affichage dans les listes ou interfaces.

        return: str -> "Titre - Date à Lieu (participants/capacité)"
        ------
        """
        # Formatage du tarif avec exactement 2 décimales
        tarif_str = f"{self.tarif:.2f}"
        return (
            f"{self.titre} - {self.date_evenement} à {self.lieu} "
            f"({len(self.inscriptions)}/{self.capacite_max} participants) - {tarif_str}€"
        )

    def __repr__(self):
        """Représentation technique de l'objet"""
        return (
            f"<Evenement #{self.id_event} - {self.titre} "
            f"({self.date_evenement} à {self.lieu})>"
        )

    def __str__(self):
        """Représentation textuelle lisible"""
        return self.resume()

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
            "description_evenement": self.description_evenement,
            "lieu": self.lieu,
            "date_evenement": self.date_evenement.isoformat() if self.date_evenement else None,
            "capacite_max": self.capacite_max,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "tarif": f"{self.tarif:.2f}",  # Formatage avec exactement 2 décimales
            "places_disponibles": self.places_disponibles(),
            "est_complet": self.est_complet(),
            "taux_remplissage": self.taux_remplissage(),
        }

    @staticmethod
    def from_dict(data: dict) -> "Evenement":
        """
        Transformation d'un dict (provenant de la DAO ou de l'API) vers un objet métier.

        data: Dictionnaire contenant les champs d'un événement

        return: Instance de Evenement
        ------
        """
        # Conversion de la date si elle est en format string
        date_evenement = data.get("date_evenement")
        if isinstance(date_evenement, str):
            date_evenement = datetime.fromisoformat(date_evenement).date()

        created_at = data.get("created_at")
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)

        return Evenement(
            id_event=data.get("id_event"),
            titre=data.get("titre", ""),
            description_evenement=data.get("description_evenement", ""),
            lieu=data.get("lieu", ""),
            date_evenement=date_evenement,
            capacite_max=data.get("capacite_max", 0),
            created_by=data.get("created_by"),
            created_at=created_at,
            tarif=data.get("tarif", 0.00),
        )

    def ajouter_bus(self, bus) -> None:
        """Associe un bus à l'événement selon son sens."""
        if bus.sens:  # True = aller
            self.bus_aller = bus
        else:  # False = retour
            self.bus_retour = bus