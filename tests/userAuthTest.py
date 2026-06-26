# Author: Ronit Verma
# Created on: 6.26.26

# This file tests the userAuth.py file

from backend.auth.userAuth import userRegister
from database.supabase_client import supabase

tf = userRegister("test")
print(tf)
response = supabase.table("users").select("*").execute()
print(response.data)

tf = userRegister("test")
print(tf)
response = supabase.table("users").select("*").execute()
print(response.data)

tf = userRegister("Testnow")
print(tf)
response = supabase.table("users").select("*").execute()
print(response.data)
