class Usuario:
    def __init__(self, nombre, usuario, contrasena):
        self.nombre = nombre
        self.usuario = usuario
        self.__contrasena = contrasena  # Atributo privado (encapsulado)[cite: 3]

    def iniciar_sesion(self, usuario, contrasena):
        # Valida si las credenciales coinciden con las registradas en el sistema
        return self.usuario == usuario and self.__contrasena == contrasena