test_local = True
from dotenv import load_dotenv
import os
load_dotenv()
bot_token = os.getenv('BOT_TOKEN')

if test_local:
    api_url = 'http://127.0.0.1:5000' 
else:
    api_url = os.getenv('API_URL')

whitelist = {289988172}