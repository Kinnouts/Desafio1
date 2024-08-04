import os
import platform

#Acá recordar no usar guión medio, los nombres de archivos solo guión bajo y comprobar que identaciones de clases sean correctas, sino no lo toma
from lab_prods import Producto, ProductoElectronico, ProductoAlimenticio, CRUDProductos

def limpiar_pantalla():
    #limpiar pantalla según sistema operativo
    if platform.system()=="Windows":
        os.system('cls')
    else:
        os.system('clear')#Para linux/unix/MacOs

def mostrar_menu():
    print("========== Menú de Gestión de Productos ==========")
    print('1-Agregar producto alimenticio')
    print('2-Agregar producto electrónico')
    print('3-Buscar producto por ID')
    print('4-Modificar precio de producto')
    print('5-Eliminar producto')
    print('6-Listar productos')


#Polimorfismo
#No requiere especificar tipo de dato, pero le ponemos por si acaso
def agregar_producto(gestion:CRUDProductos, tipo_producto):
    try: 
        idp = input("Ingrese ID del producto: ")
        nombre = input("Ingrese nombre del producto: ")
        stock = int(input("Ingrese stock del producto: "))
        precio = float(input("Ingrese precio de venta del producto: "))
        
        if tipo_producto=='1': #Alimenticio
            fecha_caducidad = input("Ingrese fecha de vencimiento del producto: ")
            #Instancio clase producto alimenticio y para inicializarla le paso los datos ingresados
            producto=ProductoAlimenticio(idp, nombre, precio, stock, fecha_caducidad)
        
        elif tipo_producto =='2':
            potencia_consumida=int(input("Ingrese la potencia que consume este producto: "))
            producto=ProductoElectronico(idp, nombre, precio, stock, potencia_consumida)
        else:
            print("Opción inválida")
            return  #Este return vacío vuelve al menú
        
        gestion.crear_producto(producto)
        input("Presione enter para continuar")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:#Error inesperado no contemplado
        print (f"Error inesperado: {e}") #No olvidarse de poner la f sino no imprime el msj


def buscar_producto_por_idp(gestion):
    idp=int(input("Ingrese el ID del producto a buscar: "))
    gestion.leer_producto(idp)
    input("Presione enter para continuar...")

def actualizar_precio_producto(gestion):
    idp=(input("Ingrese el ID del producto cuyo precio desea modificar: "))
    precio=float(input("Ingrese el nuevo valor de precio que desea asociarle: "))
    gestion.actualizar_producto(idp,precio)
    input("Presione enter para continuar")

def eliminar_producto_por_idp(gestion): 
    idp=(input("Ingrese el ID del producto que desea eliminar: "))
    gestion.eliminar_producto(idp)
    input("Presione enter para continuar")

def mostrar_todos_los_productos(gestion):

    print("###############LIstado completo de productos#################### ")
    for producto in gestion.leer_datos().values(): #Acá llamo al método en i back
        if 'fecha_caducidad' in producto:
            print(f"{producto['nombre']}- Fecha Vencimiento {producto['fecha_caducidad']}")
        else:
            print(f"{producto['nombre']}- Potencia de consumo {producto['potencia_consumida']}")
    print("########################################################## ")
    print("Presione cualquier tecla para continuar")



if __name__=="__main__": #Esto va a correr la opción que elija el user ni bien se ejecuta el main
    archivo_productos='productos_db.json' #Voy a crear este archivo
    gestion_prod=CRUDProductos(archivo_productos)#Le pasamos nuestra bd
    while True:
        # limpiar_pantalla()
         mostrar_menu()
         opcion=input("Seleccione una opción: ")
         if opcion =='1' or opcion =='2': #ESte numerillo ponerlo así entre comillas simples porque sino no lo toma
             agregar_producto(gestion_prod, opcion)
         elif opcion =='3':
             buscar_producto_por_idp(gestion_prod)
         elif opcion=='4':
             actualizar_precio_producto(gestion_prod)
         elif opcion=='5':
             eliminar_producto_por_idp(gestion_prod)
         elif opcion== '6':
             mostrar_todos_los_productos(gestion_prod)
         else:
            print("Opcion no válida")