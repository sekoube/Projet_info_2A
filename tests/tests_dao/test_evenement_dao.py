import pytest
from business_object.utilisateur import Utilisateur
from dao.evenement_dao import EvenementDAO
from dao.db_connection import DBConnection

from datetime import date, datetime
from Projet_info_2A.src.dao.evenement_dao import EvenementDao
from Projet_info_2A.src.business_object.evenement import Evenement


def test_creer_evenement_succes():
    """
    Test de création d'un événement valide.
    Vérifie que l'événement est bien créé et qu'un ID est attribué.
    """
    # Arrange
    dao = EvenementDao()
    evenement = Evenement(
        titre="Concert de Jazz",
        description_evenement="Soirée jazz avec musiciens locaux",
        lieu="Salle des fêtes",
        date_evenement=date(2025, 12, 15),
        capacite_max=100,
        created_by=1,
        tarif=15.50
    )
    
    # Act
    resultat = dao.creer(evenement)
    
    # Assert
    assert resultat is True
    assert evenement.id_event is not None
    assert evenement.id_event > 0


def test_get_by_id_existant():
    """
    Test de récupération d'un événement existant par son ID.
    Vérifie que toutes les données sont correctement récupérées.
    """
    # Arrange
    dao = EvenementDao()
    # D'abord créer un événement
    evenement_initial = Evenement(
        titre="Conférence Python",
        description_evenement="Introduction à Python pour débutants",
        lieu="Amphithéâtre B",
        date_evenement=date(2025, 11, 20),
        capacite_max=50,
        created_by=2,
        tarif=0.00
    )
    dao.creer(evenement_initial)
    id_cree = evenement_initial.id_event
    
    # Act
    evenement_recupere = dao.get_by_id(id_cree)
    
    # Assert
    assert evenement_recupere is not None
    assert evenement_recupere.id_event == id_cree
    assert evenement_recupere.titre == "Conférence Python"
    assert evenement_recupere.lieu == "Amphithéâtre B"
    assert evenement_recupere.capacite_max == 50
    assert float(evenement_recupere.tarif) == 0.00


def test_lister_futurs_evenements():
    """
    Test de récupération des événements futurs uniquement.
    Vérifie que seuls les événements avec date >= aujourd'hui sont retournés.
    """
    # Arrange
    dao = EvenementDao()
    date_future = date(2026, 6, 1)
    date_passee = date(2024, 1, 1)
    
    # Créer un événement futur
    evt_futur = Evenement(
        titre="Événement Futur",
        lieu="Lieu A",
        date_evenement=date_future,
        capacite_max=30,
        created_by=1,
        tarif=10.00
    )
    dao.creer(evt_futur)
    
    # Créer un événement passé
    evt_passe = Evenement(
        titre="Événement Passé",
        lieu="Lieu B",
        date_evenement=date_passee,
        capacite_max=20,
        created_by=1,
        tarif=5.00
    )
    dao.creer(evt_passe)
    
    # Act
    evenements_futurs = dao.lister_futurs()
    
    # Assert
    assert len(evenements_futurs) > 0
    # Vérifier que tous les événements retournés sont futurs
    for evt in evenements_futurs:
        assert evt.date_evenement >= date.today()
    # Vérifier que l'événement futur est dans la liste
    titres = [evt.titre for evt in evenements_futurs]
    assert "Événement Futur" in titres