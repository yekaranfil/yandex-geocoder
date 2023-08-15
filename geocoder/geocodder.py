import requests


def geocode_yandex(address, api_key):
    base_url = "https://geocode-maps.yandex.ru/1.x/"
    params = {
        "apikey": api_key,
        "geocode": address,
        "format": "json"
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200:
        try:
            coordinates = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
            longitude, latitude = map(float, coordinates.split())
            return latitude, longitude
        except (IndexError, KeyError):
            print("Adres koordinatları alınamadı.")
    else:
        print("API isteği başarısız oldu.")

    return None


if __name__ == "__main__":
    api_key = "YOUR APİ KEY"
    address = "ULUIRMAK MAH.ABİT ÇELEBİ SK.MEVLANA APT.NO:7/11 SELÇUKLU"

    coordinates = geocode_yandex(address, api_key)
    if coordinates:
        print("{},  {}".format(coordinates[0], coordinates[1]))
