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


## Uczenie sieci neuronowych

### Architektura sieci

Użyta sieć neuronowa składa się z kilku warstw konwolucyjnych oraz jednej warswy liniowej na końcu.

### Funkcja błędu

Typową funkcją błędu w modelach regresyjnych jest średni błąd kwadratowy. Jednak ze względu na charakter danych, bardziej interesującą metryką jest średni błąd względny.

Użycie średniego błędu względnego okazało się jednak nieskuteczne podczas nauki, dlatego kolejne próby sprowadzały się do przygotowania danych dla MSE.

Głównym problemem MSE były zbyt duże błędy wynikające z ogromnych populacji w miastach, przez co uczenie nie postępowało. Wydawać by się mogło, że normalizacja jest dobrym pomysłem (chociażby przez podzielenie przez liczbę milionów), jednak nie rozwiązywało to problemów związanych z nierównomierną czułością w zależności od wielkości miasta. 

Finalnym rozwiązaniem została normalizacja danych poprzez zastosowanie logarytmu. Dzięki temu, liniowy błąd jest odpowiednikiem błędu względnego. Interpretacją wyjścia modelu jest rząd wielkości populacji (ile zer ma populacja).

### Wyniki

Dobra wiadomość jest taka, że model jest w stanie nauczyć się danych bardzo dobrze, osiągając średni błąd 7.2%:

![image](https://github.com/user-attachments/assets/a707428f-e86c-4a19-b2d2-cbe9314658f3)

Jedynym problem jest overfitting, przez który model poradził sobie bardzo źle na danych testowych, osiągając średni błąd 429%:

![image](https://github.com/user-attachments/assets/42de3c5b-94c4-463d-a3bd-69a6f7a3c817)

Zdecydowanie nie wyszło.

Pierwszą techiką, która może pomóc, jest dodanie szumu do modelu:

Osiąga on wtedy średni błąd 25% na danych uczących:

![image](https://github.com/user-attachments/assets/5b267b6c-d39b-4ea1-9bfd-7cf75b748930)

I *tylko* 313% na danych testowych
