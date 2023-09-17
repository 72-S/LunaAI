import os
import subprocess
import json
import pkg_resources


def is_package_installed(package_name):
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


def generate_self_signed_cert():
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import serialization
    import datetime

    # Schlüsselpaar generieren
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"DE"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Bayern"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"München"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"72-S"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"https://github.com/72-S/"),
    ])
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=365)
    ).sign(private_key, hashes.SHA256())

    with open("cert.pem", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

    with open("key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    print("Certificate created!")


def config():
    city = input("Enter your city: ")
    openweather_api = input("Enter your OpenWeatherMap API key: ")
    apiKey = input("Enter your Firebase apiKey: ")
    authDomain = input("Enter your Firebase authDomain: ")
    projectId = input("Enter your Firebase projectId: ")
    storageBucket = input("Enter your Firebase storageBucket: ")
    messagingSenderId = input("Enter your Firebase messagingSenderId: ")
    appId = input("Enter your Firebase appId: ")
    measurementId = input("Enter your Firebase measurementId: ")

    firebase_js_directory = "static/scripts"
    config_json_directory = "static"

    config_data = {
        "city": city,
        "api": openweather_api
    }

    config_json_path = f"{config_json_directory}/config.json"

    with open(config_json_path, 'w') as config_json_file:
        json.dump(config_data, config_json_file, indent=4)

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

    if not is_package_installed('cryptography'):
        subprocess.check_call(['pip', 'install', 'cryptography'])

    generate_self_signed_cert()
    config()


if __name__ == "__main__":
    main()
