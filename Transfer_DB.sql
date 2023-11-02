CREATE TABLE `School` (
	`OrgCode`	TEXT,
	`College`	TEXT,
	`TwoOrFourYear`	INTEGER,
	PRIMARY KEY(`OrgCode`)
);

CREATE TABLE `Course` (
	`CrsID`	INTEGER,
	`OrgCode`	TEXT,
	`CrsCode`	TEXT,
	`CrsName`	TEXT,
	`CreditHours`	INTEGER,
	`GrdCode`	TEXT,
	constraint PKCourse PRIMARY KEY(`CrsID`),
    constraint FKCourseOrg FOREIGN KEY(`OrgCode`) REFERENCES `School`(`OrgCode`)
);

CREATE TABLE `ARC` (
    `ARCCode` TEXT PRIMARY KEY
);

CREATE TABLE `Equivalence` (
    `CrsID`      INTEGER,
    `ARCCode`       TEXT,
    `TYear`         TEXT,
    `TTerm`         TEXT,
    `CreditType`    TEXT,
    constraint PKEquiv PRIMARY KEY(`CrsID`, `ARCCode`),
    constraint FKEqCrs FOREIGN KEY(`CrsID`) REFERENCES `Course`(`CrsID`),
    constraint FKEqARC FOREIGN KEY(`ARCCode`) REFERENCES `ARC`(`ARCCode`)
);
