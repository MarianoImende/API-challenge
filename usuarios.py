import csv
import random
import string
import bcrypt

# Función para generar un correo electrónico ficticio
def generar_correo():
    dominios = ['gmail.com', 'yahoo.com', 'hotmail.com', 'example.com']
    nombre = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
    dominio = random.choice(dominios)
    return f'{nombre}@{dominio}'

# Función para generar una contraseña ficticia
def generar_contraseña():
    caracteres_permitidos = string.ascii_letters + string.digits + '*-+'
    longitud = random.randint(8, 12)
    return ''.join(random.choice(caracteres_permitidos) for _ in range(longitud))

# Generar 100 pares de correo y contraseña ficticios
datos = [(generar_correo(), generar_contraseña()) for _ in range(100)]

# Escribir los datos en un archivo CSV
with open('datos.csv', 'w', newline='') as archivo_csv:
    escritor = csv.writer(archivo_csv)
    escritor.writerow(['Correo', 'Contraseña'])  # Escribir encabezados
    escritor.writerows(datos)  # Escribir los datos


def pwd():
    password = "challenge".encode('utf-8')  # Codificar la contraseña como bytes
    salt = bcrypt.gensalt()  # Generar una sal (salt) aleatoria
    hashed_password = bcrypt.hashpw(password, salt)  # Generar el hash bcrypt
    print(hashed_password.decode('utf-8'))  # Imprimir el hash como una cadena
    
   
if __name__ == "__main__":
     pwd()