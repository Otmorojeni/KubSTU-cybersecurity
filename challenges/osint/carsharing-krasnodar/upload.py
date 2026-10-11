import urllib.request
import json

def upload_tmpfiles(file_path):
    url = 'https://tmpfiles.org/api/v1/upload'
    boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
    with open(file_path, 'rb') as f:
        file_bytes = f.read()
    
    header = (
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="file"; filename="{file_path}"\r\n'
        f'Content-Type: image/jpeg\r\n\r\n'
    ).encode('utf-8')
    footer = f'\r\n--{boundary}--\r\n'.encode('utf-8')
    body = header + file_bytes + footer

    req = urllib.request.Request(url, data=body, headers={
        'Content-Type': f'multipart/form-data; boundary={boundary}',
        'User-Agent': 'Mozilla/5.0'
    })
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        # format: https://tmpfiles.org/12345/file.jpg -> https://tmpfiles.org/dl/12345/file.jpg
        dl_url = data['data']['url'].replace('tmpfiles.org/', 'tmpfiles.org/dl/')
        return dl_url

if __name__ == '__main__':
    for name in ['crop_building.jpg', 'carsharing_hq.jpg', 'zoom_niches.jpg']:
        try:
            link = upload_tmpfiles(name)
            print(f'{name}: {link}')
        except Exception as e:
            print(f'{name} error: {e}')
