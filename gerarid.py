
import string
import random


# Função para gerar código de TXID alfanuméricos
def gerar_identificador():
    caracteres = string.ascii_letters + string.digits
    caracteres02 = string.digits
    caracteres03 = string.ascii_letters
    caracteres04 = caracteres = string.ascii_letters + string.digits
    init = "bs21"
    codigo_01 = ''.join(random.choices(caracteres, k=6))
    codigo_02 = ''.join(random.choices(caracteres02, k=4))
    codigo_03 = ''.join(random.choices(caracteres03, k=4))
    codigo_04 = ''.join(random.choices(caracteres04, k=6))
    id_codigo = f'{init}:{codigo_01}-{codigo_02}-{codigo_03}-{codigo_04}'
    return id_codigo


