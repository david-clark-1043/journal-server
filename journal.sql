CREATE TABLE `Moods` (
    `id`  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `label`  TEXT NOT NULL
);

CREATE TABLE `Entries` (
	`id`  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`concept`  TEXT NOT NULL,
	`entry` TEXT NOT NULL,
	`mood_id` INTEGER NOT NULL,
	`date` TEXT NOT NULL,
	FOREIGN KEY(`mood_id`) REFERENCES `Moods`(`id`)
);

CREATE TABLE `Tags` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `label` TEXT NOT NULL
);

CREATE TABLE `EntryTags` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `entry_id` INTEGER NOT NULL,
    `tag_id` INTEGER NOT NULL,
    FOREIGN KEY(`entry_id`) REFERENCES `Entries`(`id`),
    FOREIGN KEY(`tag_id`) REFERENCES `Tags`(`id`)
);

INSERT INTO `Entries` VALUES (null, "Javascript", "Test JS Entry", 1, "Wed Sep 15 2021 10:10:47 ");
INSERT INTO `Entries` VALUES (null, "Python", "Test Python Entry", 2, "Wed Sep 15 2021 10:11:33 ");

INSERT INTO `Moods` VALUES (null, "Happy");
INSERT INTO `Moods` VALUES (null, "Sad");

INSERT INTO `Tags` VALUES (null, "Javascript");
INSERT INTO `Tags` VALUES (null, "Python");
INSERT INTO `Tags` VALUES (null, "React");
INSERT INTO `Tags` VALUES (null, "SQL");

INSERT INTO `EntryTags` VALUES (null, 1, 1);
INSERT INTO `EntryTags` VALUES (null, 1, 3);
INSERT INTO `EntryTags` VALUES (null, 2, 2);
INSERT INTO `EntryTags` VALUES (null, 2, 4);

SELECT * FROM EntryTags;

-- DROP TABLE if exists `TestData`;

-- CREATE TABLE `TestData` (
--     `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
-- );
-- CREATE TABLE `TestData2` (
--     `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
--     `first_id` INTEGER,
--     FOREIGN KEY(`first_id`) REFERENCES `TestData`(`id`)
-- );

-- CREATE TABLE `TestData2` ();

