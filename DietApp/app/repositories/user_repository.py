class UserRepository:
    def __init__(self, db_connector):
        self.db_connector = db_connector
        
    def get_by_id(self, user_id):
        with self.db_connector.connect().cursor(named_tuple=True) as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s;", (user_id,))
            user = cursor.fetchone()
        return user
    
    def get_by_username_and_password(self, username, password):
        with self.db_connector.connect().cursor(named_tuple=True) as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s AND password_hash = SHA2(%s, 256);", (username, password))
            user = cursor.fetchone()
        return user
    
    def validate_password(self, user_id, password_to_validate):
        with self.db_connector.connect().cursor(named_tuple=True) as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s AND password_hash = SHA2(%s, 256);", (user_id, password_to_validate))
            user = cursor.fetchone()
        return user
    
    def all(self):
        with self.db_connector.connect().cursor(named_tuple=True) as cursor:
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
        return users
    
    def create(self, username, email, password, is_admin):
        connection = self.db_connector.connect()
        with connection.cursor(named_tuple=True) as cursor:
            query = (
                "INSERT INTO users (username, email, password_hash, is_admin) VALUES"
                "(%s, %s, SHA2(%s,256), %s)"
            )
            user_data = (username, email, password, is_admin)
            cursor.execute(query, user_data)
            connection.commit()
            
    def set_goal(self, user_id, goal, kalories_goal, protein_goal, fat_goal, carbohydrates_goal):
        connection = self.db_connector.connect()
        with connection.cursor(named_tuple=True) as cursor:
            query = (
                "UPDATE users SET goal = %s, "
                "kalories_goal = %s, protein_goal = %s, fat_goal = %s, carbohydrates_goal = %s WHERE id = %s"
            )
            user_data = (goal, kalories_goal, protein_goal, fat_goal, carbohydrates_goal, user_id)
            cursor.execute(query, user_data)
            connection.commit()   
            
    # def change_password(self, user_id, new_password):
    #     connection = self.db_connector.connect()
    #     with connection.cursor(named_tuple=True) as cursor:
    #         query = (
    #             "UPDATE users SET password_hash = SHA2(%s, 256) WHERE id = %s"
    #         )
    #         user_data = (new_password, user_id)
    #         cursor.execute(query, user_data)
    #         connection.commit()    
            
    # def delete(self, user_id):
    #     connection = self.db_connector.connect()
    #     with connection.cursor(named_tuple=True) as cursor:
    #         cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    #         connection.commit()