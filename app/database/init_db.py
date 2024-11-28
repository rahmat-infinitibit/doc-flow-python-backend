from app.database.database import Base, engine
from app.models.chat import ChatHistory  # Import the model

def init_database():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_database()
    print("Database initialized successfully!")
