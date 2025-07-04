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
(1,'Vincent',NULL,'van Gogh',1853,1890,'France','n'),
(2,'Rembrandt','Harmenszoon','van Rijn',1606,1669,'Netherlands','n'),
(3,'Leonardo',null,'da Vinci',1452,1519,'Italy','n'),
(4,'Venture','Lonzo','Coy',1965,null,'United States','y'),
(5,'Deborah',null,'Gill',1970,null,'United States','y'),
(6,'Claude',null,'Monet',1840,1926,'France','n'),
(7,'Pablo',null,'Picasso',1904,1973,'Spain','n'),
(8,'Michelangelo','di Lodovico','Simoni',1475,1564,'Italy','n');

INSERT INTO art_gallery.artwork VALUES
(1,1,'Irises',1889,'Impressionism','Oil','irises.jpg'),
(2,1,'The Starry Night',1889,'Post-Impressionism','Oil','starrynight.jpg'),
(3,1,'Sunflowers',1888,'Post-impressionism','Oil','sunflowers.jpg'),
(4,2,'Night Watch',1642,'Baroque','Oil','nightwatch.jpg'),
(5,2,'Storm on the Sea of Galilee',1633,'Dutch Golden Age','Oil','stormgalilee.jpg'),
(6,3,'Head of a Woman',1508,'High Renaissance','Oil','headwoman.jpg'),
(7,3,'Last Supper',1498,'Renaissance','Tempra ','lastsupper.jpg'),
(8,3,'Mona Lisa',1517,'Renaissance','Oil','monalisa.jpg'),
(9,4,'Hillside Stream',2005,'Modern','Oil','hillsidestream.jpg'),
(10,4,'Old Barn',1992,'Modern','Oil','oldbarn.jpg'),
(11,5,'Beach Baby',1999,'Modern','Watercolor','beachbaby.jpg'),
(12,6,'Women in the Garden',1866,'Impressionism','Oil','womengarden.jpg'),
(13,7,'Old Guitarist',1904,'Modern','Oil','guitarist.jpg');

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