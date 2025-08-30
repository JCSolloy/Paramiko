# Paramiko Mikrotik Automation

Este proyecto permite automatizar la gestión de rutas en routers Mikrotik usando Python y la librería Paramiko (SSH).

## Requisitos
- Python 3.7+
- Acceso SSH al router Mikrotik

## Instalación
1. Clona el repositorio:
	```
	git clone https://github.com/JCSolloy/Paramiko.git
	cd Paramiko
	```
2. Crea y activa un entorno virtual:
	```
	python -m venv paramiko
	.\paramiko\Scripts\Activate
	```
3. Instala las dependencias:
	```
	pip install -r requirements.txt
	```

## Uso
### Crear una ruta individual
Edita `crear_ruta_mikrotik.py` con los datos de tu router y ejecuta:
```
python crear_ruta_mikrotik.py
```

### Crear rutas desde un archivo CSV
1. Edita `rutas.csv` con las columnas:
	- hostname
	- dst-address
	- gateway
	- comment
2. Ejecuta:
```
python crear_rutas_desde_csv.py
```

Los errores se guardarán en `errores.csv`.

## Ejemplo de rutas.csv
```
hostname,dst-address,gateway,comment
192.168.3.189,192.168.1.0/24,10.10.10.1,zabbix
192.168.3.189,192.168.2.0/24,10.10.10.2,zabbix
```

## Notas
- No subas el entorno virtual al repositorio, usa `.gitignore`.
- Puedes modificar los scripts para otras automatizaciones SSH en Mikrotik.

## Autor
JCSolloy
# Paramiko
