import os
import logging


LOG_DIR = 'chat_assistant/logs/'


os.makedirs(LOG_DIR, exist_ok=True)  

logging.basicConfig(
    filename=os.path.join(LOG_DIR, 'app.log'),  
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
