from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import requests


# Define the configuration for the Chatbot
# Replace the placeholder values with your own email, password, and/or session token
config = {
  "session_token":
  "eyJhb2fuV2KvwtQ"
}

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Get the length of the request body
        content_length = int(self.headers['Content-Length'])
        
        # Read the request body
        body = self.rfile.read(content_length)
        
        # Handle the webhook
        self.handle_webhook(body)
        
        # Send a response
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Received POST request")


    def handle_webhook(self, body):
        # Decode the request body
        data = body.decode('utf-8')


        print("Received POST request")

        # Parse the data as a JSON object
        data = json.loads(data)  

        # Extract the pull request information from the data
        pull_request = data['pull_request']

        # Create the modified files array
        modified_files = self.create_modified_files_array(pull_request)

        print(modified_files)

    
        return modified_files

    def create_modified_files_array(self, pull_request):
        # Initialize the modified files array
        modified_files = []

        # Get the URL of the patch file for the pull request
        patch_url = pull_request['patch_url']
        print ("patch_url: " + patch_url)

        # Use the patch URL to retrieve the patch file containing the changes made by the pull request
        patch_file = requests.get(patch_url)

        # Parse the patch file to extract the list of modified files
        for line in patch_file.text.split('\n'):
          # Check if the line represents a modified file
          if line.startswith('+++ b/'):
            # Extract the file name from the line
            file_name = line[6:]
            print("file_name: " + file_name)

            # Retrieve the full code of the file from the pull request
            file_code = requests.get(pull_request['url'] + '/files/' + file_name)

            # Add the file code to the modified files array
            modified_files.append(file_code)

httpd = HTTPServer(('localhost', 8000), RequestHandler)
httpd.serve_forever()
