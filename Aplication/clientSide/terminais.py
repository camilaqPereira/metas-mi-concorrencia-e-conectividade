from Client import controller
from Client import ClientSockClass
from Client import requests

ip = ''
email = ''
match = ''
destination = ''

client = ClientSockClass.ClientSocket(ip)
(status, dados) = controller.connect(email, client)
if status == requests.ConstantsManagement.OK.value:
    (status, dados) = controller.search_routes(match, destination, client)
    if status == requests.ConstantsManagement.OK.value:
        (status, dados) = controller.buying(dados[0], client)
        if status == requests.ConstantsManagement.OK.value:
            print('Compra realizada com sucesso')
            exit(0)
        elif status == requests.ConstantsManagement.OPERATION_FAILED.value:
            print('não foi possivel realizar a compra')
            exit(0)

print(status)