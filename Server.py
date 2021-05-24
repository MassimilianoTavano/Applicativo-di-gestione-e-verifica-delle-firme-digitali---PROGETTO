'''@file Server.py'''
import BackEnd
from socket import *
import rsa
import threading
serverSocket = socket(AF_INET, SOCK_STREAM)
class Server():
    '''Classe che permette di ricevere alcuni parametri i quali saranno messagio integro, firma, chiave pubblica del client per verificare l'integrità del messaggio dopo esser stato inviato. '''
    def do_operations(self):
        '''Funzione che si occupa di creare il socket del server stabilire la connessione con il client e ricevere parametri quali messaggio, firma e chiave pubblica'''
        '''Questi serviranno per verificare l'integrità del messaggio.'''
        '''@param self riferimento all'oggetto stesso'''
        if (serverSocket):
            print("Socket creato con successo.")
        else:
            print("Errore nella creazione del socket.")
        serverSocket.bind((server_name, server_port))
        serverSocket.listen(1)
        serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        print("In attesa di connessione...")
        self.connection()
    def verify(self,connessione):
        '''Funzione vera e propria che si occupa di ricevere tutti i parametri e di verificare poi con essi l'integrità del messaggio'''
        '''Questa fa sì che il server rimanga sempre in attesa'''
        '''@param self riferimento all'oggetto stesso'''
        '''@param connessione connessione con il client'''
        while True:
            try:
                publickey = connessione.recv(2048).decode()
                with open('public_key.key', 'w') as file:
                    file.write(publickey)
                publickey = rsa.PublicKey.load_pkcs1(file_open("public_key.key"))
                message = connessione.recv(2048)
                signature = connessione.recv(2048)
                rsa.verify(bytes(message), bytes(signature), publickey)
                print("Signature successfully verified")
                print("Il messaggio inviato dal client è: ")
                print(message.decode())
            except:
                print("Signature could not be verified or connection closed by the host")
                connessione.close()
                break
    def connection(self):
        '''Funzione che si occupa di accettare connessioni e startare un thread il quale permettera la continua disponibilità del server a ricevere parametri per la verifica dell'integrità del messaggio'''
        '''@param self riferimento all'oggetto stesso'''
        while True:
            connessione, address = serverSocket.accept()
            if connessione:
                print("Richiesta di connessione accettata.")
                print("Client connesso da", address)
            threadricezione = threading.Thread(target=self.verify, args=(connessione,))
            threadricezione.start()

def file_open(file):
    '''Questa funzione permette di aprire un file e restituire l'intero messaggio di tale file per facilitarne l'invio.'''
    '''@param file file che dovrà essere letto'''
    key_file = open(file, "rb")
    key_data = key_file.read()
    key_file.close()
    return key_data

server=Server()
firma = BackEnd.Firma()
firma.modules()
firma.generate_server_keys()
server_name = firma.yamlconfigsn()
server_port = firma.yamlconfigsp()
server.do_operations()