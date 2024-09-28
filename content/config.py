from dotenv import load_dotenv
import os

load_dotenv()
PAYMONGO_API_KEY = os.getenv("PAYMONGO_API_KEY")
PAYMONGO_API_URL = "https://api.paymongo.com/v1/links"