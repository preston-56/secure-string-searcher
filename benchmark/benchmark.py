import sys
import time
import os
import threading
import matplotlib.pyplot as plt

# Append the root directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client.client import send_query
from server.server import StringSearchServer
from config.config import read_config

def run_benchmark(file_sizes, num_queries):
    results = {}
    for file_size in file_sizes:
        server = StringSearchServer()
        server_thread = threading.Thread(target=server.run)
        server_thread.start()

        start_time = time.time()
        for _ in range(num_queries):
            with open("/home/code/string-searcher/data/200k.txt", "r") as f:
                lines = f.readlines()
                random_line = lines[0].strip()
            send_query("localhost", server.port, random_line, certfile="server.crt", keyfile="server.key", cafile="ca.crt")
        end_time = time.time()
        

        results[file_size] = end_time - start_time
        server.stop()
        server_thread.join()

    return results

def generate_report(results):
    file_sizes = list(results.keys())
    execution_times = list(results.values())

    plt.figure(figsize=(12, 6))
    plt.plot(file_sizes, execution_times)
    plt.xlabel("File Size (number of lines)")
    plt.ylabel("Execution Time (seconds)")
    plt.title("String Search Performance")
    os.makedirs("benchmark", exist_ok=True)
    plt.savefig("benchmark/report.pdf")

if __name__ == "__main__":
    file_sizes = [10000, 50000, 100000, 150000, 200000]
    num_queries = 1000
    _, port, _, _, _, _, _ = read_config()
    results = run_benchmark(file_sizes, num_queries)
    generate_report(results)