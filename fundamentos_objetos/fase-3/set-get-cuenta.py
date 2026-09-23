class CuentaBancariia:
    def __init__(self, titular, saldo):
        self._titular = titular
        self._saldo = saldo
    
    def get_saldo(self):
        return self._saldo
    
    def set_saldo(self, nuevo_saldo):
        if nuevo_saldo >= 0:
            self._saldo = nuevo_saldo
        else:
            print("El saldo no puede ser negativo")
            return
     
cuenta1 = CuentaBancariia("Omar", 300000)
print(cuenta1.get_saldo())

cuenta1.set_saldo(-50000)
print("saldo actualizado: ", cuenta1.get_saldo())     
