import os
from dotenv import load_dotenv
from pymongo import AsyncMongoClient

load_dotenv()

mongo_url = os.getenv("MONGO_URI")
if not mongo_url:
    raise RuntimeError("Mongo url is not configured")

client = AsyncMongoClient(mongo_url)

db = client["nexus"]


async def create_indexs():
    await db.users.create_index("email", unique=True)
