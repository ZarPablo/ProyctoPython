import mysql.connector
import sys

class Catalogo:
    def __init__(self, host, user, password, database):
        try:
            # Establecer conexión con la base de datos
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.conn.cursor(dictionary=True)
            
            # Crear tabla si no existe
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
        
        except mysql.connector.Error as e:
            print(f"Error connecting to MySQL Platform: {e}")
            sys.exit(1)

    def agregar_producto(self, descripcion, cantidad, precio, imagen, proveedor):    
        try:
            sql = "INSERT INTO productos (descripcion, cantidad, precio, imagen_url, proveedor) VALUES (%s, %s, %s, %s, %s)"
            valores = (descripcion, cantidad, precio, imagen, proveedor)
            self.cursor.execute(sql, valores)
            self.conn.commit()
            return self.cursor.lastrowid
        except mysql.connector.Error as e:
            print(f"Error: {e}")
            return None

    def consultar_producto(self, codigo):
        try:
            self.cursor.execute("SELECT * FROM productos WHERE codigo = %s", (codigo,))
            return self.cursor.fetchone()
        except mysql.connector.Error as e:
            print(f"Error: {e}")
            return None

    def modificar_producto(self, codigo, nueva_descripcion, nueva_cantidad, nuevo_precio, nueva_imagen, nuevo_proveedor):
        try:
            sql = "UPDATE productos SET descripcion = %s, cantidad = %s, precio = %s, imagen_url = %s, proveedor = %s WHERE codigo = %s"
            valores = (nueva_descripcion, nueva_cantidad, nuevo_precio, nueva_imagen, nuevo_proveedor, codigo)
            self.cursor.execute(sql, valores)
            self.conn.commit()
            return self.cursor.rowcount > 0
        except mysql.connector.Error as e:
            print(f"Error: {e}")
            return False
    
    def mostrar_producto(self, codigo):
        producto = self.consultar_producto(codigo)
        if producto:
            print("-" * 40)
            print(f"Código.......: {producto['codigo']}")
            print(f"Descripcion..: {producto['descripcion']}")
            print(f"Cantidad.....: {producto['cantidad']}")
            print(f"Precio.......: {producto['precio']}")
            print(f"imagen_url...: {producto['imagen_url']}")
            print(f"Proveedor....: {producto['proveedor']}")
            print("-" * 40)
        else:
            print("Producto no encontrado.")
            
    def listar_productos(self):
        self.cursor.execute("SELECT * FROM productos")
        productos = self.cursor.fetchall()
        return productos
    
    def eliminar_producto(self, codigo):
        self.cursor.execute(f"DELETE FROM productos WHERE codigo = {codigo}")
        self.conn.commit()
        return self.cursor.rowcount > 0

# Crear instancia de la clase Catalogo
catalogo = Catalogo(host='localhost', user='root', password='ZarPablo77', database='python_codo')

# Agregar productos al catálogo
#catalogo.agregar_producto('Teclado usb 101 teclas', 10, 4500, 'teclado.jpg', 101)
#catalogo.agregar_producto('Mouse usb 3 botones', 5, 2500, 'mouse.jpg', 102)
#catalogo.agregar_producto('Monitor lcd 22"', 15, 52500, 'monitor22p.jpg', 103)
#catalogo.agregar_producto('Monitor lcd 27"', 25, 78500, 'monitor27p.jpg', 103)
#catalogo.agregar_producto('Parlante USB', 4, 2500, 'parlante.jpg', 104)

# Solicitar el código del producto al usuario y consultar el producto
cod_prod = int(input("Ingrese el codigo del producto a buscar: "))
producto = catalogo.consultar_producto(cod_prod)
if producto:
    print(f"Producto : {producto['codigo']} - {producto['descripcion']}")
else:
    print(f'Producto {cod_prod} no encontrado.')

# Mostrar y modificar producto
catalogo.mostrar_producto(1)
catalogo.modificar_producto(1, 'Teclado mecanico', 20, 3400, 'tecmec.jpg', 106)
catalogo.mostrar_producto(1)
productos = catalogo.listar_productos()
for producto in productos:
    print(producto)
    
cod_prod = int(input("Ingrese el codigo del producto a eliminar: "))
catalogo.eliminar_producto(cod_prod)
productos = catalogo.listar_productos()
for producto in productos:
    print(producto)
    
