from prometheus_client import start_http_server, Summary

# Create a metric to track recommendation latency
REQUEST_TIME = Summary('recommendation_latency_seconds', 'Time spent processing recommendation')

@REQUEST_TIME.time()
def process_recommendation():
    # Recommendation processing logic
    pass

if __name__ == '__main__':
    start_http_server(8000)
    while True:
        process_recommendation()
