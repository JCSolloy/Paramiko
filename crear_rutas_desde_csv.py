import paramiko
import csv

# Nombre del archivo CSV
csv_file = 'rutas.csv'
errores_file = 'errores.csv'
errores = []


with open(csv_file, newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        hostname = row['hostname']
        username = row.get('username', 'admin')
        password = row.get('password', 'admin')
        dst = row['dst-address']
        gw = row['gateway']
        comment = row['comment']

        # Validaciones básicas
        if not hostname or not dst or not gw:
            print(f"Datos faltantes en la fila: {row}")
            row['error'] = 'Datos faltantes'
            errores.append(row)
            continue

        try:
            print(f'Conectando a {hostname}...')
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname, username=username, password=password, timeout=10)
            command = f'/ip route add dst-address={dst} gateway={gw} comment={comment}'
            stdin, stdout, stderr = client.exec_command(command)
            out = stdout.read().decode()
            err = stderr.read().decode()
            if err:
                print(f'Error al crear ruta {dst}: {err}')
                row['error'] = err.strip() or 'Error desconocido'
                errores.append(row)
            else:
                print(f'Ruta creada: {dst} -> {gw} ({comment})')
            client.close()
        except Exception as e:
            print(f'Error de conexión o ejecución en {hostname}: {e}')
            row['error'] = str(e)
            errores.append(row)

# Guardar errores en errores.csv si hubo alguno
if errores:
    fieldnames = list(errores[0].keys())
    with open(errores_file, 'w', newline='') as ef:
        writer = csv.DictWriter(ef, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(errores)
