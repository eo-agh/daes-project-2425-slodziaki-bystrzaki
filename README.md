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

<img width="449" height="400" alt="image" src="https://github.com/user-attachments/assets/646ac67e-5194-45c9-b4b0-53e5f97af681" />


## tworzenie pliku z informacjami o miastach (nazwa, longitude, latitude, populacja)

`python src/fetch_and_prepare_data.py data/cities.txt`

Ten skrypt pobiera koordynaty oraz populacje miast na podstawie pliku z nazwami miast.

Output:

<img width="420" height="400" alt="image" src="https://github.com/user-attachments/assets/8f5ef116-e916-44cd-922d-8bc30ac745f7" />


## pobieranie obrazów

`python src/images_downloader.py data/full_data.csv images`

Ten skrypt pobiera obrazy satelitarne na podstawie pliku ze współrzędnymi geograficznymi.

Output:

<img width="1364" height="400" alt="image" src="https://github.com/user-attachments/assets/3564045b-48a3-4c5a-ba2a-8f0c9ec49dbf" />


## Uczenie sieci neuronowych (Regresja)

### Architektura sieci

Użyta sieć neuronowa składa się z kilku warstw konwolucyjnych oraz jednej warswy liniowej na końcu.

### Funkcja błędu

Typową funkcją błędu w modelach regresyjnych jest średni błąd kwadratowy. Jednak ze względu na charakter danych, bardziej interesującą metryką jest średni błąd względny.

Użycie średniego błędu względnego okazało się jednak nieskuteczne podczas nauki, dlatego kolejne próby sprowadzały się do przygotowania danych dla MSE.

Głównym problem MSE były zbyt duże błędy wynikające z ogromnych populacji w miastach, przez co uczenie nie postępowało. Wydawać by się mogło, że normalizacja jest dobrym pomysłem (chociażby przez podzielenie przez liczbę milionów), jednak nie rozwiązywało to problemów związanych z nierównomierną czułością w zależności od wielkości miasta.

Finalnym rozwiązaniem została normalizacja danych poprzez zastosowanie logarytmu. Dzięki temu, liniowy błąd jest odpowiednikiem błędu względnego. Interpretacją wyjścia modelu jest rząd wielkości populacji (ile zer ma populacja).

### Wyniki

Dobra wiadomość jest taka, że model jest w stanie nauczyć się danych bardzo dobrze, osiągając średni błąd 7.2%:

<img height="400" alt="image" src="https://github.com/user-attachments/assets/a707428f-e86c-4a19-b2d2-cbe9314658f3" />

Jedynym problem jest overfitting, przez który model poradził sobie bardzo źle na danych testowych, osiągając średni błąd 429%:

<img height="400" alt="image" src="https://github.com/user-attachments/assets/42de3c5b-94c4-463d-a3bd-69a6f7a3c817" />

Zdecydowanie nie wyszło.

Pierwszą techiką, która może pomóc, jest dodanie szumu do modelu:

Osiąga on wtedy średni błąd 25% na danych uczących:

<img height="400" alt="image" src="https://github.com/user-attachments/assets/5b267b6c-d39b-4ea1-9bfd-7cf75b748930" />

I *tylko* 313% na danych testowych

<img height="400" alt="image" src="https://github.com/user-attachments/assets/70bf3705-0b37-450c-828b-e44660749103" />

Ostatnim ratunkiem jest augmentacja danych, poprzez losowe odbijanie zdjęć w poziomie lub pionie.

Model osiągnął średni błąd na poziomie 135%:

<img height="400" alt="image" src="https://github.com/user-attachments/assets/d1697801-1f47-4b90-949e-e4ea5f19477f" />


a na zbiorze testowym 187%:

<img height="400" alt="image" src="https://github.com/user-attachments/assets/e9b35544-0413-4f47-b392-dfd4354a571f" />

## Uczenie sieci neuronowych (Klasyfikacja)

Przewidywanie konkretnych wartości okazało się zbyt złożonym procesem do nauki, dlatego kolejne próby polegały na nauczeniu sieci klasyfikacji miast pod względem ich rozmiaru.

Jako granice przedziałów wybierano takie populacje, które gwarantowały równą liczbę miast w każdym przedziale.

Model:

<img src="https://github.com/user-attachments/assets/83dcccc2-8fe1-4823-a4b2-928b9bfb029e" height="400">

### Dwie klasy

Klasy:
0: 0-750k mieszkańców
1: 750k+ mieszkańców

<img src="https://github.com/user-attachments/assets/06e3eb3c-05aa-4fbf-8927-d9e91463a1c5" height="400">

Model osiągnął wynik f1-score na poziomie 0.79, co jest całkiem niezłym wynikiem.

<img src="https://github.com/user-attachments/assets/675cc057-7877-45ed-b6c7-caf895786382" height="100">

## Regresja liniowa 

### Funkcja błędu

Jako funkcję błędu 
Finalnym rozwiązaniem została normalizacja danych poprzez zastosowanie logarytmu. Dzięki temu, liniowy błąd jest odpowiednikiem błędu względnego. Interpretacją wyjścia modelu jest rząd wielkości populacji (ile zer ma populacja).

### Wyniki

Dobra wiadomość jest taka, że model jest w stanie nauczyć się danych bardzo dobrze, osiągając średni błąd 7.2%:

<img height="400" alt="image" src="https://github.com/user-attachments/assets/a707428f-e86c-4a19-b2d2-cbe9314658f3" />

Jedynym problem jest overfitting, przez który model poradził sobie bardzo źle na danych testowych, osiągając średni błąd 429%:
