import os
import subprocess
import json


def install_packages():
    global package
    packages = [
        'Flask',
        'gpt4all',
        'edge_tts',
        'nest_asyncio',
        'deep_translator',
        'requests'
    ]

    try:
        for package in packages:
            subprocess.check_call(['pip', 'install', package])
        print("All packages installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing {package}.")
        print(str(e))

def config():
    # Eingabeaufforderungen
    city = input("Enter your city: ")
    openweather_api = input("Enter your OpenWeatherMap API key: ")
    apiKey = input("Enter your Firebase apiKey: ")
    authDomain = input("Enter your Firebase authDomain: ")
    projectId = input("Enter your Firebase projectId: ")
    storageBucket = input("Enter your Firebase storageBucket: ")
    messagingSenderId = input("Enter your Firebase messagingSenderId: ")
    appId = input("Enter your Firebase appId: ")
    measurementId = input("Enter your Firebase measurementId: ")

    # Pfad zum Verzeichnis der firebase.js Datei
    firebase_js_directory = "static/scripts"

    # Daten für config.json vorbereiten und schreiben
    config_data = {
        "city": city,
        "api": openweather_api
    }

    with open('config.json', 'w') as config_json_file:
        json.dump(config_data, config_json_file, indent=4)

    # Daten für firebase.js vorbereiten und schreiben
    firebase_js_content = f"""
let firebaseConfig = {{
    apiKey: "{apiKey}",
    authDomain: "{authDomain}",
    projectId: "{projectId}",
    storageBucket: "{storageBucket}",
    messagingSenderId: "{messagingSenderId}",
    appId: "{appId}",
    measurementId: "{measurementId}",
}};

firebase.initializeApp(firebaseConfig);
"""

    # Pfad zur firebase.js Datei erstellen
    firebase_js_path = f"{firebase_js_directory}/firebase.js"

    with open(firebase_js_path, 'w') as firebase_js_file:
        firebase_js_file.write(firebase_js_content)

    print("Configuration saved successfully!")

def main():
    system = os.name
    if system == 'posix':  # Linux or Mac
        print("Detected a Linux/Mac system.")
        install_packages()
    elif system == 'nt':  # Windows
        print("Detected a Windows system.")
        install_packages()
    else:
        print("Unsupported operating system detected.")

    config()

if __name__ == "__main__":
    main()
