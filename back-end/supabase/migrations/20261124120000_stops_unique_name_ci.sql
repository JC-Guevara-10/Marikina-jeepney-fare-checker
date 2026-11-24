-- Stop names are unique ignoring case and surrounding spaces.
-- Fails if existing stops collide; rename or merge them first.
create unique index stops_name_ci_key on stops (lower(btrim(name)));
