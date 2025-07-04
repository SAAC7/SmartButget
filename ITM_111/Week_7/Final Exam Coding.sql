Use world;
-- Q1 Write a query to show the country and population of all countries with population smaller than 5 million. Sort the list by population with the largest population first. What is the fifth country on your list?
select cy.Name, cy.Population
FROM country cy
WHERE cy.Population < 5000000
ORDER BY cy.Population DESC
LIMIT 5;

-- Write a query to show a list of the unique languages in the countrylanguage table. Sort the list in alphabetical order. What is the fifth language in your list? 
SELECT DISTINCT Language
FROM countrylanguage
ORDER BY Language ASC
LIMIT 5;

-- Write a query to list the continents and the number of countries in each continent.  How many countries are in North America? 
SELECT cy.Continent, COUNT(*) as Num_countries
FROM country cy
GROUP BY cy.Continent;

-- Write a query that shows the columns (with specified labels):
-- Country - the name of the country
-- Avg_Population_of_Cities - the average population of the cities of that country
-- Sort the results by the largest population average first.
-- What is the average population of the cities of Liberia?
SELECT cy.Name as Country, avg(ci.Population) as Average_of_population_of_Cities
from country cy
JOIN city ci ON cy.Code = ci.CountryCode
WHERE cy.Name = 'Liberia'
GROUP BY cy.Name 
ORDER BY Average_of_population_of_Cities DESC;


