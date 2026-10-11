import requests, base64

def upload_img(path):
    with open(path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('utf-8')
    r = requests.post('https://freeimage.host/api/1/upload', data={
        'key': '6d207e02198a847aa98d0a2a901485a5',
        'source': b64,
        'format': 'json'
    })
    data = r.json()
    return data['image']['url']

if __name__ == '__main__':
    for f in ['crop_building.jpg', 'zoom_niches.jpg', 'carsharing_hq.jpg']:
        try:
            print(f, upload_img(f))
        except Exception as e:
            print(f, 'error', e)
