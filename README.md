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

# Opis funkcji

## tworzenie pliku z nazwami miastach

`src/cities_names_fetcher.py`

Ten skrypt tworzy plik txt z nazwami miast.

Output:

<img width="449" alt="image" src="https://github.com/user-attachments/assets/646ac67e-5194-45c9-b4b0-53e5f97af681" />


## tworzenie pliku z informacjami o miastach (nazwa, longitude, latitude, populacja)

`python src/fetch_and_prepare_data.py data/cities.txt`

Ten skrypt pobiera koordynaty oraz populacje miast na podstawie pliku z nazwami miast.

Output:

<img width="420" alt="image" src="https://github.com/user-attachments/assets/8f5ef116-e916-44cd-922d-8bc30ac745f7" />


## pobieranie obrazów

`python src/images_downloader.py data/full_data.csv images`

Ten skrypt pobiera obrazy satelitarne na podstawie pliku ze współrzędnymi geograficznymi.

Output:

<img width="1364" alt="image" src="https://github.com/user-attachments/assets/3564045b-48a3-4c5a-ba2a-8f0c9ec49dbf" />

