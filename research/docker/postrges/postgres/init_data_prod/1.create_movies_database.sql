CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title text NOT NULL,
    description text,
    creation_date date,
    rating double precision,
    type text NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone,
    certificate character varying(255),
    "file_path" text,
    premium boolean
);


CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY,
    genre_id uuid NOT NULL REFERENCES content.genre (id) ON DELETE CASCADE,
    film_work_id uuid NOT NULL REFERENCES content.film_work (id) ON DELETE CASCADE,
    created timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone,
    birth_date date
);


CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    person_id uuid NOT NULL REFERENCES content.person (id) ON DELETE CASCADE,
    film_work_id uuid NOT NULL REFERENCES content.film_work (id) ON DELETE CASCADE,
    role TEXT NOT NULL,
    created timestamp with time zone
); 


CREATE INDEX film_work_creation_date_rating_idx ON content.film_work (creation_date, rating);
CREATE INDEX film_work_creation_date_idx ON content.film_work(creation_date); 


CREATE UNIQUE INDEX genre_name_idx ON content.genre (name);

CREATE UNIQUE INDEX film_work_genre_idx ON content.genre_film_work (genre_id, film_work_id);

--CREATE UNIQUE INDEX film_work_person_idx ON content.person_film_work (film_work_id, person_id);

CREATE UNIQUE INDEX person_name_idx ON content.person (full_name);


CREATE TABLE IF NOT EXISTS content.MovieViewEvent (
    movie_id uuid  NOT NULL,
    user_id uuid  NOT NULL,
    event_time date,
    view_run_time int
);

CREATE INDEX film_view_idx ON content.MovieViewEvent(movie_id);


CREATE TABLE IF NOT EXISTS content.likes (
    movie_id uuid  NOT NULL,
    user_id uuid  NOT NULL
);

CREATE INDEX film_like_idx ON content.likes(movie_id);

CREATE TABLE IF NOT EXISTS content.comments (
    movie_id uuid  NOT NULL,
    user_id uuid  NOT NULL,
    event_time date,
    title text,
    body text,
    score int
);

CREATE INDEX film_comments_idx ON content.comments(movie_id);






