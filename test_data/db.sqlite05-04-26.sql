BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(50) NOT NULL,
	"username"	VARCHAR(50) NOT NULL,
	"email"	VARCHAR(50) NOT NULL,
	"password"	VARCHAR(50) NOT NULL,
	PRIMARY KEY("id"),
	UNIQUE("email"),
	UNIQUE("username")
);
CREATE TABLE IF NOT EXISTS "quadrants" (
	"id"	INTEGER NOT NULL,
	"quadrant_summary"	VARCHAR NOT NULL,
	"quadrant_css_class"	VARCHAR NOT NULL,
	"quadrant_elem_coords"	VARCHAR NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "competencies" (
	"id"	INTEGER NOT NULL,
	"user_id"	INTEGER NOT NULL,
	"quadrant"	INTEGER,
	"sector"	INTEGER,
	"rating"	INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("user_id") REFERENCES "users"("id")
);
CREATE TABLE IF NOT EXISTS "sectors" (
	"id"	INTEGER NOT NULL,
	"quadrant_id"	INTEGER NOT NULL,
	"summary"	VARCHAR NOT NULL,
	"description"	VARCHAR NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY("quadrant_id") REFERENCES "quadrants"("id")
);
CREATE TABLE IF NOT EXISTS "sector_titles" (
	"id"	INTEGER NOT NULL,
	"sector_id"	INTEGER NOT NULL,
	"title_part"	VARCHAR NOT NULL,
	"coord_x"	INTEGER NOT NULL,
	"coord_y"	INTEGER NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY("sector_id") REFERENCES "sectors"("id")
);
CREATE TABLE IF NOT EXISTS "quadrant_titles" (
	"id"	INTEGER NOT NULL,
	"quadrant_id"	INTEGER NOT NULL,
	"title_part"	VARCHAR NOT NULL,
	"coord_x"	INTEGER NOT NULL,
	"coord_y"	INTEGER NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY("quadrant_id") REFERENCES "quadrants"("id")
);
CREATE TABLE IF NOT EXISTS "rating_description" (
	"id"	INTEGER NOT NULL,
	"title"	VARCHAR NOT NULL,
	"description"	VARCHAR NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "rating" (
	"id"	INTEGER NOT NULL,
	"title"	VARCHAR NOT NULL,
	"description"	VARCHAR NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "compass_definition" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR NOT NULL,
	"quadrant_1"	INTEGER NOT NULL,
	"quadrant_2"	INTEGER NOT NULL,
	"quadrant_3"	INTEGER NOT NULL,
	"quadrant_4"	INTEGER NOT NULL,
	"quadrant_1_sector_1"	INTEGER NOT NULL,
	"quadrant_1_sector_2"	INTEGER NOT NULL,
	"quadrant_1_sector_3"	INTEGER NOT NULL,
	"quadrant_1_sector_4"	INTEGER NOT NULL,
	"quadrant_1_sector_5"	INTEGER NOT NULL,
	"quadrant_2_sector_1"	INTEGER NOT NULL,
	"quadrant_2_sector_2"	INTEGER NOT NULL,
	"quadrant_2_sector_3"	INTEGER NOT NULL,
	"quadrant_2_sector_4"	INTEGER NOT NULL,
	"quadrant_3_sector_1"	INTEGER NOT NULL,
	"quadrant_3_sector_2"	INTEGER NOT NULL,
	"quadrant_3_sector_3"	INTEGER NOT NULL,
	"quadrant_3_sector_4"	INTEGER NOT NULL,
	"quadrant_4_sector_1"	INTEGER NOT NULL,
	"quadrant_4_sector_2"	INTEGER NOT NULL,
	"quadrant_4_sector_3"	INTEGER NOT NULL,
	"quadrant_4_sector_4"	INTEGER NOT NULL,
	"rating_1"	INTEGER NOT NULL,
	"rating_2"	INTEGER NOT NULL,
	"rating_3"	INTEGER NOT NULL,
	"rating_4"	INTEGER NOT NULL,
	"rating_5"	INTEGER NOT NULL,
	"rating_6"	INTEGER NOT NULL,
	"rating_7"	INTEGER NOT NULL,
	FOREIGN KEY("rating_7") REFERENCES "rating"("id"),
	FOREIGN KEY("rating_6") REFERENCES "rating"("id"),
	PRIMARY KEY("id"),
	FOREIGN KEY("rating_4") REFERENCES "rating"("id"),
	FOREIGN KEY("rating_5") REFERENCES "rating"("id"),
	FOREIGN KEY("quadrant_4_sector_3") REFERENCES "sectors"("id"),
	FOREIGN KEY("quadrant_1") REFERENCES "quadrants"("id"),
	FOREIGN KEY("quadrant_2_sector_4") REFERENCES "sectors"("id"),
	FOREIGN KEY("quadrant_3_sector_1") REFERENCES "sectors"("id"),
	FOREIGN KEY("quadrant_2") REFERENCES "quadrants"("id"),
	FOREIGN KEY("quadrant_4_sector_4") REFERENCES "sectors"("id"),
	FOREIGN KEY("quadrant_3_sector_2") REFERENCES "sectors"("id"),
	FOREIGN KEY("rating_1") REFERENCES "rating"("id"),
	FOREIGN KEY("quadrant_3_sector_3") REFERENCES "sectors"("id"),
	FOREIGN KEY("quadrant_3_sector_4") REFERENCES "sectors"("id"),
	FOREIGN KEY("quadrant_4_sector_1") REFERENCES "sectors"("id"),
	FOREIGN KEY("quadrant_4_sector_2") REFERENCES "sectors"("id"),
	FOREIGN KEY("quadrant_2_sector_3") REFERENCES "sectors"("id"),
	FOREIGN KEY("quadrant_1_sector_1") REFERENCES "sectors"("id"),
	FOREIGN KEY("quadrant_1_sector_2") REFERENCES "sectors"("id"),
	FOREIGN KEY("quadrant_1_sector_3") REFERENCES "sectors"("id"),
	FOREIGN KEY("rating_3") REFERENCES "rating"("id"),
	FOREIGN KEY("quadrant_1_sector_4") REFERENCES "sectors"("id"),
	FOREIGN KEY("quadrant_3") REFERENCES "quadrants"("id"),
	FOREIGN KEY("quadrant_1_sector_5") REFERENCES "sectors"("id"),
	FOREIGN KEY("quadrant_2_sector_1") REFERENCES "sectors"("id"),
	FOREIGN KEY("quadrant_2_sector_2") REFERENCES "sectors"("id"),
	FOREIGN KEY("quadrant_4") REFERENCES "quadrants"("id"),
	FOREIGN KEY("rating_2") REFERENCES "rating"("id")
);
INSERT INTO "users" VALUES (1,'han solo','silas','silas@m.c','pwd');
INSERT INTO "users" VALUES (2,'bob','bob','bob@s.f','pwd');
INSERT INTO "users" VALUES (3,'herbert2','string','herbert@example.com','string');
INSERT INTO "quadrants" VALUES (1,'q','a','a');
INSERT INTO "quadrants" VALUES (2,'summary green','green','807,92,806,174,1010,184,1005,68');
INSERT INTO "quadrants" VALUES (3,'summary blue','blue','818,693,816,761,1020,771,1022,669');
INSERT INTO "quadrants" VALUES (4,'summary red','red','45,663,211,689,207,770,45,783');
INSERT INTO "quadrants" VALUES (5,'summary yellow','yellow','38,85,237,90,242,177,46,195');
INSERT INTO "quadrants" VALUES (6,'string','green','string');
INSERT INTO "competencies" VALUES (1,1,3,3,4);
INSERT INTO "competencies" VALUES (2,1,0,4,2);
INSERT INTO "competencies" VALUES (3,1,1,1,5);
INSERT INTO "competencies" VALUES (4,1,2,2,3);
INSERT INTO "competencies" VALUES (5,2,2,3,6);
INSERT INTO "competencies" VALUES (6,2,2,2,2);
INSERT INTO "competencies" VALUES (7,2,2,1,6);
INSERT INTO "competencies" VALUES (8,2,2,0,6);
INSERT INTO "competencies" VALUES (9,2,0,3,1);
INSERT INTO "competencies" VALUES (10,1,3,1,4);
INSERT INTO "competencies" VALUES (11,1,1,3,6);
INSERT INTO "competencies" VALUES (12,1,1,2,6);
INSERT INTO "competencies" VALUES (13,1,1,0,6);
INSERT INTO "competencies" VALUES (14,1,0,1,6);
INSERT INTO "competencies" VALUES (15,1,2,1,6);
INSERT INTO "competencies" VALUES (16,3,2,3,5);
INSERT INTO "competencies" VALUES (17,2,3,2,5);
INSERT INTO "competencies" VALUES (18,2,1,1,6);
INSERT INTO "competencies" VALUES (19,2,0,4,4);
INSERT INTO "competencies" VALUES (20,3,3,3,6);
INSERT INTO "competencies" VALUES (21,1,2,3,6);
INSERT INTO "sectors" VALUES (1,1,'a','a');
INSERT INTO "sectors" VALUES (2,1,'b','b');
INSERT INTO "sectors" VALUES (3,1,'bc','cb');
INSERT INTO "sectors" VALUES (4,1,'bcd','cdb');
INSERT INTO "sector_titles" VALUES (1,1,'fishXXX',0,0);
INSERT INTO "sector_titles" VALUES (2,1,'foodYYY',0,0);
INSERT INTO "sector_titles" VALUES (3,2,'fishb',646,140);
INSERT INTO "sector_titles" VALUES (4,2,'foodb',646,155);
INSERT INTO "sector_titles" VALUES (5,3,'fishc',828,383);
INSERT INTO "sector_titles" VALUES (6,3,'foodc',828,398);
INSERT INTO "sector_titles" VALUES (7,4,'fishd',837,510);
INSERT INTO "sector_titles" VALUES (8,4,'foodd',837,525);
INSERT INTO "quadrant_titles" VALUES (1,2,'fishy',0,0);
INSERT INTO "quadrant_titles" VALUES (2,2,'chips',829,153);
INSERT INTO "quadrant_titles" VALUES (3,3,'bum',835,720);
INSERT INTO "quadrant_titles" VALUES (4,3,'girdle',835,748);
INSERT INTO "quadrant_titles" VALUES (5,4,'heavy',60,720);
INSERT INTO "quadrant_titles" VALUES (6,4,'metal',60,748);
INSERT INTO "quadrant_titles" VALUES (7,5,'gigantic',60,132);
INSERT INTO "quadrant_titles" VALUES (8,5,'fart',60,160);
INSERT INTO "rating" VALUES (1,'unrated','no rating has been chosen yet');
INSERT INTO "rating" VALUES (2,'complete numptie','crap at everything');
INSERT INTO "rating" VALUES (3,'complete noob','plays on ITYTD');
INSERT INTO "rating" VALUES (4,'jobbing','plays on HMP');
INSERT INTO "rating" VALUES (5,'getting there','plays on UV');
INSERT INTO "rating" VALUES (6,'doom god','plays on NIGHTMARE!!');
INSERT INTO "rating" VALUES (7,'THOR','the god of THUNDER');
INSERT INTO "rating" VALUES (8,'sort of OK','big long descriptive string');
INSERT INTO "compass_definition" VALUES (1,'fishone',1,2,3,4,1,2,1,2,3,3,4,3,4,1,3,2,4,4,1,2,3,1,2,3,4,5,6,7);
INSERT INTO "compass_definition" VALUES (2,'string',2,3,4,5,1,2,3,4,1,1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,5,8,7);
INSERT INTO "compass_definition" VALUES (3,'test4',2,2,2,2,1,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,1,2,2,2,2,3,4);
INSERT INTO "compass_definition" VALUES (4,'strings',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
COMMIT;
