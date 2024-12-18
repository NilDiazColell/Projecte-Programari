
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 10:43:03 2024

@author: abell
"""






import csv
from datetime import datetime
from colorama import Fore, Style, init
import json  # Afegir per treballar amb JSON

# Inicialitzar colorama
init(autoreset=True)

# ------------------ Utils ------------------

def format_date(date):
    """Format de data requerit: DD-MMM-YYYY amb zona horària"""
    return date.strftime("%d-%b-%Y").strip()  # Eliminem espais


def validate_input(prompt, validation_fn, error_message):
    """Demana una entrada vàlida a l'usuari."""
    while True:
        value = input(Fore.CYAN + prompt)
        if validation_fn(value):
            return value
        print(Fore.RED + error_message)

def is_valid_date(date_str):
    """Valida si una cadena té format de data YYYY-MM-DD."""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def is_valid_time(time_str):
    """Valida si una cadena té format d'hora HH:MM."""
    try:
        datetime.strptime(time_str, '%H:%M')
        return True
    except ValueError:
        return False

# ------------------ Singleton ------------------

class User:
    def __init__(self, user_id, name, email, registration_date):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.registration_date = registration_date


class Pacient(User):
    def __init__(self, user_id, name, email, registration_date, medical_record=None):
        super().__init__(user_id, name, email, registration_date)
        self.medical_record = medical_record


class Metge(User):
    def __init__(self, user_id, name, email, registration_date, specialty, colegiate_number):
        super().__init__(user_id, name, email, registration_date)
        self.specialty = specialty
        self.colegiate_number = colegiate_number


class Familiar(User):
    def __init__(self, user_id, name, email, registration_date, relationship):
        super().__init__(user_id, name, email, registration_date)
        self.relationship = relationship



class CSVManager:
    _instances = {}

    def __new__(cls, file_path, *args, **kwargs):
        if file_path not in cls._instances:
            instance = super().__new__(cls)
            instance.file_path = file_path
            cls._instances[file_path] = instance
        return cls._instances[file_path]
    
    def read(self):
        try:
            with open(self.file_path, mode='r', encoding='utf-8') as file:
                data = list(csv.DictReader(file))
                for row in data:
                    # Converteix camps JSON de nou als seus tipus originals
                    for key, value in row.items():
                        if value.startswith("{") or value.startswith("["):  # Comprova si és JSON
                            try:
                                row[key] = json.loads(value)
                            except json.JSONDecodeError:
                                pass
                return data
        except FileNotFoundError:
            print(f"El fitxer {self.file_path} no existeix.")
            return []
        except Exception as e:
            print(f"Error en llegir {self.file_path}: {e}")
            return []


    
    def write(self, fieldnames, data):
        try:
            # Llegeix les dades existents
            existing_data = self.read()
    
            # Combina les dades existents amb les noves, evitant duplicats
            combined_data = {}
            for row in existing_data:
                # Converteix qualsevol estructura no hashable a JSON
                row = {k: (json.dumps(v) if isinstance(v, (dict, list)) else v) for k, v in row.items()}
                combined_data[tuple(row.items())] = row
            for new_row in data:
                # Converteix qualsevol estructura no hashable a JSON
                new_row = {k: (json.dumps(v) if isinstance(v, (dict, list)) else v) for k, v in new_row.items()}
                combined_data[tuple(new_row.items())] = new_row
    
            # Escriu totes les dades al fitxer
            with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(combined_data.values())
        except Exception as e:
            print(f"Error en escriure a {self.file_path}: {e}")

    
    

# ------------------ Factory ------------------

class Factory:
    @staticmethod
    def create_user(user_id, name, email, registration_date, user_type="generic", **kwargs):
        if user_type == "pacient":
            return Pacient(user_id, name, email, registration_date, kwargs.get("medical_record"))
        elif user_type == "metge":
            return Metge(user_id, name, email, registration_date, kwargs.get("specialty"), kwargs.get("colegiate_number"))
        elif user_type == "familiar":
            return Familiar(user_id, name, email, registration_date, kwargs.get("relationship"))
        else:
            return User(user_id, name, email, registration_date)

    @staticmethod
    def create_appointment(appointment_id, user_id, doctor, specialty, date, time, medical_comment):
        return {
            "appointment_id": str(appointment_id),
            "user_id": user_id,
            "doctor": doctor,
            "specialty": specialty,
            "date": date,
            "time": time,
            "medical_comment": medical_comment,
        }

    @staticmethod
    def create_medical_profile(user_id, birth_date, gender, blood_group, allergies, address, phone, medical_comment, medications):
        return {
            "user_id": user_id,
            "birth_date": birth_date,
            "gender": gender,
            "blood_group": blood_group,
            "allergies": str(allergies),
            "address": address,
            "phone": phone,
            "medical_comment": medical_comment,
            "medications": str(medications),
        }
    
    @staticmethod
    def create_notification(notification_id, user_id, message):
        return {
            "notification_id": str(notification_id),
            "user_id": user_id,
            "message": message,
            "timestamp": datetime.now().isoformat(),
        }

    @staticmethod
    def create_social_network(network_id, title, creation_date, members_count=0):
        return {
            "network_id": network_id,
            "title": title,
            "creation_date": creation_date,
            "members_count": members_count,
        }

    @staticmethod
    def create_social_member(name, dni, phones, role, **details):
        return {
            "name": name,
            "dni": dni,
            "phones": phones,
            "role": role,
            "details": details,
        }

    @staticmethod
    def create_medical_visit(date, visit_type, prescription=None):
        return {
            "date": date,
            "visit_type": visit_type,
            "prescription": prescription,
        }

    @staticmethod
    def create_iot_device(name, serial_number, constants, sampling_frequency):
        return {
            "name": name,
            "serial_number": serial_number,
            "constants": constants,
            "sampling_frequency": sampling_frequency,
        }

    @staticmethod
    def create_alert(alert_type, risk_level, contact_number, additional_info=None):
        return {
            "alert_type": alert_type,
            "risk_level": risk_level,
            "contact_number": contact_number,
            "additional_info": additional_info,
        }

# ------------------ Models ------------------

class IoTDevice:
    def __init__(self, name, serial_number, constants, sampling_frequency):
        self.name = name
        self.serial_number = serial_number
        self.constants = constants
        self.sampling_frequency = sampling_frequency

# ------------------ View ------------------

class View:
    @staticmethod
    def display_message(message):
        print(Fore.GREEN + message)

    @staticmethod
    def get_input(prompt):
        return input(Fore.CYAN + prompt)

# ------------------ Controllers ------------------

class UserController:
    def __init__(self, users_manager, view):
        self.users_manager = users_manager
        self.view = view

    def register_user(self):
        self.view.display_message("\n--- REGISTRE D'USUARI ---")
        users = self.users_manager.read()
        user_id = len(users) + 1
        name = self.view.get_input("Introdueix el teu nom: ")
        email = self.view.get_input("Introdueix el teu correu electrònic: ")
        registration_date = format_date(datetime.now())

        user_type = validate_input(
            "Selecciona el tipus d'usuari: 1. Pacient, 2. Metge, 3. Familiar: ",
            lambda x: x in ["1", "2", "3"],
            "Tipus no vàlid. Si us plau, intenta-ho de nou."
        )

        if user_type == "1":  # Pacient
            medical_record = self.view.get_input("Introdueix l'historial mèdic (opcional): ")
            user = Factory.create_user(user_id, name, email, registration_date, "pacient", medical_record=medical_record)
        elif user_type == "2":  # Metge
            specialty = self.view.get_input("Introdueix l'especialitat mèdica: ")
            colegiate_number = self.view.get_input("Introdueix el número de col·legiat: ")
            user = Factory.create_user(user_id, name, email, registration_date, "metge", specialty=specialty, colegiate_number=colegiate_number)
        elif user_type == "3":  # Familiar
            relationship = self.view.get_input("Introdueix el grau de parentiu (ex: germà/na, pare/mare, etc.): ")
            user = Factory.create_user(user_id, name, email, registration_date, "familiar", relationship=relationship)
            
            # Assegurar que només s'afegeixin camps necessaris
        user_dict = {k: v for k, v in user.__dict__.items() if v is not None and k != "parameters"}
        user_dict["type"] = user_type  # Afegir el tipus d'usuari explícitament

        users.append(user.__dict__)  # Convertim l'objecte en diccionari per guardar-lo al CSV
        self.users_manager.write(["user_id", "name", "email", "registration_date", "type"], users)
        self.view.display_message(f"Usuari registrat amb èxit: {user.__dict__}")



    def confirm_user_id(self):
        users = self.users_manager.read()
        while True:
            user_id = self.view.get_input("Introdueix el ID d'usuari: ")
            user_data = next((u for u in users if u["user_id"] == user_id), None)
            if user_data:
                user_type = user_data.get("type", "generic")
    
                # Filtrar camps específics segons el tipus d'usuari
                if user_type == "pacient":
                    user = Pacient(
                        user_id=user_data["user_id"],
                        name=user_data["name"],
                        email=user_data["email"],
                        registration_date=user_data["registration_date"],
                        medical_record=user_data.get("medical_record")
                    )
                elif user_type == "metge":
                    user = Metge(
                        user_id=user_data["user_id"],
                        name=user_data["name"],
                        email=user_data["email"],
                        registration_date=user_data["registration_date"],
                        specialty=user_data.get("specialty"),
                        colegiate_number=user_data.get("colegiate_number")
                    )
                elif user_type == "familiar":
                    user = Familiar(
                        user_id=user_data["user_id"],
                        name=user_data["name"],
                        email=user_data["email"],
                        registration_date=user_data["registration_date"],
                        relationship=user_data.get("relationship")
                    )
                else:
                    user = User(
                        user_id=user_data["user_id"],
                        name=user_data["name"],
                        email=user_data["email"],
                        registration_date=user_data["registration_date"]
                    )
    
                confirm = self.view.get_input(f"T'estàs referint a {user.name}? (sí/no): ").strip().lower()
                if confirm == "sí":
                    return user_id
            self.view.display_message("ID d'usuari no vàlid. Si us plau, intenta-ho de nou.")
    
        


class SocialNetworkController:
    def __init__(self, social_network_manager, users_controller, view):
        self.social_network_manager = social_network_manager
        self.users_controller = users_controller
        self.view = view

    def manage_social_network(self):
        self.view.display_message("\n--- GESTIONAR XARXA SOCIAL ---")
        networks = self.social_network_manager.read()
        action = validate_input(
            "Què vols fer? (1: Crear Xarxa Social, 2: Veure Xarxes Socials, 3: Afegir Membres, 4: Veure total de participants per grup): ",
            lambda x: x in ["1", "2", "3","4"],
            "Opció no vàlida. Si us plau, intenta-ho de nou.",
        )

        if action == "1":
            self.create_social_network(networks)
        elif action == "2":
            self.view_social_networks(networks)
        elif action == "3":
            self.add_members_to_network(networks)
        elif action =='4':
            self.display_members_count()


    def create_social_network(self, networks):
        # Llegim les xarxes socials actuals
        all_networks = self.social_network_manager.read()
    
        # Creem la nova xarxa social
        title = self.view.get_input("Introdueix el títol de la xarxa social: ")
        creation_date = format_date(datetime.now())
        network_id = str(len(all_networks) + 1)
        new_network = Factory.create_social_network(network_id, title, creation_date)
    
        # Afegim la nova xarxa a la llista de xarxes existents
        all_networks.append(new_network)
    
        # Actualitzem el fitxer CSV
        self.social_network_manager.write(["network_id", "title", "creation_date", "members_count", "members"], all_networks)
        self.view.display_message(f"Xarxa social '{title}' creada amb èxit.")

    def view_social_networks(self, networks):
        if not networks:
            self.view.display_message("No hi ha xarxes socials registrades.")
        else:
            for net in networks:
                self.view.display_message(
                    f"ID: {net['network_id']} - Títol: {net['title']} - Data Creació: {net['creation_date']} - Membres: {net['members_count']}"
                )

    def add_members_to_network(self, networks):
        if not networks:
            self.view.display_message("No hi ha xarxes socials disponibles. Crea'n una primer.")
            return

        network_id = self.view.get_input("Introdueix el `network_id` de la xarxa on vols afegir membres: ")
        network = next((n for n in networks if n["network_id"] == network_id), None)

        if not network:
            self.view.display_message(f"No s'ha trobat cap xarxa amb el `network_id` {network_id}.")
            return

        user_id = self.users_controller.confirm_user_id()
        relation_type = validate_input(
            "Quina relació tindrà l'usuari amb la xarxa? (1: Família, 2: Amics, 3: Personal Sanitari): ",
            lambda x: x in ["1", "2", "3"],
            "Opció no vàlida. Si us plau, intenta-ho de nou."
        )

        if relation_type == "1":
            self.add_family_member(network, user_id)
        elif relation_type == "2":
            self.add_friend_member(network, user_id)
        elif relation_type == "3":
            self.add_medical_staff_member(network, user_id)
    


    def add_family_member(self, network, user_id):
        name = self.view.get_input("Introdueix el nom del familiar: ")
        dni = self.view.get_input("Introdueix el DNI del familiar: ")
        phones = self.view.get_input("Introdueix els telèfons del familiar (separats per comes): ").split(",")
        relationship = self.view.get_input("Introdueix el grau de parentiu: ")
        gender = self.view.get_input("Introdueix el gènere: ")
        birth_date = validate_input("Introdueix la data de naixement (YYYY-MM-DD): ", is_valid_date, "Data no vàlida.")
        member = Factory.create_social_member(name, dni, phones, "Família", relationship=relationship, gender=gender, birth_date=birth_date)
        if "members" not in network or not isinstance(network["members"], list):
            network["members"] = []

        network["members"].append(member)
        self.update_network_members(network)

    def add_friend_member(self, network, user_id):
        name = self.view.get_input("Introdueix el nom de l'amic: ")
        dni = self.view.get_input("Introdueix el DNI de l'amic: ")
        phones = self.view.get_input("Introdueix els telèfons de l'amic (separats per comes): ").split(",")
        gender = self.view.get_input("Introdueix el gènere: ")
        birth_date = validate_input("Introdueix la data de naixement (YYYY-MM-DD): ", is_valid_date, "Data no vàlida.")
        hobbies = self.view.get_input("Introdueix els hobbies de l'amic (separats per comes): ").split(",")
        member = Factory.create_social_member(name, dni, phones, "Amics", gender=gender, birth_date=birth_date, hobbies=hobbies)
        if "members" not in network or not isinstance(network["members"], list):
            network["members"] = []

        network["members"].append(member)
        self.update_network_members(network)

    def add_medical_staff_member(self, network, user_id):
        name = self.view.get_input("Introdueix el nom del personal sanitari: ")
        dni = self.view.get_input("Introdueix el DNI del personal sanitari: ")
        phones = self.view.get_input("Introdueix els telèfons del personal sanitari (separats per comes): ").split(",")
        hospital = self.view.get_input("Introdueix el nom de l'hospital o clínica de referència: ")
        role = validate_input("Quin és el rol? (1: Metge, 2: Infermer): ", lambda x: x in ["1", "2"], "Opció no vàlida.")
        if role == "1":
            colegiate_number = self.view.get_input("Introdueix el número de col·legiat: ")
            specialty = self.view.get_input("Introdueix l'especialitat (opcional): ")
            member = Factory.create_social_member(name, dni, phones, "Metge", hospital=hospital, colegiate_number=colegiate_number, specialty=specialty)
        else:
            home_assistance = self.view.get_input("Realitza assistència domiciliària? (sí/no): ").strip().lower() == "sí"
            member = Factory.create_social_member(name, dni, phones, "Infermer", hospital=hospital, home_assistance=home_assistance)
        if "members" not in network or not isinstance(network["members"], list):
            network["members"] = []

        network["members"].append(member)
        self.update_network_members(network)
        
        

    def update_network_members(self, network):
        network["members_count"] = len(network["members"])
        self.social_network_manager.write(["network_id", "title", "creation_date", "members_count", "members"], [network])
        self.view.display_message(f"Nou membre afegit a la xarxa amb ID {network['network_id']}.")
    
    
    

    def display_members_count(self):
        """
        Mostra el total de membres per cada grup únic (network_id).
        """
        # Llegeix totes les xarxes socials existents
        all_networks = self.social_network_manager.read()
    
        if not all_networks:
            self.view.display_message("No hi ha xarxes socials registrades.")
            return
    
        # Mapa per comptar el nombre de membres per cada network_id
        members_count_map = {}
        for network in all_networks:
            network_id = network["network_id"]
            members_count = int(network["members_count"]) if "members_count" in network else 0
            if network_id not in members_count_map:
                members_count_map[network_id] = {
                    "title": network["title"],
                    "total_members": members_count
                }
            else:
                members_count_map[network_id]["total_members"] += members_count

        # Mostra els resultats
        self.view.display_message("\n--- Total Membres per Grup ---")
        for network_id, data in members_count_map.items():
            self.view.display_message(f"ID: {network_id} - Títol: {data['title']} - Membres: {data['total_members']}")

    
class AppointmentController:
    def __init__(self, appointments_manager, users_controller, view):
        self.appointments_manager = appointments_manager
        self.users_controller = users_controller
        self.view = view

    def schedule_appointment(self):
        self.view.display_message("\n--- PROGRAMAR CITA MÈDICA ---")
        user_id = self.users_controller.confirm_user_id()
        appointments = self.appointments_manager.read()
        appointment_id = len(appointments) + 1
        
        doctor = self.view.get_input("Introdueix el nom del doctor: ")
        specialty = self.view.get_input("Introdueix l'especialitat mèdica: ")
        date = validate_input("Introdueix la data (YYYY-MM-DD): ", is_valid_date, "Data no vàlida.")
        time = validate_input("Introdueix l'hora (HH:MM): ", is_valid_time, "Hora no vàlida.")
        medical_comment = self.view.get_input("Descriu la teva situació mèdica actual (15-20 paraules): ")
        


        appointment = Factory.create_appointment(appointment_id, user_id, doctor, specialty, date, time, medical_comment)
        
        appointments.append(appointment)
        
        self.appointments_manager.write(["appointment_id", "user_id", "doctor", "specialty", "date", "time", "medical_comment"], appointments)
        
        self.view.display_message(f"Cita programada amb èxit: {appointment}")


class NotificationController:
    def __init__(self, notifications_manager, users_controller, view):
        self.notifications_manager = notifications_manager
        self.users_controller = users_controller
        self.view = view

    def send_notification(self):
        self.view.display_message("\n--- ENVIAR NOTIFICACIÓ ---")
        user_id = self.users_controller.confirm_user_id()
        notifications = self.notifications_manager.read()
        notification_id = len(notifications) + 1
        message = self.view.get_input("Introdueix el missatge de la notificació: ")
        notification = Factory.create_notification(notification_id, user_id, message)
        notifications.append(notification)
        self.notifications_manager.write(["notification_id", "user_id", "message", "timestamp"], notifications)
        self.view.display_message(f"Notificació enviada amb èxit: {notification}")

class ParameterController:
    def __init__(self, parameters_manager, users_controller, view):
        self.parameters_manager = parameters_manager
        self.users_controller = users_controller
        self.view = view

    
    def view_parameters(self):
        self.view.display_message("\n--- VEURE PARÀMETRES DE SALUT ---")
        user_id = self.users_controller.confirm_user_id()
        parameters = self.parameters_manager.read()
    
        # Filtrem paràmetres per l'usuari en específic
        user_parameters = [p for p in parameters if p["user_id"] == user_id]
    
        if user_parameters:
            for param in user_parameters:
                # Utilitzar les claus correctes
                constant = param.get("constant", "Desconeguda")
                value = param.get("value", "No disponible")
                
                self.view.display_message(f"\n--- PARÀMETRES DE SALUT DE L'USUARI {user_id} ---")
                self.view.display_message(f"{constant}: {value}")
        else:
            self.view.display_message("No s'han trobat paràmetres per aquest usuari.")
            
class MedicalProfileController:
    def __init__(self, profiles_manager, users_controller, view):
        self.profiles_manager = profiles_manager
        self.users_controller = users_controller
        self.view = view

    def create_medical_profile(self):
        self.view.display_message("\n--- CREAR PERFIL MÈDIC ---")
        profiles = self.profiles_manager.read()
        user_id = self.users_controller.confirm_user_id()

        # Verificar si el perfil ja existeix
        if any(p['user_id'] == user_id for p in profiles):
            self.view.display_message("Ja existeix un perfil mèdic per aquest usuari.")
            return

        # Demanar dades del perfil mèdic
        birth_date = validate_input("Introdueix la teva data de naixement (YYYY-MM-DD): ", is_valid_date, "Data no vàlida.")
        gender = self.view.get_input("Introdueix el teu gènere: ")
        blood_group = self.view.get_input("Introdueix el teu grup sanguini: ")
        allergies = self.view.get_input("Tens al·lèrgies? (sí/no): ").strip().lower() == "sí"
        address = self.view.get_input("Introdueix la teva adreça: ")
        phone = self.view.get_input("Introdueix el teu número de telèfon: ")
        medical_comment = self.view.get_input("Descriu la teva situació mèdica actual (15-20 paraules): ")

        # Gestionar medicaments
        medications = []
        takes_meds = self.view.get_input("Prens algun medicament? (sí/no): ").strip().lower() == "sí"
        while takes_meds:
            med_name = self.view.get_input("Introdueix el nom del medicament: ")
            med_duration = self.view.get_input("Quant de temps fa que el prens?: ")
            medications.append({"name": med_name, "duration": med_duration})
            takes_meds = self.view.get_input("Vols afegir un altre medicament? (sí/no): ").strip().lower() == "sí"

        # Crear i guardar el perfil mèdic
        profile = Factory.create_medical_profile(user_id, birth_date, gender, blood_group, allergies, address, phone, medical_comment, medications)
        profiles.append(profile)
        self.profiles_manager.write(["user_id", "birth_date", "gender", "blood_group", "allergies", "address", "phone", "medical_comment", "medications"], profiles)
        self.view.display_message(f"Perfil mèdic creat amb èxit per l'usuari {user_id}.")
         
class IoTDeviceController:
    def __init__(self, iot_manager, constants_manager, thresholds_manager, alerts_manager, users_controller, view):
        self.iot_manager = iot_manager
        self.constants_manager = constants_manager
        self.thresholds_manager = thresholds_manager  
        self.alerts_manager = alerts_manager
        self.users_controller = users_controller
        self.view = view

    def add_iot_device(self):
        self.view.display_message("\n--- AFEGIR DISPOSITIU IoT ---")
        user_id = self.users_controller.confirm_user_id()
        devices = self.iot_manager.read()

        name = self.view.get_input("Introdueix el nom del dispositiu IoT: ")
        serial_number = self.view.get_input("Introdueix el número de sèrie únic: ")
        constants = self.view.get_input("Introdueix les constants vitals monitoritzades (separades per comes): ")
        constants_list = [c.strip() for c in constants.split(",") if c.strip()]  # Separar correctament
        sampling_frequency = self.view.get_input("Introdueix la freqüència de mostreig (en segons): ")

        new_device = {
            "user_id": user_id,
            **Factory.create_iot_device(name, serial_number, constants_list, sampling_frequency)
        }
        devices.append(new_device)
        self.iot_manager.write(["user_id", "name", "serial_number", "constants", "sampling_frequency"], devices)
        self.view.display_message(f"Dispositiu IoT '{name}' afegit per l'usuari amb ID {user_id}.")

    def configure_thresholds(self):
        self.view.display_message("\n--- CONFIGURAR LLINDARS ---")
        constant = self.view.get_input("Introdueix el nom de la constant vital a configurar: ")
        min_level = self.view.get_input("Introdueix el nivell mínim acceptable (opcional, deixar buit per cap): ")
        max_level = self.view.get_input("Introdueix el nivell màxim acceptable (opcional, deixar buit per cap): ")
        units = self.view.get_input("Introdueix les unitats de la constant (opcional): ")

        thresholds = {
            "constant": constant,
            "min_level": min_level.strip() if min_level else None,
            "max_level": max_level.strip() if max_level else None,
            "units": units.strip() if units else None,
        }

        thresholds_data = self.thresholds_manager.read()
        thresholds_data.append(thresholds)
        self.thresholds_manager.write(["constant", "min_level", "max_level", "units"], thresholds_data)
        self.view.display_message(f"Llindars configurats per la constant '{constant}'.")

    def record_measurement(self):
        self.view.display_message("\n--- REGISTRAR UNA MESURA ---")
        user_id = self.users_controller.confirm_user_id()
        devices = [d for d in self.iot_manager.read() if d["user_id"] == user_id]

        if not devices:
            self.view.display_message("Aquest usuari no té dispositius IoT associats.")
            return

        self.view.display_message("Dispositius disponibles:")
        for idx, device in enumerate(devices):
            constants_display = (device.get("constants", []))  # Unir constants amb comes
            self.view.display_message(f"{idx + 1}. {device['name']} - Constants: [{constants_display}]")

        device_idx = int(validate_input("Selecciona el dispositiu (número): ", 
                                         lambda x: x.isdigit() and 1 <= int(x) <= len(devices), 
                                         "Selecció no vàlida.")) - 1
        device = devices[device_idx]

        constants_list = device.get("constants", [])
        constant = validate_input(
            f"Quina constant vols registrar {constants_list}: ",
            lambda x: x in constants_list,
            "Constant no vàlida. Selecciona una de la llista."
        )

        value = float(self.view.get_input(f"Introdueix el valor de {constant}: "))
        timestamp = datetime.now().isoformat()

        # Afegim la mesura al fitxer de constants
        parameters = self.constants_manager.read()
        parameters.append({
            "user_id": user_id,
            "constant": constant,
            "value": value,
            "timestamp": timestamp
        })
        self.constants_manager.write(["user_id", "constant", "value", "timestamp"], parameters)
        self.view.display_message(f"Mesura registrada: {constant} = {value} (Usuari ID {user_id})")

        # Comprovar llindars i generar alerta si cal
        self.check_thresholds(constant, value, user_id)

    def check_thresholds(self, constant, value, user_id):
        thresholds = self.thresholds_manager.read()
        threshold = next((t for t in thresholds if t["constant"] == constant), None)
    
        if not threshold:
            self.view.display_message(f"No hi ha llindars configurats per la constant {constant}.")
            return

        try:
            min_level = float(threshold["min_level"]) if threshold["min_level"] else float('-inf')
            max_level = float(threshold["max_level"]) if threshold["max_level"] else float('inf')
            if value < min_level or value > max_level:
                self.generate_alert(constant, value, threshold, user_id)
        except ValueError as e:
            self.view.display_message(f"Error al validar llindars: {e}. Els valors no són vàlids per la constant {constant}.")

    def generate_alert(self, constant, value, threshold, user_id):
        alert_type = validate_input(
            "Selecciona el tipus d'alerta (1: Urgències, 2: Personal Mèdic, 3: Cuidador): ",
            lambda x: x in ["1", "2", "3"],
            "Opció no vàlida."
        )

        risk_level = "Alt" if alert_type == "1" else "Mitjà"
        contact_number = self.view.get_input("Introdueix el número de telèfon de contacte: ")

        additional_info = {}
        if alert_type == "1":  # Urgències
            additional_info["ambulance_required"] = (
                self.view.get_input("Es necessita ambulància? (sí/no): ").strip().lower() == "sí"
            )
            additional_info["clinical_history_code"] = self.view.get_input(
                "Introdueix el codi de la història clínica: "
            )
        elif alert_type == "2":  # Personal Mèdic
            additional_info["access_key"] = "TEMP_KEY_24H"
            additional_info["message"] = self.view.get_input("Introdueix un missatge descriptiu de l'alerta: ")
        elif alert_type == "3":  # Cuidador
            additional_info["instructions"] = self.view.get_input("Introdueix les instruccions per al cuidador: ")

        alert = {
            "user_id": user_id,
            "constant": constant,
            "value": value,
            "risk_level": risk_level,
            "contact_number": contact_number,
            "additional_info": additional_info
        }

        alerts_data = self.alerts_manager.read()
        alerts_data.append(alert)
        self.alerts_manager.write(
            ["user_id", "constant", "value", "risk_level", "contact_number", "additional_info"],
            alerts_data
        )
        self.view.display_message(f"Alerta generada per la constant {constant} (Valor: {value}).")
    
    
def main_menu():
    # Models
    users_manager = CSVManager(r"C:\Users\abell\Downloads\usuaris.csv")
    appointments_manager = CSVManager(r"C:\Users\abell\Downloads\cites.csv")
    notifications_manager = CSVManager(r"C:\Users\abell\Downloads\notificacions.csv")
    profiles_manager = CSVManager(r"C:\Users\abell\Downloads\perfils_medics.csv")
    social_network_manager = CSVManager(r"C:\Users\abell\Downloads\xarxes_socials.csv")
    parameters_manager = CSVManager(r"C:\Users\abell\Downloads\constants.csv")
    iot_manager = CSVManager(r"C:\Users\abell\Downloads\dispositius_iot.csv")
    thresholds_manager = CSVManager(r"C:\Users\abell\Downloads\thresholds.csv")  
    alert_manager = CSVManager(r"C:\Users\abell\Downloads\alertes.csv")

    # Views
    view = View()

    # Controllers
    users_controller = UserController(users_manager, view)
    appointment_controller = AppointmentController(appointments_manager, users_controller, view)
    notification_controller = NotificationController(notifications_manager, users_controller, view)
    parameter_controller = ParameterController(parameters_manager, users_controller, view)
    medical_controller = MedicalProfileController(profiles_manager, users_controller, view)
    social_network_controller = SocialNetworkController(social_network_manager, users_controller, view)
    iot_controller = IoTDeviceController(
        iot_manager, parameters_manager, thresholds_manager, alert_manager, users_controller, view
    )

    print(Fore.BLUE + Style.BRIGHT + "\n\nBenvingut a SeniorLife! El teu gestor mèdic de confiança.\n")
    current_user = None

    while not current_user:
        print(Fore.YELLOW + Style.BRIGHT + "\n--- MENÚ PRINCIPAL ---")
        print("1. Iniciar Sessió")
        print("2. Registrar-se")
        print("3. Sortir")
        choice = view.get_input("Selecciona una opció: ")

        if choice == "1":
            email = view.get_input("Introdueix el teu correu electrònic: ")
            users = users_manager.read()
            current_user = next((u for u in users if u["email"] == email), None)
            if current_user:
                user_type = current_user["type"]  # Assigna el tipus d'usuari des del fitxer
                view.display_message(f"\nBenvingut/a de nou, {current_user['name']}!")
            else:
                view.display_message("Aquest correu no està registrat. Si us plau, registra't primer.")
        elif choice == "2":
            print(Fore.YELLOW + Style.BRIGHT + "\n--- REGISTRE D'USUARI ---")
            print("1. Registrar-se com a Pacient")
            print("2. Registrar-se com a Metge")
            print("3. Registrar-se com a Familiar")
            user_type_choice = view.get_input("Selecciona el tipus d'usuari: ")

            if user_type_choice in ["1", "2", "3"]:
                user_type = "pacient" if user_type_choice == "1" else "metge" if user_type_choice == "2" else "familiar"
                users = users_manager.read()
                email = view.get_input("Introdueix el teu correu electrònic per registrar-te: ")
                if any(u["email"] == email for u in users):
                    view.display_message("Aquest correu ja està registrat. Si us plau, inicia sessió.")
                else:
                    name = view.get_input("Introdueix el teu nom: ")
                    registration_date = format_date(datetime.now())
                    user_id = len(users) + 1

                    if user_type == "pacient":
                        medical_record = view.get_input("Introdueix l'historial mèdic (opcional): ")
                        new_user = Factory.create_user(user_id, name, email, registration_date, user_type, medical_record=medical_record)
                    elif user_type == "metge":
                        specialty = view.get_input("Introdueix l'especialitat mèdica: ")
                        colegiate_number = view.get_input("Introdueix el número de col·legiat: ")
                        new_user = Factory.create_user(user_id, name, email, registration_date, user_type, specialty=specialty, colegiate_number=colegiate_number)
                    elif user_type == "familiar":
                        relationship = view.get_input("Introdueix el grau de parentiu (ex: germà/na, pare/mare, etc.): ")
                        new_user = Factory.create_user(user_id, name, email, registration_date, user_type, relationship=relationship)

                    # Assegurar que el camp `type` es guarda correctament al CSV
                    user_dict = new_user.__dict__
                    user_dict["type"] = user_type  # Afegir explícitament el tipus d'usuari

                    users.append(user_dict)
                    users_manager.write(
                        ["user_id", "name", "email", "registration_date", "type", "medical_record", "specialty", "colegiate_number", "relationship"],
                        users
                    )
                    view.display_message(f"Usuari registrat amb èxit. Benvingut/da, {name}!")
                    # Un cop registrat, es reinicia el menú principal
            else:
                view.display_message("Tipus d'usuari no vàlid. Si us plau, intenta-ho de nou.")
        elif choice == "3":
            view.display_message("\nSortint del sistema... Gràcies per confiar en SeniorLife!")
            return
        else:
            view.display_message("Opció no vàlida. Si us plau, intenta-ho de nou.")

    # Un cop l'usuari ha iniciat sessió, accedeix a les funcionalitats
    running = True
    while running:
        print(Fore.YELLOW + Style.BRIGHT + "\n--- MENÚ PRINCIPAL ---")
        if current_user["type"] == "pacient":
            print("1. Programar cita")
            print("2. Crear perfil mèdic")
            print("3. Veure paràmetres de salut")
            print("4. Gestionar xarxa social")
        elif current_user["type"] == "metge":
            print("1. Enviar notificació")
            print("2. Afegir dispositiu IoT")
            print("3. Configurar llindars")
            print("4. Registrar mesura")
            print("5. Veure paràmetres de salut")
        elif current_user["type"] == "familiar":
            print("1. Gestionar xarxa social")
        print("9. Sortir")
        choice = view.get_input("Selecciona una opció: ")

        if choice == "9":  # Afegit per sortir del bucle principal
            view.display_message("\nSortint del sistema... Gràcies per confiar en SeniorLife!")
            running = False
        elif current_user["type"] == "pacient":
            if choice == "1":
                appointment_controller.schedule_appointment()
            elif choice == "2":
                medical_controller.create_medical_profile()
            elif choice == "3":
                parameter_controller.view_parameters()
            elif choice == "4":
                social_network_controller.manage_social_network()
            else:
                view.display_message("Opció no vàlida. Si us plau, intenta-ho de nou.")
        elif current_user["type"] == "metge":
            if choice == "1":
                notification_controller.send_notification()
            elif choice == "2":
                iot_controller.add_iot_device()
            elif choice == "3":
                iot_controller.configure_thresholds()
            elif choice == "4":
                iot_controller.record_measurement()
            elif choice == "5":
                parameter_controller.view_parameters()
            else:
                view.display_message("Opció no vàlida. Si us plau, intenta-ho de nou.")
        elif current_user["type"] == "familiar":
            if choice == "1":
                social_network_controller.manage_social_network()
            else:
                view.display_message("Opció no vàlida. Si us plau, intenta-ho de nou.")

if __name__ == "__main__":
    main_menu()





