from passlib.hash import sha256_crypt
import hashlib
import time
def generate_random_user_id():
    lenght = 21
    return hashlib.sha256(str(hash(time.time())).encode('utf-8')).hexdigest()[:lenght]
    
    # return hashlib.sha256(str(hash(time.time())).encode('utf-8')).hexdigest()

print(generate_random_user_id())


