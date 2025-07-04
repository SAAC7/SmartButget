-- ------------------------------
-- Database: v_art
-- ------------------------------
USE v_art;
-- Query 1: Insert the artist Johannes Vermeer
INSERT INTO artist (
    fname,
    mname,
    lname,
    dob,
    dod,
    country,
    local
) VALUES (
    'Johannes',
    null,
    'Vermeer',
    1632,
    1674,
    'Netherlands',
    'N'
);

-- Query 2:
SELECT *
FROM artist
ORDER BY lname;

-- Query 3:
UPDATE artist
SET dod = 1675
WHERE fname = 'Johannes'
  AND lname = 'Vermeer';

-- Query 4: Eliminar a Johannes Vermeer de la base de datos
DELETE
FROM artist
WHERE fname = 'Johannes'
  AND lname = 'Vermeer';


-- ------------------------------
-- Data Base: bike
-- ------------------------------

USE bike;

-- Query 5: 
SELECT
    first_name,
    last_name,
    phone
FROM customer
WHERE city = 'Houston'
  AND state = 'TX';
  

-- Query 6:
SELECT
    product_name,
    list_price,
    (list_price - 500) AS `Discount Price`
FROM product
WHERE list_price >= 5000
ORDER BY list_price DESC;

-- Query 7:
SELECT
    first_name,
    last_name,
    email
FROM staff
WHERE store_id <> 1;

-- Query 8:
SELECT
    product_name,
    model_year,
    list_price
FROM product
WHERE product_name LIKE '%spider%';

-- Query 9:
SELECT
    product_name,
    list_price
FROM product
WHERE list_price BETWEEN 500 AND 550
ORDER BY list_price ASC;

-- Query 10: 
SELECT
    first_name,
    last_name,
    phone,
    street,
    city,
    state,
    zip_code
FROM customer
WHERE phone IS NOT NULL
  AND (
        city LIKE '%ach%'
     OR city LIKE '%och%'
    
  )
   OR last_name = 'William'
LIMIT 5;

-- Query 11:
SELECT
    REGEXP_REPLACE(
      product_name,
      '( - [0-9]{4}/[0-9]{4}| [0-9]{4}( [0-9]{4})?| - [0-9]{4})$',
      ''
    ) AS product_name_without_year
FROM product
ORDER BY product_id
LIMIT 14;

-- Query 12:
SELECT
    product_name,
    CONCAT('$', FORMAT(list_price / 3, 2)) AS payment
FROM product
WHERE model_year = 2019;


-- ------------------------------
-- Data Base: magazine
-- ------------------------------

USE magazine;

-- Query 13:
SELECT
    magazineName,
    ROUND(magazinePrice * 0.97, 2) AS '3% off'
FROM magazine;

-- Query 14:
SELECT
    subscriptionKey,
    ROUND(
      DATEDIFF('2020-12-20', subscriptionStartDate) / 365.0,
      0
    ) AS 'Years since subscription'
FROM subscription;

-- Query 15: 
SELECT
    subscriptionStartDate,
    subscriptionLength,
    DATE_FORMAT(
      DATE_ADD(subscriptionStartDate, INTERVAL subscriptionLength MONTH),
      '%M %e, %Y'
    ) AS 'Subscription end'
FROM subscription;
