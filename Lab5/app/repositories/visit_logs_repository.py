class VisitLogsRepository:
    def __init__(self, db_connector):
        self.db_connector = db_connector
        
    def get_by_id(self, visit_log_id):
        with self.db_connector.connect().cursor(named_tuple=True) as cursor:
            cursor.execute("SELECT * FROM visit_logs WHERE id = %s;", (visit_log_id,))
            log = cursor.fetchone()
        return log
    
    def all(self):
        with self.db_connector.connect().cursor(named_tuple=True) as cursor:
            cursor.execute("SELECT * FROM visit_logs")
            logs = cursor.fetchall()
        return logs
    
    def create(self, path, user_id):
        connection = self.db_connector.connect()
        with connection.cursor(named_tuple=True) as cursor:
            query = (
                "INSERT INTO visit_logs (path, user_id) VALUES"
                "(%s, %s)"
            )
            user_data = (path, user_id)
            cursor.execute(query, user_data)
            connection.commit()
            
    def page_stats(self):
        with self.db_connector.connect().cursor(named_tuple=True) as cursor:
            cursor.execute("SELECT path, COUNT(*) AS count FROM visit_logs GROUP BY path ORDER BY count DESC")
            stats = cursor.fetchall()
        return stats
    
    def user_stats(self):
        with self.db_connector.connect().cursor(named_tuple=True) as cursor:
            cursor.execute("SELECT user_id, COUNT(*) AS count FROM visit_logs GROUP BY user_id ORDER BY count DESC")
            stats = cursor.fetchall()
        return stats
    
    