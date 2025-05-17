class MealRepository:
    def __init__(self, db_connector):
        self.db_connector = db_connector
        
    def get_by_id(self, meal_id):
        with self.db_connector.connect().cursor(named_tuple=True) as cursor:
            cursor.execute("SELECT * FROM meals WHERE id = %s;", (meal_id,))
            meal = cursor.fetchone()
        return meal

    def all(self):
        with self.db_connector.connect().cursor(named_tuple=True) as cursor:
            cursor.execute("SELECT * FROM meals;")
            meals = cursor.fetchall()
        return meals
        
    def all_by_date(self, meal_date):
        with self.db_connector.connect().cursor(named_tuple=True) as cursor:
            cursor.execute("SELECT * FROM meals WHERE meal_date=%s;", (meal_date,))
            meals = cursor.fetchall()
        return meals
    
    def create(self, meal_date, meal_category, kalories_total, protein_total, fat_total, carbohydrates_total, owner_id):
        connection = self.db_connector.connect()
        with connection.cursor(named_tuple=True) as cursor:
            query = (
                "INSERT INTO meals (meal_date, meal_category, kalories_total, protein_total, fat_total, carbohydrates_total, owner_id) VALUES"
                "(%s, %s, %s, %s, %s, %s, %s)"
            )
            meal_data = (meal_date, meal_category, kalories_total, protein_total, fat_total, carbohydrates_total, owner_id)
            cursor.execute(query, meal_data)
            connection.commit()
            
    def update(self, meal_id, meal_date, meal_category, kalories_total, protein_total, fat_total, carbohydrates_total):
        connection = self.db_connector.connect()
        with connection.cursor(named_tuple=True) as cursor:
            query = (
                "UPDATE meals SET meal_date = %s, "
                "meal_category = %s, kalories_total = %s, protein_total = %s, fat_total = %s, carbohydrates_total = %s WHERE id = %s"
            )
            meal_data = (meal_date, meal_category, kalories_total, protein_total, fat_total, carbohydrates_total, meal_id)
            cursor.execute(query, meal_data)
            connection.commit()     
            
    def delete(self, meal_id):
        connection = self.db_connector.connect()
        with connection.cursor(named_tuple=True) as cursor:
            cursor.execute("DELETE FROM meals WHERE id = %s", (meal_id,))
            connection.commit()