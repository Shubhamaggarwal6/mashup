import requests

headers = {
    # requests won't add a boundary if this header is set when you pass files=
    # 'Content-Type': 'multipart/form-data',
    'apy-token': 'APY0iQUQRbDAgOFF30V6ETzO0tHnaKh05DjGN5Ii8URG4Rya6O4eFPrR6QYl068MMFy',
}

params = {
    'output': 'output.mp3',
}

files = {
    'file': open('merged_audio.wav', 'rb'),
}

response = requests.post('https://api.apyhub.com/convert/audio/wav-file/mp3-file', params=params, headers=headers, files=files)

# Save the output as a file
if response.status_code == 200:
    with open('output.mp3', 'wb') as f:
        f.write(response.content)
else:
    print(f"Error: {response.status_code} - {response.text}")

# Don't forget to close the file after using it
files['file'].close()
