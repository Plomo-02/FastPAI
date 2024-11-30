import logging
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from chromadb import Settings as chroma_settings
from langchain.docstore.document import Document

# Configurazione del logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("chroma_add.log"), logging.StreamHandler()],
)


class ChromaDB:
    def __init__(self, docs=None, persist_directory="./chroma_data"):

        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.setting = chroma_settings(is_persistent=True, anonymized_telemetry=False)
        if docs is None:
            self.vectorstore = Chroma(
                persist_directory=persist_directory,
                client_settings=self.setting,
                embedding_function=self.embeddings,
            )
        else:
            self.vectorstore = Chroma.from_documents(
                documents=docs,
                embedding=self.embeddings,
                persist_directory=persist_directory,
                client_settings=self.setting,
            )

    # Inizializza il database Chroma
    # Aggiunge informazioni al database vettoriale
    def add_to_chroma(self, documents):
        try:
            logging.info("Aggiunta dei documenti al database Chroma...")
            texts = [doc.content for doc in documents]
            metadatas = [doc.metadata for doc in documents]

            # Aggiunge i documenti e i relativi metadati
            self.vectorstore.add_texts(texts=texts, metadatas=metadatas)
            logging.info(f"Aggiunti {len(documents)} documenti a Chroma.")
        except Exception as e:
            logging.error(f"Errore durante l'aggiunta di documenti a Chroma: {e}")
            raise

    def get_from_chroma(self, query, comune="RM"):
        try:
            logging.info("Esecuzione della ricerca su Chroma...")
            results = self.vectorstore.similarity_search(
                query, k=1, filter={"comune": comune}
            )
            logging.info("Ricerca completata con successo.")
            return results
        except Exception as e:
            logging.error(f"Errore durante l'elaborazione della query: {e}")
            raise


if __name__ == "__main__":
    try:
        # Definizione dei documenti
        docs = [
            Document(
                page_content="Servizio casellatio giudiziale. certificato del casellario giudiziale, fedina penale, carichi pendenti.",
                metadata={
                    "comune": "RM",
                    "date-orari": """
                    {
                        "2024-12-4": ["08.00-10.00", "14.00-16.00"],
                        "2024-12-5": ["08.00-10.00", "14.00-16.00"],
                    }
                    """,
                    "info": """
Richiesta

La richiesta va presentata dall’interessato, o da persona da lui delegata, muniti di documento di riconoscimento in corso di validità, utilizzando l’apposito modello.

I cittadini extracomunitari sprovvisti di passaporto devono presentare la copia del permesso di soggiorno.

L’interessato può presentare la richiesta per posta allegando copia del suo documento di riconoscimento in corso di validità.
 

I certificati possono essere prenotati online

 

Casi particolari

- Minorenne che non abbia compiuto 16 anni, la domanda va presentata dall'esercente la potestà genitoriale

- Interdetto, la domanda va presentata dal tutore munito di decreto di nomina

- Persona detenuta, o inserita in comunità terapeutica, la richiesta può inoltrare per posta o tramite un delegato o, se la persoba è sprovvista di documenti, con richiesta vistata dal direttore ovvero dall'ufficio matricolare del carcere

- Richiesta proveniente dall’estero

 

Il certificato ha validità per 6 mesi dalla data di rilascio.

 

I cittadini italiani che debbano presentare in altro Stato membro dell’UE la documentazione attestante l’assenza di precedenti penali possono utilizzare Modello standard multilingue e certificato relativo all’assenza di precedenti penali da allegare al certificato del casellario giudiziale

 

Costi

 

Per i certificati del Casellario giudiziale non è ancora attivo il pagamento elettronico
 

Il costo totale per il rilascio di ciascun certificato è di € 19,92, suddiviso come segue:

1 marca da bollo da € 16,00 ogni due pagine di certificato
1 marca da bollo da € 3,92 per i diritti di certificato per il ritiro dei certificati senza urgenza

Se il certificato è richiesto con urgenza (rilascio nella stessa giornata o il giorno successivo), si applica un ulteriore costo di:

1 marca da bollo da € 3,92 per i diritti di urgenza
""",
                },
            ),
            Document(
                page_content="carta d'identità, CIE, carta d'identità elettronica, documento d'identità",
                metadata={
                    "comune": "RM",
                    "date-orari": """
                    {
                        "2024-12-11": ["08.00-10.00", "14.00-16.00"],
                        "2024-12-15": ["08.00-10.00", "14.00-16.00"],
                    }
                    """,
                    "info": """
CHI PUO’ RICHIEDERE LA CIE

La CIE può essere richiesta per tutti coloro (persone italiane, comunitarie e non) che risultano residenti nel Comune di Bari.

Per le persone residenti in altro Comune italiano il rilascio della CIE può essere richiesto solo da coloro che sono impossibilitati a recarsi nel comune di residenza e solo al fine di sopperire a necessità derivanti da gravi e comprovati motivi (Circolare Ministero dell'Interno n. 23 del 10/05/2004 e nota del Ministero dell'Interno n. prot. 09905522-15100/354 del 05/11/1999).

Per richiedere il rilascio della carta d'identità a nome di minore, questi deve essere accompagnato/a allo sportello comunale da chi ha la responsabilità genitoriale (genitori o tutore), muniti di valido documento di riconoscimento e, nel caso del tutore, anche della sentenza di nomina (N.B. ai fini dell'identificazione è obbligatoria la presenza in sede del/della minore)

 

QUANDO SI PUO’ RICHIEDERE LA CIE
La nuova Carta di identità elettronica si può richiedere, esclusivamente per i seguenti motivi:

primo rilascio;
smarrimento o furto della carta d'identità in corso di validità, previa presentazione della relativa denuncia;
deterioramento della carta d'identità in corso di validità, previa verifica del relativo stato da parte dell'Ufficiale di anagrafe;
scadenza della carta d'identità (il rinnovo può essere effettuato a partire da 180 giorni prima della scadenza prevista).
N.B: il cambio di residenza non costituisce  motivo di rilascio anticipato della carta d'identità. Difatti, essendo la residenza un dato che nulla ha a che fare con l'identificazione della persona, la relativa variazione non altera la funzione del documento di riconoscimento (Circolare Ministero dell'Interno 31 dicembre 1992 n. 24)

DOCUMENTI DA ALLEGARE

Il giorno dell'appuntamento, la persona interessata deve recarsi allo sportello munita di:

vecchio documento di identità (la carta di identità scaduta o in scadenza deve essere obbligatoriamente consegnata allo sportello);
una foto formato tessera recente (fatta da non più di sei mesi) ed avente gli stessi requisiti delle foto richieste dalla Questura per il rilascio del passaporto (vedi istruzioni). Nel caso si porti una fotografia su supporto digitale USB tale foto deve rispettare, oltre quelle già indicate, le seguenti ulteriori caratteristiche:
- Definizione immagine: almeno 400 dpi
- Dimensione del file: massimo 500kb
- Formato del file: .jpg
la tessera sanitaria (facoltativo);
l'eventuale ricevuta di pagamento nel caso in cui il pagamento sia stata effettuato con i servizi PagoPA. La ricevuta non serve nel caso in cui si decide di pagare tramite POS direttamente presso gli sportelli dell’anagrafe. (ulteriori informazioni nella sezione COSTI)
certificato ISEE o altra documentazione equivalente rilasciata all’uopo dalla Ripartizione Servizi alla Persona, per poter usufruire dell’esenzione (ulteriori informazioni nella sezione COSTI).
                    """,
                },
            ),
            Document(
                page_content="passaporto, passaporto italiano valido per l'espatrio, passaporto per l'espatrio, passaporto per l'espatrio italiano",
                metadata={
                    "comune": "RM",
                    "date-orari": """
                    {
                        "2024-12-7": ["09.00-10.00", "15.00-16.00"],
                        "2024-12-12": ["09.00-10.00", "14.30-16.00"],
                    }
                    """,
                    "info": """
LA DOCUMENTAZIONE DA PRESENTARE

il modulo stampato della richiesta passaporto (attenzione a scegliere il modulo corretto tra quello per maggiorenni (Doc. 1) e minorenni (Doc. 2).
un documento di riconoscimento valido (n.b. portare con sé, oltre all'originale, anche una fotocopia del documento).
2 foto formato tessera identiche e recenti (con formato ICAO).
La ricevuta del pagamento a mezzo c/c di 42,50 euro per il passaporto ordinario. Il versamento va effettuato, per il momento, presso gli uffici postali di Posteitaliane mediante bollettino di conto corrente n. 67422808 intestato a: Ministero dell'Economia e delle Finanze - Dipartimento del tesoro. Il bollettino postale dovrà riportare nello spazio “eseguito da” i dati dell’intestatario del passaporto anche se minore e nella causale dovrà essere scritta la dicitura “importo per il rilascio del passaporto elettronico”.
Un contrassegno amministrativo per passaporto da 73,50 euro (da richiedere in una rivendita di valori bollati o tabaccaio).
Vecchio passaporto per chi ne era già titolare, anche se scaduto (in caso di smarrimento è richiesta denuncia di smarrimento).
·         Presenza di figli minorenni di GENITORI NON COMUNITARI – atto di assenso tra genitori

Nel caso di genitore non comunitario di figli minorenni, titolare di permesso di soggiorno, È SEMPRE NECESSARIA LA SUA PRESENZA ALLO SPORTELLO per esprimere l’atto d’assenso dei genitori avanti al pubblico ufficiale.
·         Minori di 18 anni di età

Il minore che ha compiuto i 12 anni dovrà presentarsi nel giorno dell’appuntamento insieme ai genitori. Se uno dei genitori non ha la possibilità di recarsi in Questura questi deve redigere l’atto di assenso all’espatrio del minore (Doc. 5) e allegare al fotocopia della carta di identità.   

TEMPI DI RILASCIO

I tempi di rilascio del passaporto ordinario sono normalmente di 15 – 30 giorni, in relazione al tipo di verifiche istruttorie richieste.

Eventuali richieste di rilascio a carattere d’urgenza, ad esempio, per motivi di lavoro, studio, cure mediche, lutti, acquisizione visti, dovranno essere rappresentate all’atto della presentazione della pratica allo sportello, e dovranno essere debitamente motivate e allegare la relativa documentazione.
""",
                },
            ),
        ]

        # Inizializza il vectorstore Chroma
        vector_store = ChromaDB(docs)

        print(
            vector_store.get_from_chroma(
                "voglio fare il passaporto come posso fare", comune="RM"
            )
        )

        # Aggiungi i documenti a Chroma

    except Exception as e:
        logging.error(f"Errore nell'esecuzione del file: {e}")
