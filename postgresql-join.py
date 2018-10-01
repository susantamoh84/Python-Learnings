SELECT c.code, name, region, e.year, fertility_rate, unemployment_rate
FROM countries AS c
INNER JOIN populations AS p
ON c.code = p.country_code
INNER JOIN economies AS e
ON c.code=e.code AND e.year=p.year;

SELECT c.name AS country, c.continent, l.name AS language, l.official
FROM countries AS c
inner JOIN languages AS l
USING(code);

SELECT p1.country_code,
       p1.size AS size2010, 
       p2.size AS size2015,
       ((p2.size - p1.size)/p1.size * 100.0) AS growth_perc
FROM populations AS p1
INNER JOIN populations AS p2
ON p1.country_code = p2.country_code
    AND p1.year = p2.year - 5;

SELECT name, continent, code, surface_area,
        -- first case
    CASE WHEN surface_area > 2000000 THEN 'large'
        -- second case
        WHEN surface_area > 350000 THEN 'medium'
        -- else clause + end
        ELSE 'small' END
        AS geosize_group
FROM countries;

-- Select region, average gdp_percapita (alias avg_gdp)
SELECT region, AVG(gdp_percapita) as avg_gdp
-- From countries (alias c) on the left
FROM countries AS c
-- Join with economies (alias e)
LEFT JOIN economies AS e
-- Match on code fields
ON c.code = e.code
-- Focus on 2010 
WHERE e.year = 2010
-- Group by region
GROUP BY region;

SELECT name AS country, code, region, basic_unit
FROM countries
INNER JOIN currencies
USING (code)
WHERE region = 'North America' OR region IS NULL
ORDER BY region;

SELECT c1.name AS country, region, l.name AS language ,
       c2.basic_unit, c2.frac_unit
FROM countries AS c1
FULL JOIN languages AS l
USING (code)
FULL JOIN currencies AS c2
USING (code)
WHERE c1.region LIKE 'M%esia';

-- pick specified columns from 2010 table
select *
-- 2010 table will be on top
from economies2010
-- which set theory clause?
union
-- pick specified columns from 2015 table
select *
-- 2015 table on the bottom
from  economies2015
-- order accordingly
order by code, year;

select country_code from cities
union
select code as country_code from currencies
order by country_code;

SELECT code, year
FROM economies
union all
SELECT country_code, year
FROM populations
ORDER BY code, year;

select code, year
from economies
INTERSECT
select country_code, year
from populations
order by code, year;

select max(inflation_rate) as max_inf
from (select name, continent, inflation_rate
from countries
inner join economies
using (code)
where year=2015) subquer
group by continent;

SELECT DISTINCT name, total_investment, imports
FROM countries AS c
LEFT JOIN economies AS e
ON (c.code = e.code
  AND c.code IN (
    SELECT l.code
    FROM languages AS l
    WHERE official = 'true'
  ) )
WHERE c.region = 'Central America' AND e.year = 2015
ORDER BY name;

-- choose fields
SELECT region, continent, avg(fertility_rate) AS avg_fert_rate
-- left table
FROM populations AS p
-- right table
INNER JOIN countries AS c
-- join conditions
ON p.country_code = c.code
-- specific records matching a condition
WHERE p.year = 2015
-- aggregated for each what?
GROUP BY region, continent
-- how should we sort?
ORDER BY avg_fert_rate;

SELECT name, country_code, city_proper_pop, metroarea_pop,  
       city_proper_pop / metroarea_pop * 100 AS city_perc
FROM cities
WHERE name IN
  (SELECT capital
   FROM countries
   WHERE (continent = 'Europe'
      OR continent LIKE '%America%'))
     AND cities.metroarea_pop IS NOT NULL
ORDER BY city_perc desc
LIMIT 10;

