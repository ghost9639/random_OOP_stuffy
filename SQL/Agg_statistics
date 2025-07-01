/*
WSDA music is a database of tracks sold by a company, turned into a typical relational database

This query groups average spending amount per customer in each city, and digs for the highest spenders

City - names of cities 
AverageSpending - average spent by customers
ordered by city name 
from invoice
results grouped by city 
only cities with averages greater than 5.40 shown
averages rounded to 2 d.p.
*/

SELECT 
	BillingCity AS City,
	round(avg(Total),2) AS AverageSpending -- rounds average spending for readability

FROM 
	Invoice 
	
GROUP BY 
	BillingCity
	
HAVING  -- GROUP BY and HAVING replace WHERE with respect to aggregate statistics 
	AverageSpending > 5.4
	
ORDER BY   -- orders by city names (default descending)
	BillingCity
