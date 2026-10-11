import requests
import json

def yandex_search_image(file_path):
    url = "https://yandex.ru/images-apphost/image-download?cname=image-search"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    with open(file_path, "rb") as f:
        files = {"upfile": ("image.jpg", f, "image/jpeg")}
        resp = requests.post(url, files=files, headers=headers)
    print("Status:", resp.status_code)
    try:
        data = resp.json()
        print("Response JSON:", json.dumps(data, indent=2))
        image_id = data.get("image_id")
        cbir_id = data.get("cbir_id")
        search_url = f"https://yandex.ru/images/search?rpt=imageview&cbir_id={cbir_id}"
        print("Search URL:", search_url)
        return search_url
    except Exception as e:
        print("Text:", resp.text[:500])

if __name__ == "__main__":
    yandex_search_image("crop_building.jpg")
