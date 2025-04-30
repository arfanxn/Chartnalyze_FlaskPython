import warnings
from app import create_app

warnings.filterwarnings("ignore", message="Using the in-memory storage for tracking rate limits")

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
