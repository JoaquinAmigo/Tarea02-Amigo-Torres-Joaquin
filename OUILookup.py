#!/usr/bin/env python3

import subprocess
import getopt
import sys

#Archivo para la base de datos de manofacturadores.
DATA_FILE = "/home/joak/Tarea02-Amigo-Torres-Joaquin/manuf"
NETWORK = "192.168.1."

# Función para obtener los datos de fabricación de una tarjeta de red por IP
def obtener_datos_por_ip(ip):
	if ip.startswith(NETWORK):
		try:
			mac_info = subprocess.check_output(["arp", "-n", ip]).decode("utf-8")
			lines = mac_info.split("\n")
			if len(lines) > 1:
				mac_line=lines[1]
				if len(mac_line.split()) > 2:
					mac = mac_line.split()[2]
					obtener_datos_por_mac(mac)
				else:
					print(f"No se encontro dirección MAC la IP {ip}")
			else:
				print(f"No se encontro dirección MAC la IP {ip}")
		except Exception as e:
			print(f"Error al obtener la direccion MAC: {e}")
	else:
		print(f"Error: IP está fuera de la red del host")

# Función para obtener los datos de fabricación de una tarjeta de red por MAC
def obtener_datos_por_mac(mac):
	try:
		with open(DATA_FILE, "r") as file:
			lines = file.readlines()
			for line in lines:
				if line.startswith(mac):
					fabricante = line.split("\t")[1]
					print(f"MAC Address : {mac}")
					print(f"Fabricante : {fabricante}")
					return
			print(f"MAC Address : {mac}")
			print(f"Fabricante : No encontrado")
	except Exception as e:
		print(f"Error al obtener la informacion por direccion MAC : {e}")
# Función para obtener la tabla ARP
def obtener_tabla_arp():
	try:
		arp_info = subprocess.check_output(["arp","-n"]).decode("utf-8")
		print("IP/MAC/Vendor:")
		print(arp_info)
	except Exception as e:
		print(f"Error al obtener la tabla ARP : {e}")

def main(argv):

	ip = None
	mac = None
	mostrar_arp = False

	try:
		opts, args = getopt.getopt(argv, "i:m:a", ["ip=" , "mac=", "arp"])

	except getopt.GetoptError:
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
		obtener_datos_por_ip(ip)
	elif mac:
		obtener_datos_por_mac(mac)
	elif mostrar_arp:
		obtener_tabla_arp()
	else:
		print("Debe proporcionar una opción válida (--ip, --mac, --arp).")

if __name__ == "__main__":
    main(sys.argv[1:])
