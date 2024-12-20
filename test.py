from src.vectordb_utils import import_csv_to_vector
from src.webhook_utils import send_email
import config

# Entry point
if __name__ == "__main__":
    # import_csv_to_vector(f"{config.SOURCE}/info.csv")
    ai = """
        Hello
    """
    send_email("visitor_name", "us", "california", "asdfasdfasdf", ai)