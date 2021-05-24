'''@file Client.py'''
import BackEnd
from tkinter import *
import tkinter as tk
from socket import *
import rsa
import time


class Client(tk.Frame):
    '''Classe che permette la visualizzazione di una finestra dal lato client e l'invio del contenuto di un file di testo per la verifica della sua integrità'''
    def __init__(self):
        '''Costruttore'''
        '''@param self riferimento all'oggetto stesso'''
        tk.Frame.__init__(self, master=None)
        self.master.title("Client")
        self.master.geometry("800x800+500+50")
        self.master.resizable(False, False)
        self.master.config(bg="black")
        self.master.iconbitmap("Signature.ico")
        self.insert_widgets()

    def insert_widgets(self):
        '''@param self riferimento all'oggetto stesso'''
        '''Funzione che permette la visualizzazione di elementi nella finestra.'''
        self.label = tk.Label(
            text="Salve, si prega di inserire nel campo sottostante ciò che si vuole inviare al server.")
        self.label.config(bg="SteelBlue", font=("Times New Roman", 12))
        self.label.place(x=130, y=20)
        self.scrollbarc = tk.Scrollbar()
        self.scrollbarc.pack(side=tk.RIGHT, fill=Y)
        self.textfieldc = Text(bg="antique white", height=38, yscrollcommand=self.scrollbarc.set)
        self.label1 = tk.Label(
            text="Questo software inserirà in un file il contenuto del campo di testo e verificherà che esso rimanga integro durante l'invio.")
        self.label1.config(bg="light green", font=("Times New Roman", 10))
        self.label1.place(x=60, y=55)
        self.textfieldc.place(x=60, y=90)
        self.scrollbarc.config(command=self.textfieldc.yview)
        self.write_button = tk.Button(font=("Times New Roman", 10), bg="salmon", text="Inserisci", width=15, height=2,
                                      command=lambda: self.write()).place(x=460, y=720)
        self.send_button = tk.Button(font=("Times New Roman", 10), bg="salmon", text="Invia", width=15, height=2,
                                     command=lambda: self.sendfile()).place(x=590, y=720)
        self.labelsocketc = tk.Label(text="Stato Socket:", font=("Times New Roman", 11))
        self.labelsocketc.place(x=60, y=715)
        self.state_client_connection = tk.Label(text="Stato Connessione: ", font=("Times New Roman", 11))
        self.state_client_connection.place(x=60, y=745)

    def write(self):
        '''Funzione che permette di scrivere il contenuto del campo di testo su un file temporaneo.'''
        '''@param self riferimento all'oggetto stesso'''
        string = self.textfieldc.get('1.0', 'end')
        writtenfile = open("WrittenFile.txt", "w")
        writtenfile.write(string)
        writtenfile.close()

    def sendfile(self):
        '''Funzione che si occupa di inviare al server tutto ciò che gli serve per verificare l'integrità del messaggio'''
        '''Ciò che viene mandato è la firma, il messaggio integro e la chiave pubblica del client.'''
        '''@param self riferimento all'oggetto stesso'''
        message=file_open("WrittenFile.txt")
        privatekey = rsa.PrivateKey.load_pkcs1(file_open("client_private_key.key"))
        with open('client_public_key.key','rb') as file:
            publickey=file.read()
        try:
            clientSocket.send(publickey)
        except:
            client.state_client_connection.config(text="Stato Connessione: Connessione Chiusa")
        clientSocket.send(message)
        '''Questa istruzione è stata inserita spontaneamente poichè servirà per simulare il malintenzionato intromessosi nella rete il quale modificherà il file'''
        time.sleep(10)
        message=file_open("WrittenFile.txt")
        signature = rsa.sign(message, privatekey, "SHA-512")
        s = open('signature_file.txt', 'wb')
        s.write(signature)
        s.close()
        with open('signature_file.txt','rb') as file:
            signature=file.read()
        clientSocket.send(signature)


def file_open(file):
    '''Funzione che permette di aprire un file e restituire l'intero messaggio di tale file per facilitarne l'invio.'''
    '''@param file file che dovrà essere letto'''
    key_file = open(file, "rb")
    key_data = key_file.read()
    key_file.close()
    return key_data


firma = BackEnd.Firma()
firma.modules()
firma.generate_client_keys()
server_name = firma.yamlconfigsn()
server_port = firma.yamlconfigsp()
client = Client()
clientSocket = socket(AF_INET, SOCK_STREAM)
if (clientSocket):
    client.labelsocketc.config(text="Stato Socket: Creato")
else:
    client.labelsocketc.config(text="Stato Socket: Errore nella creazione del socket.")
try:
    clientSocket.connect((server_name, server_port))
    client.state_client_connection.config(text="Stato Connessione: Connesso")
except:
    client.state_client_connection.config(text="Stato Connessione: Il Client non è riuscito a connettersi.")
client.mainloop()