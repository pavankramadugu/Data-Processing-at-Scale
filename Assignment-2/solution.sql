CREATE TABLE query1(name, moviecount) AS SELECT genres.name, COUNT(genres.genreid) FROM hasagenre NATURAL JOIN genres GROUP BY genres.genreid;

CREATE TABLE query2(name, rating) as SELECT genres.name, avg(ratings.rating) FROM movies NATURAL JOIN genres NATURAL JOIN ratings NATURAL JOIN hasagenre GROUP BY genres.name;

CREATE TABLE query3(title, CountOfRatings) AS SELECT movies.title, count(rating) FROM movies NATURAL JOIN ratings GROUP BY movies.title HAVING COUNT(*) >= 10;

CREATE TABLE query4(movieid, title) AS SELECT movieid, title FROM movies NATURAL JOIN genres NATURAL JOIN hasagenre WHERE genres.name = 'Comedy' GROUP BY movieid;

CREATE TABLE query5(title, average) AS SELECT movies.title, avg(ratings.rating) FROM movies NATURAL JOIN ratings GROUP BY movies.title;

CREATE TABLE query6(average) AS SELECT avg(ratings.rating) FROM movies NATURAL JOIN genres NATURAL JOIN ratings NATURAL JOIN hasagenre WHERE genres.name = 'Comedy';

CREATE TABLE query7(average) AS SELECT avg(ratings.rating) FROM ratings INNER JOIN (SELECT hasagenre.movieid FROM hasagenre NATURAL JOIN genres WHERE genres.name IN ('Comedy', 'Romance') GROUP BY hasagenre.movieid HAVING COUNT(DISTINCT genres.name) = 2 ) m ON ratings.movieid = m.movieid;

CREATE TABLE query8(average) AS SELECT avg(ratings.rating) FROM ratings WHERE movieid IN (SELECT movieid FROM hasagenre NATURAL JOIN genres GROUP BY movieid HAVING COUNT(CASE WHEN genres.name = 'Comedy' THEN 1 END) = 0 AND COUNT(CASE WHEN genres.name = 'Romance' THEN 1 END) = 1 );

CREATE TABLE query9 AS SELECT movieid, rating FROM ratings WHERE userid=:v1;