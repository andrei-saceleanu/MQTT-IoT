Tema 3 SPRC
Saceleanu Andrei, 343C1


Rulare

Lansare: ./run.sh (export SPRC_DVP + build al imaginii adaptorului + deploy)
Oprire: docker stack rm sprc3


Broker de mesaje

S-a folosit aceeasi imagine ca la laboratorul aferent MQTT, anume
eclipse-mosquitto.
Acest serviciu expune portul 1883 si permite publicare/abonare pe orice
subiect.

Adaptor

In cadrul adaptorului, se initializeaza un client MQTT care se aboneaza
la toate topicurile(i.e #) iar, la fiecare mesaj detectat, se proceseaza
si se introduc informatiile relevante in TSDB.

Mesajul trebuie sa cuprinda un payload de tip JSON (altfel este ignorat).
Singurele date introduse din payload sunt cele de tip numeric(i.e int/float)
Daca nu se gaseste campul timestamp, timpul masuratorilor introduse este cel
curent al adaptorului.

Un mesaj de la un device va putea genera de la 0 pana la mai multe
datapoints de introdus. Un punct este descris de seria de timp aferenta
(i.e. measurement_name = location.station.payload_key), un tag "station"
(utilizat pentru gruparea necesara pentru Battery Dashboard), un camp
cu valoarea inregistrata si amprenta de timp.

Toate mesajele sunt insotite de log-uri aferente (daca DEBUG_DATA_FLOW e
definit si este true, altfel nu se genereaza mesaje de log)

Baza de date

Retentia datelor este nelimitata si precizia disponibila este maxima.
Datele sunt stocate persistent in volumul Docker db_data.

Componenta de vizualizare

Configuratia a fost creata prin intermediul UI si salvata in fisiere
de configurare. Se foloseste mecanismul grafana-provisioning pentru
a initializa cele 2 dashboard-uri si sursa de date InfluxDB.

Serviciul expune portul 80 + interfata Web permite autentificarea cu
credentialele aferente.

Cele 2 dashboard-uri sunt configurate conform specificatiilor din enunt
folosind o combinatie de Flux queries si Transforms disponibile din UI.

Comunicatie

Se utilizeaza mai multe retele Docker pentru a limita comunicatia
inter-container.