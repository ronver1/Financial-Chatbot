# Author: Ronit Verma
# Created on: 6.26.26

# This file is creates the supabase client for other files to invoke

from dotenv import load_dotenv
import os
from supabase import create_client as supabase_create_client

load_dotenv()

url = os.environ["SUPABASE_URL"]
key = os.environ["SUPABASE_SERVICE_KEY"]
supabase = supabase_create_client(url, key)

