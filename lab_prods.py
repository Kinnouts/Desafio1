import json
from datetime import datetime

class Producto:
    
    def __init__(self, idp, nombre, precio, stock):
        self.__idp = self.validar_idp(idp)
        self.__nombre = self.validar_nombre(nombre)
        self.__precio = self.validar_precio(precio)
        self.__stock = self.validar_stock(stock)
   
    
    
    @property
    def idp(self):
        return self.__idp

    @property
    def nombre(self):
        return self.__nombre
    
    @property
    def precio(self):
        return self.__precio
    
    @property
    def stock(self):
        return self.__stock
    
    @precio.setter
    def precio(self, nuevo_precio):
        self.__precio = self.validar_precio(nuevo_precio)

    @stock.setter
    def stock(self, nuevo_stock):
        self.__stock = self.validar_stock(nuevo_stock)

    def validar_idp(self, idp):
        try:
            idp_num = int(idp)
            if idp_num <= 0:
                raise ValueError("El número ingresado de ID debe ser positivo")
            return idp_num
        except ValueError:
            raise ValueError("Debe ingresar un número entero positivo para ID de producto")
        
    def validar_nombre(self, nombre):
        if not nombre.replace(" ", "").isalpha():
            raise ValueError("El nombre del producto debe contener sólo letras")
        return nombre
            
    def validar_precio(self, precio):
        try:
            precio_num = float(precio)
            if precio_num <= 0:
                raise ValueError("El valor del precio asignado al producto debe ser positivo")
            return precio_num
        except ValueError:
            raise ValueError("El precio asignado debe ser un número positivo")
        
    def validar_stock(self, stock):
        try:
            stock_num = int(stock)
            if stock_num < 0:
                raise ValueError("El número ingresado de stock no puede ser negativo")
            return stock_num
        except ValueError:
            raise ValueError("Debe ingresar un número entero para stock")
        
    def to_dic(self):
        return {
            "idp": self.idp, 
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock
        }
    
    def __str__(self):
        return f"{self.nombre} {self.precio} {self.stock} unidades disponibles"

class ProductoAlimenticio(Producto):
    def __init__(self, idp, nombre, precio, stock, fecha_caducidad):
        super().__init__(idp, nombre, precio, stock)
        self.__fecha_caducidad = self.validar_fecha(fecha_caducidad)

    @property
    def fecha_caducidad(self):
        return self.__fecha_caducidad
    
    
    def to_dic(self):
        data = super().to_dic()
        data["fecha_caducidad"] = self.fecha_caducidad.strftime('%Y-%m-%d') 
        return data
    
    def validar_fecha(self,fecha_caducidad):
        try:
            fecha = datetime.strptime(fecha_caducidad, '%Y-%m-%d')
            if fecha <= datetime.now():
                raise ValueError("La fecha de caducidad debe ser una fecha futura.")
            return fecha
        except ValueError as e:
            raise ValueError("Formato de fecha inválido. Use 'YYYY-MM-DD'.") from e

    #Muestro en su respectivo formato dia-mes-año
    def __str__(self):
        return f"{super().__str__()} - Fecha Caducidad: {self.fecha_caducidad.strftime('%Y-%m-%d')}"

class ProductoElectronico(Producto):
    def __init__(self, idp, nombre, precio, stock, potencia_consumida):
        super().__init__(idp, nombre, precio, stock)
        self.__potencia_consumida = potencia_consumida

    @property
    def potencia_consumida(self):
        return self.__potencia_consumida
    
    def validar_potencia(self,potencia):
        try:
            potencia_num=int(potencia)
            if potencia_num<0:
                raise ValueError ("el valor de potencia debe ser positivo")
            else:
                return potencia_num    
        except ValueError:
            raise ValueError ("El valor de potencia ingresado debe ser un número entero")
        
    def to_dic(self):
        data = super().to_dic()
        data["potencia_consumida"] = self.potencia_consumida
        return data
    
    def __str__(self):
        return f"{super().__str__()} - Potencia de consumo: {self.potencia_consumida}"

class CRUDProductos:
    def __init__(self, archivo):
        self.archivo = archivo

    def leer_datos(self):
        try:
            with open(self.archivo, 'r') as file:
                datos = json.load(file)
        except FileNotFoundError:
            return {}
        except Exception as error:
            raise Exception(f"Error al leer el archivo: {error}")
        else:
            return datos
   
    def guardar_datos(self, datos):
        try:
            with open(self.archivo, 'w') as file:
                json.dump(datos, file, indent=4)
        except IOError as error:
            print(f"Error al intentar guardar datos en archivo {self.archivo}: {error}")
        except Exception as e:
            print(f"Error inesperado: {e}")

    def crear_producto(self, producto):
        try:
            datos = self.leer_datos()
            idp = str(producto.idp)
            if idp not in datos:
                datos[idp] = producto.to_dic()
                self.guardar_datos(datos)
                print(f"Guardado exitoso")
            else:
                print(f"El producto con id {idp} ya existe")  
        except Exception as e:
            print(f"Error inesperado al crear y añadir producto: {e}")
    
    
    
    def leer_producto(self, idp):
        producto=None
        try:
            datos=self.leer_datos() #Trae todos los datos de json
            idp_str=str(idp) #Esta parte de cooincidir las cadenas es importante
            if idp_str in datos:
                #Diferenciar tipos de prods
                #Accedo a las key idp y busco por data
                producto_data=datos[idp_str]
                #Diferencio si es tal o cual
                
                if 'fecha_caducidad' in producto_data:
                    producto=ProductoAlimenticio(**producto_data) #Ponemos dos asteriscos para desempaquetar puesto que es diccionario
                else:
                    producto=ProductoElectronico(**producto_data) #Ponemos dos asteriscos para desempaquetar puesto que es diccionario
                print(f"Producto encontrado con ID: {idp}")

            else:
                print(f"Producto no encontrado")

        except Exception as e:
            print(f"Error inesperado {e}")
        return producto

        
    def actualizar_producto(self, idp, nuevo_precio):
        try:
            datos = self.leer_datos()
            idp_str = str(idp)
            if idp_str in datos:
                datos[idp_str]['precio'] = nuevo_precio
                self.guardar_datos(datos)
                print(f"Precio actualizado correctamente para el producto cuyo ID es: {idp}")
            else:
                print(f"No se encontró ID de producto")
        except Exception as error:
            print(f"Error al actualizar producto: {error}")

    def eliminar_producto(self, idp):
        try:
            datos = self.leer_datos()
            idp_str = str(idp)
            if idp_str in datos:
                del datos[idp_str]
                self.guardar_datos(datos)
                print(f"Producto con idp: {idp} eliminado exitosamente")
            else:
                print(f"El producto con idp: {idp} no se encuentra en la BD")
        except Exception as e:
            print(f"No se pudo eliminar el producto con ID: {idp}, código error {e}")