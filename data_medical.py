import requests
import os
from pdf_generator import create_pdf

from dotenv import load_dotenv
from semantic_kernel.functions import kernel_function

load_dotenv()
# API Rest testing 
url = "https://web-production-f512.up.railway.app/api/" # URL of the API endpoint 

def send_info(info,direccion,url = url) -> None:
    """ this function sends a post request to the given url with the provided info."""  
    url += f"{direccion}/"
    x = requests.post(url=url, json = info)

    # #POST Validation
    # if x.status_code == 201:
    #     print(f"Send information... {x.status_code}")
    #     return True
    # else:
    #     print(f"informacion no valida {x.status_code}")
    #     return False
    
def query_data(consulta,url = url) -> list:
    """ this function sends a get request to the given url with the provided consulta."""
    url += f"{consulta}"
    return requests.get(url=url).json()

def update_data(info,direccion,url=url) -> list:
    url+=f"{direccion}"
    requests.patch(url=url,json= info)

class Database: 

    """Tools for the receptionist agent."""

    @kernel_function(description="Esta función consulta los datos de los médicos en la base de datos del consultorio")
    def query_data_medicos(self) -> list:
        """
        This function returns the doctors data
        """
        return query_data("medicos/")

    @kernel_function(description="Esta función consulta los medicos segun su especialidad, segun la lista de especialidades de la base de datos")
    def query_data_medico_especialidad(self,especialidad) -> list:
        """
        This function returns a dictionary containing doctors data searched by especialidad_id.
        """
        especialidad_id = query_data(f"especialidades/?search={especialidad}")
        print(f"{especialidad_id[0]["id"]}")
        if not especialidad_id == []:
            return query_data(f"medicos/?search={especialidad_id[0]["id"]}")
        return []
    
    @kernel_function(description="Esta función consulta los datos de los medicos por su nombre")
    def query_data_medico_name(self,name) -> list:
        """
        This function returns a dictionary containing doctors data searched by name.
        """
        return query_data(f"medicos/?search={name}")         
    
    @kernel_function(description="Esta función consulta los datos de las especialidades médicas en la base de datos del consultorio")
    def query_data_especialidad(self) -> list:
        """
        This function returns a dictionary containing medical specialties.
        """
        return query_data("especialidades/")

    @kernel_function(description="Esta funcion consulta los datos de un pacientes mediante su rut o dni en la base de datos del consultorio")
    def query_data_pacientes(self,dni) -> list:
        """
        This function returns a dictionary containing patient data searched by dni.
        """
        return query_data(f"pacientes/?search={dni}")

    @kernel_function(description="Esta funcion consulta los datos de las citas medicas en la base de datos del consultorio")
    def query_data_cita(self) -> list:
        """
        This function returns a dictionary containing patient data.
        """
        return query_data("citas/")
    
    @kernel_function(description="Esta función consulta las citas del paciente mediante su DNI o RUT")
    def query_data_cita_paciente(self,dni)-> list:
        """
        This function returns the patient's appointments using their dni.
        """
        return query_data(f"citas/?search={dni}")
    
    @kernel_function(description="Esta función consulta las citas de cada medico mediante su nombre")
    def query_data_cita_medico(self,name):
        """
        This function returns the doctor's appointments using his or her name.
        """
        return query_data(f"citas/?search={name}")

    @kernel_function(description="Esta funcion envia los datos del paciente a la base de datos")
    def send_data_patient(self,name,last_name,dni,brith_date,email,phone) -> None:
        """
        this function sends the patient data to the database."""

        # Create a dictionary with the patient data
        patient_data = {
            "name": name,
            "last_name": last_name,
            "brith_date": brith_date,
            "dni": dni,
            "phone": phone,
            "email": email
        }
        if send_info(patient_data,"pacientes"):
            print("Datos enviados...")



    @kernel_function(description="Esta funcion envia los datos de la cita medica a la base de datos")
    def send_data_cita(self,fecha_cita,hora_cita,name_medico, dni_paciente,comentario) -> None:
        """
        this function sends the cita data to the database.
        """
        medico_id = self.query_data_medico_name(name_medico)
        print(medico_id)
        paciente_id = self.query_data_pacientes(dni_paciente)
        print(paciente_id)
        cita_data =   {
            "Date": fecha_cita,
            "Time": hora_cita,
            "estado": "PD",
            "comentarios": comentario,
            "paciente_id": paciente_id[0]["id"],
            "medico_id": medico_id[0]["id"]
        }
                    
        send_info(cita_data,"citas")
            

    @kernel_function(description="Esta funcion retorna los horarios que cada medico puede atender vicitas")
    def available_cita(self,name_medico) -> list:
        horas_citas = ["09:30:00","10:00:00","10:30:00","11:00:00","11:30:00","12:00:00","15:00:00","15:30:00","16:00:00","16:30:00","17:00:00","17:30:00"]
        citas_medicas = self.query_data_cita_medico(name_medico)
        horas_medico = [horas['Time'] for horas in citas_medicas]
        available_hours = []
        for hora in horas_citas:
            if not hora in horas_medico:
                available_hours.append(hora)
        return available_hours    

class Generate_Report:
    @kernel_function(description="Esta funcion genera un reporte de la cita del paciente")
    def generate_report(self, name, last_name, email, telefono_paciente, brith_date, fecha_cita, hora_cita, observaciones, medico_name, medico_last_name, medico_email, medico_telefono, medico_especialidad) -> None:
        """
        This function generates a PDF report of the patient's appointment.
        """
        create_pdf(name_paciente=name, last_name_paciente=last_name, email_paciente=email, telefono_paciente=telefono_paciente, brith_date_paciente=brith_date,
                   medico_name=medico_name, medico_last_name=medico_last_name, medico_email=medico_email, medico_telefono=medico_telefono, medico_especialidad=medico_especialidad,hora_cita=hora_cita,fecha_cita=fecha_cita,
                   comentarios=observaciones)


if __name__ == "__main__":
    # Example usage
    paciente = {
        "name": "Eduard",
        "last_name": "Storn",
        "nacimiento": "1992-02-12",
        "rut": "33333333-0",
        "email": "aaa.sss@gmail.com" ,
        "telefono" : "1234567890"
        }
    dni_paciente = "77777777-0"
    name_medico = "Anya"
    #data = Database()
    # doc = Generate_Report()
    # doc.generate_report(name="Ricardo", last_name="Garcia", email="neo.rikr2@gmail.com", telefono_paciente="23443566", brith_date="2 de agosto 1992", fecha_cita="27 de abril 2025", hora_cita="09:30", observaciones="EL paciente esta enfermo", medico_name=name_medico, medico_last_name="ladis", medico_email="kok@gmail.com", medico_telefono="w22222", medico_especialidad="Cardiologo")
    # data.send_data_cita(fecha_cita="2025-05-12",hora_cita="10:30",name_medico=name_medico, dni_paciente=dni_paciente,comentario="----A solicito la hora")    
    