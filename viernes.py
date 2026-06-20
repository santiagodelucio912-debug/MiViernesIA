import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai

# Configuración de registros para ver qué pasa en la terminal
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Tus claves corregidas sin espacios
TELEGRAM_TOKEN = "8968613360:AAERJYHbLZrtuewTUYhMBrAJcyvyNi-51_g"
GEMINI_API_KEY = "AQ.Ab8RN6I8oqMCAPAYIIU4ZBW_P0lBS20NJiL7Onqh_WQ7AFevPQ"

# Inicializar el cliente de Inteligencia Artificial
ai_client = genai.Client(api_key=GEMINI_API_KEY)

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(f"Hola {user.first_name}, soy Viernes. Sistemas en línea. ¿En qué puedo ayudarte hoy, Señor?")

# Función que procesa los mensajes de texto
async def responder_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    mensaje_usuario = update.message.text
    
    prompt_personalidad = (
        "Actúa como Viernes (Friday), la inteligencia artificial asistente de Tony Stark en Marvel. "
        "Eres eficiente, sofisticada y leal. Responde de forma muy concisa en español a lo siguiente: "
    )
    
    try:
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt_personalidad + mensaje_usuario
        )
        respuesta_ia = response.text
    except Exception as e:
        respuesta_ia = "Señor, he detectado un problema en mis servidores de procesamiento."
        print(f"Error con la IA: {e}")

    await update.message.reply_text(respuesta_ia)

def main():
    try:
        # Iniciar la aplicación
        application = Application.builder().token(TELEGRAM_TOKEN).build()

        # Registrar respuestas
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_mensaje))

        print("Viernes está encendida y escuchando...")
        # Arranca el bot y bloquea la terminal para que no se cierre sola
        application.run_polling()
        
    except Exception as e:
        print(f"Error al iniciar el bot: {e}")

if __name__ == '__main__':
    main()