INSERT INTO movie_database.studio VALUES
(1,'Pixar'),
(2,'MGM'),
(3,'20th Century');
INSERT INTO movie_database.media_type VALUES
(50,'DVD'),
(51,'Blue-Ray');
INSERT INTO movie_database.Genre VALUES
(1,'Family'),
(2,'Animated'),
(3,'Musical'),
(4,'Romance'),
(5,'Sci-Fi');

INSERT INTO movie_database.features VALUES
(1,'bloopers'),
(2,'actor interviews'),
(3,'cut scenes'),
(4,'bloopers');

INSERT INTO movie_database.movie VALUES 
(1,1,'Toy Story','G',1995,19.95),
(2,1,'Toy Story 2','G',1999,24.95),
(3,2,'Brigadoone','G',1954,19.95),
(4,3,'The Empire Strikes Back','PG',1977,35.00);

INSERT INTO movie_database.movie_has_media_type VALUES 
(1,50,19.95),
(2,50,24.95),
(3,50,19.95),
(4,50,19.95),
(4,51,29.99);