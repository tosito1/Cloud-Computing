-- Crear tabla de usuarios
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL
);

-- Crear tabla de notificaciones
CREATE TABLE notificationes (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    text VARCHAR NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    president_id INTEGER NOT NULL,
    CONSTRAINT fk_president_notification FOREIGN KEY (president_id) REFERENCES users (id)
);

-- Crear tabla de votaciones
CREATE TABLE votaciones (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description VARCHAR
);

-- Crear tabla de opciones
CREATE TABLE opciones (
    id SERIAL PRIMARY KEY,
    voting_id INTEGER NOT NULL,
    option_text VARCHAR NOT NULL,
    CONSTRAINT fk_voting_option FOREIGN KEY (voting_id) REFERENCES votaciones (id)
);

-- Crear tabla de votos
CREATE TABLE votes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    option_id INTEGER NOT NULL,
    CONSTRAINT fk_user_vote FOREIGN KEY (user_id) REFERENCES users (id),
    CONSTRAINT fk_option_vote FOREIGN KEY (option_id) REFERENCES opciones (id)
);
-----

-- Crear tabla de cuotas
CREATE TABLE cuotas (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    name VARCHAR NOT NULL,
    amount FLOAT NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR NOT NULL,
    fine_id INTEGER
);

-- Crear tabla de multas
CREATE TABLE multas (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    amount FLOAT NOT NULL,
    quota_id INTEGER,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Agregar las restricciones después
ALTER TABLE cuotas ADD CONSTRAINT fk_user_quota FOREIGN KEY (user_id) REFERENCES users (id);
ALTER TABLE cuotas ADD CONSTRAINT fk_fine FOREIGN KEY (fine_id) REFERENCES multas (id);
ALTER TABLE multas ADD CONSTRAINT fk_user_fine FOREIGN KEY (user_id) REFERENCES users (id);
ALTER TABLE multas ADD CONSTRAINT fk_quota_fine FOREIGN KEY (quota_id) REFERENCES cuotas (id) ON DELETE SET NULL;

-- Crear otras tablas como antes...
