import os
import subprocess
import pkg_resources
import sys

country = "DE"


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
        'requests',
        'cryptography',
        'tkinter',
        'customtkinter'
    ]

    for package in packages:
        if not is_package_installed(package):
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"{package} installed successfully!")
            except subprocess.CalledProcessError as e:
                print(f"Error installing {package}.")
                print(str(e))
        else:
            print(f"{package} is already installed.")


install_packages()


import tkinter as tk
import customtkinter as ctk
import json
import pkg_resources


def generate_self_signed_cert():
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import serialization
    import datetime

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


def save_config():
    firebase_js_directory = "/static/scripts"
    config_json_directory = "/static"

    config_data = {
        "city": cityinput.get(),
        "country": country,
        "api": apiinput.get(),
        "apiKey": firebase_apikey.get(),
        "authDomain": firebase_authkey.get(),
        "databaseURL": databaseURLkey.get(),
        "projectId": projectIdkey.get(),
        "storageBucket": storageBucketkey.get(),
        "messagingSenderId": messagingSenderIdkey.get(),
        "appId": appIdkey.get(),
        "measurementId": measurementIdkey.get()
    }

    config_json_path = f"{config_json_directory}/config.json"

    with open(config_json_path, 'w') as config_json_file:
        json.dump(config_data, config_json_file, indent=4)

    js_template = """
import {{ initializeApp }} from "https://www.gstatic.com/firebasejs/10.4.0/firebase-app.js";
import {{ getDatabase, ref, set, get }} from "https://www.gstatic.com/firebasejs/10.4.0/firebase-database.js";

const firebaseConfig = {{
    apiKey: "{apiKey}",
    authDomain: "{authDomain}",
    projectId: "{projectId}",
    storageBucket: "{storageBucket}",
    messagingSenderId: "{messagingSenderId}",
    appId: "{appId}",
    measurementId: "{measurementId}",
}};

const app = initializeApp(firebaseConfig);
const db = getDatabase(app);

export {{ db, ref, set, get }};
"""

    js_content = js_template.format(**config_data)
    js_file_path = f"{firebase_js_directory}/firebase.js"
    with open(js_file_path, "w") as file:
        file.write(js_content)





def confirm_city():
    # Ausgabe des eingegebenen Wertes
    print(cityinput.get())

    # Erste Seite ausblenden
    main_page.pack_forget()

    # Zweite Seite anzeigen
    second_page.pack()


def confirm_api():
    # Ausgabe des eingegebenen Wertes
    print(apiinput.get())

    # Zweite Seite ausblenden
    second_page.pack_forget()

    # Dritte Seite anzeigen
    third_page.pack()


def confirm_firebase_api():
    # Ausgabe des eingegebenen Wertes
    print(firebase_apikey.get())

    # Dritte Seite ausblenden
    third_page.pack_forget()

    # Vierte Seite anzeigen
    fourth_page.pack()


def confirm_firebase_auth():
    # Ausgabe des eingegebenen Wertes
    print(firebase_authkey.get())

    # Vierte Seite ausblenden
    fourth_page.pack_forget()

    # Fünfte Seite anzeigen
    fifth_page.pack()


def confirm_databaseURL():
    # Ausgabe des eingegebenen Wertes
    print(databaseURLkey.get())

    # Fünfte Seite ausblenden
    fifth_page.pack_forget()

    # Sechste Seite anzeigen
    sixth_page.pack()


def confirm_projectId():
    # Ausgabe des eingegebenen Wertes
    print(projectIdkey.get())

    # Sechste Seite ausblenden
    sixth_page.pack_forget()

    # Siebte Seite anzeigen
    seventh_page.pack()


def confirm_storageBucket():
    # Ausgabe des eingegebenen Wertes
    print(storageBucketkey.get())

    # Siebte Seite ausblenden
    seventh_page.pack_forget()

    # Achte Seite anzeigen
    eighth_page.pack()


def confirm_messagingSenderId():
    # Ausgabe des eingegebenen Wertes
    print(messagingSenderIdkey.get())

    # Achte Seite ausblenden
    eighth_page.pack_forget()

    # Neunte Seite anzeigen
    ninth_page.pack()


def confirm_appId():
    # Ausgabe des eingegebenen Wertes
    print(appIdkey.get())

    # Neunte Seite ausblenden
    ninth_page.pack_forget()

    # Zehnte Seite anzeigen
    tenth_page.pack()


def confirm_measurementId():
    # Ausgabe des eingegebenen Wertes
    print(measurementIdkey.get())

    # Zehnte Seite ausblenden
    tenth_page.pack_forget()

    # Elfte Seite anzeigen
    eleventh_page.pack()


def finish_setup():
    # Ausgabe des eingegebenen Wertes
    print("Setup completed!")

    # Elfte Seite ausblenden
    eleventh_page.pack_forget()
    save_config()
    generate_self_signed_cert()

    # you can close the window
    close_page.pack()
    app.destroy()


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("480x340")
app.title("LunaAi - Setup")

# Hauptseite
main_page = tk.Frame(app)
main_page.pack()
main_page.configure(bg="#242424")

cityinput = tk.StringVar()
title = ctk.CTkLabel(main_page, text="Enter your city", font=("Helvetica", 18))
title.pack(padx=10, pady=10)

city = ctk.CTkEntry(main_page, width=350, height=50, textvariable=cityinput)
city.pack(padx=10, pady=10)

city_confirm = ctk.CTkButton(main_page, text="Confirm", width=350, height=50, command=confirm_city)
city_confirm.pack(padx=10, pady=10)

# Zweite Seite
apiinput = tk.StringVar()
second_page = tk.Frame(app)
second_page.configure(bg="#242424")
title2 = ctk.CTkLabel(second_page, text="Enter your OpenWeatherMap API key", font=("Helvetica", 18))
title2.pack(padx=10, pady=10)

api = ctk.CTkEntry(second_page, width=350, height=50, textvariable=apiinput)
api.pack(padx=10, pady=10)

confirm = ctk.CTkButton(second_page, text="Confirm", width=350, height=50, command=confirm_api)
confirm.pack(padx=10, pady=10)

back_button = ctk.CTkButton(second_page, text="Back", width=350, height=50,
                            command=lambda: [second_page.pack_forget(), main_page.pack()])
back_button.pack(padx=10, pady=10)

# third Page
firebase_apikey = tk.StringVar()
third_page = tk.Frame(app)
third_page.configure(bg="#242424")
title3 = ctk.CTkLabel(third_page, text="Enter your Firebase API key", font=("Helvetica", 18))
title3.pack(padx=10, pady=10)

firebase_api = ctk.CTkEntry(third_page, width=350, height=50, textvariable=firebase_apikey)
firebase_api.pack(padx=10, pady=10)

confirm2 = ctk.CTkButton(third_page, text="Confirm", width=350, height=50, command=confirm_firebase_api)
confirm2.pack(padx=10, pady=10)

back_button2 = ctk.CTkButton(third_page, text="Back", width=350, height=50,
                             command=lambda: [third_page.pack_forget(), second_page.pack()])
back_button2.pack(padx=10, pady=10)

# fourth Page
firebase_authkey = tk.StringVar()
fourth_page = tk.Frame(app)
fourth_page.configure(bg="#242424")
title4 = ctk.CTkLabel(fourth_page, text="Enter your Firebase Auth Domain", font=("Helvetica", 18))
title4.pack(padx=10, pady=10)

firebase_auth = ctk.CTkEntry(fourth_page, width=350, height=50, textvariable=firebase_authkey)
firebase_auth.pack(padx=10, pady=10)

confirm3 = ctk.CTkButton(fourth_page, text="Confirm", width=350, height=50, command=confirm_firebase_auth)
confirm3.pack(padx=10, pady=10)

back_button3 = ctk.CTkButton(fourth_page, text="Back", width=350, height=50,
                             command=lambda: [fourth_page.pack_forget(), third_page.pack()])
back_button3.pack(padx=10, pady=10)

# fifth Page
databaseURLkey = tk.StringVar()
fifth_page = tk.Frame(app)
fifth_page.configure(bg="#242424")
title5 = ctk.CTkLabel(fifth_page, text="Enter your Firebase Database URL", font=("Helvetica", 18))
title5.pack(padx=10, pady=10)

databaseURL = ctk.CTkEntry(fifth_page, width=350, height=50, textvariable=databaseURLkey)
databaseURL.pack(padx=10, pady=10)

confirm4 = ctk.CTkButton(fifth_page, text="Confirm", width=350, height=50, command=confirm_databaseURL)
confirm4.pack(padx=10, pady=10)

back_button4 = ctk.CTkButton(fifth_page, text="Back", width=350, height=50,
                             command=lambda: [fifth_page.pack_forget(), fourth_page.pack()])
back_button4.pack(padx=10, pady=10)

# sixth Page
projectIdkey = tk.StringVar()
sixth_page = tk.Frame(app)
sixth_page.configure(bg="#242424")
title6 = ctk.CTkLabel(sixth_page, text="Enter your Firebase Project ID", font=("Helvetica", 18))
title6.pack(padx=10, pady=10)

projectId = ctk.CTkEntry(sixth_page, width=350, height=50, textvariable=projectIdkey)
projectId.pack(padx=10, pady=10)

confirm5 = ctk.CTkButton(sixth_page, text="Confirm", width=350, height=50, command=confirm_projectId)
confirm5.pack(padx=10, pady=10)

back_button5 = ctk.CTkButton(sixth_page, text="Back", width=350, height=50,
                             command=lambda: [sixth_page.pack_forget(), fifth_page.pack()])
back_button5.pack(padx=10, pady=10)

# seventh Page
storageBucketkey = tk.StringVar()
seventh_page = tk.Frame(app)
seventh_page.configure(bg="#242424")
title7 = ctk.CTkLabel(seventh_page, text="Enter your Firebase Storage Bucket", font=("Helvetica", 18))
title7.pack(padx=10, pady=10)

storageBucket = ctk.CTkEntry(seventh_page, width=350, height=50, textvariable=storageBucketkey)
storageBucket.pack(padx=10, pady=10)

confirm6 = ctk.CTkButton(seventh_page, text="Confirm", width=350, height=50, command=confirm_storageBucket)
confirm6.pack(padx=10, pady=10)

back_button6 = ctk.CTkButton(seventh_page, text="Back", width=350, height=50,
                             command=lambda: [seventh_page.pack_forget(), sixth_page.pack()])
back_button6.pack(padx=10, pady=10)

# eighth Page
messagingSenderIdkey = tk.StringVar()
eighth_page = tk.Frame(app)
eighth_page.configure(bg="#242424")
title8 = ctk.CTkLabel(eighth_page, text="Enter your Firebase Messaging Sender ID", font=("Helvetica", 18))
title8.pack(padx=10, pady=10)

messagingSenderId = ctk.CTkEntry(eighth_page, width=350, height=50, textvariable=messagingSenderIdkey)
messagingSenderId.pack(padx=10, pady=10)

confirm7 = ctk.CTkButton(eighth_page, text="Confirm", width=350, height=50, command=confirm_messagingSenderId)
confirm7.pack(padx=10, pady=10)

back_button7 = ctk.CTkButton(eighth_page, text="Back", width=350, height=50,
                             command=lambda: [eighth_page.pack_forget(), seventh_page.pack()])
back_button7.pack(padx=10, pady=10)

# ninth Page
appIdkey = tk.StringVar()
ninth_page = tk.Frame(app)
ninth_page.configure(bg="#242424")
title9 = ctk.CTkLabel(ninth_page, text="Enter your Firebase App ID", font=("Helvetica", 18))
title9.pack(padx=10, pady=10)

appId = ctk.CTkEntry(ninth_page, width=350, height=50, textvariable=appIdkey)
appId.pack(padx=10, pady=10)

confirm8 = ctk.CTkButton(ninth_page, text="Confirm", width=350, height=50, command=confirm_appId)
confirm8.pack(padx=10, pady=10)

back_button8 = ctk.CTkButton(ninth_page, text="Back", width=350, height=50,
                             command=lambda: [ninth_page.pack_forget(), eighth_page.pack()])
back_button8.pack(padx=10, pady=10)

# tenth Page
measurementIdkey = tk.StringVar()
tenth_page = tk.Frame(app)
tenth_page.configure(bg="#242424")
title10 = ctk.CTkLabel(tenth_page, text="Enter your Firebase Measurement ID", font=("Helvetica", 18))
title10.pack(padx=10, pady=10)

measurementId = ctk.CTkEntry(tenth_page, width=350, height=50, textvariable=measurementIdkey)
measurementId.pack(padx=10, pady=10)

confirm9 = ctk.CTkButton(tenth_page, text="Confirm", width=350, height=50, command=confirm_measurementId)
confirm9.pack(padx=10, pady=10)

back_button9 = ctk.CTkButton(tenth_page, text="Back", width=350, height=50,
                             command=lambda: [tenth_page.pack_forget(), ninth_page.pack()])
back_button9.pack(padx=10, pady=10)

# safe and install Page
eleventh_page = tk.Frame(app)
eleventh_page.configure(bg="#242424")
title11 = ctk.CTkLabel(eleventh_page, text="Setup completed!", font=("Helvetica", 18))
title11.pack(padx=10, pady=40)

confirm10 = ctk.CTkButton(eleventh_page, text="Finish", width=350, height=50, command=finish_setup)
confirm10.pack(padx=10, pady=10)

back_button10 = ctk.CTkButton(eleventh_page, text="Back", width=350, height=50,
                              command=lambda: [eleventh_page.pack_forget(), tenth_page.pack()])
back_button10.pack(padx=10, pady=10)

# close window
close_page = tk.Frame(app)
close_page.configure(bg="#242424")
title12 = ctk.CTkLabel(close_page, text="You can close the Window now", font=("Helvetica", 18))
title12.pack(padx=10, pady=150)

app.mainloop()
