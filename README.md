# TikTok
Mathematica online jude system

# Opis 
Platforma testujca zadania napisane w programie Mathematica

### Cel
Doskonalenie umiejętności korzystania z programu Mathematica oraz szybkiego modelowania i rozwiązywania problemów przy pomocy Mathematici. 

### Technologia:
Python3.4, Django1.9, Mathematica 10

###Ogólny opis kodu:
news - moduł z wiadomościami ogólnymi. Dodawane przez administratora. Stanowi docelową stronę startową 
problems - moduł z problemami. Umożliwia ich dodawanie, oglądanie, komentowania, oraz zgłaszanie rozwiązań
submits - moduł z zgłoszeniami. Pozwala na wyświetlanie zgłoszeń użytkownika. Posiada w sobie funkcje uruchamiającą skrypt testowy.
user - moduł pozwalacjący na logowanie/rejestrowanie.
submits/executer - skrypt uruchamiajcy zgłoszenia


# Instalacja do rozwoju 
Zainstaluj pakiety wymienione w Technologi. Dla Windows należy podpiąć je pod PATH.  Skolonuj repozytorium.

`python manage.py migrate --run-syncdb`

`python manage.py createsuperuser`

`python setup.py`

`python manage.py runserver`



