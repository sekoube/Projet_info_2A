import re
import pytest
from datetime import datetime
from business_object.bus import Bus


# ========================== Tests de levée d'erreurs ==========================
@pytest.mark.parametrize(
    'params, erreur, message_erreur',
    [
        ({'id_event': '', 'sens': 'Aller', 'description': ['Bruz'], 'heure_depart': "10:00", 'capacite_max': 50},
        ValueError, "L'identifiant de l'évènement doit être renseigné"),
        ({'id_event': '1234', 'sens': "", 'description': ['direct'], 'heure_depart': "10:00", 'capacite_max': 50},
        ValueError, "Le sens ne peut pas être vide"),
        ({'id_event': '1234', 'sens': 'vers ENSAI', 'description': ['direct'], 'heure_depart': "10:00", 'capacite_max': 50},
        ValueError, "Le sens doit être 'Aller' ou 'Retour' (majuscule/minuscule acceptée)"),
    ]
)
def test_bus_erreurs(params, erreur, message_erreur):
    """Vérifie que les mauvaises valeurs lèvent les erreurs appropriées"""
    with pytest.raises(erreur, match=re.escape(message_erreur)):
        Bus(**params)


# ========================== Tests de création valide ==========================
@pytest.mark.parametrize(
    'params, sens_attendu',
    [
        (
            {'id_event': '1234', 'sens': "Aller", 'description': ["direct"], 'heure_depart': "10:00", 'capacite_max': 50},
            True
        ),
        (
            {'id_event': '5678', 'sens': "Retour", 'description': ["Bruz"], 'heure_depart': "18:30", 'capacite_max': 40},
            False
        ),
    ]
)
def test_bus_creation_valide(params, sens_attendu):
    """Vérifie la création correcte des bus et l'assignation des attributs"""
    bus_cour = Bus(**params)
    
    # Vérifie que les attributs correspondent aux paramètres
    assert bus_cour.id_event == params['id_event']
    assert bus_cour.sens == sens_attendu  # Vérifie le booléen
    assert bus_cour.description == params['description']
    assert bus_cour.capacite_max == params['capacite_max']
    
    # Vérifie que l'heure de départ est bien un datetime
    assert isinstance(bus_cour.heure_depart, datetime)
    
    # Vérifie que l'heure correspond à celle entrée
    heure_attendue = datetime.strptime(params['heure_depart'], "%H:%M")
    assert bus_cour.heure_depart.hour == heure_attendue.hour
    assert bus_cour.heure_depart.minute == heure_attendue.minute
    
    # Vérifie que id_bus est None par défaut
    assert bus_cour.id_bus is None


# ========================== Tests de validation flexible du sens ==========================
@pytest.mark.parametrize(
    'sens_input, sens_booleen_attendu',
    [
        ("Aller", True),
        ("aller", True),
        ("ALLER", True),
        ("Retour", False),
        ("retour", False),
        ("RETOUR", False),
    ]
)
def test_bus_sens_case_insensitive(sens_input, sens_booleen_attendu):
    """Vérifie que le sens accepte différentes casses (majuscule/minuscule)"""
    bus = Bus(
        id_event='1234',
        sens=sens_input,
        description=["direct"],
        heure_depart="10:00",
        capacite_max=50
    )
    
    assert bus.sens == sens_booleen_attendu
    # Vérifie que get_sens_str() retourne toujours le format standard
    assert bus.get_sens_str() in ["Aller", "Retour"]


# ========================== Tests de capacité maximale ==========================
@pytest.mark.parametrize(
    'capacite_max, valide',
    [
        (0, False),      # Capacité nulle invalide
        (-10, False),    # Capacité négative invalide
        (1, True),       # Capacité minimale valide
        (50, True),      # Capacité standard
        (100, True),     # Grande capacité
    ]
)
def test_bus_capacite_max(capacite_max, valide):
    """Vérifie la validation de la capacité maximale du bus"""
    if valide:
        bus = Bus(
            id_event='1234',
            sens="Aller",
            description=["direct"],
            heure_depart="10:00",
            capacite_max=capacite_max
        )
        assert bus.capacite_max == capacite_max
    else:
        with pytest.raises(ValueError):
            Bus(
                id_event='1234',
                sens="Aller",
                description=["direct"],
                heure_depart="10:00",
                capacite_max=capacite_max
            )


# ========================== Test de la méthode get_sens_str() ==========================
def test_bus_get_sens_str():
    """Vérifie que get_sens_str() retourne la bonne représentation textuelle"""
    bus_aller = Bus(
        id_event='1234',
        sens="aller",  # minuscule
        description=["direct"],
        heure_depart="10:00",
        capacite_max=50
    )
    assert bus_aller.get_sens_str() == "Aller"
    assert bus_aller.sens is True
    
    bus_retour = Bus(
        id_event='5678',
        sens="RETOUR",  # majuscule
        description=["Bruz"],
        heure_depart="18:00",
        capacite_max=40
    )
    assert bus_retour.get_sens_str() == "Retour"
    assert bus_retour.sens is False


# ========================== Test avec id_bus fourni ==========================
def test_bus_avec_id_fourni():
    """Vérifie qu'un bus peut être créé avec un id_bus spécifié"""
    bus = Bus(
        id_event='1234',
        sens="Aller",
        description=["direct"],
        heure_depart="10:00",
        capacite_max=50,
        id_bus=42
    )
    
    assert bus.id_bus == 42
    assert bus.id_event == '1234'
    assert bus.sens is True
    assert bus.capacite_max == 50