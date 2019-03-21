# Smart Lamp System

Questo sistema va installato su RaspberryPi 3 B+.

## Descrizione

Il sistema è stato elaborato durante il lavoro di tesi nell'ambito di un progetto di SmartCity.

### Prerequisiti

Per l'utilizzo del sistema è necesarrio che siano installate alcune librerie:
-APScheduler==3.5.3
-Flask==1.0.2
-PyJWT==1.7.1
-PyHive
-ElasticSearch==6.3.1
-psycopg2-binary=2.7.7


## Installazione

Per l'installazione è necessario modificare solamente il file system_info.py presente all'interno della directory core/.

Per tutti i parametri presenti sul file è necessario settare quelli scelti durante la fase di inserimento del nuovo lampione
nel sistema, insieme anche a quelli che vengono restituiti dall'operazione di inserimento.
