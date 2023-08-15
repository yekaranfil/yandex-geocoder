import pandas as pd
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

    # Mevcut Excel dosyasını okuma
    excel_path = "pema-koordinatlar.xlsx"
    df = pd.read_excel(excel_path)

    # Yeni sütunları ekleme
    df["kordinatlar"] = None


    # Koordinatları mevcut DataFrame'e ekleme
    for index, row in df.iterrows():
        address = row["adres"]  # Adres sütunu adını düzeltebilirsiniz
        coordinates = geocode_yandex(address, api_key)
        if coordinates:
            print(index,": ",str(coordinates[0]) + ", " + str(coordinates[1]))
            df.at[index, "koordinatlar"] = str(coordinates[0]) + ", " + str(coordinates[1])

    # Güncellenmiş DataFrame'i Excel'e yazma
    df.to_excel(excel_path, index=False)

    print("Koordinatlar başarıyla eklenip kaydedildi.")
