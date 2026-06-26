# Author: Ronit Verma
# Created on: 6.26.26

# This file handles authentication and registration within the database

from supabase import create_client as supabase_create_client
from database.supabase_client import supabase

def userRegister(username) -> bool:
    response = supabase.table("users").select("username").eq("username", username).execute()
    if response.data:
        # print("Username already exists")
        return False
    
    response = supabase.table("users").insert({
        "username": username,
    }).execute()
    return True