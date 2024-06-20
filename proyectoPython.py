import mariadb
import sys

class Catalogo:
    def __init__(self, host, user, password, database):
        try:
            # Establish a connection to the database
            self.conn = mariadb.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.conn.cursor(dictionary=True)
            
         # Create table if it doesn't exist
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS productos (
                    codigo INT AUTO_INCREMENT PRIMARY KEY,
                    descripcion VARCHAR(255) NOT NULL,
                    cantidad INT NOT NULL,
                    precio DECIMAL(10,2) NOT NULL,
                    imagen_url VARCHAR(255),
                    proveedor INT
                )
            ''')
            self.conn.commit()
        
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

    def agregar_producto(self, descripcion, cantidad, precio, imagen, proveedor):    
        try:
            sql = "INSERT INTO productos (descripcion, cantidad, precio, imagen_url, proveedor) VALUES (?, ?, ?, ?, ?)"
            valores = (descripcion, cantidad, precio, imagen, proveedor)
            self.cursor.execute(sql, valores)
            self.conn.commit()
            return self.cursor.lastrowid
        except mariadb.Error as e:
            print(f"Error: {e}")
            return None

# Creating an instance of Catalogo class
catalogo = Catalogo(host='localhost', user='root', password='ZarPablo77', database='python_codo')

# Adding products to the catalog
#catalogo.agregar_producto('Teclado usb 101 teclas', 10, 4500, 'teclado.jpg', 101)
#catalogo.agregar_producto('Mouse usb 3 botones', 5, 2500, 'mouse.jpg', 102)
#catalogo.agregar_producto('Monitor lcd 22"', 15, 52500, 'monitor22p.jpg', 103)
#catalogo.agregar_producto('Monitor lcd 27"', 25, 78500, 'monitor27p.jpg', 103)
#catalogo.agregar_producto('Parlante USB', 4, 2500, 'parlante.jpg', 104)
