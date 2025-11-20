import pytest
from datetime import date, timedelta
from unittest.mock import Mock, MagicMock, patch
from service.inscription_service import InscriptionService
from business_object.utilisateur import Utilisateur
from business_object.evenement import Evenement
from business_object.inscription import Inscription
from business_object.bus import Bus


class TestInscriptionService:
    """Tests unitaires pour InscriptionService avec mocks des DAOs"""

    @pytest.fixture
    def mock_daos(self):
        """Crée les mocks des DAOs"""
        return {
            'inscription_dao': Mock(),
            'evenement_dao': Mock(),
            'utilisateur_dao': Mock()
        }

    @pytest.fixture
    def inscription_service(self, mock_daos):
        """Fixture pour créer une instance du service avec les DAOs mockés"""
        return InscriptionService(
            inscription_dao=mock_daos['inscription_dao'],
            evenement_dao=mock_daos['evenement_dao'],
            utilisateur_dao=mock_daos['utilisateur_dao']
        )

    @pytest.fixture
    def utilisateur_valide(self):
        """Crée un utilisateur mock de test valide"""
        user = Mock(spec=Utilisateur)
        user.id_utilisateur = 1
        user.nom = "Test"
        user.prenom = "User"
        user.email = "test@example.com"
        return user

    @pytest.fixture
    def evenement_valide(self, utilisateur_valide):
        """Crée un événement mock de test valide"""
        evt = Mock(spec=Evenement)
        evt.id_event = 1
        evt.titre = "Soirée Test"
        evt.description_event = "Event pour les tests"
        evt.lieu = "Rennes"
        evt.date_event = date.today() + timedelta(days=30)
        evt.capacite_max = 50
        evt.created_by = utilisateur_valide.id_utilisateur
        evt.tarif = 15.0
        return evt

    @pytest.fixture
    def params_inscription_valides(self, utilisateur_valide, evenement_valide):
        """Paramètres valides pour créer une inscription"""
        return {
            "boit": True,
            "created_by": utilisateur_valide.id_utilisateur,
            "mode_paiement": "en ligne",
            "id_event": evenement_valide.id_event,
            "nom_event": evenement_valide.titre,
            "id_bus_aller": 1,
            "id_bus_retour": 2
        }

    # ==================== TESTS : Génération de code ====================

    def test_generer_code_reservation_format(self, inscription_service):
        """
        Test : Le code de réservation a le bon format
        WHEN on génère un code de réservation
        THEN c'est un entier de 8 chiffres
        """
        inscription_service.inscription_dao.get_by.return_value = []

        code = inscription_service.generer_code_reservation()

        assert isinstance(code, int)
        assert 10000000 <= code <= 99999999  # 8 chiffres
        assert len(str(code)) == 8

    def test_generer_code_reservation_unique(self, inscription_service):
        """
        Test : Les codes générés sont uniques
        WHEN on génère plusieurs codes
        THEN ils sont tous différents
        """
        inscription_service.inscription_dao.get_by.return_value = []

        codes = [inscription_service.generer_code_reservation() for _ in range(10)]

        assert len(codes) == len(set(codes))  # Tous uniques

    def test_generer_code_reservation_evite_doublons(self, inscription_service):
        """
        Test : Un code déjà existant est rejeté et on en génère un nouveau
        GIVEN un code déjà utilisé
        WHEN on génère un code
        THEN on n'obtient pas le code existant
        """
        code_existant = 12345678
        inscription_service.inscription_dao.get_by.side_effect = [
            [Mock()],  # Premier appel : le code existe
            [],        # Deuxième appel : le nouveau code n'existe pas
        ]

        code = inscription_service.generer_code_reservation()

        assert code != code_existant
        assert inscription_service.inscription_dao.get_by.call_count == 2

    # ==================== TESTS : Création d'inscription ====================

    def test_creer_inscription_succes(self, inscription_service, mock_daos, 
                                      utilisateur_valide, evenement_valide, 
                                      params_inscription_valides):
        """
        Test : Création d'une inscription valide
        GIVEN tous les paramètres valides
        WHEN on crée une inscription
        THEN l'inscription est créée avec succès
        """
        # Setup
        mock_daos['utilisateur_dao'].get_by.return_value = utilisateur_valide
        mock_daos['evenement_dao'].get_by.return_value = [evenement_valide]
        mock_daos['inscription_dao'].compter_par_evenement.return_value = 0
        mock_daos['inscription_dao'].est_deja_inscrit.return_value = False
        mock_daos['inscription_dao'].get_by.return_value = []
        mock_daos['inscription_dao'].creer.return_value = Inscription(
            code_reservation=12345678,
            boit=True,
            mode_paiement="en ligne",
            id_event=1,
            nom_event="Soirée Test",
            id_bus_aller=1,
            id_bus_retour=2,
            created_by=1
        )

        # Act
        result = inscription_service.creer_inscription(**params_inscription_valides)

        # Assert
        assert result is not None
        assert result.code_reservation == 12345678
        mock_daos['inscription_dao'].creer.assert_called_once()

    def test_creer_inscription_utilisateur_inexistant(self, inscription_service, mock_daos,
                                                       params_inscription_valides):
        """
        Test : Création d'inscription avec un utilisateur inexistant
        GIVEN un ID utilisateur inexistant
        WHEN on crée une inscription
        THEN la création échoue et retourne None
        """
        mock_daos['utilisateur_dao'].get_by.return_value = None

        result = inscription_service.creer_inscription(**params_inscription_valides)

        assert result is None
        mock_daos['inscription_dao'].creer.assert_not_called()

    def test_creer_inscription_evenement_inexistant(self, inscription_service, mock_daos,
                                                     utilisateur_valide, 
                                                     params_inscription_valides):
        """
        Test : Création d'inscription avec un événement inexistant
        GIVEN un ID événement inexistant
        WHEN on crée une inscription
        THEN la création échoue et retourne None
        """
        mock_daos['utilisateur_dao'].get_by.return_value = utilisateur_valide
        mock_daos['evenement_dao'].get_by.return_value = []

        result = inscription_service.creer_inscription(**params_inscription_valides)

        assert result is None
        mock_daos['inscription_dao'].creer.assert_not_called()

    def test_creer_inscription_evenement_complet(self, inscription_service, mock_daos,
                                                  utilisateur_valide, evenement_valide,
                                                  params_inscription_valides):
        """
        Test : Création d'inscription à un événement complet
        GIVEN un événement avec capacité atteinte
        WHEN on crée une inscription
        THEN la création échoue
        """
        mock_daos['utilisateur_dao'].get_by.return_value = utilisateur_valide
        mock_daos['evenement_dao'].get_by.return_value = [evenement_valide]
        mock_daos['inscription_dao'].compter_par_evenement.return_value = 50  # Complet

        result = inscription_service.creer_inscription(**params_inscription_valides)

        assert result is None
        mock_daos['inscription_dao'].creer.assert_not_called()

    def test_creer_inscription_doublon(self, inscription_service, mock_daos,
                                       utilisateur_valide, evenement_valide,
                                       params_inscription_valides):
        """
        Test : Tentative de double inscription
        GIVEN un utilisateur déjà inscrit à l'événement
        WHEN on crée une nouvelle inscription
        THEN la création échoue
        """
        mock_daos['utilisateur_dao'].get_by.return_value = utilisateur_valide
        mock_daos['evenement_dao'].get_by.return_value = [evenement_valide]
        mock_daos['inscription_dao'].compter_par_evenement.return_value = 0
        mock_daos['inscription_dao'].est_deja_inscrit.return_value = True  # Déjà inscrit

        result = inscription_service.creer_inscription(**params_inscription_valides)

        assert result is None
        mock_daos['inscription_dao'].creer.assert_not_called()

    # ==================== TESTS : Suppression d'inscription ====================

    def test_supprimer_inscription_succes(self, inscription_service, mock_daos):
        """
        Test : Suppression d'une inscription valide
        GIVEN une inscription existante créée par l'utilisateur
        WHEN on la supprime
        THEN elle est supprimée
        """
        inscription = Inscription(
            code_reservation=12345678,
            boit=True,
            mode_paiement="en ligne",
            id_event=1,
            nom_event="Event",
            id_bus_aller=1,
            id_bus_retour=2,
            created_by=1
        )
        inscription_service.inscription_dao.get_by.return_value = [inscription]
        inscription_service.inscription_dao.supprimer.return_value = True

        result = inscription_service.supprimer_inscription("12345678", 1)

        assert result is True
        inscription_service.inscription_dao.supprimer.assert_called_once()

    def test_supprimer_inscription_non_existante(self, inscription_service, mock_daos):
        """
        Test : Suppression d'une inscription inexistante
        GIVEN un code de réservation inexistant
        WHEN on tente de la supprimer
        THEN une ValueError est levée
        """
        mock_daos['inscription_dao'].get_by.return_value = []

        with pytest.raises(ValueError, match="Aucune inscription trouvée"):
            inscription_service.supprimer_inscription("99999999", 1)

    def test_supprimer_inscription_pas_proprietaire(self, inscription_service, mock_daos):
        """
        Test : Suppression d'une inscription par un utilisateur qui ne l'a pas créée
        GIVEN une inscription créée par utilisateur A
        WHEN utilisateur B tente de la supprimer
        THEN une PermissionError est levée
        """
        inscription = Inscription(
            code_reservation=12345678,
            boit=True,
            mode_paiement="en ligne",
            id_event=1,
            nom_event="Event",
            id_bus_aller=1,
            id_bus_retour=2,
            created_by=1  # Créée par utilisateur 1
        )
        mock_daos['inscription_dao'].get_by.return_value = [inscription]

        with pytest.raises(PermissionError, match="ne pouvez supprimer"):
            inscription_service.supprimer_inscription("12345678", 2)  # Tentée par utilisateur 2

    def test_supprimer_inscription_code_vide(self, inscription_service, mock_daos):
        """
        Test : Suppression avec un code vide
        GIVEN un code de réservation vide
        WHEN on tente de supprimer
        THEN une ValueError est levée
        """
        with pytest.raises(ValueError, match="code de réservation valide"):
            inscription_service.supprimer_inscription("", 1)

    # ==================== TESTS : Récupération d'inscriptions ====================

    def test_lister_toutes_inscriptions(self, inscription_service, mock_daos):
        """
        Test : Listage de toutes les inscriptions
        WHEN on liste toutes les inscriptions
        THEN on obtient la liste du DAO
        """
        inscriptions_mock = [
            Mock(code_reservation=111),
            Mock(code_reservation=222),
            Mock(code_reservation=333),
        ]
        inscription_service.inscription_dao.lister_toutes.return_value = inscriptions_mock

        result = inscription_service.lister_toutes_inscriptions()

        assert len(result) == 3
        assert result == inscriptions_mock

    def test_get_inscription_by_valide(self, inscription_service, mock_daos):
        """
        Test : Récupération d'une inscription par champ
        GIVEN un champ et une valeur valides
        WHEN on récupère l'inscription
        THEN on obtient l'inscription
        """
        inscription_mock = Mock(code_reservation=12345678)
        inscription_service.inscription_dao.get_by.return_value = inscription_mock

        result = inscription_service.get_inscription_by("code_reservation", 12345678)

        assert result == inscription_mock
        inscription_service.inscription_dao.get_by.assert_called_once_with(
            "code_reservation", 12345678
        )

    def test_get_inscription_by_champ_invalide(self, inscription_service, mock_daos):
        """
        Test : Récupération avec un champ invalide
        GIVEN un champ non autorisé
        WHEN on récupère
        THEN une ValueError est levée par le DAO
        """
        inscription_service.inscription_dao.get_by.side_effect = ValueError("Colonne non autorisée")

        with pytest.raises(ValueError):
            inscription_service.get_inscription_by("champ_invalide", "valeur")