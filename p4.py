#file integrity checker
import hashlib

def file_hash(filename):
    h = hashlib.md5()

    with open(filename,'rb') as file:
         while chunk := file.read(4096):
              h.update(chunk)

    return h.hexdigest()
file1 = input("Enter file: ")
print("File hash:", file_hash(file1))
