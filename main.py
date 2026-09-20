import re
from modelos.persona import Usuario
from modelos.articulo import Articulo
from modelos.venta import Venta

def menu_general():
    print("\n=== MENÚ GENERAL ===") 
    print("1. Ingresar al inventario")
    print("2. Realizar venta")
    print("4. Salir del sistema")

    inventario = []  # Inventario compartido entre menús
    
    while True:
        opcion = input("Selecciona una opción: ")
        
        if opcion == "1":
            print("Ingresando al inventario...")
            menu_inventario(inventario)
        elif opcion == "2":
            print("Ingresando a la sección de ventas...")
            menu_ventas(inventario)
        elif opcion == "4":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Por favor, intente nuevamente.")

def menu_ventas(inventario):
    ventas = []

    while True:
        print("\n=== MENÚ DE VENTA ===")
        print("1. Ingresar nueva venta")
        print("2. Calcular total de la venta")
        print("3. Modificar venta")
        print("4. Eliminar venta")
        print("5. Volver al menú principal")
        opcion = input("Selecciona una opción: ")
        
        if opcion == "1":
            print("Realizar venta.")
            if not inventario:
                print("No hay productos en el inventario. Debe agregar productos primero.")
                continue
            
            print("\n--- PRODUCTOS DISPONIBLES ---")
            for art in inventario:
                print(art)
            
            codigo = input("\nIngrese el código del producto a vender: ")
            articulo_venta = None
            for art in inventario:
                if art.codigo == codigo:
                    articulo_venta = art
                    break
            
            if not articulo_venta:
                print("Producto no encontrado.")
                continue
            
            if articulo_venta.stock <= 0:
                print(f"Error: El producto '{articulo_venta.nombre}' no tiene stock disponible.")
                continue
            
            cantidad = int(input(f"Ingrese la cantidad a vender (Stock disponible: {articulo_venta.stock}): "))
            
            if cantidad <= 0:
                print("Error: Cantidad inválida.")
                continue
            
            if not articulo_venta.descontarStock(cantidad):
                print(f"Error: No hay suficiente stock. Stock disponible: {articulo_venta.stock}")
                continue
            
            descuento = float(input("Ingrese el descuento aplicado (en porcentaje): "))
            fecha = input("Ingrese la fecha de la venta (YYYY-MM-DD): ")
            total = float(input("Ingrese el total de la venta: "))
            nueva_venta = Venta(len(ventas) + 1, descuento, fecha, total)
            nueva_venta.articulo = articulo_venta
            nueva_venta.cantidad = cantidad
            ventas.append(nueva_venta)
            print(f"Venta registrada con ID: {nueva_venta.id}")
            print(f"Stock de '{articulo_venta.nombre}' actualizado a: {articulo_venta.stock}")
        elif opcion == "2":
            print("Calcular el total de la venta.")
            if ventas:
                id_venta = int(input("Ingrese el ID de la venta: "))
                venta_encontrada = None
                for venta in ventas:
                    if venta.id == id_venta:
                        venta_encontrada = venta
                        break
                if venta_encontrada:
                    total_calculo = venta_encontrada.calcularTotal(venta_encontrada.total, venta_encontrada._descuento)
                    articulo = getattr(venta_encontrada, 'articulo', None)
                    cantidad = getattr(venta_encontrada, 'cantidad', 1)
                    if articulo:
                        print(f"Venta ID: {venta_encontrada.id}")
                        print(f"Producto: {articulo.nombre}")
                        print(f"Cantidad: {cantidad}")
                        print(f"Total calculado (con descuento): ${total_calculo:.2f}")
                    else:
                        print(f"Total calculado: ${total_calculo:.2f}")
                else:
                    print("Venta no encontrada.")
            else:
                print("No hay ventas registradas.")
        elif opcion == "3":
            print("Modificar venta.")
            if ventas:
                id_venta = int(input("Ingrese el ID de la venta a modificar: "))
                venta_encontrada = None
                for venta in ventas:
                    if venta.id == id_venta:
                        venta_encontrada = venta
                        break
                if venta_encontrada:
                    print(f"Venta actual - Descuento: {venta_encontrada._descuento}%, Fecha: {venta_encontrada.fecha}, Total: {venta_encontrada.total}")
                    descuento = input("Nuevo descuento (en porcentaje) o Enter para no cambiar: ")
                    fecha = input("Nueva fecha (YYYY-MM-DD) o Enter para no cambiar: ")
                    total = input("Nuevo total o Enter para no cambiar: ")
                    
                    descuento = float(descuento) if descuento else None
                    total = float(total) if total else None
                    fecha = fecha if fecha else None
                    
                    if venta_encontrada.modificarVenta(descuento, fecha, total):
                        print("Venta modificada correctamente.")
                else:
                    print("Venta no encontrada.")
            else:
                print("No hay ventas registradas.")
        elif opcion == "4":
            print("Eliminar venta.")
            if ventas:
                id_venta = int(input("Ingrese el ID de la venta a eliminar: "))
                venta_encontrada = None
                for i, venta in enumerate(ventas):
                    if venta.id == id_venta:
                        venta_encontrada = i
                        break
                if venta_encontrada is not None:
                    venta_eliminada = ventas[venta_encontrada]
                    # Restaurar stock del artículo si fue descontado
                    articulo = getattr(venta_eliminada, 'articulo', None)
                    cantidad = getattr(venta_eliminada, 'cantidad', 0)
                    if articulo and cantidad > 0:
                        articulo.stock += cantidad
                        print(f"Stock de '{articulo.nombre}' restaurado a: {articulo.stock}")
                    id_eliminada = venta_eliminada.eliminarVenta()
                    ventas.pop(venta_encontrada)
                    print(f"Venta con ID {id_eliminada} eliminada correctamente.")
                else:
                    print("Venta no encontrada.")
            else:
                print("No hay ventas registradas.")
        elif opcion == "5":
            break
        else:
            print("Opción no válida. Por favor, intente nuevamente.")

def menu_inventario(inventario):
    while True:
        print("\n=== MENÚ DE INVENTARIO (STOCK MASTER) ===")
        print("1. Ingresar producto")
        print("2. Modificar producto")
        print("3. Eliminar producto")
        print("4. Buscar / Listar productos")
        print("5. Cerrar sesión")
        
        opcion = input("Selecciona una opción: ")
        
        if opcion == "1":
            # RQ03: Ingreso de productos[cite: 2]
            print("\n--- NUEVO PRODUCTO ---")
            nombre = input("Ingrese nombre del producto: ")
            precio = float(input("Ingrese el precio: "))
            stock = int(input("Ingrese la cantidad en stock: "))
            descripcion = input("Ingrese una descripción (máx 250 caracteres): ")
            
            # El código se genera automáticamente en la clase Articulo[cite: 2]
            nuevo_articulo = Articulo(nombre, precio, stock, descripcion)
            inventario.append(nuevo_articulo)
            print(f"¡Producto ingresado exitosamente con el código: {nuevo_articulo.codigo}!")
            
        elif opcion == "2":
            # RQ04: Modificar productos[cite: 2]
            codigo = input("Ingrese el código del producto a editar: ")
            for art in inventario:
                if art.codigo == codigo:
                    print(f"Editando: {art.nombre}")
                    nuevo_nombre = input("Nuevo nombre: ")
                    nuevo_precio = float(input("Nuevo precio: "))
                    nuevo_stock = int(input("Nuevo stock: "))
                    nueva_desc = input("Nueva descripción: ")
                    
                    art.modificar(nuevo_nombre, nuevo_precio, nuevo_stock, nueva_desc)
                    print("¡Producto modificado con éxito!")
                    break
            else:
                print("Alerta: Producto no existente[cite: 2].")
                
        elif opcion == "3":
            codigo = input("Ingrese el código del producto a eliminar: ")
            for art in inventario:
                if art.codigo == codigo:
                    inventario.remove(art)
                    print("¡Producto eliminado!")
                    break
            else:
                print("Alerta: Producto no existente[cite: 2].")
                
        elif opcion == "4":
            # RQ07: Búsqueda de productos[cite: 2]
            busqueda = input("\nIngrese el nombre o código a buscar (o presione Enter para ver todos): ")
            encontrados = [art for art in inventario if busqueda.lower() in art.nombre.lower() or busqueda == art.codigo]
            
            if not encontrados:
                print("Alerta: Producto no existente[cite: 2].")
            else:
                print("\n--- RESULTADOS ---")
                for art in encontrados:
                    print(art)
                    
        elif opcion == "5":
            # RQ05: Cerrar sesión[cite: 2]
            print("Cierre de sesión exitoso :)[cite: 2]")
            break
        else:
            print("Opción no válida.")

def main():
    usuarios_registrados = []
    
    while True:
        print("\n=== SISTEMA DE ACCESO ===")
        print("1. Registrarse")
        print("2. Iniciar Sesión")
        print("3. Salir")
        
        opcion = input("Elige una opción: ")
        
        if opcion == "1":
            print("\n--- REGISTRO ---")
            nombre = input("Ingrese su nombre: ")
            
            # Validación RNF016: Campos obligatorios y duplicidad[cite: 2]
            while True:
                usuario = input("Cree un nombre de usuario: ")
                if not usuario:
                    print("Alerta: Debe llenar todos los campos obligatorios[cite: 2].")
                    continue
                if any(u.usuario == usuario for u in usuarios_registrados):
                    print("Error: Este nombre de usuario ya está registrado.")
                else:
                    break
            
            # Validación RQ02: Contraseña segura[cite: 2]
            while True:
                contrasena = input("Cree una contraseña: ")
                if not contrasena:
                    print("Alerta: Debe llenar todos los campos obligatorios[cite: 2].")
                elif len(contrasena) < 8:
                    print("Error: La longitud de la contraseña será mínimo de 8 caracteres[cite: 2].")
                elif usuario.lower() in contrasena.lower():
                    print("Error: La contraseña no puede contener el nombre del usuario[cite: 2].")
                elif not re.search(r"[A-Z]", contrasena):
                    print("Error: La contraseña debe tener al menos una letra mayúscula[cite: 2].")
                elif not re.search(r"[0-9]", contrasena):
                    print("Error: La contraseña debe contener números[cite: 2].")
                elif not re.search(r"[!@#$%^&*(),.?\":{}|<>]", contrasena):
                    print("Error: La contraseña debe tener al menos un carácter especial[cite: 2].")
                else:
                    break
            
            nuevo_usuario = Usuario(nombre, usuario, contrasena)
            usuarios_registrados.append(nuevo_usuario)
            print("¡Usuario registrado exitosamente!")
            
        elif opcion == "2":
            # RQ01: Inicio de sesión[cite: 2]
            print("\n--- LOGIN ---")
            usuario = input("Usuario: ")
            contrasena = input("Contraseña: ")
            
            autenticado = False
            for u in usuarios_registrados:
                if u.iniciar_sesion(usuario, contrasena):
                    print(f"\n¡Bienvenido, {u.nombre}!")
                    autenticado = True
                    menu_general()
                    break
            
            if not autenticado:
                # RNF15: Contraseña invalida[cite: 2]
                print("Alerta: Usuario o contraseña incorrecta[cite: 2].")
                
        elif opcion == "3":
            print("Hasta pronto :)[cite: 2]")
            break
        else:
            print("Opcion errada!![cite: 2]")

if __name__ == "__main__":
    main()