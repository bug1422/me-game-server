import os
from app import create_app

env = os.getenv("", "development")
if env == "production":
    from config import ProductionConfig as Config
elif env == "development":
    from config import DevelopmentConfig as Config
else:
    from config import TestingConfig as Config

app = create_app(Config)

if __name__ == "__main__":
    print("My Flask app is running on http://127.0.0.1:5000/apidocs/")
    app.run()
