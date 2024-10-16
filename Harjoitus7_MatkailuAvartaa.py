import tkinter as tk
import threading
import time
import random
import winsound

# Tkinterillä sininen kangas kuvaamaan merta
ikkuna = tk.Tk()
ikkuna.title("Saaristo")
ikkuna.geometry("800x800")
kangas = tk.Canvas(ikkuna, bg='lightblue', width=800, height=800)
kangas.pack()

saaret={}           #Sanakirja, jossa säilytetään saarten tiedot (sijainti ja apinat).
saarien_maara=0     #Laskuri, joka seuraa kuinka monta saarta on luotu.
saaren_sade = 50    #Saarten säde, joka määrittelee, kuinka suuren alueen saari vie.
maksimi_saaret = 10 #Maksimi määrä saaria, jotka voivat olla merellä kerralla.
apinoiden_maara = 10#Kuinka monta apinaa lisätään saarelle.

#Globaali muuttuja jota käytetään apinan tekemisten looppaamisessa
running = True

#Funktio saaren lisäämiseen
def saaren_lisays():
        global saarien_maara, saaren_sade
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
                    jo_tehty_saari_x = saaret[saari]['sijainti'].get('x')
                    jo_tehty_saari_y = saaret[saari]['sijainti'].get('y')
                    if jo_tehty_saari_x is not None and jo_tehty_saari_y is not None:
                        if (x - jo_tehty_saari_x) ** 2 + (y - jo_tehty_saari_y) ** 2 < (saaren_sade * 2) ** 2:
                            saaret_paallekkain = True
                            break

            if not saaret_paallekkain:
                sopiva_sijainti = True

        saaret[nimi] = {
        'sijainti': {
            'x': x,
            'y': y},
        'apinat': []
    }       
        
        #Piirtää saaria kuvastavia ympyröitä
        saaren_sade = 50
        kangas.create_oval(x - saaren_sade, y - saaren_sade, x + saaren_sade, y + saaren_sade, fill="green", outline="black")
        kangas.create_text(x, y - saaren_sade + 50, text=nimi, fill="black")
        
        #Lisää apinoita saarelle nimen ja ääntelytaajuuden kanssa
        apinan_koko = 10
        for i in range(apinoiden_maara):
            apina_nimi = f'Apina{i+1} ({nimi})'
            taajuus = random.randint(400, 2000)
            offset_x = random.randint(-saaren_sade + 10, saaren_sade - 10)
            offset_y = random.randint(-saaren_sade + 10, saaren_sade - 10)
            saaret[nimi]['apinat'].append({
                'nimi': apina_nimi,
                'taajuus': taajuus,
                'apina_ympyrä': kangas.create_oval(
                x + offset_x - apinan_koko // 2,
                y + offset_y - apinan_koko // 2,
                x + offset_x + apinan_koko // 2,
                y + offset_y + apinan_koko // 2,
                fill="brown", 
                outline="black"
            ),
            'suunta': None #Uintia varten alustettu suunta
        })
            
        # Käynnistä apinoiden toiminta (äänet ja kuoleman tarkistus)
        kaynnista_apinat(nimi)
            
        # Ensimmäinen saari saa myös laiturit pohjoiseen, etelää, länteen ja itään
        if nimi == "S1":
            stick_length = 20
            stick_width = 2

            kangas.create_line(x, y - saaren_sade, x, y - saaren_sade - stick_length, width=stick_width, fill="brown")
            kangas.create_line(x, y + saaren_sade, x, y + saaren_sade + stick_length, width=stick_width, fill="brown")
            kangas.create_line(x - saaren_sade, y, x - saaren_sade - stick_length, y, width=stick_width, fill="brown")
            kangas.create_line(x + saaren_sade, y, x + saaren_sade + stick_length, y, width=stick_width, fill="brown")
            


# Funktio joka tappaa apinoita nauruun (1% todennäköisyys)
def apina_kuolee_nauruun():
    return random.random() < 0.01

# Funktio joka hoitaa yksittäisen apinan ääntelyn ja kuoleman tarkistamisen
def apina_toiminta(saari_nimi, apina_index):
    global running
    while running:
        saari = saaret[saari_nimi]

        if not saari:
            print(f"Saarta '{saari_nimi}' ei löydy.")
            return
    
        # Tarkista, onko apina jo kuollut
        if apina_index >= len(saari['apinat']):
            return
        
        #Haetaan apina listalta
        apina = saari['apinat'][apina_index]

        # Jos apina kuolee nauruun, poista apina
        if apina_kuolee_nauruun():
            print(f"{apina['nimi']} kuoli nauruun!")
            winsound.PlaySound("Laugh+2.wav", winsound.SND_FILENAME)
            kangas.delete(apina['apina_ympyrä'])
            saari['apinat'].pop(apina_index)
            return

        # Apina ääntää
        taajuus = apina['taajuus']
        print(f"{apina['nimi']} ääntää taajuudella {taajuus} Hz")
        winsound.Beep(taajuus, 500)

        time.sleep(10)  # Viivästys 10 sekuntia ennen seuraavaa ääntelyä ja nauruun kuolemisen mahdollisuutta

# Funktio joka luo uudet säikeet jokaiselle apinalle saarella
def kaynnista_apinat(saari_nimi):
    saari = saaret[saari_nimi]
    for i, apina in enumerate(saari['apinat']):
        threading.Thread(target=apina_toiminta, args=(saari_nimi, i), daemon=True).start()


# Funktio nollausnapille. Nollaa kaiken, ja valmistaa saaret dictionaryn
#uusien saarten luomisen varalle
def reset():
    global saaret, saarien_maara, running
    running = False
    saaret.clear()
    kangas.delete("all")
    saarien_maara = 0
    for i in range(1, 11):
        saaret[f'S{i}'] = {
        'apinat': [], 
        'sijainti': {}
    }
    running = True
    threading.Thread(target=apina_ui, daemon=True).start()

# Funktio apinan uimiseen satunnaiseen suuntaan
def liikuta_apinaa(saari_nimi, apina_index):
    saari = saaret[saari_nimi]

    #Jos apina on jo kuollut niin return
    if apina_index >= len(saari['apinat']):
        return
    
    apina = saari['apinat'][apina_index]

    if not kangas.coords(apina['apina_ympyrä']):
        return

    nyky_koordinaatit = kangas.coords(apina['apina_ympyrä'])
    nykyinen_x = (nyky_koordinaatit[0] + nyky_koordinaatit[2]) / 2
    nykyinen_y = (nyky_koordinaatit[1] + nyky_koordinaatit[3]) / 2
    
    # Jos suuntaa ei ole vielä valittu, apina valitsee se pohjoisesta, etelästä, idästä tai lännestä
    if apina['suunta'] is None:
        apina['suunta'] = random.choice(['pohjoinen', 'etelä', 'länsi', 'itä'])

    uinti_askel = 10
    
    # Päivitä apinan sijaintia riippuen suunnasta
    if  apina['suunta'] == 'pohjoinen':
        uusi_x, uusi_y = nykyinen_x, nykyinen_y - uinti_askel
    elif  apina['suunta'] == 'etelä':
        uusi_x, uusi_y = nykyinen_x, nykyinen_y + uinti_askel
    elif  apina['suunta'] == 'länsi':
        uusi_x, uusi_y = nykyinen_x - uinti_askel, nykyinen_y
    elif  apina['suunta'] == 'itä':
        uusi_x, uusi_y = nykyinen_x + uinti_askel, nykyinen_y
    

    # Päivitä myös apinan koordinaatit canvasilla
    apinan_koko = 10
    kangas.coords(
        apina['apina_ympyrä'], 
        uusi_x - apinan_koko // 2, 
        uusi_y - apinan_koko // 2,
        uusi_x + apinan_koko // 2, 
        uusi_y + apinan_koko // 2
    )

    # Tarkistetaan, onko apina syöty haiksi
    if hai_syö_apinan():
        winsound.PlaySound("Chomp+1.wav", winsound.SND_FILENAME)
        print(f"{apina['nimi']} syötiin!")
        kangas.delete(apina['apina_ympyrä'])
        saari['apinat'].pop(apina_index)

# Funktio, joka tarkistaa 1% todennäköisyydellä, syökö hai apinan
def hai_syö_apinan():
    return random.random() < 0.01

# Funktio, joka liikuttaa apinoita S1 saarelta
def apina_ui():
    while running:
        if 'S1' in saaret:  # Tarkistetaan, että S1 saari on olemassa
            saari_nimi = 'S1'
            apinat = saaret[saari_nimi]['apinat']
            for i in range(len(apinat) - 1, -1, -1):     #Iteroi apinalistaa lopusta alkuun päin jotta
                if i < len(apinat):                      #apinoiden syönti ei aiheuta "IndexError: list index out of range":iä
                    liikuta_apinaa(saari_nimi, i)        
        time.sleep(1)

        
#Nappi jota painamalla "tulivuori purkautuu" eli syntyy saaria
#Käyttää saaren_lisays funktiota
tulivuorenpurkaus = tk.Button(ikkuna, text="Tulivuorenpurkaus", command=saaren_lisays)
tulivuorenpurkaus.place(x=350, y=750)

#Nappi, joka nollaa kaiken
reset_nappi = tk.Button(ikkuna, text="Reset", command=reset)
reset_nappi.place(x=500, y=750)

# Käynnistetään apinoiden liikuttaminen (liikkuminen joka 10 sekunti)
threading.Thread(target=apina_ui, daemon=True).start()

ikkuna.mainloop()