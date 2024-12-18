from src.vectordb_utils import import_csv_to_vector
import config

# Entry point
if __name__ == "__main__":
    import_csv_to_vector(f"{config.SOURCE}/info.csv")