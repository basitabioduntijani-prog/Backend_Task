from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Sample data
data = [
    {
        "name": "Sam Lary",
        "track": "AI Developer"
    }
]

# Define request handler
class BasicAPI(BaseHTTPRequestHandler):
    def send_data(self, data, status=200):
        """Helper function to send JSON response"""
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    # Handle GET requests
    def do_GET(self):
        self.send_data(data)


# Run the server
def run():
    server_address = ('localhost', 8000)
    httpd = HTTPServer(server_address, BasicAPI)
    print("✅ GET API running on http://localhost:8000")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
