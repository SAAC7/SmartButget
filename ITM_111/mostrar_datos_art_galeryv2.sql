SELECT 
  at.first_name,
  a.title,
  a.type,
  GROUP_CONCAT(k.name ORDER BY k.name SEPARATOR ', ') AS keywords
FROM 
  art_gallery.artwork a
LEFT JOIN 
  art_gallery.artwork_has_keyword ak ON a.artwork_id = ak.artwork_artwork_id
LEFT JOIN 
  art_gallery.keyword k ON ak.keyword_keyword_id = k.keyword_id
left join
	art_gallery.artist at on a.artist_artist_id =  at.artist_id
group by
a.title,a.artwork_id
ORDER BY 
  a.artwork_id;
