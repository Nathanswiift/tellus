import MySQLdb
import functools
from config import TellusConfig

def connect(func):
    """Database decorator
    
    The decorator is being used whenever the developer wants  
    to make a query to the database.
    
    The decorator first opens a connection
    then executes the query togheter with the arguments
    and finally it closes the connection and returns the response
    """
    def wrapper(cls, query, *args):
        cls.conn = MySQLdb.connect(
            db=TellusConfig.DB_NAME,
            host=TellusConfig.DB_HOST,
            user=TellusConfig.DB_USER,
            passwd=TellusConfig.DB_PW,
            charset=TellusConfig.ENCODE
        )
        cls.cur = cls.conn.cursor()
        cls.cur.execute(query, *args)
        res = func(cls, query, *args)
        cls.close()
        return res
    return wrapper

class Database:
    def __new__(cls):
        # initialize these variables for precausion 
        # because otherwise a error will occur with most lints
        # and telling you that these variables are not defined 
        # within the classmethods
        cls.conn = None
        cls.cur = None

    @connect
    @classmethod
    def commit(cls, query, *args):
        """Commits the SQL query
        """
        cls.conn.commit()
        if cls.cur.rowcount > 0:
            return True
        else:
            return False

    @classmethod
    @connect
    def select_all(cls, query, *args):
        """Used when you want to select multiply rows 
        """
        return cls.cur.fetchall()

    
    @classmethod
    @connect
    def select_single(cls, query, *args):
        """Used when you want to select a single row 
        """
        return cls.cur.fetchone()

    @classmethod
    def close(cls):
        """Close the database connection
        """
        cls.cur.close()
        cls.conn.close()
