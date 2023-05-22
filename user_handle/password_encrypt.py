from passlib.hash import sha256_crypt

class PasswordCrypter():
    def encrypt(self, password):
        return sha256_crypt.hash(password)
    
    def decrypt(self,password, hash_password):
        return sha256_crypt.verify(password,hash_password)
    
    
if __name__ == "__main__":
    pass_crypt = PasswordCrypter()
    password = "123456"
    hash_password = pass_crypt.encrypt(password)
    print(hash_password)
    print(pass_crypt.decrypt(password,hash_password))