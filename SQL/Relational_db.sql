/* 

WSDA music is a database containing information about sales for tracks, stored in a typical stata relational database

Request:
list including track ID, track name, composer and genre 
ordered track name ascending 
tracks aliased as track = t, invoiceline - li, genre - g

specifically looking for unique tracks that never sell

*/

SELECT                   -- specifically want this information about the tracks
	t.TrackId AS "Track ID",
	t.Name AS "Track Name",
	t.Composer AS "Track Composer",
	g.Name AS "Genre"


	
FROM 
	Track AS t
INNER JOIN 
	Genre AS g
ON 
	t.GenreId = g.GenreId   -- genre needed since it's not stored on track list

WHERE 
	t.TrackId
NOT IN
(SELECT -- subquery digging for shared individual tracks between the invoice and tracks lists
	DISTINCT
	il.TrackId
FROM 
	InvoiceLine AS il
INNER JOIN 
	Track AS t
ON 
	il.TrackId = t.TrackId)  -- overall looking for tracks that aren't on the union of sold tracks and database tracks
	
ORDER BY 
	t.Name ASC  #organised by name "za%" first

