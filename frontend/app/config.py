import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BACKEND_ADDRESS = os.getenv("BACKEND_ADDRESS")
BACKEND_PORT = os.getenv("BACKEND_PORT")
PLOUF_BACKEND_URL = f"http://{BACKEND_ADDRESS}:{BACKEND_PORT}"
