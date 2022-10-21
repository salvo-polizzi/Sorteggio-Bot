COMANDI: dict = {
    "sorteggio_admin": "sorteggioAdmin",
    "sorteggio_utenti_scelti": "sorteggioManuale",
    "sorteggio_tutti_utenti": "sorteggioUtenti",
    "sorteggio_non_admin": "sorteggioNonAdmin"
}

RISPOSTE: dict = {
    "numero_partecipanti": "Il numero di partecipanti al sorteggio è minore del\
	numero di partecipanti da sorteggiare",
    "specificare_partecipanti": "Il comando deve essere utilizzato specificando il numero\
	di partecipanti da sorteggiare"
}

HELP: str = f"Comandi disponibili:\
	\n\n /{COMANDI['sorteggio_admin']} N - Per sorteggiare N utenti amministratori\
	\n /{COMANDI['sorteggio_utenti_scelti']} N username1 username2 (specificare la @) ecc... - Per sorteggiare N utenti scelti (che hanno scritto\
	almento una volta nel gruppo da quando il bot è stato inserito)\
	\n /{COMANDI['sorteggio_tutti_utenti']} N - Per sorteggiare N utenti qualsiasi (che hanno scritto\
	almento una volta nel gruppo da quando il bot è stato inserito)\
	\n /{COMANDI['sorteggio_non_admin']} N - Per sorteggiare N utenti non amministratori\
	(che hanno scritto almento una volta nel gruppo da quando il bot è stato inserito)"