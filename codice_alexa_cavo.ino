#include <LiquidCrystal.h>

const int ledPin = 13;                  // LED collegato al pin 13
const int buzzerPin = 12;               // Buzzer collegato al pin 12

// Definizione dei pin per il display LCD (RS, E, D4, D5, D6, D7)
LiquidCrystal lcd(2, 3, 4, 5, 6, 7);

int modalita = 0;
int stato = 0;

unsigned long tempoIniziale = 0;        // Variabili per il cronometro
bool running = false;

void setup() {

  Serial.begin(9600);                    // Avvia la comunicazione seriale
  
  pinMode(ledPin, OUTPUT);               // Inizializza il LED e il buzzer
  pinMode(buzzerPin, OUTPUT);
  
  lcd.begin(16, 2);                      // Inizializza il display (16 colonne, 2 righe)
  lcd.print("Arduino Inizializzato");
  delay(2000);
  lcd.clear();
}

void loop() {
  // Controlla se ci sono dati disponibili sulla porta seriale
  if (Serial.available() >= 2) {
    modalita = Serial.read();                  // Legge la modalità (1, 2, 3)
    stato = Serial.read();                     // Legge lo stato (0 o 1)
    
    // Azione in base alla modalità
    switch (modalita) {
      case 1:                          // Modalità LED
        if (stato == 1) {
          digitalWrite(ledPin, HIGH);  // Accende il LED
          lcd.clear();
          lcd.print("LED Acceso");
        } else {
          digitalWrite(ledPin, LOW);   // Spegne il LED
          lcd.clear();
          lcd.print("LED Spento");
        }
        break;
        
      case 2:                             // Modalità Buzzer (Sirena)
        if (stato == 1) {
          digitalWrite(buzzerPin, HIGH);  // Accende il buzzer
          lcd.clear();
          lcd.print("Buzzer Attivo");
        } else {
          digitalWrite(buzzerPin, LOW);   // Spegne il buzzer
          lcd.clear();
          lcd.print("Buzzer Spento");
        }
        break;
        
      case 3:                          // Modalità Cronometro con LCD
        if (stato == 1) {
          if (!running) {
            tempoIniziale = millis();  // Inizia il cronometro
            running = true;
            lcd.clear();
            lcd.print("Cronometro Avviato");
          }
        } else {
          running = false;
          lcd.clear();
          lcd.print("Cronometro Fermato");
        }
        break;
        
      default:
        lcd.clear();
        lcd.print("Modalita non valida");
        break;
    }
  }
  
  // Se la modalità è 3 (cronometro) e il cronometro è in esecuzione
  if (modalita == 3 && running) {
    unsigned long tempoContato = millis() - tempoIniziale;
    int secondi = (tempoContato / 1000) % 60;
    int minuti = (tempoContato / 60000) % 60;
    
    lcd.setCursor(0, 1);  // Posiziona il cursore sulla seconda riga
    lcd.print("Tempo: ");
    lcd.print(minuti);
    lcd.print(":");
    if (secondi < 10) lcd.print("0");
    lcd.print(secondi);
  }
}
