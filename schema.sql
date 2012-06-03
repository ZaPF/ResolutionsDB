DROP TABLE IF EXISTS resolutions;
CREATE TABLE resolutions (
  id integer primary key autoincrement,
  title string not null,
  text string not null,
  kind string not null,
  passed_on string not null,
  entered_by string not null,
  entered_on string not null,
  wiki_url string,
  related_file string
);
