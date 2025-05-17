class ProductRepository:
    def __init__(self, db_connector):
        self.db_connector = db_connector
        
    def get_by_id(self, product_id):
        with self.db_connector.connect().cursor(named_tuple=True) as cursor:
            cursor.execute("SELECT * FROM products WHERE id = %s;", (product_id,))
            product = cursor.fetchone()
        return product
    
    def get_by_product_name(self, product_name):
        with self.db_connector.connect().cursor(named_tuple=True) as cursor:
            cursor.execute("SELECT * FROM products WHERE product_name = %s;", (product_name,))
            product = cursor.fetchone()
        return product

    def all(self):
        with self.db_connector.connect().cursor(named_tuple=True) as cursor:
            cursor.execute("SELECT * FROM products;")
            products = cursor.fetchall()
        return products
        
    def all_by_owner(self, owner_id):
        with self.db_connector.connect().cursor(named_tuple=True) as cursor:
            cursor.execute("SELECT * FROM products WHERE owner_id=%s", (owner_id,))
            products = cursor.fetchall()
        return products
    
    def create(self, product_name, kalories, protein, fat, carbohydrates, img_path, is_public, owner_id):
        connection = self.db_connector.connect()
        with connection.cursor(named_tuple=True) as cursor:
            query = (
                "INSERT INTO products (product_name, kalories, protein, fat, carbohydrates, img_path, is_public, owner_id) VALUES"
                "(%s, %s, %s, %s, %s, %s, %s, %s)"
            )
            product_data = (product_name, kalories, protein, fat, carbohydrates, img_path, is_public, owner_id)
            cursor.execute(query, product_data)
            connection.commit()
            
    def update(self, product_id, product_name, kalories, protein, fat, carbohydrates, img_path):
        connection = self.db_connector.connect()
        with connection.cursor(named_tuple=True) as cursor:
            query = (
                "UPDATE products SET product_name = %s, "
                "kalories = %s, protein = %s, fat = %s, carbohydrates = %s, img_path = %s WHERE id = %s"
            )
            product_data = (product_name, kalories, protein, fat, carbohydrates, img_path, product_id)
            cursor.execute(query, product_data)
            connection.commit()     
            
    def delete(self, product_id):
        connection = self.db_connector.connect()
        with connection.cursor(named_tuple=True) as cursor:
            cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
            connection.commit()