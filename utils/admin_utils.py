import os
from dotenv import load_dotenv

load_dotenv()

ADMIN_IDS = [int(admin_id) for admin_id in os.getenv('ADMIN_IDS').split(',')]

def is_admin(user_id):
    return user_id in ADMIN_IDS
