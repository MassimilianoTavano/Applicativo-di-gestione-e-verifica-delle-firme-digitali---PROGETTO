'''
@mainpage
@author Tavano Massimiliano
@version 1.0
@section UML DIAGRAMMA UML DEL PROGETTO
@image html UMLCasiUsoGestioneFirmeDigitali.png
@section CLASS DIAGRAMMA DELLE CLASSI PRESENTI NEL PROGETTO
@image html UMLClassiGestioneFirmeDigitali.png
@section SEQUENCE DIAGRAMMA DI SEQUENZA
@image html UMLSequenzaGestioneFirmeDigitali.png
@file BackEnd.py
'''

import os
import yaml
import rsa


class Firma():
    '''Classe che permette di generare chiave per client e server e verificare l'integrità del messaggio'''
    def modules(self):
        '''Questa funzione prova a importare i moduli yaml ed rsa. Nel caso non siano installati verranno installate le versioni specificate nel file requirements.txt'''
        '''@param self riferimento all'oggetto stesso'''
        try:
            import yaml
            import rsa
        except:
            print("Installando librerie...")
            os.system("pip install -r requirements.txt")
            import yaml
            import rsa

    def yamlconfigsn(self):
        '''Funzione che permette di configurare 2 delle variabili più importanti del codice ovvero nome e porta del server.'''
        '''Queste serviranno a rendere il server riconoscibile.'''
        '''@param self riferimento all'oggetto stesso'''
        with open('Config.yaml', 'r') as ymlconfig:
            config = yaml.load(ymlconfig, Loader=yaml.FullLoader)
        return config["server_name"]

    def yamlconfigsp(self):
        '''Funzione che permette di configurare 2 delle variabili più importanti del codice ovvero nome e porta del server.'''
        '''Queste serviranno a rendere il server riconoscibile.'''
        '''@param self riferimento all'oggetto stesso'''
        with open('Config.yaml', 'r') as ymlconfig:
            config = yaml.load(ymlconfig, Loader=yaml.FullLoader)
        return config["server_port"]

    def generate_client_keys(self):
        '''Funzione che provvede alla generazione di chiave pubblica e privata del client'''
        '''@param self riferimento all'oggetto stesso'''
        (pubkey, privkey) = rsa.newkeys(2048)

        '''Questa istruzione scrive la chiave pubblica del server in un file'''
        with open('client_public_key.key', 'wb') as key_file:
            key_file.write(pubkey.save_pkcs1('PEM'))

        '''Questa istruzione scrive la chiave privata del server in un file'''
        with open('client_private_key.key', 'wb') as key_file:
            key_file.write(privkey.save_pkcs1('PEM'))
    def generate_server_keys(self):
        '''Questa funzione provvede alla generazione di chiave pubblica e privata del server'''
        '''@param self riferimento all'oggetto stesso'''
        (pubkey, privkey) = rsa.newkeys(2048)

        '''Questa istruzione scrive la chiave pubblica del server in un file'''
        with open('server_public_key.key', 'wb') as key_file:
            key_file.write(pubkey.save_pkcs1('PEM'))

        '''Questa istruzione scrive la chiave privata del server in un file'''
        with open('server_private_key.key', 'wb') as key_file:
            key_file.write(privkey.save_pkcs1('PEM'))