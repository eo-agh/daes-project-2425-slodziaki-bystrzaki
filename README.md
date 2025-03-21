# Autorzy:
Anielka Biczak, Kamil Kminkowski

# Co trzeba zrobić

- zamiana nazw miast na współrzędne geograficzne (jedna para współrzędnych pokazujących środek miasta)
- pobieranie zdjęć satelitarnych na podstawie wpółrzędnych i promienia (na przykład kwadrat o szerokości 30km)
- pobieranie informacji na temat liczby ludności na podstawie nazwy miasta lub współrzędnych
- stworzenie modelu modelującego liczbę ludności na podstawie zdjęcia miast

# Uruchomienie

```
unix:
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt

w*ndows:
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```