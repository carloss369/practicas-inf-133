from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs

patients = [
    {
        "id": 2487566,
        "first_name": "Elena",
        "last_name": "Gómez",
        "age": 30,
        "gender": "Femenino",
        "diagnosis": "Resfriado",
        "physician": "Dr. Roberto Martínez", 
    },
    {
        "id": 664559,
        "first_name": "Juan",
        "last_name": "Sánchez",
        "age": 45,
        "gender": "Masculino",
        "diagnosis": "Artritis",
        "physician": "Dra. María López",
    },    
    {
        "id": 8464559,
        "first_name": "Laura",
        "last_name": "Martínez",
        "age": 25,
        "gender": "Femenino",
        "diagnosis": "Diabetes",
        "physician": "Dr. Pedro González",
    }, 
]

class Patient:
    def __init__(self):
        self.id = None
        self.first_name = None
        self.last_name = None
        self.age = None
        self.gender = None
        self.diagnosis = None
        self.physician = None
    
    def __str__(self):
        return f"Patient, id: {self.id}, first_name: {self.first_name}, last_name: {self.last_name}, age: {self.age}, gender: {self.gender}, diagnosis: {self.diagnosis}, physician: {self.physician}"
                    
class PatientBuilder:
    def __init__(self):
        self.patient = Patient()
        
    def set_id(self, id):
        self.patient.id = id
        
    def set_first_name(self, first_name):
        self.patient.first_name = first_name
        
    def set_last_name(self, last_name):
        self.patient.last_name = last_name
    
    def set_age(self, age):
        self.patient.age = age
    
    def set_gender(self, gender):
        self.patient.gender = gender
        
    def set_diagnosis(self, diagnosis):
        self.patient.diagnosis = diagnosis
    
    def set_physician(self, physician):
        self.patient.physician = physician
        
    def get_patient(self):
        return self.patient
        
class Hospital:
    def __init__(self, builder):
        self.builder = builder
    
    def create_patient(self, id, first_name, last_name, age, gender, diagnosis, physician):
        self.builder.set_id(id)
        self.builder.set_first_name(first_name)
        self.builder.set_last_name(last_name)
        self.builder.set_age(age)
        self.builder.set_gender(gender)
        self.builder.set_diagnosis(diagnosis)
        self.builder.set_physician(physician)
        
        return self.builder.get_patient()

class PatientService:
    def __init__(self):
        self.builder = PatientBuilder()
        self.hospital = Hospital(self.builder)
        self.patients = patients
        
    def create_patient(self, post_data):
        id = post_data.get('id', None)
        first_name = post_data.get('first_name', None)
        last_name = post_data.get('last_name', None)
        age = post_data.get('age', None)
        gender = post_data.get('gender', None)
        diagnosis = post_data.get('diagnosis', None)
        physician = post_data.get('physician', None)
        
        patient = self.hospital.create_patient(id, first_name, last_name, age, gender, diagnosis, physician)
        self.patients.append(patient.__dict__)

        return patient
    
    def read_patient(self):
        return patients
    
    def read_patient_id(self, id):
        for patient in self.patients:
            if patient["id"] == id:
                return patient
        return None
    
    def read_patients_by_diagnosis(self, diagnosis):
        return [patient for patient in self.patients if patient['diagnosis'] == diagnosis]
    
    def read_patients_by_physician(self, physician):
        return [patient for patient in self.patients if patient['physician'] == physician]
    
    def update_patient(self, id, post_data):
        for patient in self.patients:
            if patient["id"] == id:
                patient.update(post_data)
                return patient
        return None
    
    def delete_patient(self, id):
        for patient in self.patients:
            if patient["id"] == id:
                self.patients.remove(patient)
                return patient
        return None

class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))
        
    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers['Content-Length'])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode('utf-8'))
    
class PatientHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.controller = PatientService()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        # Create a patient
        if self.path == "/patients":
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.controller.create_patient(data)
            HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Path not found"})

    def do_GET(self):
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        
        # List all patients
        if self.path == "/patients":
            response_data = self.controller.read_patient()
            HTTPDataHandler.handle_response(self, 200, response_data)
        
        # List patients with specific diagnosis
        elif self.path.startswith("/patients") and "diagnosis" in query_params:            
            diagnosis = query_params["diagnosis"][0]
            patients_diabetes = self.controller.read_patients_by_diagnosis(diagnosis)                
            if patients_diabetes:
                HTTPDataHandler.handle_response(self, 200, patients_diabetes)
            else:
                HTTPDataHandler.handle_response(self, 204, [])
        
        # List patients attended by a specific physician
        elif self.path.startswith("/patients") and "physician" in query_params:            
            physician = query_params['physician'][0]
            patients_doctor = self.controller.read_patients_by_physician(physician)                
            HTTPDataHandler.handle_response(self, 200, patients_doctor)            
        
        # Search patients by ID
        elif self.path.startswith("/patients/"):            
            id = int(self.path.split("/")[-1])
            response_data = self.controller.read_patient_id(id)
            HTTPDataHandler.handle_response(self, 200, response_data)
        
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Path not found"})

    def do_PUT(self):
        # Update patient information
        if self.path.startswith("/patients/"):
            index = int(self.path.split("/")[2])
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.controller.update_patient(index, data)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data)
            else:
                HTTPDataHandler.handle_response(self, 404, {"Error": "Invalid patient index"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Path not found"})

    def do_DELETE(self):
        # Delete a patient
        if self.path.startswith("/patients/"):
            index = int(self.path.split("/")[2])
            deleted_patient = self.controller.delete_patient(index)
            if deleted_patient:
                HTTPDataHandler.handle_response(self, 200, {"message": "Patient deleted successfully"})
            else:
                HTTPDataHandler.handle_response(self, 404, {"Error": "Invalid patient index"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Path not found"})


def run(server_class=HTTPServer, handler_class=PatientHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting HTTP server on port {port}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping HTTP server...")
        httpd.server_close()
        print("Server stopped successfully.")

if __name__ == "__main__":
    run()
