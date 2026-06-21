# Author: Ronit Verma
# Created on: 6.21.26

# This file is a test to verify a working connection to the Supabase Database

from dotenv import load_dotenv
import os
from supabase import create_client

load_dotenv()

url = os.environ["SUPABASE_URL"]
key = os.environ["SUPABASE_SERVICE_KEY"]
supabase = create_client(url, key)

response = supabase.table("users").insert({
    "username": "testUser",
    "token_hash": "testHash"
}).execute()

response = supabase.table("users").select("*").execute()
print(response.data)

insertedID = response.data[0]["id"]
supabase.table("users").delete().eq("id", insertedID).execute()

response = supabase.table("users").select("*").execute()
print(response.data)