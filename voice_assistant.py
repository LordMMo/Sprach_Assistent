import speech_recognition as sr
import pyttsx3
import datetime
import pywhatkit
import webbrowser
from timer_GUI import TimerGUI

# Initialisieren der Spracherkennung- und Text-to-Speech-Engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Wählen eine Stimme aus der Liste der verfügbaren Stimmen
voices = engine.getProperty('voices')
selected_voice = voices[0]
engine.setProperty('voice', selected_voice.id)

voice_assistant_running = None


# Funktion zu sprechen
def sprech(text):
    engine.say(text)
    engine.runAndWait()


# Funktion zum Verarbeiten von Befehlen
def Prozessbefehl(befehl):
    if "datum" in befehl:
        sprech(get_date_time())
    elif "rechne" in befehl:
        math = befehl.split("rechne")[1].strip()
        sprech(Matheaufgabe(math))
    elif "timer" in befehl:
        try:
            minutes = int(befehl.split("timer")[1].strip().split(" ")[0])
            set_timer(minutes)
        except ValueError:
            sprech("Bitte geben Sie eine gültige Zeit für den Timer an.")
    elif "suche nach" in befehl:
        Abfrage = befehl.split("suche nach")[1].strip()
        googeln(Abfrage)
    elif "öffne" in befehl:
        Webseite = befehl.split("öffne")[1].strip().lower()
        open_Webseite(Webseite)
    elif "stop" in befehl:
        stop()
    else:
        sprech("Ich habe den Befehl nicht verstanden.")


# Funktion zum Abrufen von Datum und Uhrzeit
def get_date_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    current_date = now.strftime("%d-%m-%Y")
    print("Aktuelles Datum ist",current_date, ". Es ist",current_time," Uhr.")
    return f"Aktuelles Datum ist {current_date}. Es ist {current_time} Uhr."


# Funktion zum Öffnen einer Webseite
def open_Webseite(Webseite):
    if not Webseite.startswith("http://") and not Webseite.startswith("https://"):
        Webseite = Webseite + ".com"
        print("Ich öffne",Webseite)
    sprech(f"Ich öffne {Webseite}")
    try:
        webbrowser.open(Webseite)
    except Exception as e:
        sprech(f"Es gab einen Fehler beim Öffnen der Webseite: {e}")


# Funktion zur Suche bei Google mit pywhatkit
def googeln(Abfrage):
    print("Ich suche nach",Abfrage,"auf Google.")
    sprech(f"Ich suche nach {Abfrage} auf Google.")
    pywhatkit.search(Abfrage)


# Funktion zum Einstellen eines Timers
def set_timer(minutes, seconds=0):
    print("Ich stelle einen Timer für",minutes,"Minuten und",seconds,"Sekunden.")
    sprech(f"Ich stelle einen Timer für {minutes} Minuten und {seconds} Sekunden.")
    timer_gui = TimerGUI(minutes, seconds)
    timer_gui.start()


# Funktion zum Lösen eine Matheaufgabe
def Matheaufgabe(math):
    operators = set('+-*/')

    for op in operators:
        if op in math:
            operator = op
            operands = math.split(op)
            break
    else:
        return "Ungültiger mathematischer Ausdruck."

    # Versuche die Berechnung
    try:
        operand1 = float(operands[0].strip())
        operand2 = float(operands[1].strip())

        if operator == '+':
            result = operand1 + operand2
        elif operator == '-':
            result = operand1 - operand2
        elif operator == '*':
            result = operand1 * operand2
        elif operator == '/':
            result = operand1 / operand2
        else:
            return "Ungültiger Operator."
        print("Das Ergebnis der Rechnung",math,"ist",result,".")
        return f"Das Ergebnis der Rechnung {math} ist {result}."
    except ValueError:
        return "Ungültige Operanden. Bitte geben Sie numerische Werte ein."
    except ZeroDivisionError:
        return "Division durch Null ist nicht erlaubt."
    except Exception as e:
        return f"Fehler bei der Berechnung: {e}"


# Funktion zur Spracheingabe
def Spracheingabe():
    global voice_assistant_running
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=3)
            befehl = recognizer.recognize_google(audio, language="de-DE").lower()
            Prozessbefehl(befehl)
        except sr.UnknownValueError:
            print("Ich habe Sie nicht verstanden.")
            sprech("Ich habe Sie nicht verstanden.")
        except sr.RequestError as e:
            sprech(f"Fehler bei der Google-Spracherkennung; {e}")


# Funktion zum Starten des Sprachassistenten
def start():
    global voice_assistant_running
    voice_assistant_running = True
    print("Hallo! Wie kann ich Ihnen helfen?")
    sprech("Hallo! Wie kann ich Ihnen helfen?")
    while voice_assistant_running:
        Spracheingabe()


# Funktion zum Stoppen des Sprachassistenten
def stop():
    global voice_assistant_running
    voice_assistant_running = False
    sprech("Voice Assistent wird gestoppt")
    print("Voice Assistent wird gestoppt!")
    print("Tschüss.. Bis Bald")
    sprech("Tschüss.. Bis Bald")
