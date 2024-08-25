import aiomysql
from dotenv import load_dotenv
import os

load_dotenv()

async def connect():
    return await aiomysql.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        db=os.getenv("MYSQL_DATABASE")
    )
