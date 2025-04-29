import asyncio
import os
import azure.identity
import datetime as date
import streamlit as st

from data_medical import Database , Generate_Report
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI, AsyncOpenAI, AzureOpenAI
from semantic_kernel import Kernel , exceptions
from semantic_kernel.contents import ChatHistory
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion 

load_dotenv(override=True)
API_HOST = os.getenv("API_HOST")

# Set up the environment variables for Azure OpenAI Rerpo: https://github.com/Azure-Samples/python-ai-agent-frameworks-demos/tree/main
def create_kernel() -> Kernel:
    """Crea una instancia de Kernel con un servicio."""
    kernel = Kernel()

    if API_HOST == "azure":
        token_provider = azure.identity.get_bearer_token_provider(azure.identity.DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")
        chat_client = AsyncAzureOpenAI(
        api_version=os.environ["AZURE_OPENAI_VERSION"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        azure_ad_token_provider=token_provider,
        )
        chat_completion_service = OpenAIChatCompletion(ai_model_id=os.environ["AZURE_OPENAI_CHAT_MODEL"], async_client=chat_client)
    else:
        chat_client = AsyncOpenAI(api_key=os.environ["GITHUB_TOKEN"], base_url="https://models.inference.ai.azure.com")
        chat_completion_service = OpenAIChatCompletion(ai_model_id=os.getenv("GITHUB_MODEL", "gpt-4o"), async_client=chat_client)
    kernel.add_service(chat_completion_service)
    return kernel


date_now = date.datetime.now()

instructions = f"""
    - Dile que entre tus funciones está el agendar horas médicas y dar información de los médicos del consultorio.
    - Si el paciente quiere saber los médicos que hay en el consultorio, usa la herramienta query_data_medicos para saber el nombre y apellidos de los médicos y query_data_especialidad para saber los id de las especialidades de cada médico. Solo di los nombres de los médicos y sus especialidades.
    - Para Agendar hora, preguntar los síntomas al paciente, y con la herramienta query_data_especialidad busca la mejor especialidad que concuerde con sus síntomas, si no hay coincidencias, muéstrale al paciente la lista de los médicos disponibles. Usa la herramienta query_data_medicos para saber el nombre y apellidos de los médicos y pregunta a quién quiere pedir la hora. Busca al médico con la herramienta query_data_medico_especialidad mediante la especialidad de la base de datos si es que no tienes el nombre.
    - Para elegir el horario consulta, primero consulta al usuario por esta Fecha: {date_now.year}-{date_now.month}-{date_now.day} hora: {date_now.hour}{date_now.minute}, si son más de las de las 17:30 solicita otro horario, si no puede que el paciente diga un día de esta semana. 
    - Para elegir la hora de la consulta, usa la herramienta available_cita con el nombre del médico para saber las horas disponibles, y preséntaselo al paciente mediante el formato horas mañana y horas Tarde. Una vez que el paciente elija día y hora agendar la cita con estos datos, usa la herramienta send_data_cita para agendar una cita médica. Luego con la herramienta generate_report genera un reporte pdf con los datos de la cita médica.
    - Si el paciente quiere agendar hora médica debes pedirle su dni y usar la herramienta query_data_pacientes para buscarlo en la base de datos, si no está, pedirle 
    sus datos que son: Nombre, Apellido, Rut o Dni, Fecha de nacimiento, Teléfono y Email y enviar los datos a la base de datos con la herramienta send_data_patient, siempre trata al paciente por su nombre.
"""

description = """Eres un muy inteligente recepcionista Virtual de un Consultorio Médico. Tu trabajo es ayudar a los pacientes a 
    pedir hora médica recomendando a los médicos del Consultorio. Eres muy empático y amigable."""


kernel = create_kernel()

# Create a Agent with the kernel and the system content
main_agent = ChatCompletionAgent(
kernel=kernel, 
name="receptionist_agent",
description=description,
instructions= instructions,
plugins=[Database(),Generate_Report()]
)


async def main() -> None:

    history = ChatHistory()
    st.set_page_config(page_title="Generador de Citas Medicas", layout= "centered", page_icon="./public/logo_1.png")
    st.title("🤖 Agenda tu cita médica")

    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Escribe un mensaje...."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role":"user","content":prompt})
        if "bye" in prompt.lower():
            st.session_state.messages = []
            history.clear()    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            #agregar historial de mensajes 
            if prompt is not None:
                for message in st.session_state.messages:
                    history.add_message(message)
                thread : ChatHistoryAgentThread = ChatHistoryAgentThread(history)
                stream = await main_agent.get_response(messages= prompt, thread=thread)
                message_placeholder.markdown(str(stream.content))
                st.session_state.messages.append({"role":"assistant","content":str(stream.content)})
        except exceptions.service_exceptions.ServiceResponseException as ex:
            message_placeholder.markdown(f"Limite de prompts alcanzado :c")
            st.exception(f"{ex}") #If you see this, help me continue developing ^^ https://www.paypal.com/donate/?hosted_button_id=C7ZS9EPYWTVV4
        except Exception as e:
            st.exception(f"Excepcion {e}")
            print(f"Excepcion {e}")
    
if __name__ == "__main__":                
    asyncio.run(main())