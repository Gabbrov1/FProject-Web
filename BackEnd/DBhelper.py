#MSSQL DB Helper
import os,pymssql



class DBHelper:
    db_con = None
    
    @staticmethod
    def get_db_connection():
        server = os.getenv('DB_SERVER', 'localhost')  # Use environment variable or default value
        user = os.getenv('DB_USER', 'your_username')  # Use environment variable or default value
        password = os.getenv('DB_PASSWORD', 'your_password')  # Use environment variable or default value
        database = os.getenv('DB_NAME', 'your_database')  # Use environment variable or default value

        try:
            conn = pymssql.connect(server=server, user=user, password=password, database=database)
            DBHelper.db_con = conn
            
        except Exception as e:
            print(f"Error connecting to database: {e}")
    
    
    def fetch_user(self, username):
        """Fetch user by username and password if password is provided, otherwise fetch by username only."""
        if DBHelper.db_con is None:
            DBHelper.get_db_connection()
        
        cursor = DBHelper.db_con.cursor(as_dict=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        return user
    
    def fetch_user(self,username,password):
        if DBHelper.db_con is None:
            DBHelper.get_db_connection()
        
        cursor = DBHelper.db_con.cursor(as_dict=True)
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username,password))
        user = cursor.fetchone()
        return user
    
    def close_connection(self):
        if DBHelper.db_con:
            DBHelper.db_con.close()
            DBHelper.db_con = None
        
    