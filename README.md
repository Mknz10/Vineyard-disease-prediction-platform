# proiect-tpi

## Team
- Ghiriti Denisa
- Koncz Melania
- Tămâian Răzvan


## IoT Scenario

# Sistemul fizic simulat

Simulam o parcela de vita-de-vie si interactiunea dintre 3 elemente: frunzisul, solul pe diferite adancimi si aerul din jur. In frunzis ne intereseaza locul unde se depune apa din roua sau ploaia, solul care retine rezerva de apa pentru radacini iar aerul este cel care dicteza cat de repede se evapora umezeala sub influenta diferitilor factori de mediu.

# Senzori utilizati

Utilizam o gama larga de senzori de pe o statie meteo:
- pentru a sti stare frunzelor folosim un senzor de umiditate foliara, care se pune pe spatele funzei, si care indica daca suprafata lor este uscata sau acoperita de o pelicula de apa.
- senzori de umiditate si temperatura situati in sol la diferite adancimi pentru a urmari cum patrunde apa catre radacini.
- deasupra solului avem avem mai mult senzori, umiditatea si temperatura aerului, un pluviometru care masoara cantitatea de precipitatii si un senzor de radiatie solara care capteaza lumina solara si ne ajuta sa determinam cat de senin sau innorat este cerul.

# Anomaliile asteptate

Avem doua tipuri de anomalii pe partea de cultura si pe partea sistemului tehnic. Pe partea de cultura, principala anomalie este riscul iminent de boala fungica, momentul in care funza ramane uda prea multe ore la o temperatura favorabila ciupercii. 
Si o anomalie tehnica este momentul in care apar ciudatenii, date contradictoruu intre senzori. De exemplu. daca e soare arzator si aer foarte uscat, dar senzorul foliar indica funze complet ude. 

## Intrebari de cercetare

1. In ce masura integrarea unui senzor de umiditate pe frunza alaturi de ceilalti senzori creste precizia de a detecta infectia fungica, comparativ cu modelele clasice bazate exclusiv pe prognoza meteo? 

2. Cum poate modelul virtual sa distinga in mod fiabil intre o anomalie reala din teren si o eroare harware? (pentru ca fiecare senzor are o marja de eroare)

3. Unde trebuie amplasat senzorul de umiditate pentru frunza pentru a reflecta cel mai periculos microclimat favorabil ciupercii? In interiorul vitei de vie, la umbra, sau in exteriorul vitei de vie, cu funzele orientate catre soare? 

## Ce este nou?

Majoritatea solutiilor actuale trateaza irigatia si protectia impotriva bolilor ca pe doua probleme complet separate. Pe de o parte exista solutii de irigare automate bazate pe praguri fixe de sol, iar pe de alta parte exista aplicatii meteo care dau alerte de stropire la nivel regional, ignorand ce se intampla efectiv pe frunza sau in pamant.

Solutia noastra combina, unifica cele 2 procese intr-un singur proces, bazat pe diferentiatori clari: rwezolvarea automata a conflictului dintre udare si boala si optimizare cost eficienta a hardware-ului si detectia automata a anomaliilor. 

## Arhitectura

Sistemul este structurat pe 5 procese Python independente care comunica asincron:

Sensor Simulator - (UDP) -> Gateway Proxy - (TCP/REST) -> Backend API -> Frontend

Sensor Simulator: Simuleaza statia agro-meteo.
ateway Proxy: Punct de agregare care colecteaza datele de la senzori si le trimite stabil catre backend.
Backend API: Preceseaza datele, calculeaza riscul de infectie, detecteaza anomalii. 
Storage (TimescaleDB): Inregistreaza istoricul seriilor de timp de la senzori.
Frontend: Panoul de control pentru vizualizare starii culturii si a alertelor. 