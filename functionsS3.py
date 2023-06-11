import os
import boto3
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

bucket_name = 'lab09-mguzman'

client = boto3.client('s3',
                      aws_access_key_id =os.getenv('AWS_ACCESS_KEY_ID'),
                      aws_secret_access_key =os.getenv('AWS_SECRET_ACCESS_KEY'),
                      )

def cargarS3(key, file_root):
    client.upload_file(file_root, bucket_name, key)
    print('Archivo cargado')

def descargarS3(key, file_root):
    with open(file_root, "wb") as data:
        client.download_fileobj(bucket_name, key, data)
    print("Archivo descargado")

def eliminarS3(key):
    client.delete_object(Bucket=bucket_name, Key=key)
    print('Archivo eliminado')

def editarS3(key, file_root, old_key):
    eliminarS3(old_key)
    cargarS3(key, file_root)
    print('Archivo Actualizado')


# cargar(client)
# descargar (client)
# eliminar(client)
