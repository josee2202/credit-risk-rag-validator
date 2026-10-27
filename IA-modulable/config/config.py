import os
import yaml
from dotenv import load_dotenv

# Cargar las variables de entorno del archivo .env
load_dotenv()

# Obtener la API key del entorno
groq_api_key = os.getenv("GROQ_API_KEY")

# Descargar la configuración 
with open('./config/config.yaml', 'r') as config_file:
    cfg_param = yaml.safe_load(config_file)