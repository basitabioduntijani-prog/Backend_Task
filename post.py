from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Sample in-memory data
data = [
    {
        "name": "Sam Lary",
        "track": "AI Developer"
    }
]

# Define request handler
class BasicAPI(BaseHTTPRequestHandler):
    def send_data(self, data, status=200):
        """Helper function to send JSON responses"""
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    # GET - return all data
    def do_GET(self):
        self.send_data(data)

    # POST - receive and add new data
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        try:
            new_item = json.loads(body)
            data.append(new_item)
            self.send_data({"message": "Data added successfully", "data": new_item}, 201)
        except json.JSONDecodeError:
            self.send_data({"error": "Invalid JSON format"}, 400)


# Run the server
def run():
    server_address = ('localhost', 8000)
    httpd = HTTPServer(server_address, BasicAPI)
    print("✅ POST API running on http://localhost:8000")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
