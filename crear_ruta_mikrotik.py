import paramiko

# Datos de conexión
hostname = '192.168.3.189'
username = 'admin'
password = 'admin'

# Comando para crear la ruta
command = '/ip route add dst-address=10.10.10.0/24 gateway=10.10.10.2 comment=prueba2'

# Conexión SSH y ejecución del comando
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname, username=username, password=password)

stdin, stdout, stderr = client.exec_command(command)
print(stdout.read().decode())
print(stderr.read().decode())

client.close()
