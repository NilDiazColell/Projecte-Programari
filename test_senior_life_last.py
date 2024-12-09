
# # -*- coding: utf-8 -*-
# """
# Test suite para el sistema SeniorLife.
# """

# import unittest
# from unittest.mock import patch, MagicMock
# from datetime import datetime
# import sys
# import os

# # Ruta al archivo programa_FINAL_SeniorLife.py
# module_dir = r"C:\Users\abell\OneDrive\Documentos\3r_Carrera\Programari\Projecte_programari"
# sys.path.append(module_dir)

# from programa_FINAL_SeniorLife import (
#     format_date, validate_input, is_valid_date, is_valid_time, CSVManager, Factory,
#     UserController, AppointmentController, View, MedicalProfileController,
#     NotificationController, ParameterController, IoTDeviceController, SocialNetworkController
# )

# # Clase de prueba
# class TestSeniorLife(unittest.TestCase):
#     def setUp(self):
#         """
#         Configuración inicial para las pruebas. Simula un entorno limpio.
#         """
#         # Crear instancias de managers simulados con datos predefinidos
#         self.users_manager = MagicMock(spec=CSVManager)
#         self.view = MagicMock(spec=View)
#         self.users_controller = UserController(self.users_manager, self.view)

#     def test_register_user(self):
#         """
#         Test para la función de registro de usuario.
#         """
#         # Simular datos existentes
#         self.users_manager.read.return_value = [
#             {"user_id": "1", "name": "John Doe", "email": "john@example.com", "registration_date": "01-Jan-2024"}
#         ]

#         # Simular inputs de usuario
#         self.view.get_input.side_effect = ["Alice", "alice@example.com"]

#         # Simular la fecha actual
#         mock_date = datetime(2024, 12, 7, 15, 30)
#         with patch("programa_FINAL_SeniorLife.datetime") as mock_datetime:
#             mock_datetime.now.return_value = mock_date
#             mock_datetime.strftime = datetime.strftime

#             # Ejecutar la función
#             self.users_controller.register_user()

#         # Verificar que el usuario fue registrado correctamente
#         self.users_manager.write.assert_called_once_with(
#             ["user_id", "name", "email", "registration_date"],
#             [
#                 {"user_id": "1", "name": "John Doe", "email": "john@example.com", "registration_date": "01-Jan-2024"},
#                 {"user_id": "2", "name": "Alice", "email": "alice@example.com", "registration_date": "07-Dec-2024"},
#             ]
#         )

#     def test_confirm_user_id(self):
#         """
#         Test para la confirmación del ID de usuario.
#         """
#         # Simular datos existentes
#         self.users_manager.read.return_value = [
#             {"user_id": "1", "name": "John Doe", "email": "john@example.com", "registration_date": "01-Jan-2024"}
#         ]

#         # Simular inputs del usuario
#         self.view.get_input.side_effect = ["1", "sí"]

#         # Ejecutar la función
#         user_id = self.users_controller.confirm_user_id()

#         # Verificar que se confirmó correctamente
#         self.assertEqual(user_id, "1")

#     def test_schedule_appointment(self):
#         """
#         Test para la programación de citas médicas.
#         """
#         # Configurar managers y datos
#         appointments_manager = MagicMock(spec=CSVManager)
#         appointments_manager.read.return_value = []
#         user_id = "1"
#         users_controller = MagicMock(spec=UserController)
#         users_controller.confirm_user_id.return_value = user_id
#         view = MagicMock(spec=View)
    
#         # Simular inputs
#         view.get_input.side_effect = [
#             "Dr. Smith",         # doctor
#             "Cardiología",       # specialty
#             "Chequeo general"    # medical_comment
#         ]
    
#         # Instanciar el controlador
#         appointment_controller = AppointmentController(appointments_manager, users_controller, view)
    
#         # Ejecutar la función
#         appointment_controller.schedule_appointment()
    
#         # Verificar que se programó la cita correctamente
#         appointments_manager.write.assert_called_once_with(
#             ["appointment_id", "user_id", "doctor", "specialty", "date", "time", "medical_comment"],
#             [
#                 {
#                     "appointment_id": "1",
#                     "user_id": "1",
#                     "doctor": "Dr. Smith",
#                     "specialty": "Cardiología",
#                     "date": "2024-12-20",
#                     "time": "14:00",
#                     "medical_comment": "Chequeo general",
#                 }
#             ]
#         )
    
            


#     def test_send_notification(self):
#         """
#         Test para enviar notificaciones.
#         """
#         # Configurar managers y datos
#         notifications_manager = MagicMock(spec=CSVManager)
#         notifications_manager.read.return_value = []
#         user_id = "1"
#         users_controller = MagicMock(spec=UserController)
#         users_controller.confirm_user_id.return_value = user_id
#         view = MagicMock(spec=View)

#         # Simular inputs
#         view.get_input.side_effect = ["Recordatorio de cita médica"]

#         # Instanciar el controlador
#         notification_controller = NotificationController(notifications_manager, users_controller, view)

#         # Simular fecha y hora
#         mock_date = datetime(2024, 12, 7, 15, 30)
#         with patch("programa_FINAL_SeniorLife.datetime") as mock_datetime:
#             mock_datetime.now.return_value = mock_date
#             mock_datetime.isoformat.return_value = mock_date.isoformat()

#             # Ejecutar la función
#             notification_controller.send_notification()

#         # Verificar que se envió la notificación correctamente
#         notifications_manager.write.assert_called_once_with(
#             ["notification_id", "user_id", "message", "timestamp"],
#             [
#                 {
#                     "notification_id": "1",
#                     "user_id": "1",
#                     "message": "Recordatorio de cita médica",
#                     "timestamp": mock_date.isoformat(),
#                 }
#             ]
#         )
     

#         #FINS AQUÍ PASSA TOTS ELS TESTS
        
#     def test_create_medical_profile(self):
#         """
#         Test para la creación de un perfil médico.
#         """
#         # Configurar managers y datos
#         profiles_manager = MagicMock(spec=CSVManager)
#         profiles_manager.read.return_value = []
#         user_id = "1"
#         users_controller = MagicMock(spec=UserController)
#         users_controller.confirm_user_id.return_value = user_id
#         view = MagicMock(spec=View)
    
#         # Simular inputs en el orden correcto (sin birth_date aquí)
#         view.get_input.side_effect = [
#             "Femenino",        # gender
#             "O+",              # blood_group
#             "sí",              # allergies
#             "123 Main St.",    # address
#             "555-1234",        # phone
#             "No problemas recientes",  # medical_comment
#             "sí",              # takes_meds
#             "Ibuprofeno",      # medication name
#             "1 semana",        # medication duration
#             "no"               # no más medicamentos
#         ]
    
#         # Simular la entrada directa para `validate_input`
#         with patch("builtins.input", side_effect=["2000-01-01"]):  # Simular solo el birth_date
#             # Instanciar el controlador
#             medical_controller = MedicalProfileController(profiles_manager, users_controller, view)
    
#             # Ejecutar la función
#             medical_controller.create_medical_profile()

#             # Verificar que se creó el perfil médico correctamente
#             profiles_manager.write.assert_called_once_with(
#                 ["user_id", "birth_date", "gender", "blood_group", "allergies", "address", "phone", "medical_comment", "medications"],
#                 [
#                     {
#                         "user_id": "1",
#                         "birth_date": "2000-01-01",
#                         "gender": "Femenino",
#                         "blood_group": "O+",
#                         "allergies": "True",
#                         "address": "123 Main St.",
#                         "phone": "555-1234",
#                         "medical_comment": "No problemas recientes",
#                         "medications": "[{'name': 'Ibuprofeno', 'duration': '1 semana'}]"
#                     }
#                 ]
#             )

    
#     def test_add_iot_device(self):
#         """
#         Test para agregar un dispositivo IoT.
#         """
#         # Configurar managers y datos
#         iot_manager = MagicMock(spec=CSVManager)
#         iot_manager.read.return_value = []
#         user_id = "1"
#         users_controller = MagicMock(spec=UserController)
#         users_controller.confirm_user_id.return_value = user_id
#         view = MagicMock(spec=View)
    
#         # Simular inputs
#         view.get_input.side_effect = [
#             "SmartWatch",       # device name
#             "1234567890",       # serial number
#             "Pulso,Oxígeno",    # constants
#             "60"                # sampling frequency
#         ]
    
#         # Instanciar el controlador
#         iot_controller = IoTDeviceController(iot_manager, MagicMock(), MagicMock(), MagicMock(), users_controller, view)
    
#         # Ejecutar la función
#         iot_controller.add_iot_device()
    
#         # Verificar que se agregó el dispositivo IoT correctamente
#         iot_manager.write.assert_called_once_with(
#             ["user_id", "name", "serial_number", "constants", "sampling_frequency"],
#             [
#                 {
#                     "user_id": "1",
#                     "name": "SmartWatch",
#                     "serial_number": "1234567890",
#                     "constants": ["Pulso", "Oxígeno"],
#                     "sampling_frequency": "60"
#                 }
#             ]
#         )
        
#     def test_view_parameters(self):
#             """
#             Test para visualizar los parámetros de salud.
#             """
#             # Configurar managers y datos
#             parameters_manager = MagicMock(spec=CSVManager)
#             parameters_manager.read.return_value = [
#                 {"user_id": "1", "constant": "Frecuencia cardíaca", "value": "75", "timestamp": "2024-12-07T15:00:00"},
#                 {"user_id": "1", "constant": "Oxígeno en sangre", "value": "98", "timestamp": "2024-12-07T15:10:00"}
#             ]
#             user_id = "1"
#             users_controller = MagicMock(spec=UserController)
#             users_controller.confirm_user_id.return_value = user_id
#             view = MagicMock(spec=View)
    
#             # Instanciar el controlador
#             parameter_controller = ParameterController(parameters_manager, users_controller, view)
    
#             # Ejecutar la función
#             parameter_controller.view_parameters()
    
#             # Verificar que los mensajes se mostraron correctamente
#             view.display_message.assert_any_call("Frecuencia cardíaca: 75")
#             view.display_message.assert_any_call("Oxígeno en sangre: 98")
    
#     def test_manage_social_network(self):
#         """
#         Test per gestionar una xarxa social.
#         """
#         # Configurar managers i dades
#         social_network_manager = MagicMock(spec=CSVManager)
#         social_network_manager.read.return_value = []
#         user_id = "1"
#         users_controller = MagicMock(spec=UserController)
#         users_controller.confirm_user_id.return_value = user_id
#         view = MagicMock(spec=View)
    
#         # Simular només el títol de la xarxa social
#         view.get_input.side_effect = [
#             "Red Familiar"  # Títol de la xarxa social
#         ]
    
#         # Instanciar el controlador
#         social_network_controller = SocialNetworkController(social_network_manager, users_controller, view)
    
#         # Simular data actual
#         mock_date = datetime(2024, 12, 7, 15, 30)
#         with patch("programa_FINAL_SeniorLife.datetime") as mock_datetime, patch(
#             "builtins.input", side_effect=["1"]  # Acció de crear xarxa social
#         ):
#             mock_datetime.now.return_value = mock_date
#             mock_datetime.strftime = datetime.strftime
    
#             # Executar la funció
#             social_network_controller.manage_social_network()
    
#         # Verificar que es va crear correctament la xarxa social
#         social_network_manager.write.assert_called_once_with(
#             ["network_id", "title", "creation_date", "members_count", "members"],
#             [
#                 {
#                     "network_id": "1",
#                     "title": "Red Familiar",
#                     "creation_date": "07-Dec-2024",
#                     "members_count": 0,
#                 }
#             ]
#         )


# # Ejecutar las pruebas
# if __name__ == "__main__":
#     unittest.main()
    
    
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import sys
import os

# Ruta al archivo programa_FINAL_SeniorLife.py
module_dir = r"C:\Users\abell\OneDrive\Documentos\3r_Carrera\Programari\Projecte_programari"
sys.path.append(module_dir)

from programa_FINAL_SeniorLife import (
    format_date, validate_input, is_valid_date, is_valid_time, CSVManager, Factory,
    UserController, AppointmentController, View, MedicalProfileController,
    NotificationController, ParameterController, IoTDeviceController, SocialNetworkController
)


class TestSeniorLife(unittest.TestCase):
    total_score = 0
    max_score = 10  # Nota màxima
    accumulated_score = 0  # Variable global per acumular puntuació
    test_scores = {
        "test_register_user": 2,
        "test_confirm_user_id": 1,
        "test_schedule_appointment": 2,
        "test_send_notification": 1,
        "test_create_medical_profile": 2,
        "test_add_iot_device": 1,
        "test_view_parameters": 0.5,
        "test_manage_social_network": 0.5,
    }

    def setUp(self):
        """
        Configuració inicial per a les proves. Simula un entorn net.
        """
        self.users_manager = MagicMock(spec=CSVManager)
        self.view = MagicMock(spec=View)
        self.users_controller = UserController(self.users_manager, self.view)

    def assert_with_score(self, expected, actual, test_name):
        """
        Compara valors esperats i obtinguts, mostrant resultats i assignant puntuació.
        """
        print(f"\n--- {test_name} ---")
        print(f"Esperat: {expected}")
        print(f"Obtingut: {actual}")
        if expected == actual:
            score = self.test_scores[test_name]
            print(f"✅ Test passat. Puntuació obtinguda: {score}/{self.test_scores[test_name]}")
            TestSeniorLife.accumulated_score += score
        else:
            print(f"❌ Test fallit. Puntuació obtinguda: 0/{self.test_scores[test_name]}")

    @classmethod
    def tearDownClass(cls):
        """
        Mostra la nota final un cop tots els tests han acabat.
        """
        print("\n=== RESULTAT FINAL ===")
        print(f"Puntuació acumulada: {cls.accumulated_score}/{cls.max_score}")
        print(f"Nota final: {(cls.accumulated_score / cls.max_score) * 10:.2f}/10\n")

    def tearDown(self):
        """
        Mostra la puntuació acumulada després de cada test.
        """
        print(f"\nPuntuació acumulada fins ara: {TestSeniorLife.accumulated_score}/{self.max_score}")


    def test_register_user(self):
        self.users_manager.read.return_value = [
            {"user_id": "1", "name": "John Doe", "email": "john@example.com", "registration_date": "01-Jan-2024"}
        ]
        self.view.get_input.side_effect = ["Alice", "alice@example.com"]

        mock_date = datetime(2024, 12, 7, 15, 30)
        with patch("programa_FINAL_SeniorLife.datetime") as mock_datetime:
            mock_datetime.now.return_value = mock_date
            mock_datetime.strftime = datetime.strftime
            self.users_controller.register_user()

        expected = [
            {"user_id": "1", "name": "John Doe", "email": "john@example.com", "registration_date": "01-Jan-2024"},
            {"user_id": "2", "name": "Alice", "email": "alice@example.com", "registration_date": "07-Dec-2024"},
        ]
        actual = self.users_manager.write.call_args[0][1]
        self.assert_with_score(expected, actual, "test_register_user")

    def test_confirm_user_id(self):
        self.users_manager.read.return_value = [
            {"user_id": "1", "name": "John Doe", "email": "john@example.com", "registration_date": "01-Jan-2024"}
        ]
        self.view.get_input.side_effect = ["1", "sí"]
        user_id = self.users_controller.confirm_user_id()
        expected = "1"
        self.assert_with_score(expected, user_id, "test_confirm_user_id")
        
    def test_schedule_appointment(self):
        appointments_manager = MagicMock(spec=CSVManager)
        appointments_manager.read.return_value = []
        user_id = "1"
        users_controller = MagicMock(spec=UserController)
        users_controller.confirm_user_id.return_value = user_id
        view = MagicMock(spec=View)
    
        # Simular inputs sense preguntar per data i hora
        view.get_input.side_effect = [
            "Dr. Smith",       # doctor
            "Cardiología",     # specialty
            "Chequeo general"  # medical_comment
        ]
        
        # Simular data i hora utilitzant mocks
        mock_date = "2024-12-20"
        mock_time = "14:00"
        with patch("programa_FINAL_SeniorLife.validate_input", side_effect=[mock_date, mock_time]):
            appointment_controller = AppointmentController(appointments_manager, users_controller, view)
            appointment_controller.schedule_appointment()
    
        expected = [
            {
                "appointment_id": "1",
                "user_id": "1",
                "doctor": "Dr. Smith",
                "specialty": "Cardiología",
                "date": "2024-12-20",
                "time": "14:00",
                "medical_comment": "Chequeo general",
            }
        ]
        actual = appointments_manager.write.call_args[0][1]
        self.assert_with_score(expected, actual, "test_schedule_appointment")


    def test_send_notification(self):
        notifications_manager = MagicMock(spec=CSVManager)
        notifications_manager.read.return_value = []
        user_id = "1"
        users_controller = MagicMock(spec=UserController)
        users_controller.confirm_user_id.return_value = user_id
        view = MagicMock(spec=View)

        view.get_input.side_effect = ["Recordatorio de cita médica"]

        notification_controller = NotificationController(notifications_manager, users_controller, view)

        mock_date = datetime(2024, 12, 7, 15, 30)
        with patch("programa_FINAL_SeniorLife.datetime") as mock_datetime:
            mock_datetime.now.return_value = mock_date
            mock_datetime.isoformat.return_value = mock_date.isoformat()
            notification_controller.send_notification()

        expected = [
            {
                "notification_id": "1",
                "user_id": "1",
                "message": "Recordatorio de cita médica",
                "timestamp": mock_date.isoformat(),
            }
        ]
        actual = notifications_manager.write.call_args[0][1]
        self.assert_with_score(expected, actual, "test_send_notification")
        
        
    def test_create_medical_profile(self):
        """
        Test para la creación de un perfil médico.
        """
        profiles_manager = MagicMock(spec=CSVManager)
        profiles_manager.read.return_value = []
        user_id = "1"
        users_controller = MagicMock(spec=UserController)
        users_controller.confirm_user_id.return_value = user_id
        view = MagicMock(spec=View)
    
        view.get_input.side_effect = [
            "Femenino",  # gender
            "O+",  # blood_group
            "sí",  # allergies
            "123 Main St.",  # address
            "555-1234",  # phone
            "No problemas recientes",  # medical_comment
            "sí",  # takes_meds
            "Ibuprofeno",  # medication name
            "1 semana",  # medication duration
            "no"  # no más medicamentos
        ]
    
        with patch("builtins.input", side_effect=["2000-01-01"]):  # Simular solo el birth_date
            medical_controller = MedicalProfileController(profiles_manager, users_controller, view)
            medical_controller.create_medical_profile()
    
        expected = [
            {
                "user_id": "1",
                "birth_date": "2000-01-01",
                "gender": "Femenino",
                "blood_group": "O+",
                "allergies": "True",
                "address": "123 Main St.",
                "phone": "555-1234",
                "medical_comment": "No problemas recientes",
                "medications": "[{'name': 'Ibuprofeno', 'duration': '1 semana'}]"
            }
        ]
        actual = profiles_manager.write.call_args[0][1]
        self.assert_with_score(expected, actual, "test_create_medical_profile")
    
    
    def test_add_iot_device(self):
        """
        Test para agregar un dispositivo IoT.
        """
        iot_manager = MagicMock(spec=CSVManager)
        iot_manager.read.return_value = []
        user_id = "1"
        users_controller = MagicMock(spec=UserController)
        users_controller.confirm_user_id.return_value = user_id
        view = MagicMock(spec=View)
    
        view.get_input.side_effect = [
            "SmartWatch",  # device name
            "1234567890",  # serial number
            "Pulso,Oxígeno",  # constants
            "60"  # sampling frequency
        ]
    
        iot_controller = IoTDeviceController(iot_manager, MagicMock(), MagicMock(), MagicMock(), users_controller, view)
        iot_controller.add_iot_device()
    
        expected = [
            {
                "user_id": "1",
                "name": "SmartWatch",
                "serial_number": "1234567890",
                "constants": ["Pulso", "Oxígeno"],
                "sampling_frequency": "60"
            }
        ]
        actual = iot_manager.write.call_args[0][1]
        self.assert_with_score(expected, actual, "test_add_iot_device")
    
    
    def test_view_parameters(self):
        """
        Test para visualizar los parámetros de salud.
        """
        parameters_manager = MagicMock(spec=CSVManager)
        parameters_manager.read.return_value = [
            {"user_id": "1", "constant": "Frecuencia cardíaca", "value": "75", "timestamp": "2024-12-07T15:00:00"},
            {"user_id": "1", "constant": "Oxígeno en sangre", "value": "98", "timestamp": "2024-12-07T15:10:00"}
        ]
        user_id = "1"
        users_controller = MagicMock(spec=UserController)
        users_controller.confirm_user_id.return_value = user_id
        view = MagicMock(spec=View)
    
        parameter_controller = ParameterController(parameters_manager, users_controller, view)
        parameter_controller.view_parameters()
    
        # Filtrar solo los mensajes relevantes
        actual_messages = [
            msg for msg in [call[0][0] for call in view.display_message.call_args_list]
            if not msg.startswith("\n--- VEURE PARÀMETRES DE SALUT ---")
        ]
        expected_messages = [
            "Frecuencia cardíaca: 75",
            "Oxígeno en sangre: 98"
        ]
        self.assert_with_score(expected_messages, actual_messages, "test_view_parameters")
    
        
    
    def test_manage_social_network(self):
        """
        Test per gestionar una xarxa social.
        """
        social_network_manager = MagicMock(spec=CSVManager)
        social_network_manager.read.return_value = []
        user_id = "1"
        users_controller = MagicMock(spec=UserController)
        users_controller.confirm_user_id.return_value = user_id
        view = MagicMock(spec=View)
    
        view.get_input.side_effect = ["Red Familiar"]  # Títol de la xarxa social
    
        social_network_controller = SocialNetworkController(social_network_manager, users_controller, view)
    
        mock_date = datetime(2024, 12, 7, 15, 30)
        with patch("programa_FINAL_SeniorLife.datetime") as mock_datetime, patch(
            "builtins.input", side_effect=["1"]  # Acció de crear xarxa social
        ):
            mock_datetime.now.return_value = mock_date
            mock_datetime.strftime = datetime.strftime
            social_network_controller.manage_social_network()
    
        expected = [
            {
                "network_id": "1",
                "title": "Red Familiar",
                "creation_date": "07-Dec-2024",
                "members_count": 0,
            }
        ]
        actual = social_network_manager.write.call_args[0][1]
        self.assert_with_score(expected, actual, "test_manage_social_network")
    


# Ejecutar las pruebas
if __name__ == "__main__":
    unittest.main()
