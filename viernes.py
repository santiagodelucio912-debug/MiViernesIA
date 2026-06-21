import os
import asyncio
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai

# Cargar tokens desde las variables de entorno de Render
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Inicializar el cliente oficial de Gemini
client = genai.Client(api_key=GEMINI_API_KEY)

# Mini servidor web para mantener Render gratis
class MockServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Bot activo")

def run_mock_server():
    server = HTTPServer(('0.0.0.0', 10000), MockServer)
    server.serve_forever()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_name = update.effective_user.first_name
    await update.message.reply_text(f"Hola {user_name}, soy Viernes. Sistemas en línea. ¿En qué puedo ayudarte hoy, Señor?")

async def responder_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    
    try:
        # Llamada correcta usando la librería oficial y el modelo recomendado
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
        )
        respuesta_ia = response.text
    except Exception as e:
        respuesta_ia = "Señor, he detectado un problema en mis servidores de procesamiento."
        print(f"Error con la IA: {e}")
        
    await update.message.reply_text(respuesta_ia)

async def main():
    try:
        threading.Thread(target=run_mock_server, daemon=True).start()

        application = Application.builder().token(TELEGRAM_TOKEN).build()
        
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_mensaje))
        
        print("Viernes está encendida y escuchando...")
        
        await application.initialize()
        await application.start()
        await application.updater.start_polling()
        
        while True:
            await asyncio.sleep(1)
            
    except Exception as e:
        print(f"Error al iniciar el bot: {e}")

if __name__ == '__main__':
    asyncio.run(main())