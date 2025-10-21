import pytest
from unittest.mock import Mock, patch
from admin import Admin
from utilisateur import Utilisateur
from evenement import Evenement


@pytest.fixture
def admin_instance():
    return Admin(
        id_utilisateur=1234,
        pseudo="abc",
        nom="truc",
        prenom="much",
        email="truc.much@mail.fr",
        mdp="9876"
    )


@pytest.fixture
def participant_instance():
    return Utilisateur(
        id_utilisateur=2345,
        pseudo="utilisateur_a_retirer",
        nom="Martin",
        prenom="Jean",
        email="jean.martin@mail.com",
        mdp="0000"
    )


@pytest.fixture
def autre_participant():
    return Utilisateur(
        id_utilisateur=3456,
        pseudo="utilisateur_temoin",
        nom="Dupont",
        prenom="Martine",
        email="martine.dupont@test.com",
        mdp="9999"
    )

class TestAdmin:

    def test_admin_init(self, admin_instance):
        """ Vérifie la bonne création d'un administrateur"""
        assert isinstance(admin_instance, Admin)
        assert isinstance(admin_instance, Utilisateur)
        assert admin_instance.id_utilisateur == 1234
        assert admin_instance.pseudo == "abc"
        assert admin_instance.nom == "truc"
        assert admin_instance.prenom == "much"
        assert admin_instance.email == "truc.much@mail.fr"
        assert admin_instance.mdp == "9876"

@patch("admin.Evenement")
    def test_creer_evenement(self, MockEvenement, admin_instance):
        """ Vérifie la bonne création d'un évènement par un administrateur"""
        evenement = admin_instance.creer_evenement(
            id_event=1,
            date_event="2025-10-20",
            titre="fête de fin de projet info",
            description="c'est fini",
            lieu="foyer"
            capacite_max=4,
            tarif=3.00
        )

        """vérification de l'appel correct des arguments de evenement"""
        MockEvenement.assert_called_once_with(
            id_event=1,
            date_event="2025-10-20",
            titre="fête de fin de projet info",
            description="c'est fini",
            lieu="foyer",
            capacite_max=4,
            tarif=3.00
        )

        """vérification du bon résultat de la fonction"""

        assert evenement is MockEvenement.return_value

    def test_supp_participant_succes(self, admin_instance, participant_instance, participant_temoin):
        """vérification de la suppression d'un participant inscrit sans supprimer l'autre"""
        mock_evenement = Mock() # initialisation de l'evenement (mock)
        mock_evenement.participants = [participant_instance, participant_temoin]

        resultat = admin_instance.supp_participant(mock_evenement, participant_instance)

        assert resultat is True # vérifie le retour du Mock

        mock_evenement.participants.remove.assert_called_once_with(participant_instance) # vérifie l'état final de la liste des participants

#    def test_supp_participant_echec(self, admin_instance, participant_instance, participant_temoin):
#        """ vérification de l'échec de la suppression d'un participant non inscrit """
        
