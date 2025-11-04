import pytest
from datetime import datetime, date, timedelta
from decimal import Decimal
from unittest.mock import Mock
import sys
import os

# Chemin du projet racine (2 niveaux au-dessus du fichier test)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_root)

from src.business_object.evenement import Evenement


# ==================== FIXTURES ====================

@pytest.fixture
def date_future():
    """Date dans 30 jours."""
    return date.today() + timedelta(days=30)


@pytest.fixture
def date_passee():
    """Date il y a 30 jours."""
    return date.today() - timedelta(days=30)


@pytest.fixture
def evenement_valide_data(date_future):
    """Dictionnaire de données valides pour créer un événement."""
    return {
        "titre": "Festival Rock",
        "lieu": "Rennes",
        "date_evenement": date_future,
        "capacite_max": 100,
        "created_by": 1,
        "description_evenement": "Un super festival de rock",
        "tarif": 25.50
    }


@pytest.fixture
def evenement(evenement_valide_data):
    """Instance d'événement valide pour les tests."""
    return Evenement(**evenement_valide_data)


@pytest.fixture
def evenement_avec_id(evenement_valide_data):
    """Événement avec un ID pour les inscriptions."""
    evenement = Evenement(**evenement_valide_data)
    evenement.id_event = 1
    return evenement


@pytest.fixture
def mock_utilisateur():
    """Mock simple d'un utilisateur."""
    user = Mock()
    user.id_utilisateur = 1
    user.nom = "Dupont"
    user.prenom = "Jean"
    return user


@pytest.fixture
def mock_utilisateur2():
    """Mock d'un second utilisateur."""
    user = Mock()
    user.id_utilisateur = 2
    user.nom = "Martin"
    user.prenom = "Sophie"
    return user


# ==================== TESTS DE VALIDATION ====================

class TestValidation:
    """Tests de validation des données d'entrée."""

    def test_creation_evenement_valide(self, evenement, date_future):
        """Test : création d'un événement avec des données valides."""
        assert evenement.titre == "Festival Rock"
        assert evenement.lieu == "Rennes"
        assert evenement.date_evenement == date_future
        assert evenement.capacite_max == 100
        assert evenement.created_by == 1
        assert evenement.tarif == Decimal("25.50")
        assert evenement.id_event is None
        assert isinstance(evenement.created_at, datetime)

    def test_titre_vide(self, evenement_valide_data):
        """Test : titre vide doit lever une ValueError."""
        evenement_valide_data["titre"] = ""
        
        with pytest.raises(ValueError, match="titre ne peut pas être vide"):
            Evenement(**evenement_valide_data)

    def test_titre_trop_long(self, evenement_valide_data):
        """Test : titre trop long doit lever une ValueError."""
        evenement_valide_data["titre"] = "A" * 101
        
        with pytest.raises(ValueError, match="100 caractères"):
            Evenement(**evenement_valide_data)

    def test_lieu_vide(self, evenement_valide_data):
        """Test : lieu vide doit lever une ValueError."""
        evenement_valide_data["lieu"] = "   "
        
        with pytest.raises(ValueError, match="lieu ne peut pas être vide"):
            Evenement(**evenement_valide_data)

    def test_lieu_trop_long(self, evenement_valide_data):
        """Test : lieu trop long doit lever une ValueError."""
        evenement_valide_data["lieu"] = "B" * 101

        with pytest.raises(ValueError, match="100 caractères"):
            Evenement(**evenement_valide_data)

    def test_date_evenement_none(self, evenement_valide_data):
        """Test : date None doit lever une ValueError."""
        evenement_valide_data["date_evenement"] = None

        with pytest.raises(ValueError, match="date de l'événement est obligatoire"):
            Evenement(**evenement_valide_data)

    def test_date_evenement_mauvais_type(self, evenement_valide_data):
        """Test : date avec mauvais type doit lever une ValueError."""
        evenement_valide_data["date_evenement"] = "2025-12-25"

        with pytest.raises(ValueError, match="objet date"):
            Evenement(**evenement_valide_data)

    @pytest.mark.parametrize("capacite", [0, -10, -100])
    def test_capacite_max_invalide(self, evenement_valide_data, capacite):
        """Test : capacité max invalide (0 ou négative) doit lever une ValueError."""
        evenement_valide_data["capacite_max"] = capacite

        with pytest.raises(ValueError, match="supérieure à 0"):
            Evenement(**evenement_valide_data)

    def test_capacite_max_non_entier(self, evenement_valide_data):
        """Test : capacité max non entière doit lever une ValueError."""
        evenement_valide_data["capacite_max"] = 50.5

        with pytest.raises(ValueError, match="entier"):
            Evenement(**evenement_valide_data)

    def test_created_by_none(self, evenement_valide_data):
        """Test : created_by None doit lever une ValueError."""
        evenement_valide_data["created_by"] = None

        with pytest.raises(ValueError, match="créateur est obligatoire"):
            Evenement(**evenement_valide_data)

    def test_created_by_negatif(self, evenement_valide_data):
        """Test : created_by négatif doit lever une ValueError."""
        evenement_valide_data["created_by"] = -1

        with pytest.raises(ValueError, match="entier positif"):
            Evenement(**evenement_valide_data)

    def test_tarif_negatif(self, evenement_valide_data):
        """Test : tarif négatif doit lever une ValueError."""
        evenement_valide_data["tarif"] = -10.0

        with pytest.raises(ValueError, match="tarif ne peut pas être négatif"):
            Evenement(**evenement_valide_data)

    def test_tarif_zero_valide(self, evenement_valide_data):
        """Test : tarif à 0 (gratuit) est valide."""
        evenement_valide_data["tarif"] = 0.0

        evenement = Evenement(**evenement_valide_data)
        assert evenement.tarif == Decimal("0.00")

    def test_tarif_deja_decimal(self, evenement_valide_data):
        """Test : tarif déjà en Decimal est accepté directement."""
        evenement_valide_data["tarif"] = Decimal("30.00")

        evenement = Evenement(**evenement_valide_data)

        assert evenement.tarif == Decimal("30.00")
        assert isinstance(evenement.tarif, Decimal)


# ==================== TESTS DES MÉTHODES MÉTIER ====================

class TestMethodesMetier:
    """Tests des méthodes métier de l'événement."""

    def test_places_disponibles_evenement_vide(self, evenement):
        """Test : places disponibles = capacité max pour événement vide."""
        assert evenement.places_disponibles() == 100

    def test_est_complet_evenement_vide(self, evenement):
        """Test : événement vide n'est pas complet."""
        assert not evenement.est_complet()

    def test_taux_remplissage_evenement_vide(self, evenement):
        """Test : taux de remplissage à 0% pour événement vide."""
        assert evenement.taux_remplissage() == 0.0

    def test_taux_remplissage_capacite_zero(self, evenement):
        """Test : taux de remplissage avec capacité 0 (cas limite)."""
        evenement.capacite_max = 0
        assert evenement.taux_remplissage() == 0.0

    def test_est_passe_evenement_futur(self, evenement):
        """Test : événement futur n'est pas passé."""
        assert not evenement.est_passe()

    def test_est_passe_evenement_passe(self, evenement_valide_data, date_passee):
        """Test : événement passé est bien détecté."""
        evenement_valide_data["date_evenement"] = date_passee
        evenement = Evenement(**evenement_valide_data)

        assert evenement.est_passe()

    def test_est_passe_evenement_aujourdhui(self, evenement_valide_data):
        """Test : événement aujourd'hui n'est pas passé."""
        evenement_valide_data["date_evenement"] = date.today()
        evenement = Evenement(**evenement_valide_data)

        assert not evenement.est_passe()


# ==================== TESTS DES BUS ====================

class TestBus:
    """Tests de gestion des bus."""

    @pytest.fixture
    def bus_aller(self):
        """Mock d'un bus aller."""
        bus = Mock()
        bus.sens = True
        return bus

    @pytest.fixture
    def bus_retour(self):
        """Mock d'un bus retour."""
        bus = Mock()
        bus.sens = False
        return bus

    def test_ajouter_bus_aller(self, evenement, bus_aller):
        """Test : ajout d'un bus aller."""
        evenement.ajouter_bus(bus_aller)

        assert evenement.bus_aller == bus_aller
        assert evenement.bus_retour is None

    def test_ajouter_bus_retour(self, evenement, bus_retour):
        """Test : ajout d'un bus retour."""
        evenement.ajouter_bus(bus_retour)

        assert evenement.bus_aller is None
        assert evenement.bus_retour == bus_retour


# ==================== TESTS DE REPRÉSENTATION ====================

class TestRepresentation:
    """Tests des méthodes de représentation."""

    def test_resume(self, evenement):
        """Test : méthode resume retourne le format attendu."""
        resume = evenement.resume()

        assert "Festival Rock" in resume
        assert "Rennes" in resume
        assert "0/100" in resume
        assert "25.50€" in resume

    def test_str_representation(self, evenement):
        """Test : __str__ retourne le résumé."""
        assert str(evenement) == evenement.resume()

    def test_repr_representation(self, evenement_valide_data):
        """Test : __repr__ contient les infos essentielles."""
        evenement_valide_data["id_event"] = 42
        evenement = Evenement(**evenement_valide_data)

        repr_str = repr(evenement)
        assert "Evenement #42" in repr_str
        assert "Festival Rock" in repr_str


# ==================== TESTS DE SÉRIALISATION ====================

class TestSerialisation:
    """Tests de conversion dictionnaire/objet."""

    def test_to_dict_complet(self, evenement):
        """Test : conversion complète en dictionnaire."""
        evenement.id_event = 1
        data = evenement.to_dict()

        assert data["id_event"] == 1
        assert data["titre"] == "Festival Rock"
        assert data["lieu"] == "Rennes"
        assert data["capacite_max"] == 100
        assert data["created_by"] == 1
        assert data["tarif"] == "25.50"
        assert data["places_disponibles"] == 100
        assert data["est_complet"] is False
        assert data["taux_remplissage"] == 0.0
        assert data["date_evenement"] is not None
        assert data["created_at"] is not None

    def test_to_dict_date_format(self, evenement):
        """Test : les dates sont au format ISO dans to_dict."""
        data = evenement.to_dict()

        # Vérification du format ISO (YYYY-MM-DD)
        assert len(data["date_evenement"]) == 10
        assert data["date_evenement"].count("-") == 2

        # Format datetime ISO
        assert "T" in data["created_at"]
        assert ":" in data["created_at"]

    def test_from_dict_creation(self):
        """Test : création d'un événement depuis un dictionnaire."""
        data = {
            "id_event": 5,
            "titre": "Concert Jazz",
            "description_evenement": "Soirée jazz",
            "lieu": "Paris",
            "date_evenement": "2025-12-25",
            "capacite_max": 50,
            "created_by": 2,
            "created_at": "2025-10-21T10:00:00",
            "tarif": 15.00
        }

        evenement = Evenement.from_dict(data)

        assert evenement.id_event == 5
        assert evenement.titre == "Concert Jazz"
        assert evenement.lieu == "Paris"
        assert evenement.capacite_max == 50
        assert evenement.created_by == 2
        assert evenement.tarif == Decimal("15.00")
        assert isinstance(evenement.date_evenement, date)
        assert isinstance(evenement.created_at, datetime)

    def test_from_dict_avec_date_objet(self):
        """Test : from_dict accepte aussi des objets date."""
        data = {
            "titre": "Test",
            "lieu": "Lyon",
            "date_evenement": date(2025, 12, 25),
            "capacite_max": 30,
            "created_by": 1,
            "created_at": datetime.now(),
            "tarif": 10.00
        }

        evenement = Evenement.from_dict(data)
        assert isinstance(evenement.date_evenement, date)
        assert isinstance(evenement.created_at, datetime)

    def test_cycle_complet_dict(self, evenement):
        """Test : conversion objet → dict → objet préserve les données."""
        evenement.id_event = 10

        # Objet → Dict
        data = evenement.to_dict()

        # Dict → Objet
        evenement_reconstruit = Evenement.from_dict(data)

        # Vérifications
        assert evenement.id_event == evenement_reconstruit.id_event
        assert evenement.titre == evenement_reconstruit.titre
        assert evenement.lieu == evenement_reconstruit.lieu
        assert evenement.capacite_max == evenement_reconstruit.capacite_max
        assert evenement.created_by == evenement_reconstruit.created_by


# ==================== TESTS DES RELATIONS ====================

class TestRelations:
    """Tests des relations avec autres entités."""

    def test_initialisation_relations(self, evenement):
        """Test : les relations sont initialisées correctement."""
        assert evenement.inscriptions == []
        assert evenement.bus_aller is None
        assert evenement.bus_retour is None
        assert evenement.createur is None

    def test_get_participants_liste_vide(self, evenement):
        """Test : get_participants retourne liste vide si pas d'inscriptions."""
        participants = evenement.get_participants()
        assert participants == []


# ==================== TESTS DES INSCRIPTIONS ====================

class TestInscriptions:
    """Tests des méthodes d'inscription et désinscription."""

    def test_inscrire_utilisateur_succes(self, evenement_avec_id, mock_utilisateur, capsys):
        """Test : inscription réussie d'un utilisateur."""
        resultat = evenement_avec_id.inscrire(
            utilisateur=mock_utilisateur,
            boit=True,
            mode_paiement="CB"
        )

        assert resultat is True
        assert len(evenement_avec_id.inscriptions) == 1
        captured = capsys.readouterr()
        assert "inscrit à Festival Rock" in captured.out

    def test_inscrire_utilisateur_deja_inscrit(self, evenement_avec_id, mock_utilisateur, capsys):
        """Test : impossible d'inscrire un utilisateur déjà inscrit."""
        evenement_avec_id.inscrire(mock_utilisateur, boit=False, mode_paiement="CB")
        resultat = evenement_avec_id.inscrire(mock_utilisateur, boit=True, mode_paiement="CB")

        assert resultat is False
        assert len(evenement_avec_id.inscriptions) == 1
        captured = capsys.readouterr()
        assert "déjà inscrit" in captured.out

    def test_inscrire_evenement_complet(self, evenement_valide_data, mock_utilisateur, mock_utilisateur2, capsys):
        """Test : impossible d'inscrire si événement complet."""
        evenement_valide_data["capacite_max"] = 1
        evenement = Evenement(**evenement_valide_data)
        evenement.id_event = 1

        evenement.inscrire(mock_utilisateur, boit=False, mode_paiement="CB")
        resultat = evenement.inscrire(mock_utilisateur2, boit=False, mode_paiement="CB")

        assert resultat is False
        assert len(evenement.inscriptions) == 1
        captured = capsys.readouterr()
        assert "Capacité maximale" in captured.out

    def test_desinscrire_utilisateur_succes(self, evenement_avec_id, mock_utilisateur, capsys):
        """Test : désinscription réussie d'un utilisateur."""
        evenement_avec_id.inscrire(mock_utilisateur, boit=False, mode_paiement="CB")
        resultat = evenement_avec_id.desinscrire(mock_utilisateur)

        assert resultat is True
        assert len(evenement_avec_id.inscriptions) == 0
        captured = capsys.readouterr()
        assert "désinscrit" in captured.out

    def test_desinscrire_utilisateur_non_inscrit(self, evenement_avec_id, mock_utilisateur, capsys):
        """Test : impossible de désinscrire un utilisateur non inscrit."""
        resultat = evenement_avec_id.desinscrire(mock_utilisateur)

        assert resultat is False
        captured = capsys.readouterr()
        assert "n'est pas inscrit" in captured.out

    def test_inscrire_avec_bus(self, evenement_avec_id, mock_utilisateur):
        """Test : inscription avec bus aller et retour."""
        resultat = evenement_avec_id.inscrire(
            mock_utilisateur, 
            boit=True, 
            mode_paiement="CB",
            id_bus_aller=1,
            id_bus_retour=2
        )

        assert resultat is True
        assert len(evenement_avec_id.inscriptions) == 1