# Simulacija Telekomunikacionog Kanala u Python-u
Simulacija telekomunikacionog kanala sa LZW kodovanjem/dekodovanjem i zastitnim koderom sa ponavljanjem uz algoritam vecinskog odlucivanja\
\
Za pokretanje simulacije potrebno je da fajlovi ***test.txt*** i ***simulation.py*** budu u istom direktorijumu.\
Zatim treba otvoriti komandnu liniju za taj direktorijum (pozicionirati se u direktorijum fajlova) i ukucati sledecu komnadu:
```
...\Desktop> python simulation.py
```
***Napomene:***
> Potrebno je imati instaliran Python3 (ocigledno...)
> Simulacija koristi biblioteke:
> > matplotlib
> > 
> > math
> > 
> > random
> > 
> Tokom simulacije se povecava verovatnoca greske u kanalu, a to dovodi do gresaka u LZW dekodovanju
> Iz tog razloga se vrsi sve veci broj retransmisija poruke, sto dovodi do duzeg izvrsavanja tekuce simulacije
