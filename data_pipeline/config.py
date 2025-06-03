import os

from dotenv import load_dotenv


load_dotenv()

hostname=os.getenv("HOST")
username=os.getenv("USER")
password=os.getenv("PASSWORD")
database=os.getenv("DATABASE")