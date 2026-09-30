def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    album = {} # come chiave ha l'anno e come valore ha una lista di dizionari di liste che ha come chiave il codice univoco delle foto e come valore un alista contenente tutti i campi delle foto
    infile = None # inizializzo all'inizio perché altrimenti nel finally, se veniva sollevata l'eccezione, non poteva chiudere il file perché infile non veniva mai creata

    try:
        infile = open(file_path, "r")
        _ = infile.readline() # leggo l'intestazione

        for line in infile:
            campi = line.strip().split(',') # pulisco la riga dai caratteri come \n finale e la splitto
            cod = campi[0]
            titolo = campi[1]
            autore = campi[2]
            mese = campi[3]
            anno = campi[4]

            foto = {cod: [titolo, autore, mese, anno]}

            if anno not in list(album.keys()):
                album[anno] = [foto]
            else:
                album[anno].append(foto)

    except FileNotFoundError:
        return None
    finally:
        if infile is not None:
            infile.close()
    return album



def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""

    # controllo codice già presente
    codici = [] # lista che contiene tutti i codici delle varie foto presenti nell'album
    photos = list(album.values()) # lista di liste

    for i in range(len(photos)):
        for j in range(len(photos[i])):
            # photos[i][j]                 è un dizionario che rappresenta una foto
            # photos[i][j].keys()          mi estraggo la chiave --> che rarebbe il codice della foto
            # list(photos[i][j].keys())    lo converto in lista perché altrimenti sarebbe di tipo <class 'dict_keys'>
            # list(photos[i][j].keys())[0] estraggo il primo elemento della lista (che è anche l'unico) solo per averlo come valore
            # convertire direttamente la chiave in int da errore perché non può farlo
            codici.append(list(photos[i][j].keys())[0])

    if (codice not in codici) and (1 <= mese <= 12):
        # update del file
        outfile = None
        try:
            outfile = open(file_path, "a") # aperto in append per non sovrascrivere il contenuto
            outfile.write(f"{codice},{titolo},{autore},{mese},{anno}\n")
        except FileNotFoundError:
            return None
        finally:
            if outfile is not None:
                outfile.close()

        # update dell'album
        foto = {codice:[titolo,autore,mese,anno]}
        if anno not in list(album.keys()):
            album[anno] = [foto]
        else:
            album[anno].append(foto)

        return foto

    else:
        return None


def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    codici = []  # lista che contiene tutti i codici delle varie foto presenti nell'album
    photos = list(album.values())  # lista di liste

    for i in range(len(photos)):
        for j in range(len(photos[i])):
            codici.append(list(photos[i][j].keys())[0])

    for i in range(len(photos)):
        for j in range(len(photos[i])):
            if list(photos[i][j].keys())[0] == codice: # se il codice combacia estraggo i parametri della foto da returnare
                # doppio indice perché convertendo i valori da dict_values a list (i valori sono già dentro una lista
                # quindi il primo indice [0] indica quella lista interna all'interno di quella esterna, mentre il secondo indice [0] indica
                # quale elemento prendere all'interno della lista interna
                titolo = list(photos[i][j].values())[0][0]
                autore = list(photos[i][j].values())[0][1]
                mese = list(photos[i][j].values())[0][2]
                anno = list(photos[i][j].values())[0][3]
                return f"{codice}, {titolo}, {autore}, {mese}, {anno}"
    return None



def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    # TODO


def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
