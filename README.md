# proiect-tpi

## Team
- Ghiriti Denisa
- Koncz Melania
- Tămâian Răzvan


## IoT Scenario

# Sistemul fizic simulat

Proiectul simulează un sistem IoT amplasat pe un teren agricol în pantă de o lungime de 100 m și înclinație de 30, pe care sunt distribuite 5 stații de monitorizare: de la baza văi până pe creastă .

Avem două fenomene naturale esențiale:
1. Scurgerea apei pe pantă : Din cauza înclinației de 30°, o parte din apa de ploaie nu intră în sol în vârful pantei, ci se scurge la vale. Astfel, baza pantei acumulează mai multă apă, în timp ce creasta rămâne mai uscată.
2. Infiltrarea pe verticală în sol (Percolare): Apa pătrunde treptat prin 3 straturi de adâncime (5 cm, 25 cm și 60 cm), în timp ce soarele și temperatura evaporă apa din stratul de la suprafață

Proiectul își propune să folosească aceste date (împreună cu o reprezentare grafică a pantei) pentru a găsi modul optim de așezare a stațiilor și a senzorilor, astfel încât eroarea de predicție a umidității pe tot terenul să fie cât mai mică.


# Senzori utilizati

Fiecare stație de pe pantă transmite date de la 7 senzori (4 de suprafață și 3 în sol)

Temperatură aer  | Simulează ciclul zi/noapte și influențează direct umiditatea aerului și uscarea solului
Umiditate aer  | Indică stresul termic/hidric de la suprafața culturii (scade când temperatura crește)
Radiație solară | Arată cât de însorit sau înnorat este cerul și determină viteza cu care se evaporă apa din stratul superficial al solului
Precipitații | Măsoară cantitatea de apă căzută și declanșează calculul de infiltrare și de scurgere pe pantă
Umiditate sol – 5 cm | Monitorizează stratul de la suprafață: reacționează imediat la ploaie, dar se usucă rapid la soare
Umiditate sol – 25 cm | Monitorizează zona rădăcinilor active, unde apa ajunge mai lent prin infiltrare de la suprafață
Umiditate sol – 60 cm | Monitorizează rezerva de apă din adâncime (strat tampon stabil), evidențiind acumularea apei la baza pantei

# Anomaliile asteptate

Sistemul urmărește detectarea următoarelor situații anormale:
- Dezechilibru extrem Creastă vs. Vale: Secetă pedologică în vârful pantei (ex. umiditate minimă de 10% la suprafață) simultan cu exces de apă / băltire la baza văii în stratul profund
- Anomalii de infiltrare (Sol compactat): Când senzorul de ploaie și cel de la 5 cm indică apă din abundență, dar umiditatea la 25 cm și 60 cm nu crește (apa se pierde doar prin scurgere la suprafață).
- Eroare mare de predicție (Căderea unei stații): Dacă o stație dintr-o zonă critică a pantei se oprește, estimarea umidității între stațiile rămase devine imprecisă.
- Senzor defect / Valori înghețate: Salturi bruște, imposibile fizic, sau pierderea conexiunii cu Gateway-ul


## Intrebari de cercetare

1. Optimizarea poziției pe pantă:Cum putem așeza un număr minim de stații de-a lungul pantei (între 0 m și 100 m) astfel încât eroarea de predicție a umidității pe întregul teren să fie minimă?
2. 
3. Formula de influență pe adâncime:Putem găsi o formulă matematică de legătură între straturile solului astfel încât să folosim doar 2 senzori de adâncime (5 cm și 25 cm) pentru a prezice exact umiditatea la 60 cm, reducând costul unei stații?
4. 
3.Impactul unghiului pantei:Cum influențează înclinația terenului (ex. panta de 30°) și radiația solară diferența de umiditate și timpul de acumulare a apei între vârful pantei și baza văii?

## Arhitectura

Fluxul de date este următorul:
Simulator Stații (`sensors.py`) → Gateway TCP (`gateway.py`) → Stocare & Analiză (`telemetry_data.csv` / Backend) → Vizualizare Grafică & Dashboard
