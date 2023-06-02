# Imenik.hr API Server

Ova aplikacija omogućava pretraživanje i dohvaćanje kontaktnih podataka s web stranice Imenik.hr. Možete pretraživati po imenu ili broju telefona i dobiti informacije kao što su puno ime, broj telefona, adresa i operater.

## Preduvjeti

- Python 3.x
- Chrome preglednik
- ChromeDriver

## Instalacija

1. Klonirajte ovaj repozitorij na svoje računalo.

2. Instalirajte potrebne Python pakete iz `requirements.txt` datoteke pomoću sljedeće naredbe:

   ```pip install -r requirements.txt```

3. Preuzmite [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/) za svoju verziju Chrome preglednika i postavite izvršnu datoteku `chromedriver` u direktorij projekta.

## Korištenje

Pokrenite program pokretanjem `server.py` datoteke:

```python server.py```

Nakon što program bude pokrenut, možete pristupiti API-ju putem sljedećeg URL-a:

http://localhost:5000/contacts


### POST zahtjev

Pošaljite POST zahtjev na URL `/contacts` s sljedećim JSON tijelom:

```json 
{
  "input": "ime prezime",
  "page_id": 1
}
```

- "input": Unesite ime i prezime osobe koju želite pretražiti. Također možete upisati i druge podatke kao što su adresa ili broj telefona
- "page_id" (opcionalno): Broj stranice za pretraživanje. Ako nije navedeno, koristit će se stranica 1.

Program će izvršiti pretraživanje na Imenik.hr stranici i vratiti rezultate kao JSON odgovor u sljedećem formatu

``` 
[
  {
    "full_name": "John Doe",
    "phone_number": "+123456789",
    "address": "123 Main St, City",
    "operator": "Unknown Operator",
    "profile_url": "https://www.example.com/profile/johndoe"
  },
  ...
]
```

# Napomena
Ovaj program se koristi samo u edukacijske svrhe i za osobnu upotrebu. Molimo vas da ga ne koristite za neovlašteno prikupljanje podataka ili bilo koje druge zlonamjerne aktivnosti.

# License
This project is licensed under the MIT License.

