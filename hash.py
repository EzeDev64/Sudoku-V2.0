import hashlib

# 1. El texto que queremos procesar
texto = "174932"

# 2. SHA-256 trabaja con BYTES, por lo que debemos codificar el string usando .encode()
texto_en_bytes = texto.encode('utf-8')

# 3. Creamos el objeto hash y le pasamos los bytes
objeto_hash = hashlib.sha256(texto_en_bytes)

# 4. Obtenemos el resultado final en un formato legible (hexadecimal)
hash_resultado = objeto_hash.hexdigest()

print("Texto original:", texto)
print("Código SHA-256 :", hash_resultado)