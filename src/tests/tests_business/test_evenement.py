from business_object.evenement import Evenement
from datetime import date, datetime
from decimal import Decimal
import pytest


def test_creation_evenement_valide():
    """
    Test de création d'un événement avec des données valides.
    Vérifie que tous les attributs sont correctement initialisés.
    """
    # Arrange & Act
    evenement = Evenement(
        titre="Soirée Gala",
        description_evenement="Grande soirée de fin d'année",
        lieu="Château de Versailles",
        date_evenement=date(2025, 12, 31),
        capacite_max=200,
        created_by=1,
        tarif=50.00
    )
    
    # Assert
    assert evenement.titre == "Soirée Gala"
    assert evenement.lieu == "Château de Versailles"
    assert evenement.capacite_max == 200
    assert float(evenement.tarif) == 50.00
    assert evenement.inscriptions == []


def test_evenement_titre_vide_erreur():
    """
    Test de validation : un titre vide doit lever une ValueError.
    """
    # Act & Assert
    try:
        evenement = Evenement(
            titre="",
            lieu="Salle A",
            date_evenement=date(2025, 11, 15),
            capacite_max=50,
            created_by=1
        )
        assert False, "Une ValueError aurait dû être levée"
    except ValueError as e:
        assert "titre ne peut pas être vide" in str(e)


def test_places_disponibles_calcul():
    """
    Test du calcul des places disponibles.
    Vérifie que le nombre de places diminue avec les inscriptions.
    """
    # Arrange
    evenement = Evenement(
        titre="Workshop Python",
        lieu="Lab Info",
        date_evenement=date(2025, 11, 20),
        capacite_max=30,
        created_by=1
    )
    
    # Act - Simuler des inscriptions
    class InscriptionMock:
        pass
    
    evenement.inscriptions = [InscriptionMock() for _ in range(10)]
    
    # Assert
    assert evenement.places_disponibles() == 20
    assert evenement.est_complet() is False


def test_evenement_complet():
    """
    Test de vérification qu'un événement est complet.
    Vérifie le comportement quand capacité maximale est atteinte.
    """
    # Arrange
    evenement = Evenement(
        titre="Atelier Photo",
        lieu="Studio",
        date_evenement=date(2025, 12, 1),
        capacite_max=5,
        created_by=1
    )
    
    # Act - Remplir complètement l'événement
    class InscriptionMock:
        pass
    
    evenement.inscriptions = [InscriptionMock() for _ in range(5)]
    
    # Assert
    assert evenement.est_complet() is True
    assert evenement.places_disponibles() == 0
    assert evenement.taux_remplissage() == 100.0


def test_evenement_passe():
    """
    Test de vérification qu'un événement est passé.
    Compare la date de l'événement avec la date actuelle.
    """
    # Arrange
    evenement_passe = Evenement(
        titre="Événement Historique",
        lieu="Musée",
        date_evenement=date(2020, 1, 1),
        capacite_max=100,
        created_by=1
    )
    
    evenement_futur = Evenement(
        titre="Événement à Venir",
        lieu="Centre",
        date_evenement=date(2026, 12, 31),
        capacite_max=100,
        created_by=1
    )
    
    # Act & Assert
    assert evenement_passe.est_passe() is True
    assert evenement_futur.est_passe() is False

def test_evenement_validations_erreurs_multiples():
    """
    Test des différentes validations avec messages d'erreur.
    Vérifie que chaque validation lève la bonne exception.
    """
    
    # Test 1: Titre vide
    with pytest.raises(ValueError, match="Le titre ne peut pas être vide"):
        Evenement(
            titre="",
            lieu="Salle A",
            date_evenement=date(2025, 12, 15),
            capacite_max=50,
            created_by=1
        )
    
    # Test 2: Titre trop long (> 100 caractères)
    with pytest.raises(ValueError, match="Le titre ne peut pas dépasser 100 caractères"):
        Evenement(
            titre="A" * 101,
            lieu="Salle A",
            date_evenement=date(2025, 12, 15),
            capacite_max=50,
            created_by=1
        )
    
    # Test 3: Lieu vide
    with pytest.raises(ValueError, match="Le lieu ne peut pas être vide"):
        Evenement(
            titre="Concert",
            lieu="",
            date_evenement=date(2025, 12, 15),
            capacite_max=50,
            created_by=1
        )
    
    # Test 4: Lieu trop long
    with pytest.raises(ValueError, match="Le lieu ne peut pas dépasser 100 caractères"):
        Evenement(
            titre="Concert",
            lieu="B" * 101,
            date_evenement=date(2025, 12, 15),
            capacite_max=50,
            created_by=1
        )
    
    # Test 5: Date None
    with pytest.raises(ValueError, match="La date de l'événement est obligatoire"):
        Evenement(
            titre="Concert",
            lieu="Salle A",
            date_evenement=None,
            capacite_max=50,
            created_by=1
        )
    
    # Test 6: Date invalide (pas un objet date)
    with pytest.raises(ValueError, match="La date de l'événement doit être un objet date"):
        Evenement(
            titre="Concert",
            lieu="Salle A",
            date_evenement="2025-12-15",  # String au lieu de date
            capacite_max=50,
            created_by=1
        )
    
    # Test 7: Capacité <= 0
    with pytest.raises(ValueError, match="La capacité maximale doit être supérieure à 0"):
        Evenement(
            titre="Concert",
            lieu="Salle A",
            date_evenement=date(2025, 12, 15),
            capacite_max=0,
            created_by=1
        )
    
    # Test 8: Capacité non entier
    with pytest.raises(ValueError, match="La capacité maximale doit être un entier"):
        Evenement(
            titre="Concert",
            lieu="Salle A",
            date_evenement=date(2025, 12, 15),
            capacite_max=50.5,  # Float au lieu d'int
            created_by=1
        )
    
    # Test 9: created_by None
    with pytest.raises(ValueError, match="L'ID du créateur est obligatoire"):
        Evenement(
            titre="Concert",
            lieu="Salle A",
            date_evenement=date(2025, 12, 15),
            capacite_max=50,
            created_by=None
        )
    
    # Test 10: created_by négatif
    with pytest.raises(ValueError, match="L'ID du créateur doit être un entier positif"):
        Evenement(
            titre="Concert",
            lieu="Salle A",
            date_evenement=date(2025, 12, 15),
            capacite_max=50,
            created_by=-1
        )
    
    # Test 11: Tarif négatif
    with pytest.raises(ValueError, match="Le tarif ne peut pas être négatif"):
        Evenement(
            titre="Concert",
            lieu="Salle A",
            date_evenement=date(2025, 12, 15),
            capacite_max=50,
            created_by=1,
            tarif=-10.0
        )


def test_to_dict_complet():
    """
    Test de la méthode to_dict avec toutes les propriétés.
    Vérifie que toutes les données sont correctement sérialisées.
    """
    # Arrange
    evenement = Evenement(
        id_event=42,
        titre="Festival de Jazz",
        description_evenement="Un super festival",
        lieu="Parc de la ville",
        date_evenement=date(2025, 7, 14),
        capacite_max=200,
        created_by=5,
        tarif=25.50
    )
    
    # Simuler quelques inscriptions
    evenement.inscriptions = [1, 2, 3]  # 3 inscrits fictifs
    
    # Act
    resultat = evenement.to_dict()
    
    # Assert
    assert resultat["id_event"] == 42
    assert resultat["titre"] == "Festival de Jazz"
    assert resultat["description_evenement"] == "Un super festival"
    assert resultat["lieu"] == "Parc de la ville"
    assert resultat["date_evenement"] == "2025-07-14"
    assert resultat["capacite_max"] == 200
    assert resultat["created_by"] == 5
    assert resultat["tarif"] == "25.50"
    assert resultat["places_disponibles"] == 197  # 200 - 3
    assert resultat["est_complet"] is False
    assert resultat["taux_remplissage"] == 1.5  # (3/200)*100
    assert "created_at" in resultat


def test_from_dict_avec_dates_invalides():
    """
    Test de from_dict avec conversion de dates depuis des strings.
    Vérifie que les dates ISO sont correctement converties.
    """
    # Test 1: Dates en format string ISO
    data = {
        "id_event": 10,
        "titre": "Conférence",
        "description_evenement": "Description test",
        "lieu": "Amphithéâtre",
        "date_evenement": "2025-12-01",  # String ISO
        "capacite_max": 100,
        "created_by": 2,
        "created_at": "2024-11-01T10:30:00",  # String ISO avec heure
        "tarif": 15.00
    }
    
    evenement = Evenement.from_dict(data)
    
    assert evenement.id_event == 10
    assert evenement.titre == "Conférence"
    assert evenement.date_evenement == date(2025, 12, 1)
    assert isinstance(evenement.date_evenement, date)
    assert evenement.created_at == datetime(2024, 11, 1, 10, 30, 0)
    assert isinstance(evenement.created_at, datetime)
    assert evenement.tarif == Decimal("15.00")
    
    # Test 2: Dates déjà en format date/datetime
    data2 = {
        "titre": "Atelier",
        "lieu": "Salle B",
        "date_evenement": date(2026, 1, 15),  # Déjà un objet date
        "capacite_max": 30,
        "created_by": 3,
        "created_at": datetime(2024, 12, 1, 14, 0, 0),  # Déjà datetime
        "tarif": "20.50"  # Tarif en string
    }
    
    evenement2 = Evenement.from_dict(data2)
    
    assert evenement2.date_evenement == date(2026, 1, 15)
    assert evenement2.created_at == datetime(2024, 12, 1, 14, 0, 0)
    assert evenement2.tarif == Decimal("20.50")
    
    # Test 3: Valeurs par défaut pour champs optionnels
    data3 = {
        "titre": "Sortie",
        "lieu": "Extérieur",
        "date_evenement": date(2025, 6, 1),
        "capacite_max": 50,
        "created_by": 1
    }
    
    evenement3 = Evenement.from_dict(data3)
    
    assert evenement3.description_evenement == ""
    assert evenement3.id_event is None
    assert evenement3.tarif == Decimal("0.00")


def test_str_et_repr():
    """
    Test des méthodes __str__ et __repr__.
    Vérifie le formatage des représentations textuelles.
    """
    # Arrange
    evenement = Evenement(
        id_event=123,
        titre="Marathon 2025",
        lieu="Centre-ville",
        date_evenement=date(2025, 5, 20),
        capacite_max=500,
        created_by=10,
        tarif=35.00
    )
    
    # Simuler 150 inscrits
    evenement.inscriptions = list(range(150))
    
    # Test __repr__ (représentation technique)
    repr_result = repr(evenement)
    assert repr_result == "<Evenement #123 - Marathon 2025 (2025-05-20 à Centre-ville)>"
    
    # Test __str__ (représentation lisible = resume())
    str_result = str(evenement)
    assert "Marathon 2025" in str_result
    assert "2025-05-20" in str_result
    assert "Centre-ville" in str_result
    assert "150/500" in str_result
    assert "35.00€" in str_result
    
    # Vérifier le format exact
    expected_str = "Marathon 2025 - 2025-05-20 à Centre-ville (150/500 participants) - 35.00€"
    assert str_result == expected_str


def test_taux_remplissage():
    """
    Test du calcul du taux de remplissage.
    Vérifie les pourcentages avec différents scénarios.
    """
    # Test 1: Événement vide
    evenement = Evenement(
        titre="Concert",
        lieu="Salle",
        date_evenement=date(2025, 12, 1),
        capacite_max=100,
        created_by=1
    )
    assert evenement.taux_remplissage() == 0.0
    
    # Test 2: Événement à moitié plein
    evenement.inscriptions = list(range(50))
    assert evenement.taux_remplissage() == 50.0
    
    # Test 3: Événement complet
    evenement.inscriptions = list(range(100))
    assert evenement.taux_remplissage() == 100.0
    
    # Test 4: Capacité 0 (cas limite)
    evenement_zero = Evenement(
        titre="Test",
        lieu="Lieu",
        date_evenement=date(2025, 12, 1),
        capacite_max=1,
        created_by=1
    )
    evenement_zero.capacite_max = 0  # Modifier après création pour tester
    assert evenement_zero.taux_remplissage() == 0.0


def test_resume():
    """
    Test de la méthode resume avec formatage du tarif.
    """
    evenement = Evenement(
        titre="Sortie vélo",
        lieu="Forêt",
        date_evenement=date(2025, 8, 15),
        capacite_max=25,
        created_by=1,
        tarif=12.5  # Devrait être formaté en 12.50
    )
    
    evenement.inscriptions = [1, 2, 3, 4, 5]
    
    resume = evenement.resume()
    
    assert "Sortie vélo" in resume
    assert "2025-08-15" in resume
    assert "Forêt" in resume
    assert "5/25" in resume
    assert "12.50€" in resume  # Vérifier le format avec 2 décimales


def test_ajouter_bus():
    """
    Test de l'ajout de bus (aller/retour).
    """
    from unittest.mock import Mock
    
    evenement = Evenement(
        titre="Excursion",
        lieu="Montagne",
        date_evenement=date(2025, 9, 1),
        capacite_max=40,
        created_by=1
    )
    
    # Mock d'un bus aller
    bus_aller = Mock()
    bus_aller.sens = True
    
    # Mock d'un bus retour
    bus_retour = Mock()
    bus_retour.sens = False
    
    # Test ajout bus aller
    evenement.ajouter_bus(bus_aller)
    assert evenement.bus_aller == bus_aller
    assert evenement.bus_retour is None
    
    # Test ajout bus retour
    evenement.ajouter_bus(bus_retour)
    assert evenement.bus_aller == bus_aller
    assert evenement.bus_retour == bus_retour