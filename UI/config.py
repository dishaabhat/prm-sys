import os
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")

AWS_ACCESS_KEY = os.getenv("S3_AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("S3_AWS_SECRET_KEY")

USER_POOL_ID = os.getenv("USER_POOL_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")