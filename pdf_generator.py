from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'UB', 14)
        self.cell(0, 10, "Reporte de cita medica", 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_pdf(name_paciente, last_name_paciente,telefono_paciente, email_paciente,  brith_date_paciente, fecha_cita, hora_cita, medico_name, medico_last_name, medico_email, medico_telefono, medico_especialidad, comentarios):
    """
    This function creates a PDF file with the doctor and patient data. 
    """
    pdf = PDF(orientation='P', unit='mm',format='A4')
    #Metadata
    pdf.set_title(title="Reporte de Cita médica")
    pdf.set_author(author="Ricardo Vergara")
    pdf.set_creator('Ricardo Vergara')
    pdf.set_keywords(keywords='Cita,médico,paciente,hora,datos,comentarios,fecha')
    pdf.set_subject(subject="datos de cita médica")

    #Create pdf
    pdf.add_page()
    pdf.set_font('Arial','B',10)

    #Title section
    pdf.cell(w=0,h=15,txt="Datos del Paciente:",border='B',align='L',ln=1,fill=0)
    pdf.set_font('Arial','',10)
    #data
    pdf.cell(w=47,h=15,txt='Nombre:',border=0,align='C',fill=0)
    pdf.cell(w=47,h=15,txt=name_paciente,border=0,align='C',fill=0)
    pdf.cell(w=47,h=15,txt='Apellido:',border=0,align='C',fill=0)
    pdf.multi_cell(w=0,h=15,txt=last_name_paciente,border=0,align='C',fill=0)

    pdf.cell(w=47,h=15,txt='Teléfono:',border=0,align='C',fill=0)
    pdf.cell(w=47,h=15,txt=telefono_paciente,border=0,align='C',fill=0)
    pdf.cell(w=47,h=15,txt='Email:',border=0,align='C',fill=0)
    pdf.multi_cell(w=0,h=15,txt=email_paciente,border=0,align='C',fill=0)

    pdf.cell(w=60,h=15,txt='Fecha de nacimiento:',border=0,align='C',fill=0)
    pdf.multi_cell(w=0,h=15,txt=brith_date_paciente,border=0,align='L',fill=0)

    pdf.set_font('Arial','B',10)
    pdf.cell(w=0,h=15,txt="Datos del Médico:",border='B',align='L',ln = 2,fill=0)
    #data medico
    pdf.set_font('Arial','',10)
    pdf.cell(w=47,h=15,txt='Nombre:',border=0,align='C',fill=0)
    pdf.cell(w=47,h=15,txt=medico_name,border=0,align='C',fill=0)
    pdf.cell(w=47,h=15,txt='Apellido:',border=0,align='C',fill=0)
    pdf.multi_cell(w=0,h=15,txt=medico_last_name,border=0,align='C',fill=0)

    pdf.cell(w=47,h=15,txt='Teléfono:',border=0,align='C',fill=0)
    pdf.cell(w=47,h=15,txt=medico_telefono,border=0,align='C',fill=0)
    pdf.cell(w=47,h=15,txt='Email:',border=0,align='C',fill=0)
    pdf.multi_cell(w=0,h=15,txt=medico_email,border=0,align='C',fill=0)

    pdf.cell(w=60,h=15,txt='Especialidad:',border=0,align='C',fill=0)
    pdf.multi_cell(w=0,h=15,txt=medico_especialidad,border=0,align='L',fill=0)

    #Datos de cita medica
    pdf.set_font('Arial','B',10)
    pdf.cell(w=0,h=15,txt="Fecha de la Cita:",border=0,align='L',ln = 3,fill=0)
    pdf.set_font('Arial','',10)
    pdf.cell(w=47,h=15,txt='Fecha:',border=0,align='C',fill=0)
    pdf.cell(w=47,h=15,txt=fecha_cita,border=0,align='C',fill=0)
    pdf.cell(w=47,h=15,txt='Hora:',border=0,align='C',fill=0)
    pdf.multi_cell(w=0,h=15,txt=hora_cita,border=0,align='C',fill=0)

    pdf.set_font('Arial','B',10)
    pdf.cell(w=0,h=15,txt="Comentarios:",border='B',align='L',ln = 3,fill=0)
    pdf.set_font('Arial','',10)
    pdf.multi_cell(w=0,h=60,txt=comentarios,border=1,align='L',fill=0)


    pdf.output(f'./PDF/Reporte_cite_medica_{name_paciente}_{last_name_paciente}.pdf')


if __name__ == '__main__':
    #Example
    #Datos del paciente
    name = "Ricardo"
    last_name = "Gonzalez"
    email = "juna_gonx@gmail.com"
    telefono = "1234567890"
    fecha_nacimiento = "01/01/1990"
    #datos del medicos
    medico_name = "Dr. Pedro"
    medico_last_name = "Pérez"
    medico_email = "Pedo_per@gmail.com"
    medico_telefono = "0987654321"
    medico_especialidad = "Cardiología"
    #datos de la cita
    hora_cita = "10:00"
    fecha_cita = "01/01/2023"
    observaciones = "Paciente con antecedentes de hipertensión. Requiere seguimiento regular."
    
    create_pdf(name_paciente=name,last_name_paciente=last_name,email_paciente=email,telefono_paciente=telefono,brith_date_paciente=fecha_nacimiento,fecha_cita=fecha_cita, hora_cita=hora_cita, medico_name=medico_name, medico_last_name=medico_last_name, medico_email=medico_email, medico_telefono=medico_telefono, medico_especialidad=medico_especialidad, comentarios=observaciones)