from typing import Tuple
import os


def read_config() -> Tuple[str, int, str, bool, bool, str, str]:
    config_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.ini")
    host = "0.0.0.0"
    port = 44445
    file_path = None
    reread_on_query = False
    ssl_enabled = False
    ssl_cert = ""
    ssl_key = ""

    try:
        with open(config_file, "r") as f:
            lines = f.readlines()

        for line in lines:
            if line.startswith("LINUXPATH="):
                file_path = line.split("=")[1].strip()
            elif line.startswith("REREAD_ON_QUERY="):
                reread_on_query = line.split("=")[1].strip().lower() == "true"
            elif line.startswith("SSL_ENABLED="):
                ssl_enabled = line.split("=")[1].strip().lower() == "true"
            elif line.startswith("SSL_CERT="):
                ssl_cert = line.split("=")[1].strip()
            elif line.startswith("SSL_KEY="):
                ssl_key = line.split("=")[1].strip()
    except FileNotFoundError:
        print(f"Config file {config_file} not found. Using default settings.")
    except Exception as e:
        print(f"Error reading config file {config_file}: {e}")

    return host, port, file_path, reread_on_query, ssl_enabled, ssl_cert, ssl_key