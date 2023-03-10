CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    file_path TEXT,
    rating FLOAT,
    type TEXT NOT NULL,
    created TIMESTAMP WITH TIME ZONE,
    modified TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name TEXT,
    description TEXT,
    created TIMESTAMP WITH TIME ZONE,
    modified TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name TEXT,
    created TIMESTAMP WITH TIME ZONE,
    modified TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL,
    genre_id uuid NOT NULL,
    created TIMESTAMP WITH TIME ZONE,
    CONSTRAINT fk_film_work FOREIGN KEY (film_work_id) REFERENCES content.film_work(id) ON DELETE CASCADE,
    CONSTRAINT fk_genre FOREIGN KEY (genre_id) REFERENCES content.genre(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL,
    person_id uuid NOT NULL,
    role TEXT NOT NULL,
    created TIMESTAMP WITH TIME ZONE,
    CONSTRAINT fk_film_work FOREIGN KEY (film_work_id) REFERENCES content.film_work(id) ON DELETE CASCADE,
    CONSTRAINT fk_person FOREIGN KEY (person_id) REFERENCES content.person(id) ON DELETE CASCADE
);

CREATE INDEX film_work_title_idx ON content.film_work (title);
CREATE INDEX film_work_creation_date_idx ON content.film_work (creation_date);
CREATE INDEX person_idx ON content.person (full_name);
CREATE UNIQUE INDEX film_work_genre_idx ON content.genre_film_work (film_work_id, genre_id);
CREATE UNIQUE INDEX film_work_person_role_idx ON content.person_film_work (film_work_id, person_id, role);
