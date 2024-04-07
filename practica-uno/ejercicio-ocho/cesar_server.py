from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib import parse as urlparse

messages = []

class HTTPResponseHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode("utf-8"))

class MessageService:
    @staticmethod
    def encrypt_message(message):
        message = message.lower()
        new_message = ""
        for char in message:
            if char.isalpha():
                ascii_code = ord(char)
                ascii_code = (ascii_code - 97 + 3) % 26 + 97
                new_message += chr(ascii_code)
            else:
                new_message += char
        return new_message
    
    @staticmethod
    def create_message(data):
        content = data.get("content", "")
        encrypted_content = MessageService.encrypt_message(content)
        message = {
            "id" : len(messages)+1,
            "content": content,
            "encrypted_content": encrypted_content
        }
        messages.append(message)
        return messages

    @staticmethod
    def list_messages():
        return messages

    @staticmethod
    def find_message_id(message_id):
        for message in messages:
            if message["id"] == message_id:
                return message
        return None

    @staticmethod
    def update_message(message_id, data):
        message = MessageService.find_message_id(message_id)
        if message:
            content = data.get("content", "")
            encrypted_content = MessageService.encrypt_message(content)
            message["content"] = content
            message["encrypted_content"] = encrypted_content
            return message
        return None

    @staticmethod
    def delete_message(message_id):
        for message in messages:
            if message["id"] == message_id:
                messages.remove(message)
                return messages
        return None

class RESTRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        query_params = urlparse.parse_qs(parsed_path.query)

        if parsed_path.path == "/messages":
            HTTPResponseHandler.handle_response(self, 200, MessageService.list_messages())
        elif self.path.startswith("/messages/"):
            message_id = int(self.path.split("/")[-1])
            message = MessageService.find_message_id(message_id)
            if message:
                HTTPResponseHandler.handle_response(self, 200, message)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"error": "Message not found"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"error": "Path not found"})

    def do_POST(self):
        if self.path == "/messages":
            data = self.read_data()
            message = MessageService.create_message(data)
            HTTPResponseHandler.handle_response(self, 201, message)
        else:
            HTTPResponseHandler.handle_response(self, 404, {"error": "Path not found"})

    def do_PUT(self):
        if self.path.startswith("/messages/"):            
            message_id = int(self.path.split("/")[-1])
            data = self.read_data()
            messages = MessageService.update_message(message_id, data)
            if messages:
                HTTPResponseHandler.handle_response(self, 200, messages)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"error": "Message not found"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"error": "Path not found"})

    def do_DELETE(self):
        if self.path.startswith("/messages/"):
            message_id = int(self.path.split("/")[-1])
            messages = MessageService.delete_message(message_id)
            if messages:
                HTTPResponseHandler.handle_response(self, 200, messages)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"error": "Message not found"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"error": "Path not found"})

    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data

def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f"Starting web server at http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down the web server...")
        httpd.server_close()
        print("Web server stopped.")

if __name__ == "__main__":
    run_server()
