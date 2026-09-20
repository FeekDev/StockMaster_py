class Venta():
    def __init__(self, id, descuento, fecha, total):
        self.id = id
        self._descuento = descuento
        self.fecha = fecha
        self.total = total
    
    ''' Metodo calcular total'''
    def calcularTotal(self, total, descuento):
        total = total - (total * (descuento / 100))
        return total
    
    ''' Metodo para modificar venta'''
    def modificarVenta(self, descuento=None, fecha=None, total=None):
        if descuento is not None:
            self._descuento = descuento
        if fecha is not None:
            self.fecha = fecha
        if total is not None:
            self.total = total
        return True
    
    ''' Metodo para eliminar venta'''
    def eliminarVenta(self):
        return self.id