import pytest
from datetime import datetime, date, timedelta
from business_object.bus import Bus
from business_object.utilisateur import Utilisateur
from business_object.evenement import Evenement
from dao.bus_dao import BusDAO
from dao.evenement_dao import EvenementDAO
from dao.utilisateur_dao import UtilisateurDAO
from service.bus_service import BusService


class TestIntegrationBus:
    """
    Tests d'intégration pour le module Bus.
    Ces tests vérifient l'interaction entre Service, DAO et la base de données.
    Utilise les fixtures de conftest.py pour la configuration.
    """

    @pytest.fixture(autouse=True)
    def setup(self, utilisateur_test, evenement_test):
        """
        Configuration automatique avant chaque test.
        Utilise les fixtures conftest pour créer utilisateur et événement.
        """
        # Initialiser les DAO et Services
        self.bus_dao = BusDAO()
        self.evenement_dao = EvenementDAO()
        self.utilisateur_dao = UtilisateurDAO()
        self.bus_service = BusService()
        
        # Utiliser les fixtures
        self.test_user = utilisateur_test
        self.test_event = evenement_test


    def test_creer_bus_complet(self):
        """
        Test 1 : Création d'un bus complet avec tous les champs.
        Vérifie que le bus est bien créé en base avec un id_bus généré.
        """
        
        # Créer un bus via le service
        bus = self.bus_service.creer_bus(
            id_event=self.test_event.id_event,
            sens="aller",
            description="Départ Gare Montparnasse - Arrêt Place de la République",
            heure_depart="08:30",
            capacite_max=50
        )
        
        # Assertions
        assert bus is not None, "Le bus devrait être créé"
        assert bus.id_bus is not None, "Un id_bus devrait être généré"
        assert bus.sens == "ALLER", "Le sens devrait être normalisé en majuscules"
        assert bus.id_event == self.test_event.id_event
        assert bus.capacite_max == 50
        assert bus.description == "Départ Gare Montparnasse - Arrêt Place de la République"
        
        print(f"✅ Bus créé avec succès")
        print(f"   ID Bus : {bus.id_bus}")
        print(f"   Sens : {bus.sens}")
        print(f"   Heure départ : {bus.heure_depart.strftime('%H:%M')}")
        print(f"   Capacité : {bus.capacite_max} places")


    def test_creer_plusieurs_bus_et_lister(self):
        """
        Test 2 : Création de plusieurs bus (aller et retour) et listage complet.
        Vérifie que tous les bus sont bien récupérés.
        """
        
        # Créer plusieurs bus
        bus_crees = []
        
        # Bus aller
        bus_aller = self.bus_service.creer_bus(
            id_event=self.test_event.id_event,
            sens="aller",
            description="Bus aller - Départ Paris",
            heure_depart="09:00",
            capacite_max=45
        )
        bus_crees.append(bus_aller)
        
        # Bus retour
        bus_retour = self.bus_service.creer_bus(
            id_event=self.test_event.id_event,
            sens="retour",
            description="Bus retour - Retour Paris",
            heure_depart="23:00",
            capacite_max=45
        )
        bus_crees.append(bus_retour)
        
        # Bus aller supplémentaire
        bus_aller_2 = self.bus_service.creer_bus(
            id_event=self.test_event.id_event,
            sens="ALLER",
            description="Bus aller 2 - Départ Province",
            heure_depart="10:30",
            capacite_max=30
        )
        bus_crees.append(bus_aller_2)
        
        # Lister tous les bus
        tous_les_bus = self.bus_service.get_tous_les_bus()
        
        # Assertions
        assert len(tous_les_bus) >= 3, "Au moins 3 bus devraient exister"
        
        # Vérifier que nos bus sont dans la liste
        ids_crees = [bus.id_bus for bus in bus_crees]
        ids_listes = [bus.id_bus for bus in tous_les_bus]
        
        for id_bus in ids_crees:
            assert id_bus in ids_listes, f"Le bus {id_bus} devrait être dans la liste"
        
        print(f"✅ {len(tous_les_bus)} bus listés avec succès")
        print(f"   Bus créés : {ids_crees}")


    def test_rechercher_bus_par_id(self):
        """
        Recherche d'un bus par son ID.
        Vérifie que la méthode get_by retourne le bon bus.
        """
        
        # Créer un bus
        bus_original = self.bus_service.creer_bus(
            id_event=self.test_event.id_event,
            sens="retour",
            description="Bus test recherche - Retour festival",
            heure_depart="22:00",
            capacite_max=40
        )
        
        # Rechercher le bus par son ID
        bus_trouves = self.bus_service.get_bus_by("id_bus", bus_original.id_bus)
        
        # Assertions
        assert bus_trouves is not None, "Le bus devrait être trouvé"
        assert len(bus_trouves) == 1, "Un seul bus devrait correspondre"
        
        bus_trouve = bus_trouves[0]
        assert bus_trouve.id_bus == bus_original.id_bus
        assert bus_trouve.sens == "RETOUR"
        assert bus_trouve.capacite_max == 40
        assert bus_trouve.description == "Bus test recherche - Retour festival"
        
        print(f"✅ Bus trouvé")
        print(f"   ID : {bus_trouve.id_bus}")
        print(f"   Sens : {bus_trouve.sens}")
        print(f"   Description : {bus_trouve.description}")
        print(f"   Capacité : {bus_trouve.capacite_max} places")


    def test_rechercher_bus_par_evenement(self):
        """
        Recherche de tous les bus associés à un événement.
        Vérifie que tous les bus d'un événement sont récupérés.
        """
        
        # Créer plusieurs bus pour le même événement
        nb_bus_a_creer = 4
        bus_crees = []
        
        for i in range(nb_bus_a_creer):
            sens = "aller" if i % 2 == 0 else "retour"
            heure = f"{8 + i}:00" if sens == "aller" else f"{20 + i}:00"
            
            bus = self.bus_service.creer_bus(
                id_event=self.test_event.id_event,
                sens=sens,
                description=f"Bus {sens} numéro {i+1}",
                heure_depart=heure,
                capacite_max=35 + (i * 5)
            )
            bus_crees.append(bus)
        
        # Rechercher tous les bus de cet événement
        bus_de_evenement = self.bus_service.get_bus_by("id_event", self.test_event.id_event)
        
        # Assertions
        assert bus_de_evenement is not None, "Des bus devraient être trouvés"
        assert len(bus_de_evenement) >= nb_bus_a_creer, \
            f"Au moins {nb_bus_a_creer} bus devraient être associés à l'événement"
        
        # Vérifier que tous nos bus créés sont dans les résultats
        ids_crees = [bus.id_bus for bus in bus_crees]
        ids_trouves = [bus.id_bus for bus in bus_de_evenement]
        
        for id_bus in ids_crees:
            assert id_bus in ids_trouves, \
                f"Le bus {id_bus} devrait être dans la liste de l'événement"
        
        # Vérifier la répartition aller/retour
        bus_aller = [b for b in bus_de_evenement if b.sens == "ALLER"]
        bus_retour = [b for b in bus_de_evenement if b.sens == "RETOUR"]
        
        print(f"✅ {len(bus_de_evenement)} bus trouvés pour l'événement {self.test_event.titre}")
        print(f"   Bus aller : {len(bus_aller)}")
        print(f"   Bus retour : {len(bus_retour)}")

    def test_suppression_bus(self):
        """
        Suppression d'un bus.
        Vérifie que le bus est bien supprimé de la base.
        """
        
        # Créer un bus
        bus = self.bus_service.creer_bus(
            id_event=self.test_event.id_event,
            sens="aller",
            description="Bus à supprimer",
            heure_depart="07:00",
            capacite_max=25
        )
        
        id_bus = bus.id_bus
        print(f"Bus créé avec l'ID : {id_bus}")
        
        # Vérifier que le bus existe
        bus_avant = self.bus_service.get_bus_by("id_bus", id_bus)
        assert len(bus_avant) == 1, "Le bus devrait exister avant suppression"
        
        # Supprimer le bus
        resultat = self.bus_service.supprimer_bus(id_bus)
        
        # Assertions
        assert resultat is True, "La suppression devrait réussir"
        
        # Vérifier que le bus n'existe plus
        bus_apres = self.bus_service.get_bus_by("id_bus", id_bus)
        assert len(bus_apres) == 0, "Le bus ne devrait plus exister après suppression"
        
        print(f"✅ Bus {id_bus} supprimé avec succès")


    def test_normalisation_sens_bus(self):
        """
        Vérification de la normalisation du sens (aller/retour).
        Vérifie que peu importe la casse, le sens est correctement normalisé.
        """
        
        # Tester différentes variantes de casse
        variantes = [
            ("aller", "ALLER"),
            ("ALLER", "ALLER"),
            ("Aller", "ALLER"),
            ("retour", "RETOUR"),
            ("RETOUR", "RETOUR"),
            ("Retour", "RETOUR")
        ]
        
        bus_crees = []
        
        for sens_input, sens_attendu in variantes:
            bus = self.bus_service.creer_bus(
                id_event=self.test_event.id_event,
                sens=sens_input,
                description=f"Test normalisation : {sens_input}",
                heure_depart="12:00",
                capacite_max=20
            )
            bus_crees.append(bus)
            
            # Vérifier la normalisation
            assert bus.sens == sens_attendu, \
                f"Le sens '{sens_input}' devrait être normalisé en '{sens_attendu}'"
        
        print(f"✅ Normalisation du sens validée pour {len(variantes)} variantes")
        for bus in bus_crees:
            print(f"   '{bus.description}' → sens : {bus.sens}")


if __name__ == "__main__":
    # Pour exécuter les tests directement
    pytest.main([__file__, "-v"])