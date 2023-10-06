# Import the hashlib module to calculate MD5 hash
# and Flask for building the web application
import hashlib
import requests
from flask import Flask, request, jsonify

# Create a Flask web application instance
app = Flask(__name__)

# Define a common function to generate the response JSON
def generate_response(input_value, output_value):
    return jsonify({"input": input_value, "output": output_value})

# Define a route for calculating the MD5 hash of an input string
@app.route('/md5/<string:input_string>')
def calculate_md5(input_string):
    # Calculates the MD5 hash
    md5_hash = hashlib.md5(input_string.encode()).hexdigest()
    
    # Return the result as a JSON object
    return generate_response(input_string, md5_hash)

# Define a route for calculating the factorial of a positive integer
@app.route('/factorial/<int:number>')
def calculate_factorial(number):
    # Check if the input number is less than 0 (not a positive integer)
    if number < 0:
        # Return an error response with a 400 status code
        return jsonify({"error": "Input must be a positive integer."}), 400

    # Initialize the factorial result as 1
    factorial_result = 1

    # Calculate the factorial of the input number using a loop
    for i in range(1, number + 1):
        factorial_result *= i

    # Return the result as a JSON object
    return generate_response(number, factorial_result)
#Define a route for fibonacci
@app.route('/fibonacci/<int:number>')
def calculate_fibonacci(number):
    if number < 0:
        return generate_response(number, None, "Input must be a non-negative integer.")

    fibonacci_sequence = []
    a, b = 0, 1
    while a <= number:
        fibonacci_sequence.append(a)
        a, b = b, a + b

    return generate_response(number, fibonacci_sequence)

# Define a route for checking if a number is prime
@app.route('/is-prime/<int:number>')
def check_prime(number):
    # Check if the input number is less than 2 (not prime)
    if number < 2:
        is_prime = False
    else:
        is_prime = True
        
   # This is a prime check sequence I found online. It should work.
        for i in range(2, int(number ** 0.5) + 1):
            if number % i == 0:
                is_prime = False
                break

    # Return the result as a JSON object
    return generate_response(number, is_prime)

@app.route('/slack-alert/<string:message>')
def send_slack_alert(message):
    try:
        slack_url = 'https://hooks.slack.com/services/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'
        payload = {"text": message}
        response = requests.post(slack_url, json=payload)

        if response.status_code == 200:
            return generate_response(message, True)
        else:
            return generate_response(message, False)
    except Exception as e:
        return generate_response(message, False, str(e))

# Start the Flask application on port 4000 when executed directly
if __name__ == '__main__':
    app.run(port=4000)
