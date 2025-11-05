DROP SCHEMA IF EXISTS projet CASCADE;
CREATE SCHEMA projet;

CREATE TABLE projet.utilisateur (
    id_utilisateur SERIAL PRIMARY KEY,
    pseudo         VARCHAR(50),
    nom            VARCHAR(50),
    prenom         VARCHAR(50),
    email          VARCHAR(100) UNIQUE,
    mot_de_passe   VARCHAR(100),
    role           BOOLEAN DEFAULT FALSE
                                );

-- Création de la table admin
<<<<<<< HEAD
CREATE TABLE projet.administrateur (
    id_admin      SERIAL PRIMARY KEY,
    id_utilisateur INT NOT NULL UNIQUE,
        FOREIGN KEY (id_utilisateur) 
            REFERENCES projet.utilisateur(id_utilisateur) 
            ON DELETE CASCADE
);  -- si on supprimes un utilisateur dans utilisateur, alors la ligne correspondante est automatiquement supprimée dans admin
=======
-- CREATE TABLE projet.administrateur (
--     id_admin      SERIAL PRIMARY KEY,
--     id_utilisateur INT NOT NULL UNIQUE,
--     FOREIGN KEY (id_utilisateur) 
--         REFERENCES projet.utilisateur(id_utilisateur) 
--         ON DELETE CASCADE
-- );  -- si on supprimes un utilisateur dans utilisateur, alors la ligne correspondante est automatiquement supprimée dans admin
DROP TABLE projet.administrateur;

>>>>>>> da2aca4dd7bb4d199bc77f8d1b5b9b4dae0cadd7

-- Création de la table evenement
CREATE TABLE projet.evenement (
    id_event                SERIAL PRIMARY KEY,
    titre                   VARCHAR(100) NOT NULL,
    description_evenement   TEXT,
    lieu                    VARCHAR(100) NOT NULL,
    date_evenement          DATE NOT NULL,
    capacite_max            INT CHECK (capacite_max > 0), -- on refuse la création d'un évènement vide
    created_by              INT NOT NULL REFERENCES projet.utilisateur(id_utilisateur) ON DELETE CASCADE,
    created_at              TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tarif                   NUMERIC(10,2) CHECK (tarif >= 0)
                                );

-- Création de la table bus
CREATE TABLE projet.bus (
    id_bus                  SERIAL PRIMARY KEY,
    id_event                INT NOT NULL UNIQUE,
    sens                    BOOLEAN NOT NULL,
    description_bus         TEXT,
    heure_depart            TIMESTAMP NOT NULL,
    FOREIGN KEY (id_event) 
        REFERENCES projet.evenement(id_event) 
        ON DELETE CASCADE
);
-- Création de la table inscription
CREATE TABLE projet.inscription (
    code_reservation SERIAL PRIMARY KEY,
    date_inscription TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    boit             BOOLEAN NOT NULL, 
    mode_paiement    VARCHAR(50) NOT NULL,
    id_utilisateur   INT NOT NULL,
    id_event         INT NOT NULL,
    id_bus_aller     INT,
    id_bus_retour    INT,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_utilisateur) 
        REFERENCES projet.utilisateur(id_utilisateur) 
        ON DELETE CASCADE,
    FOREIGN KEY (id_event) 
        REFERENCES projet.evenement(id_event) 
        ON DELETE CASCADE,
    FOREIGN KEY (id_bus_aller) 
        REFERENCES projet.bus(id_bus) 
        ON DELETE SET NULL,
    FOREIGN KEY (id_bus_retour) 
        REFERENCES projet.bus(id_bus) 
        ON DELETE SET NULL
);
