import serial
import time

# Funzione per inviare i comandi ad Arduino tramite Bluetooth
def invia_comando(modalita, stato):
    try:
        arduino = serial.Serial('/dev/rfcomm0', 9600, timeout=1)
        time.sleep(2)  # Aspetta che la connessione venga stabilita
        arduino.write(bytes([modalita, stato]))  # Invia i dati come byte
        response = arduino.readline().decode().strip()
        print("Risposta Arduino:", response)
        arduino.close()
    except Exception as e:
        print("Errore nella comunicazione Bluetooth:", e)

# Funzione per comando "perché"
def maperche():
    print("maperchè")

# Dizionario dei comandi
comandi = {
    "perché": maperche,
    "accendi luci": lambda: invia_comando(1, 1),
    "spegni luci": lambda: invia_comando(1, 0),
    "accendi allarme": lambda: invia_comando(2, 1),
    "spegni allarme": lambda: invia_comando(2, 0),
    "imposta timer": lambda: invia_comando(3, 1),
    "spegni timer": lambda: invia_comando(3, 0),
    "comandi": lambda: print(list(comandi.keys())),
    "fine": exit
}

# Interfaccia testuale
while True:
    comando = input("Inserisci un comando (scrivi 'comandi' per l'elenco): ").lower().strip()
    if comando in comandi:
        comandi[comando]()
    else:
        print("Comando non riconosciuto.")
