import subprocess
import getopt
import sys
import ipaddress #Con esto podremos verificar si la ip pertenece a la misma red o no

#Archivo para la base de datos de manofacturadores.
DATA_FILE = "manuf.txt"

# Función para obtener los datos de fabricación de una tarjeta de red por IP
def obtener_datos_por_ip(ip):
	try:
		mac_info = subprocess.check_output(["arp", "-n", ip]).decode("utf-8")
		lineas = mac_info.split("\n")
		if len(lineas) > 1:
			mac = lineas[1].split()[2]
			obtencion_datos_mac(mac)
		else:
			print(f"No se encontro dirección MAC la IP {ip}")
	except Exception as e:
		print(f"Error al obtener la direccion MAC: {e}")
    # Implementa la lógica para obtener los datos por IP aquí
   # print("Aqui su codigo para obtener los datos por ip")
   # pass

# Función para obtener los datos de fabricación de una tarjeta de red por MAC
def obtener_datos_por_mac(mac):
	try:
		with open(DATA_FILE, "r") as file:
			lineas = file.readlines()
			for linea in lineas:
				if linea.startswith(mac):
					manofacturadores = linea.split("\t")[1]
					print(f"MAC Address : {mac}")
					print(f"Fabricante : {manofacturadores}")
					return
			print(f"MAC Address : {mac}")
			print(f"Fabricante : No encontrado")
	except Exception as e:
		print(f"Error al obtener la informacion por direccion MAC : {e}")
    # Implementa la lógica para obtener los datos por MAC aquí
   # print("Aqui su codigo para obtener los datos por mac")
   # pass

# Función para obtener la tabla ARP
def obtener_tabla_arp():
        # Implementa la lógica para procesar la tabla ARP aquí
	try:
		arp_info = subprocess.check_output(["arp","-n"]).decode("utf-8")
		print("IP/MAC/Vendor:")
		print(arp_info)
	except Exception as e:
		print(f"Error al obtener la tabla ARP : {e}")

	 # Imprime la tabla ARP
# pass


def main(argv):

	ip = None
	mac = None
	mostrar_arp = False

	try:
		opts, args = getopt.getopt(argv, "i:m:a", ["ip=", "mac=", "arp"])

	except getopt.GeetoptError
		print("Uso: python OUILookup.py --ip <IP> | --mac <MAC> | --arp")
		sys.exit(2)

	for opt, arg in opts:
		if opt in ("-i", "--ip"):
			ip = arg
		elif opt in ("-m","--mac"):
			mac = arg
		elif opt in ("-a", "--arp"):
			mostrar_arp = True
	if ip:
		if ipaddress.IPv4Address(ip) in ipaddress.IPv4Network("192.168.1.30/24"):
			obtener_datos_por_ip(ip)
		else:
			print("Error: La IP esta fuera de la red del host")
	elif mac:
		obtener_datos_por_mac(mac)
	elif mostrar_arp:
		obtener_tabla_arp()
	else:
		print("Debe proporcionar una opción válida (-i, -m, -a).")

if __name__ == "__main__":
    main(sys.argv[1:])
