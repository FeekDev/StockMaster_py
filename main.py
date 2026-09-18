import re
from modelos.persona import Usuario
from modelos.articulo import Articulo

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
    inventario = []
    
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
                    menu_inventario(inventario)
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