# #class CuentaBancaria:
#     def __init__(self, titular,saldo):
#         self.titular = titular
#         self.saldo = saldo


# cuenta1 = CuentaBancaria("Omar", 300000)
# cuenta1.saldo = -50000


# print(cuenta1.saldo)
# print(cuenta1.__dict__)


class CuentaBancaria:
    def __init__(self, titular, saldo):
        self.titular = titular
        self.__saldo = saldo
        
cuenta1 = CuentaBancaria("Omar", 300000)
print(cuenta1._CuentaBancaria__saldo)  
cuenta1.__saldo = -50000  
print(cuenta1.__saldo) 