from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Sample in-memory data
data = [
    {"id": 1, "name": "Sam Lary", "track": "AI Developer"},
    {"id": 2, "name": "Basit Tijani", "track": "Backend Developer"}
]

class BasicAPI(BaseHTTPRequestHandler):
    def send_data(self, data, status=200):
        """Send JSON responses"""
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    # GET - Return all data
    def do_GET(self):
        self.send_data(data)

    # PUT - Update an existing record by ID
    def do_PUT(self):
        try:
            # Extract ID from URL path (e.g., /users/2)
            path_parts = self.path.strip('/').split('/')
            if len(path_parts) != 2 or path_parts[0] != "users":
                self.send_data({"error": "Invalid URL format. Use /users/<id>"}, 400)
                return

            user_id = int(path_parts[1])

            # Read and parse the request body
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            updated_data = json.loads(body)

            # Find the user by ID
            user = next((u for u in data if u["id"] == user_id), None)
            if not user:
                self.send_data({"error": "User not found"}, 404)
                return

            # Replace existing user data (full update)
            user.update(updated_data)
            self.send_data({"message": "User updated successfully", "user": user}, 200)

        except json.JSONDecodeError:
            self.send_data({"error": "Invalid JSON format"}, 400)
        except Exception as e:
            self.send_data({"error": str(e)}, 500)


def run():
    server_address = ('localhost', 8000)
    httpd = HTTPServer(server_address, BasicAPI)
    print("✅ PUT API running on http://localhost:8000")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
