import os
from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer

app = Flask(__name__)

access_token = os.environ["HF_TOKEN"]
model_id = "google/gemma-2b-it"

tokenizer = AutoTokenizer.from_pretrained(model_id, token=os.environ['HF_TOKEN'])
model = AutoModelForCausalLM.from_pretrained(model_id, token=os.environ['HF_TOKEN'])


# Test this api first to make sure docker is running and port is exposed
@app.route('/', methods=['GET'])
def index():
    return 'App is successfully running!'

@app.route('/generate', methods=['POST'])
def generate_text():
    # Get the input text from the request
    input_text = request.json['input_text']

    # Tokenize the input text
    inputs = tokenizer(input_text, return_tensors='pt')

    # Generate text using the model
    outputs = model.generate(**inputs,  max_new_tokens=50)

    # Decode the generated output
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Return the generated text as JSON response
    return jsonify({'generated_text': generated_text})

if __name__ == '__main__':
    app.run(debug=True)
