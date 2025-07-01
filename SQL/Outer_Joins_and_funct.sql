/*
WSDA is a relational database of information about music tracks sold by a company

Query wants the Full name of US customers, the first five digits of their post-codes, and the full name of their customer service reps
CustomerFullName concats first and last name
StandardizedPostalCode has postal code set to 5 digits
results from US buyers
ordered by customer full name
*/

SELECT
	c.FirstName || ' ' || c.LastName AS CustomerFullName, -- concatenates the first and last name of customers into a single column 
	substr(c.PostalCode,1,5) AS StandardizedPostalCode, -- only takes first five digits of US post code (the only crucial ones for a delivery here)
	e.FirstName || ' ' || e.LastName AS EmployeeLastName

FROM 
	Customer as c
LEFT OUTER JOIN    -- we want all customers, even if we don't have information on their reps, in this case there aren't any missing reps, but this query would give us all customers even if there wasn't a rep recorded for them
	Employee as e
ON 
	c.SupportRepId = e.EmployeeId  -- support rep id in the customer table and the employee id in the employee information table are the same
	
WHERE
	c.Country = 'USA'
	
ORDER BY 
	CustomerFullName
