import speech_recognition as sr
import serial
import time

# Funzione per inviare i comandi ad Arduino tramite USB
def invia_comando(modalita, stato):
    try:
        # Sostituisci '/dev/ttyACM0' con la porta corretta se necessario (es. 'COM3' su Windows)
        arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  
        time.sleep(2)  # Attendi che la connessione sia stabilita
        
        # Invia la modalità e lo stato come byte
        arduino.write(bytes([modalita, stato]))  # I valori devono essere interi tra 0 e 255
        
        # Leggi la risposta di Arduino (opzionale)
        response = arduino.readline().decode().strip()
        print("Risposta Arduino:", response)
        
        arduino.close()
    except Exception as e:
        print("Errore nella comunicazione USB:", e)

# Funzione per il comando vocale "perché"
def maperche():
    print("maperchè")

# Dizionario comandi vocali
comandi = {
    "perché": maperche,
    "accendi luci": lambda: invia_comando(1, 1),
    "spegni luci": lambda: invia_comando(1, 0),
    "accendi allarme": lambda: invia_comando(2, 1),
    "spegni allarme": lambda: invia_comando(2, 0),
    "imposta timer": lambda: invia_comando(3, 1),
    "spegni timer": lambda: invia_comando(3, 0),
    "fine": exit
}

# Inizializzazione del riconoscitore vocale
r = sr.Recognizer()
while True:
    with sr.Microphone() as source:
        print("Parla ora:")
        audio = r.listen(source)
        try:
            testo = r.recognize_google(audio, language='it-IT')
            testo = testo.lower().strip()
            print("Hai detto:", testo)
            if testo in comandi:
                comandi[testo]()
            elif testo == "comandi":
                print(comandi)
            else:
                print("Comando non riconosciuto.")
        except sr.UnknownValueError:
            print("Non ho capito")
