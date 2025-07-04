INSERT INTO art_gallery.type VALUES
(1,'Oil'),
(2,'Tempra'),
(3,'Watercolor');
INSERT INTO art_gallery.period VALUES
(1,'Baroque'),
(2,'Dutch Golden Age'),
(3,'High Renaissance'),
(4,'Impressionism'),
(5,'Modern'),
(6,'Post-Impressionism'),
(7,'Renaissance');

INSERT INTO art_gallery.country VALUES
(1,'France'),
(2,'Italy'),
(3,'Netherlands'),
(4,'Spain'),
(5,'United States');

INSERT INTO art_gallery.keyword VALUES
(1,'flowers'),
(2,'blue'),
(3,'landscape'),
(4,'girl'),
(5,'people'),
(6,'battle'),
(7,'boat'),
(8,'water'),
(9,'Christ'),
(10,'Food'),
(11,'baby');


INSERT INTO art_gallery.artist VALUES
(1,'Vincent',NULL,'van Gogh',1853,1890,'n',1),
(2,'Rembrandt','Harmenszoon','van Rijn',1606,1669,'n',3),
(3,'Leonardo',null,'da Vinci',1452,1519,'n',2),
(4,'Venture','Lonzo','Coy',1965,null,'y',5),
(5,'Deborah',null,'Gill',1970,null,'y',5),
(6,'Claude',null,'Monet',1840,1926,'n',1),
(7,'Pablo',null,'Picasso',1904,1973,'n',4),
(8,'Michelangelo','di Lodovico','Simoni',1475,1564,'n',2);

INSERT INTO art_gallery.artwork VALUES
(1,1,'Irises',1889,4,1,'irises.jpg'),
(2,1,'The Starry Night',1889,6,1,'starrynight.jpg'),
(3,1,'Sunflowers',1888,6,1,'sunflowers.jpg'),
(4,2,'Night Watch',1642,1,1,'nightwatch.jpg'),
(5,2,'Storm on the Sea of Galilee',1633,2,1,'stormgalilee.jpg'),
(6,3,'Head of a Woman',1508,3,1,'headwoman.jpg'),
(7,3,'Last Supper',1498,7,NULL,'lastsupper.jpg'),
(8,3,'Mona Lisa',1517,7,1,'monalisa.jpg'),
(9,4,'Hillside Stream',2005,5,1,'hillsidestream.jpg'),
(10,4,'Old Barn',1992,5,1,'oldbarn.jpg'),
(11,5,'Beach Baby',1999,5,3,'beachbaby.jpg'),
(12,6,'Women in the Garden',1866,4,1,'womengarden.jpg'),
(13,7,'Old Guitarist',1904,5,1,'guitarist.jpg');

INSERT INTO art_gallery.artwork_has_keyword VALUES
(1,1),
(2,2),	(2,3),
(3,1),
(4,4),	(4,5),	(4,6),
(5,7),	(5,8),	(5,5),	(5,9),
(6,4),	(6,5),
(7,10),	(7,5),	(7,9),
(8,4),	(8,5),
(9,8),	(9,3),
(10,3),
(11,8),(11,5),	(11,11),
(12,3),	(12,5),	(12,1),
(13,2),	(13,5);