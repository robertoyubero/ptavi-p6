#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys


class Cliente():

    IP_receptor = ''
    peticion = ''
    receptor = ''
    puertoSIP_receptor = 0

    metodos_sip = ["INVITE", "ACK", "BYE"]

    def leer_entrada(self, texto_entrada):
        """ Extraido los datos por la entrada"""
        try:
            self.peticion = texto_entrada[1]
            argumento = texto_entrada[2]
            self.receptor = argumento.split('@')[0]
            argumento = argumento.split('@')[1]
            self.IP_receptor = argumento.split(':')[0]
            self.puertoSIP_receptor = int(argumento.split(':')[1])

        except:
            print("Usage: python client.py method receiver@IP:SIPport")

    def get_peticion(self, tipo_peticion):
        """ Envío mi peticion: INVITE ó BYE """
        if tipo_peticion in self.metodos_sip:
            return tipo_peticion
        else:
            peticion = "peticion de ???"
            print(tipo_peticion + " es un tipo de petición no aceptada")


if __name__ == "__main__":

    if len(sys.argv) == 3:

        cliente = Cliente()
        cliente.leer_entrada(sys.argv)

        # Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        my_socket.connect((cliente.IP_receptor, cliente.puertoSIP_receptor))

        peticion = cliente.peticion
        #formo la peticion SIP
        dir_SIP = cliente.receptor + '@' + cliente.IP_receptor
        peticion = (peticion + ' sip:' + dir_SIP + ' SIP/2.0' + '\r\n')
        my_socket.send(bytes(peticion, 'utf-8'))
        print("\nEnviado: " + peticion)

        #-------------PRIMERA RESPUESTA--------------------
        respuesta = my_socket.recv(1024)
        respuesta = respuesta.decode('utf-8')
        codigo = int(respuesta.split('SIP/2.0 ')[-1][0:3])

        if codigo != 200:
            #mi peticion ha sido denegada
            print(respuesta)
            # Cerramos conexion
            my_socket.close()

        else:
            print('Recibido:')
            print(respuesta)

            #------------envio ACK
            peticion_ACK = ('ACK sip:' + dir_SIP + ' SIP/2.0' + '\r\n')
            my_socket.send(bytes(peticion_ACK, 'utf-8'))
            print('Enviado: ' + peticion_ACK)
            print('...Recibiendo paquetes\r\n')

            #espero a recibir el archivo
            respuesta = my_socket.recv(1024)
            print('Recibido: ' + respuesta.decode('utf8') + '\n')

            #------------envio BYE
            peticion_BYE = ('BYE sip:' + dir_SIP + ' SIP/2.0' + '\r\n')
            my_socket.send(bytes(peticion_BYE, 'utf-8'))
            print('Enviado: ' + peticion_BYE)

            respuesta = my_socket.recv(1024)
            print("Recibido: " + respuesta.decode('utf-8'))
            print("Cerramos la sesion SIP\n")
            my_socket.close()

    else:
        raise Exception("\nUsage: python server.py IP port audio_file")

    # Cerramos todo
    my_socket.close()
