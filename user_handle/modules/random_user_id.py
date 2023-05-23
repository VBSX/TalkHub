import hashlib
import time

def generate_random_user_id(string):
    # gera um id aleatório para o usuário, ele se baseia no tempo atual e uma string para criar, e necessita
    # ter um tamanho de 35 caracteres para ser um id válido 
    lenght = 35
    to_hash = str(time.time()) + str(string)
    return hashlib.sha256(str(hash(to_hash)).encode('utf-8')).hexdigest()[:lenght]

if __name__ == '__main__':
    print(generate_random_user_id('asdasdas'))


def generate_random_chat_id(string):
    # gera um id aleatário para o chat, ele se baseia no tempo atual e uma string para criar, e necessita
    # ter um tamanho de 25 caracteres para ser um id válido 
    lenght = 25
    to_hash = str(time.time()) + str(string)
    return hashlib.sha256(str(hash(to_hash)).encode('utf-8')).hexdigest()[:lenght]