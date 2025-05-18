# Cellular automata ~~simulator~~ visualiser

## Textový popis

Projekt do VVP

Cílem projektu je simulovat celulární automaty (zkratka CA), a následně je vykreslit. CA je dynamický systém, diskrétní v hodnotách, prostoru i čase. Ku příkladu [Conwayova hra života](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) je tvořena 2d = čtvercovou mřížkou buněk, které každé můžou mít hodnotu 0 nebo 1 (mrtvá nebo živá). Tyto hodnoty se mění podle předem daných pravidel každý časový krok (= generaci).

Prostory CA mohou být konečné, nekonečné, nebo třeba toroidiální. Na konečné oblasti tohoto prostoru ovšem musí být konečný počet buněk. Buňky nabývají konečného počtu hodnot. V čase 0 je definován počáteční stav buněk. Jejich následující stav závisí na jejich aktuálním stavu a stavu sousedních buněk. Způsob, jakým se mění stav a definice sousední buňky jsou typicky časově neměnné.

Dalšími příklady CA jsou:
 - Langtonův mravenec
 - Turmiti (Generalizace předchozího)
 - Brian's Brain
 - Seeds
 - Rule 30, Rule 90, Rule 184

## Funkcionality

 - Implementace Conwayovy hry života
 - Implementace nějakého dalšího CA
 - Interaktivní vykreslení aktuálního stavu
   - Přiblížení, posun po hrací ploše
   - Zrychlení / zpomalení / pauza simulace
 - Výpis statistik (např. populace)
 - Uložení / načtení stavu (celý / výběr)

## Todo:

 - add optimized conway
 - universe expansion
 - ups changing
 - save, load
 - cleaning ui code
 - jupyter examples
 - docs
 - asynchronous updates
 - repeating keys
