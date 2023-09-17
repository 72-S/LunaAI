import os
import subprocess
import json
import pkg_resources



def is_package_installed(package_name):
    """Überprüft, ob ein Python-Paket bereits installiert ist."""
    try:
        pkg_resources.get_distribution(package_name)
        return True
    except pkg_resources.DistributionNotFound:
        return False

def install_packages():
    packages = [
        'Flask',
        'gpt4all',
        'edge_tts',
        'nest_asyncio',
        'deep_translator',
        'requests'
    ]

    for package in packages:
        if not is_package_installed(package):
            try:
                subprocess.check_call(['pip', 'install', package])
                print(f"{package} installed successfully!")
            except subprocess.CalledProcessError as e:
                print(f"Error installing {package}.")
                print(str(e))
        else:
            print(f"{package} is already installed.")

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
    config_json_directory = "static"

    # Daten für config.json vorbereiten und schreiben
    config_data = {
        "city": city,
        "api": openweather_api
    }

    config_json_path = f"{config_json_directory}/config.json"

    with open(config_json_path, 'w') as config_json_file:
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
