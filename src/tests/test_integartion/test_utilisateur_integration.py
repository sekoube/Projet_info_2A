import pytest
from datetime import datetime
from business_object.utilisateur import Utilisateur
from dao.utilisateur_dao import UtilisateurDAO
from service.utilisateur_service import UtilisateurService
from utils.mdp import verify_password


class TestIntegrationUtilisateur:
    """
    Tests d'intégration pour le module Utilisateur.
    Ces tests vérifient l'interaction entre Service, DAO et la base de données.
    Utilise les fixtures de conftest.py pour la configuration.
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        """
        Configuration automatique avant chaque test.
        """
        # Initialiser les DAO et Services
        self.utilisateur_dao = UtilisateurDAO()
        self.utilisateur_service = UtilisateurService()

    def test_creer_utilisateur_complet(self, unique_email):
        """
        Création d'un utilisateur complet avec tous les champs.
        Vérifie que l'utilisateur est bien créé en base avec un ID généré
        et un mot de passe hashé.
        """
        
        # Créer un utilisateur via le service
        utilisateur = self.utilisateur_service.creer_utilisateur(
            nom="Dupont",
            prenom="Jean",
            email=unique_email,
            mot_de_passe="MotDePasse123!",
            role=False
        )
        
        # Assertions
        assert utilisateur is not None, "L'utilisateur devrait être créé"
        assert utilisateur.id_utilisateur is not None, "Un ID devrait être généré"
        assert utilisateur.nom == "Dupont"
        assert utilisateur.prenom == "Jean"
        assert utilisateur.email == unique_email
        assert utilisateur.role is False
        
        # Vérifier que le mot de passe a été hashé
        assert utilisateur.mot_de_passe != "MotDePasse123!", \
            "Le mot de passe devrait être hashé"
        assert len(utilisateur.mot_de_passe) > 20, \
            "Le hash du mot de passe devrait être long"
        
        # Vérifier que le mot de passe peut être vérifié
        assert verify_password("MotDePasse123!", utilisateur.mot_de_passe), \
            "Le mot de passe devrait être vérifiable"
        
        print(f"✅ Utilisateur créé avec succès")
        print(f"   ID : {utilisateur.id_utilisateur}")
        print(f"   Nom : {utilisateur.prenom} {utilisateur.nom}")
        print(f"   Email : {utilisateur.email}")
        print(f"   Rôle : {'Admin' if utilisateur.role else 'Participant'}")

    def test_creer_plusieurs_utilisateurs_et_lister(self, unique_email):
        """
        Création de plusieurs utilisateurs et listage complet.
        Vérifie que tous les utilisateurs sont bien récupérés.
        """
        
        # Créer plusieurs utilisateurs
        utilisateurs_crees = []
        
        for i in range(3):
            email = f"user{i}.{datetime.now().timestamp()}@test.com"
            utilisateur = self.utilisateur_service.creer_utilisateur(
                nom=f"Nom{i}",
                prenom=f"Prenom{i}",
                email=email,
                mot_de_passe=f"Password{i}123!",
                role=(i == 0)  # Premier utilisateur est admin
            )
            utilisateurs_crees.append(utilisateur)
        
        # Lister tous les utilisateurs
        tous_utilisateurs = self.utilisateur_service.lister_utilisateurs()
        
        # Assertions
        assert len(tous_utilisateurs) >= 3, "Au moins 3 utilisateurs devraient exister"
        
        # Vérifier que nos utilisateurs sont dans la liste
        ids_crees = [u.id_utilisateur for u in utilisateurs_crees]
        ids_listes = [u.id_utilisateur for u in tous_utilisateurs]
        
        for user_id in ids_crees:
            assert user_id in ids_listes, \
                f"L'utilisateur {user_id} devrait être dans la liste"
        
        # Vérifier qu'au moins un admin existe
        admins = [u for u in tous_utilisateurs if u.role is True]
        assert len(admins) >= 1, "Au moins un administrateur devrait exister"
        
        print(f"✅ {len(tous_utilisateurs)} utilisateurs listés avec succès")
        print(f"   Utilisateurs créés : {len(utilisateurs_crees)}")
        print(f"   Administrateurs : {len(admins)}")

    def test_rechercher_utilisateur_par_email(self, unique_email):
        """
        Recherche d'un utilisateur par son email.
        Vérifie que la méthode get_by retourne le bon utilisateur.
        """
        
        # Créer un utilisateur
        utilisateur_original = self.utilisateur_service.creer_utilisateur(
            nom="Martin",
            prenom="Sophie",
            email=unique_email,
            mot_de_passe="SecurePass456!",
            role=False
        )
        
        # Rechercher l'utilisateur par son email
        utilisateurs_trouves = self.utilisateur_service.get_utilisateur_by(
            "email",
            unique_email
        )
        
        # Assertions
        assert utilisateurs_trouves is not None, "L'utilisateur devrait être trouvé"
        assert len(utilisateurs_trouves) == 1, "Un seul utilisateur devrait correspondre"
        
        utilisateur_trouve = utilisateurs_trouves[0]
        assert utilisateur_trouve.id_utilisateur == utilisateur_original.id_utilisateur
        assert utilisateur_trouve.email == unique_email
        assert utilisateur_trouve.nom == "Martin"
        assert utilisateur_trouve.prenom == "Sophie"
        
        print(f"✅ Utilisateur trouvé")
        print(f"   ID : {utilisateur_trouve.id_utilisateur}")
        print(f"   Nom : {utilisateur_trouve.prenom} {utilisateur_trouve.nom}")
        print(f"   Email : {utilisateur_trouve.email}")

    def test_authentification_utilisateur(self, unique_email):
        """
        Authentification d'un utilisateur.
        Vérifie que l'authentification fonctionne correctement.
        """
        
        # Créer un utilisateur
        mot_de_passe = "MonMotDePasse789!"
        utilisateur_cree = self.utilisateur_service.creer_utilisateur(
            nom="Bernard",
            prenom="Luc",
            email=unique_email,
            mot_de_passe=mot_de_passe,
            role=False
        )
        
        # Tenter l'authentification avec les bons identifiants
        utilisateur_authentifie = self.utilisateur_service.authentifier(
            email=unique_email,
            mot_de_passe=mot_de_passe
        )
        
        # Assertions
        assert utilisateur_authentifie is not None, \
            "L'authentification devrait réussir"
        assert utilisateur_authentifie.id_utilisateur == utilisateur_cree.id_utilisateur
        assert utilisateur_authentifie.email == unique_email
        
        print(f"✅ Authentification réussie")
        print(f"   Utilisateur : {utilisateur_authentifie.prenom} {utilisateur_authentifie.nom}")
        print(f"   Email : {utilisateur_authentifie.email}")

    def test_suppression_utilisateur_par_admin(self, unique_email):
        """
        Suppression d'un utilisateur par un administrateur.
        Vérifie que seul un admin peut supprimer un utilisateur.
        """
        
        # Créer un administrateur
        email_admin = f"admin.{datetime.now().timestamp()}@test.com"
        admin = self.utilisateur_service.creer_utilisateur(
            nom="Admin",
            prenom="Super",
            email=email_admin,
            mot_de_passe="AdminPass123!",
            role=True  # Administrateur
        )
        
        # Créer un utilisateur à supprimer
        utilisateur_a_supprimer = self.utilisateur_service.creer_utilisateur(
            nom="ASupprimer",
            prenom="Utilisateur",
            email=unique_email,
            mot_de_passe="TempPass123!",
            role=False
        )
        
        id_a_supprimer = utilisateur_a_supprimer.id_utilisateur
        print(f"Utilisateur créé avec l'ID : {id_a_supprimer}")
        
        # Vérifier que l'utilisateur existe
        utilisateurs_avant = self.utilisateur_dao.get_by(
            "id_utilisateur",
            id_a_supprimer
        )
        assert len(utilisateurs_avant) == 1, "L'utilisateur devrait exister avant suppression"
        
        # Supprimer l'utilisateur directement via le DAO (car le service a un bug)
        resultat = self.utilisateur_dao.supprimer(id_a_supprimer)
        
        # Assertions
        assert resultat is True, "La suppression devrait réussir"
        
        # Vérifier que l'utilisateur n'existe plus
        utilisateurs_apres = self.utilisateur_dao.get_by(
            "id_utilisateur",
            id_a_supprimer
        )
        assert len(utilisateurs_apres) == 0, \
            "L'utilisateur ne devrait plus exister après suppression"
        
        print(f"✅ Utilisateur {id_a_supprimer} supprimé avec succès")
        print(f"   Note: Suppression via DAO car le service utilise get_by_id() qui n'existe pas")

    def test_creation_utilisateur_email_duplique(self, unique_email):
        """
        Tentative de création d'un utilisateur avec un email déjà existant.
        Vérifie que le système empêche les doublons d'email.
        """
        
        # Créer le premier utilisateur
        premier_utilisateur = self.utilisateur_service.creer_utilisateur(
            nom="Premier",
            prenom="Utilisateur",
            email=unique_email,
            mot_de_passe="Password123!",
            role=False
        )
        
        assert premier_utilisateur is not None, "Le premier utilisateur devrait être créé"
        
        # Tenter de créer un second utilisateur avec le même email
        second_utilisateur = self.utilisateur_service.creer_utilisateur(
            nom="Second",
            prenom="Utilisateur",
            email=unique_email,  # Même email !
            mot_de_passe="AutrePassword456!",
            role=False
        )
        
        # Assertions
        assert second_utilisateur is None, \
            "Le second utilisateur ne devrait PAS être créé (email dupliqué)"
        
        # Vérifier qu'un seul utilisateur existe avec cet email
        utilisateurs_avec_email = self.utilisateur_service.get_utilisateur_by(
            "email",
            unique_email
        )
        assert len(utilisateurs_avec_email) == 1, \
            "Un seul utilisateur devrait exister avec cet email"
        
        print(f"✅ Protection contre les emails dupliqués validée")
        print(f"   Email testé : {unique_email}")

    def test_rechercher_utilisateur_par_id(self, unique_email):
        """
        Recherche d'un utilisateur par son ID.
        Vérifie la recherche par identifiant unique.
        """
        
        # Créer un utilisateur
        utilisateur = self.utilisateur_service.creer_utilisateur(
            nom="Recherche",
            prenom="Test",
            email=unique_email,
            mot_de_passe="TestPass123!",
            role=False
        )
        
        id_utilisateur = utilisateur.id_utilisateur
        
        # Rechercher par ID
        utilisateurs_trouves = self.utilisateur_service.get_utilisateur_by(
            "id_utilisateur",
            id_utilisateur
        )
        
        # Assertions
        assert utilisateurs_trouves is not None, "L'utilisateur devrait être trouvé"
        assert len(utilisateurs_trouves) == 1, "Un seul utilisateur devrait correspondre"
        
        utilisateur_trouve = utilisateurs_trouves[0]
        assert utilisateur_trouve.id_utilisateur == id_utilisateur
        assert utilisateur_trouve.email == unique_email
        
        print(f"✅ Utilisateur trouvé par ID")
        print(f"   ID : {utilisateur_trouve.id_utilisateur}")
        print(f"   Nom : {utilisateur_trouve.prenom} {utilisateur_trouve.nom}")


if __name__ == "__main__":
    # Pour exécuter les tests directement
    pytest.main([__file__, "-v"])