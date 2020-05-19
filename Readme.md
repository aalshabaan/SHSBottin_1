# BottinBot1

Ce bot a été réalisé dans le cadre du cours de SHS Digital humanities (HUM-369).

Plus d'infos : [Page wiki du Bot](http://wikipast.epfl.ch/wiki/BottinBot1)

## Utilisation:

Le bot peut être lancé sur des données non processées ou bien des données préprocessées a moyen du flag `--pre_process` qui doit prendre les valeurs `1` pour effetuer le préprocessing  ou `0` pour indiquer que le fichié donné en entrée est déjà préprocessé et prêt à être uploadé sur wikipast.

L'argument `--file_name` est utilisé pour indiquer un fichier CSV ou bien un fichier Pickle de données préprocessées. 

Note : le fichier .pkl généré par le bot est nommé `save.pkl`

### Exemple d'utilisation

Preprocessing :
```
$ python backend.py --file_name bottinbot1.csv --pre_process 1
```

Upload only from pickle file :
```
$ python backend.py --file_name save.pkl --pre_process 0
```

## Used libraries

- [Edit Distance](https://github.com/roy-ht/editdistance)
