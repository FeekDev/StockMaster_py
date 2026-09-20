class Articulo:
    # Atributo de clase para llevar el control del código progresivo
    _contador_codigo = 1

    def __init__(self, nombre, precio, stock, descripcion):
        # Asigna el contador actual como código y lo convierte a texto
        self.codigo = str(Articulo._contador_codigo)
        
        # Incrementa el contador automáticamente para el próximo producto
        Articulo._contador_codigo += 1
        
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.descripcion = descripcion

    def modificar(self, nombre, precio, stock, descripcion):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.descripcion = descripcion

    def descontarStock(self, cantidad):
        """Descuenta stock del artículo cuando se realiza una venta"""
        if self.stock >= cantidad:
            self.stock -= cantidad
            return True
        return False

    def __str__(self):
        return f"[{self.codigo}] {self.nombre} | Precio: ${self.precio} | Stock: {self.stock} | Desc: {self.descripcion}"