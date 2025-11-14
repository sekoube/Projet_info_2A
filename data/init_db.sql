-- ==============================
--  Réinitialisation du schéma
-- ==============================
DROP SCHEMA IF EXISTS projet CASCADE;
CREATE SCHEMA projet;

-- ==============================
--  Table utilisateur
-- ==============================
CREATE TABLE projet.utilisateur (
    id_utilisateur SERIAL PRIMARY KEY,
    pseudo         VARCHAR(50) NOT NULL,
    nom            VARCHAR(50) NOT NULL,
    prenom         VARCHAR(50) NOT NULL,
    email          VARCHAR(100) UNIQUE NOT NULL,
    mot_de_passe   VARCHAR(100) NOT NULL,
    date_creation  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    role           BOOLEAN DEFAULT FALSE
);

-- ==============================
--  Table evenement
-- ==============================
CREATE TABLE projet.evenement (
    id_event              SERIAL PRIMARY KEY,
    titre                 VARCHAR(100) NOT NULL,
    description_event TEXT,
    lieu                  VARCHAR(100) NOT NULL,
    date_event        DATE NOT NULL,
    capacite_max          INT CHECK (capacite_max > 0),
    created_by            INT NOT NULL REFERENCES projet.utilisateur(id_utilisateur) ON DELETE SET NULL,
    created_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tarif                 NUMERIC(10,2) CHECK (tarif >= 0)
);


-- ==============================
--  Table bus
-- ==============================
CREATE TABLE projet.bus (
    id_bus          SERIAL PRIMARY KEY,
    id_event        INT NOT NULL,
    sens            BOOLEAN NOT NULL,
    description     TEXT,
    heure_depart    TIME,
    FOREIGN KEY (id_event)
        REFERENCES projet.evenement(id_event)
        ON DELETE CASCADE
);

-- ==============================
--  Table inscription
-- ==============================
CREATE TABLE projet.inscription (
    code_reservation SERIAL PRIMARY KEY,
    date_inscription TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    boit             BOOLEAN NOT NULL,
    mode_paiement    VARCHAR(50) NOT NULL,
    created_by   INT NOT NULL,
    id_event         INT NOT NULL,
    id_bus_aller     INT,
    id_bus_retour    INT,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by)
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
