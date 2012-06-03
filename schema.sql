DROP TABLE IF EXISTS entries;
CREATE TABLE entries (
  id integer primary key autoincrement,
  title string not null,
  text string not null
);
