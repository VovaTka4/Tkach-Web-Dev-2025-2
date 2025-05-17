class M2MProductMealRepository:
    def __init__(self, db_connector):
        self.db_connector = db_connector
        
    def get_by_id(self, mp_id):
        with self.db_connector.connect().cursor(named_tuple=True) as cursor:
            cursor.execute("SELECT * FROM m2m_products_meals WHERE id = %s;", (mp_id,))
            meal_product= cursor.fetchone()
        return meal_product

    def all(self):
        with self.db_connector.connect().cursor(named_tuple=True) as cursor:
            cursor.execute("SELECT * FROM m2m_products_meals;")
            meal_products = cursor.fetchall()
        return meal_products
        
    def all_by_meal_id(self, meal_id):
        with self.db_connector.connect().cursor(named_tuple=True) as cursor:
            cursor.execute("SELECT * FROM m2m_products_meals WHERE meal_id=%s;", (meal_id,))
            meal_products = cursor.fetchall()
        return meal_products
    
    def create(self, total_weight, product_id, meal_id):
        connection = self.db_connector.connect()
        with connection.cursor(named_tuple=True) as cursor:
            query = (
                "INSERT INTO m2m_products_meals (total_weight, product_id, meal_id) VALUES"
                "(%s, %s, %s)"
            )
            meal_product_data = (total_weight, product_id, meal_id)
            cursor.execute(query, meal_product_data)
            connection.commit()
            
    def update(self, mp_id, total_weight):
        connection = self.db_connector.connect()
        with connection.cursor(named_tuple=True) as cursor:
            query = (
                "UPDATE m2m_products_meals SET total_weight = %s WHERE id = %s"
            )
            meal_product_data = (total_weight, mp_id)
            cursor.execute(query, meal_product_data)
            connection.commit()     
            
    def delete(self, mp_id):
        connection = self.db_connector.connect()
        with connection.cursor(named_tuple=True) as cursor:
            cursor.execute("DELETE FROM m2m_products_meals WHERE id = %s", (mp_id,))
            connection.commit()