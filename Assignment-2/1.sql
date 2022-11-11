CREATE TABLE query1 AS
SELECT name, moviecount
FROM genres JOIN (SELECT genreid, COUNT(movieid) AS moviecount
                  FROM hasagenre
                  GROUP BY genreid) AS genrecount
                 ON genres.genreid = genrecount.genreid

----------------------------------------------------------------------------------
CREATE TABLE query2 AS
SELECT name, rating
FROM genres JOIN (SELECT genreid, AVG(rating) AS rating FROM ratings JOIN hasagenre
                                                                          ON ratings.movieid = hasagenre.movieid
                  GROUP BY genreid) AS genrerating
                 ON genres.genreid = genrerating.genreid

----------------------------------------------------------------------------------
CREATE TABLE query3 AS
SELECT title, countofratings
FROM movies JOIN (SELECT movieid, COUNT(rating) AS countofratings
                  FROM ratings
                  GROUP BY movieid
                  HAVING COUNT(rating) >= 10) AS ratingcount
                 ON movies.movieid = ratingcount.movieid

----------------------------------------------------------------------------------
CREATE TABLE query4 AS
SELECT movies.movieid, title
FROM movies JOIN hasagenre
                 ON movies.movieid = hasagenre.movieid
WHERE genreid = (SELECT genreid FROM genres
                 WHERE name = 'Comedy')

----------------------------------------------------------------------------------
CREATE TABLE query5 AS
SELECT movies.title, AVG(ratings.rating)
FROM ratings JOIN movies
                  ON movies.movieid = ratings.movieid
GROUP BY movies.title

----------------------------------------------------------------------------------
CREATE TABLE query6 AS
SELECT AVG(ratings.rating)
FROM ratings JOIN (SELECT movies.movieid, title
                   FROM movies JOIN hasagenre
                                    ON movies.movieid = hasagenre.movieid
                   WHERE genreid = (SELECT genreid FROM genres
                                    WHERE name = 'Comedy')) AS comedymovies
                  ON ratings.movieid = comedymovies.movieid

----------------------------------------------------------------------------------
CREATE TABLE query7 AS
SELECT AVG(ratings.rating)
FROM ratings
         JOIN (SELECT comedymovies.movieid
               FROM (SELECT movies.movieid, title
                     FROM movies JOIN hasagenre
                                      ON movies.movieid = hasagenre.movieid
                     WHERE genreid = (SELECT genreid FROM genres
                                      WHERE name = 'Comedy')) AS comedymovies
                        JOIN (SELECT movies.movieid, title
                              FROM movies JOIN hasagenre
                                               ON movies.movieid = hasagenre.movieid
                              WHERE genreid = (SELECT genreid FROM genres
                                               WHERE name = 'Romance')) AS romancemovies
                             ON comedymovies.movieid = romancemovies.movieid) AS romcommovies
              ON ratings.movieid = romcommovies.movieid

----------------------------------------------------------------------------------
CREATE TABLE query8 AS
SELECT AVG(ratings.rating)
FROM ratings
         JOIN (SELECT romancemovies.movieid
               FROM (SELECT movies.movieid, title
                     FROM movies JOIN hasagenre
                                      ON movies.movieid = hasagenre.movieid
                     WHERE genreid = (SELECT genreid FROM genres
                                      WHERE name = 'Romance')) AS romancemovies
                        LEFT JOIN (SELECT movies.movieid, title
                                   FROM movies JOIN hasagenre
                                                    ON movies.movieid = hasagenre.movieid
                                   WHERE genreid = (SELECT genreid FROM genres
                                                    WHERE name = 'Comedy')) AS comedymovies
                                  ON comedymovies.movieid = romancemovies.movieid
               WHERE comedymovies.movieid IS NULL) AS romnotcommovies
              ON ratings.movieid = romnotcommovies.movieid

----------------------------------------------------------------------------------
CREATE TABLE query9 AS
SELECT ratings.userid, movieid, rating
FROM ratings JOIN users
                  ON ratings.userid = users.userid
WHERE users.userid = :v1