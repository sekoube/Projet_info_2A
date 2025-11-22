import re
import pytest
from datetime import datetime
from business_object.bus import Bus


# ========================== Tests de levée d'erreurs ==========================
@pytest.mark.parametrize(
    'params, erreur, message_erreur',
    [
        ({'id_event': '', 'sens': 'Aller', 'description': 'Bruz', 'heure_depart': "10:00", 'capacite_max': 50},
        ValueError, "L'identifiant de l'évènement doit être renseigné"),
        ({'id_event': '1234', 'sens': "", 'description': 'direct', 'heure_depart': "10:00", 'capacite_max': 50},
        ValueError, "Le sens ne peut pas être vide"),
        ({'id_event': '1234', 'sens': 'vers ENSAI', 'description': 'direct', 'heure_depart': "10:00", 'capacite_max': 50},
        ValueError, "Le sens doit être 'Aller' ou 'Retour' (majuscule/minuscule acceptée)"),
        ({'id_event': '1234', 'sens': 'Aller', 'description': 'direct', 'heure_depart': "10:00", 'capacite_max': 0},
        ValueError, "La capacité maximale doit être supérieure à 0"),
        ({'id_event': '1234', 'sens': 'Aller', 'description': 'direct', 'heure_depart': "10:00", 'capacite_max': -10},
        ValueError, "La capacité maximale doit être supérieure à 0"),
    ]
)
def test_bus_erreurs(params, erreur, message_erreur):
    """Vérifie que les mauvaises valeurs lèvent les erreurs appropriées"""
    with pytest.raises(erreur, match=re.escape(message_erreur)):
        Bus(**params)


# ========================== Tests de création valide ==========================
@pytest.mark.parametrize(
    'params, sens_booleen_attendu',
    [
        (
            {'id_event': '1234', 'sens': "Aller", 'description': "direct", 'heure_depart': "10:00", 'capacite_max': 50},
            "ALLER"
        ),
        (
            {'id_event': '5678', 'sens': "Retour", 'description': "Bruz", 'heure_depart': "18:30", 'capacite_max': 40},
            "RETOUR"
        ),
    ]
)
def test_bus_creation_valide(params, sens_booleen_attendu):
    """Vérifie la création correcte des bus et l'assignation des attributs"""
    bus = Bus(**params)
    
    # Vérifie que les attributs correspondent aux paramètres
    assert bus.id_event == params['id_event']
    assert bus.sens == sens_booleen_attendu  # Vérifie que le sens est normalisé en majuscules
    assert bus.description == params['description']
    assert bus.capacite_max == params['capacite_max']
    
    # Vérifie que l'heure de départ est bien un datetime
    assert isinstance(bus.heure_depart, datetime)
    
    # Vérifie que l'heure correspond à celle entrée
    heure_attendue = datetime.strptime(params['heure_depart'], "%H:%M")
    assert bus.heure_depart.hour == heure_attendue.hour
    assert bus.heure_depart.minute == heure_attendue.minute
    
    # Vérifie que id_bus est None par défaut
    assert bus.id_bus is None


# ========================== Tests de validation flexible du sens ==========================
@pytest.mark.parametrize(
    'sens_input, sens_normalise_attendu',
    [
        ("Aller", "ALLER"),
        ("aller", "ALLER"),
        ("ALLER", "ALLER"),
        ("Retour", "RETOUR"),
        ("retour", "RETOUR"),
        ("RETOUR", "RETOUR"),
    ]
)
def test_bus_sens_case_insensitive(sens_input, sens_normalise_attendu):
    """Vérifie que le sens accepte différentes casses et est normalisé en majuscules"""
    bus = Bus(
        id_event='1234',
        sens=sens_input,
        description="direct",
        heure_depart="10:00",
        capacite_max=50
    )
    
    assert bus.sens == sens_normalise_attendu


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
            description="direct",
            heure_depart="10:00",
            capacite_max=capacite_max
        )
        assert bus.capacite_max == capacite_max
    else:
        with pytest.raises(ValueError, match="La capacité maximale doit être supérieure à 0"):
            Bus(
                id_event='1234',
                sens="Aller",
                description="direct",
                heure_depart="10:00",
                capacite_max=capacite_max
            )


# ========================== Test de la méthode to_dict() ==========================
def test_bus_to_dict():
    """Vérifie que to_dict() retourne un dictionnaire correct"""
    bus = Bus(
        id_event='1234',
        sens="aller",
        description="direct",
        heure_depart="10:00",
        capacite_max=50,
        id_bus=42
    )
    
    result = bus.to_dict()
    
    assert result['id_bus'] == 42
    assert result['id_event'] == '1234'
    assert result['sens'] == 'ALLER'
    assert result['description'] == 'direct'
    assert result['heure_depart'] == '10:00'
    assert result['capacite_max'] == 50





# ========================== Test avec id_bus fourni ==========================
def test_bus_avec_id_fourni():
    """Vérifie qu'un bus peut être créé avec un id_bus spécifié"""
    bus = Bus(
        id_event='1234',
        sens="Aller",
        description="direct",
        heure_depart="10:00",
        capacite_max=50,
        id_bus=42
    )
    
    assert bus.id_bus == 42
    assert bus.id_event == '1234'
    assert bus.sens == 'ALLER'
    assert bus.capacite_max == 50


# ========================== Tests avec heure_depart comme datetime ==========================
def test_bus_heure_depart_datetime():
    """Vérifie que heure_depart peut être un objet datetime"""
    dt = datetime.strptime("14:30", "%H:%M")
    bus = Bus(
        id_event='1234',
        sens="Aller",
        description="direct",
        heure_depart=dt,
        capacite_max=50
    )
    
    assert isinstance(bus.heure_depart, datetime)
    assert bus.heure_depart.hour == 14
    assert bus.heure_depart.minute == 30


# ========================== Tests heure_depart comme string ==========================
def test_bus_heure_depart_string():
    """Vérifie que heure_depart peut être une string au format HH:MM"""
    bus = Bus(
        id_event='1234',
        sens="Retour",
        description="Bruz",
        heure_depart="18:45",
        capacite_max=40
    )
    
    assert isinstance(bus.heure_depart, datetime)
    assert bus.heure_depart.hour == 18
    assert bus.heure_depart.minute == 45