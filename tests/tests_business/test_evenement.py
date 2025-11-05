from Projet_info_2A.src.business_object.evenement import Evenement
from datetime import date, datetime


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