CREATE DATABASE IF NOT EXISTS indie;

USE indie;

CREATE TABLE IF NOT EXISTS albums(
    AlbumID INT NOT NULL AUTO_INCREMENT KEY,
    AlbumName VARCHAR(128),
    AlbumURL VARCHAR(512) NOT NULL,
    AuthorID INT,
    Price INT,
    ReleaseDate VARCHAR(128),
    RecommendedAlbumURL VARCHAR(128));

CREATE TABLE IF NOT EXISTS artists(
    ArtistsID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    ArtistName VARCHAR(128));
