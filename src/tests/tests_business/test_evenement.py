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
        description_event="Grande soirée de fin d'année",
        lieu="Château de Versailles",
        date_event=date(2025, 12, 31),
        capacite_max=200,
        created_by=1,
        tarif=50.00
    )
    
    # Assert
    assert evenement.titre == "Soirée Gala"
    assert evenement.lieu == "Château de Versailles"
    assert evenement.capacite_max == 200
    assert evenement.tarif == Decimal('50.00')
    assert evenement.statut == "en_cours"


def test_evenement_titre_vide_erreur():
    """
    Test de validation : un titre vide doit lever une ValueError.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="Le titre ne peut pas être vide"):
        Evenement(
            titre="",
            lieu="Salle A",
            date_event=date(2025, 11, 15),
            capacite_max=50,
            created_by=1
        )


def test_evenement_titre_espaces_vides():
    """
    Test : un titre contenant uniquement des espaces doit lever une ValueError.
    """
    with pytest.raises(ValueError, match="Le titre ne peut pas être vide"):
        Evenement(
            titre="   ",
            lieu="Salle A",
            date_event=date(2025, 11, 15),
            capacite_max=50,
            created_by=1
        )


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
            date_event=date(2025, 12, 15),
            capacite_max=50,
            created_by=1
        )
    
    # Test 2: Titre trop long (> 100 caractères)
    with pytest.raises(ValueError, match="Le titre ne peut pas dépasser 100 caractères"):
        Evenement(
            titre="A" * 101,
            lieu="Salle A",
            date_event=date(2025, 12, 15),
            capacite_max=50,
            created_by=1
        )
    
    # Test 3: Lieu vide
    with pytest.raises(ValueError, match="Le lieu ne peut pas être vide"):
        Evenement(
            titre="Concert",
            lieu="",
            date_event=date(2025, 12, 15),
            capacite_max=50,
            created_by=1
        )
    
    # Test 4: Lieu trop long
    with pytest.raises(ValueError, match="Le lieu ne peut pas dépasser 100 caractères"):
        Evenement(
            titre="Concert",
            lieu="B" * 101,
            date_event=date(2025, 12, 15),
            capacite_max=50,
            created_by=1
        )
    
    # Test 5: Date None
    with pytest.raises(ValueError, match="La date de l'événement est obligatoire"):
        Evenement(
            titre="Concert",
            lieu="Salle A",
            date_event=None,
            capacite_max=50,
            created_by=1
        )
    
    # Test 6: Date invalide (pas un objet date)
    with pytest.raises(ValueError, match="La date de l'événement doit être un objet date"):
        Evenement(
            titre="Concert",
            lieu="Salle A",
            date_event="2025-12-15",
            capacite_max=50,
            created_by=1
        )
    
    # Test 7: Capacité <= 0
    with pytest.raises(ValueError, match="La capacité maximale doit être supérieure à 0"):
        Evenement(
            titre="Concert",
            lieu="Salle A",
            date_event=date(2025, 12, 15),
            capacite_max=0,
            created_by=1
        )
    
    # Test 8: Capacité non entier
    with pytest.raises(ValueError, match="La capacité maximale doit être un entier"):
        Evenement(
            titre="Concert",
            lieu="Salle A",
            date_event=date(2025, 12, 15),
            capacite_max=50.5,
            created_by=1
        )
    
    # Test 9: created_by None
    with pytest.raises(ValueError, match="L'ID du créateur est obligatoire"):
        Evenement(
            titre="Concert",
            lieu="Salle A",
            date_event=date(2025, 12, 15),
            capacite_max=50,
            created_by=None
        )
    
    # Test 10: created_by négatif
    with pytest.raises(ValueError, match="L'ID du créateur doit être un entier positif"):
        Evenement(
            titre="Concert",
            lieu="Salle A",
            date_event=date(2025, 12, 15),
            capacite_max=50,
            created_by=-1
        )
    
    # Test 11: Tarif négatif
    with pytest.raises(ValueError, match="Le tarif ne peut pas être négatif"):
        Evenement(
            titre="Concert",
            lieu="Salle A",
            date_event=date(2025, 12, 15),
            capacite_max=50,
            created_by=1,
            tarif=-10.0
        )

    # Test 12: Statut invalide
    with pytest.raises(ValueError, match="le satut doit être en_cours, passe ou complet"):
        Evenement(
            titre="Concert",
            lieu="Salle A",
            date_event=date(2025, 12, 15),
            capacite_max=50,
            created_by=1,
            statut="invalide"
        )


def test_to_dict_complet():
    """
    Test de la méthode to_dict avec toutes les propriétés.
    Vérifie que toutes les données sont correctement sérialisées.
    """
    # Arrange
    now = datetime.now()
    evenement = Evenement(
        id_event=42,
        titre="Festival de Jazz",
        description_event="Un super festival",
        lieu="Parc de la ville",
        date_event=date(2025, 7, 14),
        capacite_max=200,
        created_by=5,
        tarif=25.50,
        created_at=now
    )
    
    # Act
    resultat = evenement.to_dict()
    
    # Assert
    assert resultat["id_event"] == 42
    assert resultat["titre"] == "Festival de Jazz"
    assert resultat["description_event"] == "Un super festival"
    assert resultat["lieu"] == "Parc de la ville"
    assert resultat["date_event"] == "2025-07-14"
    assert resultat["capacite_max"] == 200
    assert resultat["created_by"] == 5
    assert resultat["tarif"] == "25.50"
    assert resultat["statut"] == "en_cours"
    assert "created_at" in resultat

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
        date_event=date(2025, 5, 20),
        capacite_max=500,
        created_by=10,
        tarif=35.00
    )
    
    # Test __repr__ (représentation technique)
    repr_result = repr(evenement)
    assert repr_result == "<Evenement #123 - Marathon 2025 (2025-05-20 à Centre-ville)>"
    
    # Test __str__ (représentation lisible)
    str_result = str(evenement)
    assert "Marathon 2025" in str_result
    assert "2025-05-20" in str_result
    assert "Centre-ville" in str_result
    assert "35.00€" in str_result


def test_tarif_quantize():
    """
    Test que le tarif est correctement quantifié avec 2 décimales.
    """
    # Test avec tarif float
    evenement1 = Evenement(
        titre="Concert",
        lieu="Salle",
        date_event=date(2025, 12, 1),
        capacite_max=100,
        created_by=1,
        tarif=25.5
    )
    assert evenement1.tarif == Decimal('25.50')
    
    # Test avec tarif string (depuis from_dict)
    evenement2 = Evenement(
        titre="Concert",
        lieu="Salle",
        date_event=date(2025, 12, 1),
        capacite_max=100,
        created_by=1,
        tarif="15.9"
    )
    assert evenement2.tarif == Decimal('15.90')
    
    # Test tarif par défaut
    evenement3 = Evenement(
        titre="Concert",
        lieu="Salle",
        date_event=date(2025, 12, 1),
        capacite_max=100,
        created_by=1
    )
    assert evenement3.tarif == Decimal('0.00')


def test_statut_default():
    """
    Test que le statut par défaut est 'en_cours'.
    """
    evenement = Evenement(
        titre="Event",
        lieu="Lieu",
        date_event=date(2025, 12, 1),
        capacite_max=50,
        created_by=1
    )
    assert evenement.statut == "en_cours"


def test_statut_custom():
    """
    Test la création avec un statut personnalisé valide.
    """
    for statut in ["en_cours", "passe", "complet"]:
        evenement = Evenement(
            titre="Event",
            lieu="Lieu",
            date_event=date(2025, 12, 1),
            capacite_max=50,
            created_by=1,
            statut=statut
        )
        assert evenement.statut == statut


def test_created_at_auto():
    """
    Test que created_at est automatiquement défini à la date/heure actuelle.
    """
    before = datetime.now()
    evenement = Evenement(
        titre="Event",
        lieu="Lieu",
        date_event=date(2025, 12, 1),
        capacite_max=50,
        created_by=1
    )
    after = datetime.now()
    
    assert before <= evenement.created_at <= after


def test_created_by_zero():
    """
    Test que created_by = 0 est rejeté (doit être positif).
    """
    with pytest.raises(ValueError, match="L'ID du créateur doit être un entier positif"):
        Evenement(
            titre="Event",
            lieu="Lieu",
            date_event=date(2025, 12, 1),
            capacite_max=50,
            created_by=0
        )


def test_lieu_espaces_vides():
    """
    Test : un lieu contenant uniquement des espaces doit lever une ValueError.
    """
    with pytest.raises(ValueError, match="Le lieu ne peut pas être vide"):
        Evenement(
            titre="Concert",
            lieu="   ",
            date_event=date(2025, 12, 15),
            capacite_max=50,
            created_by=1
        )