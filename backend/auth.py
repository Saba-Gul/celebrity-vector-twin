from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Get the Supabase URL and Key from the environment
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Check if the variables were loaded
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in the environment variables")

from supabase import create_client

# Set up Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def verify_user(token):
    user = supabase.auth.get_user(token)
    return user is not None
