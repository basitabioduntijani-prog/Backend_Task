from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# In-memory sample data
data = [
    {"id": 1, "name": "Sam Lary", "track": "AI Developer"},
    {"id": 2, "name": "Basit Tijani", "track": "Backend Developer"},
    {"id": 3, "name": "Aisha Bello", "track": "Frontend Developer"}
]

class BasicAPI(BaseHTTPRequestHandler):
    def send_data(self, data, status=200):
        """Helper to send JSON response"""
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    # GET - Show all records
    def do_GET(self):
        self.send_data(data)

    # DELETE - Remove a user by ID
    def do_DELETE(self):
        try:
            # Extract ID from URL path (/users/<id>)
            path_parts = self.path.strip('/').split('/')
            if len(path_parts) != 2 or path_parts[0] != "users":
                self.send_data({"error": "Invalid URL format. Use /users/<id>"}, 400)
                return

            user_id = int(path_parts[1])

            # Find user by ID
            global data
            user = next((u for u in data if u["id"] == user_id), None)

            if not user:
                self.send_data({"error": "User not found"}, 404)
                return

            # Remove the user
            data = [u for u in data if u["id"] != user_id]
            self.send_data({"message": f"User with ID {user_id} deleted successfully"}, 200)

        except ValueError:
            self.send_data({"error": "Invalid ID format. Use a number."}, 400)
        except Exception as e:
            self.send_data({"error": str(e)}, 500)


def run():
    server_address = ('localhost', 8000)
    httpd = HTTPServer(server_address, BasicAPI)
    print("✅ DELETE API running on http://localhost:8000")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
