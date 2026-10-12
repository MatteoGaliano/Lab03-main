import csv
from operator import attrgetter

class Strumento:

  def __init__(self, codice, tipo, marca, anno_acquisto, valore):
    self.codice = codice
    self.tipo = tipo
    self.marca = marca
    self.anno_acquisto = anno_acquisto
    self.valore = valore

  def __str__(self):
    return (
        f"[{self.codice}] {self.tipo} - {self.marca} ({self.anno_acquisto}) - €{self.valore:.2f}"
    )

class Prestito:

  def __init__(self, id_prestito, data, id_strumento, cognome_allievo):
    self.id_prestito = id_prestito
    self.data = data
    self.id_strumento = id_strumento
    self.cognome_allievo = cognome_allievo

  def __str__(self):
    return (
        f"Prestito {self.id_prestito}: Strumento {self.id_strumento}"
        f" affidato a {self.cognome_allievo} ({self.data})"
    )

class DepositoStrumenti:

  def __init__(self, nome, responsabile):
    """Inizializza gli attributi e le strutture dati"""
    self.nome = nome
    self.responsabile = responsabile
    self.strumenti = []  # Lista con strumenti del deposito
    self.prestiti = []  # Lista con prestiti attivi
    self.contatore_prestiti = 0  # Parto da 0 così il primo sarà P1

  def carica_file_strumenti(self, file_path):
    """Carica gli strumenti dal file"""
    with open(file_path, mode="r", encoding="utf-8") as f:
      reader = csv.reader(f)
      for riga in reader:
        if not riga or len(riga) < 5:
          continue
        # se riga è vuota oppure ha meno dati, passa alla riga successiva

        codice = riga[0].strip()
        tipo = riga[1].strip()
        marca = riga[2].strip()
        anno_acquisto = int(riga[3].strip())
        valore = float(riga[4].strip())

        # crea l'oggetto Strumento e lo aggiunge alla lista
        strumento = Strumento(codice, tipo, marca, anno_acquisto, valore)
        self.strumenti.append(strumento)

  def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
    """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""

    # trovo il codice più alto tra quelli già esistenti
    ultimo_numero = 0
    for s in self.strumenti:
      num = int(s.codice[1:])  # prende parte numerica dopo S (es. S4 -> 4)
      if num > ultimo_numero:
        ultimo_numero = num

    nuovo_codice = f"S{ultimo_numero + 1}"  # creo nuovo codice stringa (es. S5)
    nuovo_strumento = Strumento(
        nuovo_codice, tipo, marca, anno_acquisto, valore
    )
    self.strumenti.append(nuovo_strumento)
    return nuovo_strumento

  def strumenti_ordinati_per_marca(self):
    """Ordina gli strumenti per marca in ordine alfabetico"""
    return sorted(self.strumenti, key=attrgetter("marca"))
    # key serve per specificare il criterio per ordinare la lista
    # attrgetter serve per estrarre da ciascun oggetto il singolo attributo

  def nuovo_prestito(self, data, id_strumento, cognome_allievo):
    """Crea un nuovo prestito"""

    # verifico che lo strumento sia nel deposito
    strumento_esiste = False
    for s in self.strumenti:
      if s.codice == id_strumento:  # Corretto da id.strumento a id_strumento
        strumento_esiste = True  # Corretto da Tru a True
        break  # se ho trovato lo strumento, esci dal ciclo

    if not strumento_esiste:
      raise Exception(
          f"Errore: lo strumento {id_strumento} non esiste nel deposito."
      )

    # verifico che lo strumento non sia già in prestito
    for p in self.prestiti:
      if p.id_strumento == id_strumento:
        raise Exception(
            f"Errore: lo strumento {id_strumento} è già in prestito."
        )

    # genero il codice del prestito (P1, P2...)
    self.contatore_prestiti += 1
    id_prestito = f"P{self.contatore_prestiti}"

    # Creo il prestito, lo aggiungo alla lista e lo restituisco
    prestito = Prestito(id_prestito, data, id_strumento, cognome_allievo)
    self.prestiti.append(prestito)
    return prestito

  def termina_prestito(self, id_prestito):
    """Termina un prestito in atto"""
    for prestito in self.prestiti:
      if prestito.id_prestito == id_prestito:
        self.prestiti.remove(prestito)
        return

    # Se il ciclo finisce senza aver trovato l'id_prestito
    raise Exception(f"Errore: prestito {id_prestito} non trovato.")