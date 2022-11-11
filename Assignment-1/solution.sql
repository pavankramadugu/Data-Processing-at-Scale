CREATE TABLE users
(
    userid INTEGER PRIMARY KEY,
    name   text NOT NULL
);

CREATE TABLE movies
(
    movieid INTEGER PRIMARY KEY,
    title   text NOT NULL
);

CREATE TABLE taginfo
(
    tagid   INTEGER PRIMARY KEY,
    content text NOT NULL
);

CREATE TABLE genres
(
    genreid INTEGER PRIMARY KEY,
    name    text NOT NULL
);

CREATE TABLE ratings
(
    userid    INTEGER,
    movieid   INTEGER,
    PRIMARY KEY (userid, movieid),
    rating    NUMERIC CHECK (rating >= 0.0 and rating <= 5.0),
    timestamp bigint NOT NULL DEFAULT date_part('epoch', now()),
    FOREIGN KEY (userid) REFERENCES users (userid),
    FOREIGN KEY (movieid) REFERENCES movies (movieid)
);

CREATE TABLE tags
(
    userid    INTEGER,
    movieid   INTEGER,
    tagid     INTEGER,
    PRIMARY KEY (userid, movieid, tagid),
    timestamp bigint NOT NULL DEFAULT date_part('epoch', now()),
    FOREIGN KEY (userid) REFERENCES users (userid),
    FOREIGN KEY (movieid) REFERENCES movies (movieid),
    FOREIGN KEY (tagid) REFERENCES taginfo (tagid)
);

CREATE TABLE hasagenre
(
    movieid INTEGER,
    genreid INTEGER,
    PRIMARY KEY (movieid, genreid),
    FOREIGN KEY (movieid) REFERENCES movies (movieid),
    FOREIGN KEY (genreid) REFERENCES genres (genreid)
);