# 🤖 AI Medical Receptionist Agent

### Proyecto desarrollado por **Ricardo Vergara**  
Hackathon de Agentes de IA en Español

---

## 📌 Descripción

Este proyecto presenta un **agente inteligente que actúa como recepcionista virtual para un consultorio médico**. Utiliza procesamiento de lenguaje natural para interactuar con pacientes, gestionar citas médicas y automatizar tareas administrativas.

El agente está diseñado para mejorar la eficiencia en centros de salud, reduciendo la carga operativa del personal y ofreciendo una experiencia más ágil a los pacientes.

---

## 🚀 Funcionalidades Principales

- 🗂️ **Registro de pacientes nuevos** mediante RUT o DNI.
- 🧠 **Recomendación automática de especialidad médica** según los síntomas del paciente.
- 🕒 **Agendamiento de citas médicas** proponiendo el primer horario disponible (por defecto el del día actual).
- 📝 **Generación automática de reportes PDF** con los datos de la cita médica y observaciones.
- 🔎 **Consulta en base de datos** para evitar registros duplicados.

---

## 🛠️ Tecnologías Utilizadas

- **Lenguaje:** Python
- **Framework de IA:** semantic kernel  
- **Frontend:** streamlit   
- **Generación de PDFs: ** FPDF

---

## Running FrontEnd

```shell
# Run 
$ streamlit run main_streamlit.py
```
---

## Running in terminal

```shell
$ python main_agent.py
```

enjoy :D
