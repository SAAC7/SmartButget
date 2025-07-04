Use v_art;
-- Question 1: Search by Period/Style = 'Impressionism'
SELECT artfile FROM artwork
WHERE period = "Impressionism";

-- Question 2: Search by Subject with keyword 'flower'
SELECT ar.artfile 
FROM keyword k INNER JOIN artwork_keyword ak
ON ak.keyword_id = k.keyword_id
INNER JOIN artwork ar
ON ak.artwork_id = ar.artwork_id 
WHERE k.keyword LIKE "%flower%";

-- Question 3: List artists (first, last name) and related artwork titles
SELECT ar.fname First_Name, ar.lname Last_Name, aw.title Title
FROM artist ar LEFT JOIN artwork aw
ON ar.artist_id = aw.artist_id;

-- Question 4: Subscriptions with magazine name, last name, first name
USE magazine;
SELECT m.magazineName,sr.subscriberLastName, sr.subscriberFirstName
FROM magazine m INNER JOIN subscription sn
ON m.magazineKey = sn.magazineKey
LEFT JOIN subscriber sr
ON sn.subscriberKey = sr.subscriberKey 
ORDER BY m.magazineName;

-- Question 5: Magazines subscribed to by Samantha Sanders
SELECT m.magazineName
FROM magazine m INNER JOIN subscription sn
ON m.magazineKey = sn.magazineKey
LEFT JOIN subscriber sr
ON sn.subscriberKey = sr.subscriberKey 
WHERE sr.subscriberLastName = "Sanders" AND sr.subscriberFirstName = "Samantha"
ORDER BY m.magazineName;

-- Question 6: First five employees from Customer Service, ordered by last name
USE employees;
SELECT es.first_name, es.last_name
from employees es INNER JOIN dept_emp dp
ON es.emp_no = dp.emp_no
INNER JOIN departments ds
ON dp.dept_no = ds.dept_no
WHERE ds.dept_name like "%Customer Service%"
ORDER BY es.last_name
LIMIT 5;

-- Question 7: Current salary and department of Berni Genin (most recent)
SELECT es.first_name, es.last_name, ds.dept_name, ss.salary, ss.from_date
from employees es INNER JOIN dept_emp dp
ON es.emp_no = dp.emp_no
INNER JOIN departments ds
ON dp.dept_no = ds.dept_no
LEFT JOIN salaries ss
ON ss.emp_no = es.emp_no
WHERE es.first_name="Berni" AND es.last_name="Genin"
ORDER BY ss.from_date DESC
LIMIT 1;

-- Question 8: Average quantity in bike stocks, rounded
USE bike;
SELECT ROUND(AVG(quantity)) as avg_stock
FROM stock;

-- Question 9: Bikes that need to be reordered (quantity = 0, distinct)
SELECT DISTINCT p.product_name 
FROM stock s
JOIN product p ON s.product_id = p.product_id
WHERE s.quantity = 0
ORDER BY p.product_name;

-- Question 10: Inventory per category at store_id = 2 (Baldwin Bikes)
SELECT cy.category_name, SUM(sk.quantity) AS inventory
FROM stock sk
JOIN product pt ON sk.product_id = pt.product_id
JOIN category cy ON pt.category_id = cy.category_id
WHERE sk.store_id = 2
GROUP BY cy.category_name
ORDER BY inventory;

-- Question 11: Total number of employees
USE employees;
SELECT COUNT(*) AS total_employees 
FROM employees;

-- Question 12: Average salaries < 60,000 by department (formatted)
SELECT 
    ds.dept_name, FORMAT(AVG(ss.salary), 2) AS avg_salary 
FROM departments ds LEFT JOIN dept_emp dp
ON ds.dept_no = dp.dept_no
INNER JOIN salaries ss
ON dp.emp_no = ss.emp_no
GROUP BY ds.dept_name
HAVING AVG(ss.salary) < 60000
order by ds.dept_name;

-- Question 13: Number of females in each department
SELECT 
    ds.dept_name,
    COUNT(*) AS female_count 
FROM employees es JOIN dept_emp dp
ON es.emp_no = dp.emp_no
JOIN departments ds
ON dp.dept_no = ds.dept_no
WHERE es.gender = 'F'
GROUP BY ds.dept_name
ORDER BY ds.dept_name;