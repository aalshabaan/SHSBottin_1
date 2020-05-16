# Best Bot ever

## Brainstorm :

- How to link to gallica source ?
    - see start of EX3 notebook
- ~~Add images related to context~~
- Create page for the street also
    - Maybe in the future

## TODO :

- [x] download CSV file to project
- [ ] Presentation

## First project session (21 / 04 / 2020)

#### Basile:
- [ ] Statistiques (pandas) des données

#### Abed:
- [ ] Méthode de traitements des données

#### Ahmed:
- [ ] Interaction avec wikipast (prototypage des fonctions)
    - [ ] création d'une nouvelle page
    - [ ] lecture d'une page
    - [ ] ajout à une page

Mise en forme:  lecture 1 personne est une Série PANDA. (Date dans l'ordre, nom, metier, adresse) ==> voir si la page existe, sinon en rajouter.

### Présentation (plan d'action + planning avec deadline personnelles)
1. Intro
1. Statistiques du jeu de données (doublons, erreurs, ...)
1. Traitement prévu pour ces statistiques (doublons, erreurs, ...)
1. Présenter les fonctions wikipast (formatage de données JSON, stratégies de création / append optimales pour les pages )
1. Conclusion


### Charger les données :

- [ ] Nombre de doublons
- [ ] Statistiques générales (nombre, plus automatisation optimales)
- [ ] Entrés problématiques (mal orthographiées, erronés)

### Interaction avec wikipast:

- [ ] Fonctions utilitaires (voir si l'article existe  ==>create/append)
- [ ] Eviter les doublons d'information issus d'autres groupes
- [ ] Ne pas écraser les articles préexistants, (toujours check si l'info est là avant d'append)


## Second project session (28 / 04 / 2020)

### General remarks :

- Désambiguation de noms
- Essais / performances
- Pages d'homonymes


### Analysis :

[Regex testing](https://regex101.com/r/osAamG/1)
Regex nom simple + parnethèse: '^\s*\w+\s*(?:\s?\(.*\)\s*)?\s*$'
Regex nom à particules : '^(?:\s*\w+)+\s*(?:\(\s*\w+.*\s*)?$'
Regex avec char spéciaux : '^(?:(?:\s*\w+)*\s?[#*]?)*(?:\(\s*\w+.*\s*)?$'
Regex nom composé : '^(?:(?:\s*\w+-?)*\s?)*(?:\(\s*\w+.*\s*)?$'
Regex avec point à la fin:'^(?:(?:\s*\w+)*\s?)+(?:\(\s*\w+\.*\s*\))?\.?$'
Regex avec plusieurs points dans les parenthèses : ^(?:(?:\s*\w+)*\s?)+(?:\(\s*\w*\.*\s*\))?$
Regex avec parenthèse manquante: ^(?:(?:\s*\w+)*\s?)+(?:\((?:\s*\w*\.*)*\s*\)?)?$


Noms à considérer quand la recherche sef ait pour des noms simple : 
- 'Castan de Bages' -> indlure la possibilité d'avoir un nom à particule (inclure plusieurs mots dans le RegEx)
- noms avec des spécifications comme : 'fils', 'ainé', 'frères' etc ... (avoir une dictionnaire de ces mots et les traiter séparément)
- noms sans espaces avant la parenthèse : 'Cesbron(J. ) et Cie' (Petite correction du RegEx)
- noms avec symboles supplémentaires : 'Chabrillan (Mis de) *', ' Chalot #', ' Chantrier * frères', 'Charpentier ¥' (Ignorer ces caractères dans le RegEx?)
- noms avec erreurs d'OCR : 'Cha'lot' (Je ne vois pas un autre moyen que le traîtement manuel)
- noms composés : 'Chabrol-Chaméane (de)' (Petite modification du RegEx)
- noms avec chiffre : ' Chambry 14' (RegEx)
- noms avec poinst supplémentaires : 'Chattet (J.).', 'Cheder y (..)' (RegEx encore)
- noms avec parenthèses incomplètes : 'Choisy (A.1' (Faire tel que la 2ème paranthèse soit optionnele dans le RegEx et ensuite vérifier les parenthèses de chaque entrée)
- appostrophes à la place d'une lettre : 'Co'inet (P.-J.)' (Erreur OCR?)

Il y 390223 entrées, dont 98072 noms uniques, 41282 métiers uniques, 25293 rue uniques

La distribution d'entrées par année est la suivante:
	1839: 37177
	1841: 42666
	1842: 44140
	1843: 38279
	1844: 42003
	1845: 43238
	1846: 44808
	1847: 46900
	1848: 51012

One word + parenthesis : 319293/390223 (81.823214%)

### Count for filters
filter : '^\s*\w+(?:\s?\(.*\)\s*)?\s*$'
Final number of pages : 185240

# Todo : 
- job in lowercase
- number has to be a number + a point (no spaces, no additional text except for 'bis')
- clean number : sometimes there is a '-' signe

Mne is Mme

## Problems :
- groupby is sensible to accents
- sometimes the job is not written the same : use a substring finder and if they share >50% they are the same
- 'number' field can be messy : suppress the point after the number

## Documentation distance

- [Edit Distance](https://github.com/roy-ht/editdistance)
- [Polylenv](https://github.com/fujimotos/polyleven)
