import asyncio
import os
import azure.identity
import datetime as date

from data_medical import Database , Generate_Report
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI, AsyncOpenAI, AzureOpenAI
from semantic_kernel import Kernel , exceptions
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
    - Si el paciente quiere saber los medicos que hay en el consultorio usa la herramienta query_data_medicos para saber el nombre y apellidos de los medicos y query_data_especialidad para saber los id de las especialidades de cada medico. Solo di los nombres de los médicos y sus especialidades.
    - Para Agendar hora, preguntar los síntomas al paciente, y con la herramienta query_data_especialidad busca la mejor especialidad que concuerde con sus síntomas, si no hay conincidencias, muestrale al paciente la lista de los medicos disponibles y pregunta a quien quiere pedir la hora. Busca al medico con la herramienta query_data_medico_especialidad mediante la especialidad si es que no tienes el nombre.
    - Para elegir el horario consulta si el paciente puede el dia de hoy Fecha: {date_now.year}-{date_now.month}-{date_now.day} hora: {date_now.hour}{date_now.minute}, si son mas de las de las 17:30 solicita otro horario, si no puede que el paciente diga un dia de esta semana. 
    - Para elegir la hora de la consulta usa la herramienta available_cita con el nombre del medico para saber las horas dispobibles, y precentacelo al paciente mediaante el formato horas mañana y horas Tarde. Una vez que el paciente elija dia y hora agendar la cita con estos datos usa la herramienta send_data_cita para agendar una cita medica. Luego con la herramienta generate_report genera un reporte pdf con los datos de la cita medica.
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
    # Create a chat history for the agent
    print("¡Hola! Soy un recepcionista virtual. ¿En qué puedo ayudarte hoy? Puedo agendar horas médicas para ti o brindarte información sobre los médicos del consultorio.")
    while True:
        thread : ChatHistoryAgentThread = ChatHistoryAgentThread()
        # Get user input
        user_message = input("\nUsuario > ")
        if "bye" in user_message.lower():
            print("¡De nada! Espero haber sido de ayuda. Si necesitas algo más en el futuro, no dudes en escribirme. Que tengas un excelente día y cuídate mucho. ¡Hasta pronto! 😊")
            break
        try:
            respuesta = await main_agent.get_response(messages= user_message, thread=thread)
            print(f"\n -- {respuesta.content}")
        except exceptions.service_exceptions.ServiceResponseException:
            print(f"Limite de promts alcanzado :c") #If you see this, help me continue developing ^^ https://www.paypal.com/donate/?hosted_button_id=C7ZS9EPYWTVV4
            break
        except Exception as e:
            print(f"Excepcion {e}")

    
if __name__ == "__main__":                
    asyncio.run(main())