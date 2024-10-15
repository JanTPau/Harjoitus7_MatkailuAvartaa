import tkinter as tk
import threading
import time
import random
import winsound

# Tkinterillä sininen kangas kuvaamaan merta
ikkuna = tk.Tk()
ikkuna.title("Autiosaari: Apinat ja Ojat")
ikkuna.geometry("800x800")
kangas = tk.Canvas(ikkuna, bg='lightblue', width=800, height=800)
kangas.pack()

#Sanakirja saarille
saaret={}
saarien_maara=0
saaren_sade = 50
maksimi_saaret = 10

#Funcktio saaren lisäämiseen
def saaren_lisays():
        global saarien_maara
        #Tarkistetaan että saarien määrä ei ole ylittänyt kymmenen maksimia
        if saarien_maara >= maksimi_saaret:
            print("Merelle mahtuu vain 10 saarta!")
            return  

        saarien_maara += 1
        nimi = f'S{saarien_maara}'

        #Tarkistetaan että saaret ei mene päällekkäin, sitten arvotaan koordinaatit
        sopiva_sijainti = False
        while not sopiva_sijainti:
            x = random.randint(20 + saaren_sade, 780 - saaren_sade)
            y = random.randint(20 + saaren_sade, 750 - saaren_sade)

            saaret_paallekkain = False
            for saari in saaret:
                if saari != 'Saarien maara':
                    jo_tehty_saari_x = saaret[saari]['sijainti']['x']
                    jo_tehty_saari_y = saaret[saari]['sijainti']['y']
                    if (x - jo_tehty_saari_x) ** 2 + (y - jo_tehty_saari_y) ** 2 < (saaren_sade * 2) ** 2:
                        saaret_paallekkain = True
                        break

            if not saaret_paallekkain:
                sopiva_sijainti = True

        saaret[nimi] = {
        'sijainti': {
            'x': x,
            'y': y
        }
    }
        #Piirtää saaria kuvastavia ympyröitä
        sade = 50
        kangas.create_oval(x - sade, y - sade, x + sade, y + sade, fill="green", outline="black")
        kangas.create_text(x, y - sade + 50, text=nimi, fill="black")

        
#Nappi jota painamalla "tulivuori purkautuu" eli syntyy saaria
#Käyttää saaren lisays funktiota
tulivuorenpurkaus = tk.Button(ikkuna, text="Tulivuorenpurkaus", command=saaren_lisays)
tulivuorenpurkaus.place(x=350, y=750)

ikkuna.mainloop()