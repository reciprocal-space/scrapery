import sqlite3

class __BaseDatabase:
    def __init__(self, logger=print):
        self.log=logger
        
    def closeConnection(self):
        self.connection.close()

    def connect(self, databaseName):
        try:
            self.databaseName = databaseName
            self.connection = sqlite3.connect(databaseName)
        except Exception as e:
            self.log.error('Something went wrong while connecting to the database: ' + str(e))
        

    def read(self, query, values=None):
        try:
            with self.connection as c:
                if values == None:
                    return c.execute(query).fetchall()
                else:
                    
                    result = c.execute(query, values).fetchall()
                    return result
        except Exception as e:
            self.log.error('Something went wrong while reading from the database: ' + str(e))
            
    def write(self, query, values=None):
        try:
            with self.connection as c:
                if values == None:
                    return c.execute(query)
                else:
                    return c.execute(query, values)
        except Exception as e:
            self.log.error('Something went wrong while writing to the database: ' + str(e))

    def writeBatch(self, query, values=None):
        try:
            with self.connection as c:
                if values == None:
                    return c.executemany(query)
                else:
                    return c.executemany(query, values)
        except Exception as e:
            self.log.error('Something went wrong while batch writing to the database: ' + str(e))

    def writeScript(self, query, values=None):
        try:
            with self.connection as c:
                if values == None:
                    return c.executescript(query)
                else:
                    return c.executescript(query, values)
        except Exception as e:
            self.log.error('Something went wrong while writing script to the database: ' + str(e))



