"""
module provides facilities for saving data
"""

#import mysql.connector as mysql
import json


class FileSaver:
    """
    Writes album data as json to a file.
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.__reset()

    def __reset(self):
        """
        Clears the file for a new run
        """
        open(self.file_path, 'w').close()

    def insert(self, album_data):
        """
        Append album data to file
        writes each json object on one line
        """
        with open(self.file_path, 'a') as f:
            json.dump(album_data, fp=f)
            f.write('\n')


class DBSaver:
    """
    Used to simplify insertion into indie song database
    schema is sql/album_schema.sql
    """

    def __init__(self, database):
        self.db = mysql.connect(host='localhost',
                                user='arthur',
                                passwd='Wolfie2005',
                                database=database)

    def insert(self, data):
        self.insert_needed_data(data['author'], data['album'], data['album_url'],
                                data['album_data']['price'],
                                data['album_data']['release_date'],
                                data['recommended_albums'])

    def insert_needed_data(self, author, album_name, album_url, price, release_data,
                           recommended_album_urls):
        """
        insert an entry into database for each recommendation. 
        """
        if not self.author_in_table(author):
            cursor = self.db.cursor()
            insert_artist = '''
                INSERT INTO artists (ArtistName) VALUES (%s)
            '''
            print(author)
            cursor.execute(insert_artist, (author, ))
        print(recommended_album_urls)
        for rec_url in recommended_album_urls:
            self.insert_album_rec(author, album_name, album_url, price,
                                  release_data, rec_url)
        self.db.commit()


    def author_in_table(self, author):
        """
        function checks if author is in the artists table. 
        cursor has an iterator of items that where returned by the query.
        if a single iteration of the loop occurs, then the author is in
        the table. Otherwise, the author is not in the table. 
        """
        cursor = self.db.cursor()
        author_query = '''
            select ArtistName from artists where ArtistName = (%s)
        '''
        cursor.execute(author_query, (author, ))
        for item in cursor:
            return True
        return False

    def author_ID(self, author):
        """
        given the artist's name, retrieves the artist's id from database. 
        We know the author must be in the database already because we check
        before we insert the album. We also know there is only one occurence.
        So, we can just query for artistsID and return the first name in
        cursors iterator. 
        """
        cursor = self.db.cursor()
        author_ID_query = '''
            select ArtistsID from artists where ArtistName = (%s)
        '''
        cursor.execute(author_ID_query, (author, ))
        for item in cursor:
            return item

    def insert_album_rec(self, author, album_name, album_url, price,
                         release_date, recommended_album_url):
        """
        inserts data into the database. 
        """
        author_ID = self.author_ID(author)[0]
        print(author_ID)
        cursor = self.db.cursor()
        insert_album = '''
            INSERT INTO albums
            (AlbumName, AlbumURL, AuthorID, Price, ReleaseDate, 
             RecommendedAlbumURL)
            VALUES (%s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(insert_album, (album_name, album_url, author_ID, price,
                                      release_date, recommended_album_url))
