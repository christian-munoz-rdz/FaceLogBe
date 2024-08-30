# start transaction;

START TRANSACTION;

# drop tables

DROP TABLE IF EXISTS `photo_embeddings`;
DROP TABLE IF EXISTS `time_records`;
DROP TABLE IF EXISTS `user_photos`;
DROP TABLE IF EXISTS `roles`;
DROP TABLE IF EXISTS `user_codes`;
DROP TABLE IF EXISTS `area_users`;
DROP TABLE IF EXISTS `areas`;
DROP TABLE IF EXISTS `tickets`;
DROP TABLE IF EXISTS `users`;

# create tables

CREATE TABLE `photo_embeddings`
(
    `id`            integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `user_photo_id` integer,
    `dimension`     int,
    `value`         double
);

CREATE TABLE `user_photos`
(
    `id`         integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `user_id`    integer,
    `photo`      mediumblob,
    `type`       varchar(255) COMMENT 'PROFILE | SYSTEM ',
    `created_at` datetime
);

CREATE TABLE `roles`
(
    `id`          integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `role`        varchar(255) COMMENT 'SUPERUSER | DEVELOPER | WRITER | REGULAR | NONE ',
    `description` varchar(255)
);

CREATE TABLE `users`
(
    `id`         integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `role_id`    integer,
    `name`       varchar(255),
    `email`      varchar(255) UNIQUE,
    `created_at` timestamp
);

CREATE TABLE `user_codes`
(
    `id`       integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `user_id`  integer,
    `code`     varchar(255) UNIQUE,
    `category` varchar(255) COMMENT 'TEACHER | STUDENT | RECTOR | ADMINISTRATIVE | VOLUNTEER'
);

CREATE TABLE `area_users`
(
    `id`        integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `area_id`   integer,
    `user_id`   integer,
    `user_type` varchar(255) COMMENT 'SUPERVISOR | PRACTITIONER | INTERN | VOLUNTEER | GUEST | TEACHER_VISITOR | TEACHER_ASSIGNED | ADMINISTRATIVE'
);

CREATE TABLE `areas`
(
    `id`          integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `name`        varchar(255) UNIQUE,
    `description` varchar(255),
    `module`      varchar(255),
    `classroom`   varchar(255),
    `campus`      varchar(255),
    `department`  varchar(255),
    `division`    varchar(255),
    `image`       mediumblob
);

CREATE TABLE `tickets`
(
    `id`          integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `area_id`     integer,
    `created_by`  integer,
    `title`       varchar(255) COMMENT 'small description of the ticket',
    `description` varchar(255),
    `status`      varchar(255) COMMENT 'CREATED | APPROVED | DENIED',
    `created_at`  timestamp
);

CREATE TABLE `time_records`
(
    `id`             integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `user_id`        integer,
    `area_id`        integer,
    `enter_photo_id` integer,
    `exit_photo_id`  integer,
    `created_at`     timestamp,
    `entered_at`     timestamp           NOT NULL,
    `exited_at`      timestamp
);

ALTER TABLE `photo_embeddings`
    ADD FOREIGN KEY (`user_photo_id`) REFERENCES `user_photos` (`id`);

ALTER TABLE `user_photos`
    ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `users`
    ADD FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`);

ALTER TABLE `user_codes`
    ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `area_users`
    ADD FOREIGN KEY (`area_id`) REFERENCES `areas` (`id`);

ALTER TABLE `area_users`
    ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `tickets`
    ADD FOREIGN KEY (`area_id`) REFERENCES `areas` (`id`);

ALTER TABLE `tickets`
    ADD FOREIGN KEY (`created_by`) REFERENCES `users` (`id`);

ALTER TABLE `time_records`
    ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `time_records`
    ADD FOREIGN KEY (`area_id`) REFERENCES `areas` (`id`);

ALTER TABLE `time_records`
    ADD FOREIGN KEY (`enter_photo_id`) REFERENCES `user_photos` (`id`);

ALTER TABLE `time_records`
    ADD FOREIGN KEY (`exit_photo_id`) REFERENCES `user_photos` (`id`);

#insert data

#table roles
INSERT INTO `roles` (`role`, `description`)
VALUES ('SUPERUSER', 'Super User'),
       ('DEVELOPER', 'Developer'),
       ('WRITER', 'Writer'),
       ('REGULAR', 'Regular'),
       ('NONE', 'None');

#table areas
INSERT INTO `areas` (`name`, `description`, `module`, `classroom`, `campus`, `department`, `division`)
VALUES ('iLabTDI', 'La mejor area de todas claro que si', 'N', '001', 'CUCEI', 'Ingenierias', 'DIVEC');

# end transaction
COMMIT;
