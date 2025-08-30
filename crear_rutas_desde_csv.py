import paramiko
import csv

errores = []



# Script para crear rutas en Mikrotik desde un archivo CSV usando Paramiko (SSH)
import paramiko
import csv

# Nombre del archivo CSV con las rutas a crear
csv_file = 'rutas.csv'
# Nombre del archivo donde se guardarán los errores
errores_file = 'errores.csv'
# Lista para almacenar las filas que presenten errores
errores = []


# Puerto SSH por defecto (puedes cambiarlo aquí)
ssh_port = 22

# Abrir el archivo CSV y procesar cada fila
with open(csv_file, newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Extraer los datos de cada columna
        hostname = row['hostname']
        username = row.get('username', 'admin')  # Usuario SSH, por defecto 'admin'
        password = row.get('password', 'admin')  # Contraseña SSH, por defecto 'admin'
        dst = row['dst-address']                 # Dirección de destino de la ruta
        gw = row['gateway']                      # Gateway de la ruta
        comment = row['comment']                 # Comentario de la ruta

        # Validar que los datos esenciales estén presentes
        if not hostname or not dst or not gw:
            print(f"Datos faltantes en la fila: {row}")
            row['error'] = 'Datos faltantes'
            errores.append(row)
            continue

        try:
            print(f'Conectando a {hostname}:{ssh_port}...')
            # Crear cliente SSH y aceptar claves automáticamente
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # Conectar al router Mikrotik usando el puerto definido
            client.connect(hostname, port=ssh_port, username=username, password=password, timeout=10)
            # Comando para agregar la ruta en Mikrotik
            command = f'/ip route add dst-address={dst} gateway={gw} comment={comment}'
            # Ejecutar el comando por SSH
            stdin, stdout, stderr = client.exec_command(command)
            out = stdout.read().decode()
            err = stderr.read().decode()
            # Si hay error, guardar la fila y el mensaje
            if err:
                print(f'Error al crear ruta {dst}: {err}')
                row['error'] = err.strip() or 'Error desconocido'
                errores.append(row)
            else:
                print(f'Ruta creada: {dst} -> {gw} ({comment})')
            # Cerrar la conexión SSH
            client.close()
        except Exception as e:
            # Si ocurre una excepción, guardar la fila y el error
            print(f'Error de conexión o ejecución en {hostname}:{ssh_port}: {e}')
            row['error'] = str(e)
            errores.append(row)

# Si hubo errores, guardarlos en errores.csv para revisión
if errores:
    fieldnames = list(errores[0].keys())
    with open(errores_file, 'w', newline='') as ef:
        writer = csv.DictWriter(ef, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(errores)
