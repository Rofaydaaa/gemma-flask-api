# Quick tutorial on how to dockerize your gemma model for your flutter app
## Overview
In the repository, you can find some resources for the Gemma model consumed in a Flask app, a Dockerfile, and how to access the model endpoint running in the container in a Flutter app. Please note that this is not an end-to-end app but rather a template that you can follow based on your requirements. After:

- Fine-tuning the model and optimizing it
- Choosing your backend framework (you may use something other than Flask)
- Making modifications in the Dockerfile based on the requirements of the backend (you may need to change the base image, the run command, and the entry point)
- Finally, you can change the access point for getting it in Flutter or any other framework like React.

## Table of Contents

- [Get your AI model](#get-your-ai-model)
- [Consume the model in Flask app](#consume-the-model-in-flask-app)
- [Write the Dockerfile](#write-the-dockerfile)
- [Run your container on the suitable server](#run-your-container-on-the-suitable-server)
- [Access the endpoint of the Flask app running in the container](#access-the-endpoint-of-the-flask-app-running-in-the-container)


# Get your AI model

One of the easy way to use your AI model is getting it from Hugging Face and use it with the Transformers library in Python.

### Get Gemma Model from Hugging Face:

- Visit the Hugging Face website (https://huggingface.co/) and search for the Gemma-2B-IT model.

### Grant Access and Obtain Access Token:

- Gemma model requires you to register on the Hugging Face platform and grant access to the Gemma-2B-IT model.
- Obtain an access token from Hugging Face, which will be needed to use the model programmatically.

### Use Transformers Library:

The Transformers library provides easy-to-use interfaces for working with pre-trained models like Gemma-2B-IT.

**You can find my simple code snippet to get you started with Gemma-2B-IT on Google Colab:** [Access it here](https://colab.research.google.com/drive/1yZ79ids-llKBjEZ9e8luF8sIwFDtzKSO)

#### You will also notice the GPU vs CPU Execution Time Differences:

If your laptop doesn't support GPU, running the code on Google Colab with GPU acceleration will significantly reduce execution time compared to running it on a CPU-only environment.
You'll notice the speed difference in model inference and processing tasks.

### Fine-tuning and Optimization:

For real projects, fine-tune the Gemma-2B-IT model based on your specific requirements.
Adjust model prompts, hyperparameters, and optimization techniques to achieve faster and more accurate results for your use case.
The Transformers library in Python simplifies the usage of pre-trained models like Gemma-2B-IT for various natural language processing tasks, including translation, summarization, and more. Experiment with different prompts and configurations to explore the full capabilities of the model.

[You can find a quick overview on how the fine tuning occurs through this tutorial](https://medium.com/@mohammed97ashraf/your-ultimate-guide-to-instinct-fine-tuning-and-optimizing-googles-gemma-2b-using-lora-51ac81467ad2)

# Consume the model in Flask app
Once you have your AI model, check this [simple flask code](https://github.com/Rofaydaaa/gemma-flask-api/blob/master/app.py) to see the how you can make your endpoint

# Write the Dockerfile

You can find my docker image used in the session through this [DockerHub link](https://hub.docker.com/repository/docker/rofayda/gemma-flask/general), or you can get the [dockerfile](https://github.com/Rofaydaaa/gemma-flask-api/blob/master/dockerfile) in the repo, and build the image yourself<br>
#### Prerequisites
- Python
- Docker
### 1- Run the container immediately through my image
 #### Download the rofayda/gemma-flask Docker image to your local machine.
 ```
 docker pull rofayda/gemma-flask
 ```

### 2- Or Build your own image

#### Clone the repository:
```bash
git clone https://github.com/Rofaydaaa/gemma-flask-api
```
#### Navigate to the project directory:

```bash
cd gemma-flask-api
```

#### Create your access_token.txt  and add your hugging face token

#### Build the image

```bash
docker build -t gemma-flask . 
```

# Run your container on the suitable server
Deploy and run your Docker container on a suitable server environment.
## Run the container by the following command
```bash
docker run -d -p 5000:5000 rofayda/gemma-flask 
# '-d': Detached mode, which runs the container in the background.
# '-p' 5000:5000: Maps port 5000 from the container to port 5000 on your host machine, allowing you to access the Flask app running inside the container.
```
Access the application in your browser at http://localhost:5000 or on your server by its IP address.

# Access the endpoint of the Flask app running in the container on your client server

Send Requests: Send HTTP requests to the endpoint using tools like cURL, Postman, or programming languages to interact with the Flask app and receive AI model predictions, on this end point ```\generate```.

In the session I tested the app through a flutter application and here is the main 2 functions for reference.

<details>
<summary>Click to expand and see the code</summary>

```dart
TextEditingController _textController = TextEditingController();
String _responseText = '';
String _testingText = '';

String _url = 'Add your server URL or localhost URL.';
Future<void> _callEndpoint() async {
  String inputText = _textController.text.trim();
  if (inputText.isNotEmpty) {
    Map<String, dynamic> requestBody = {'input_text': inputText};

    String jsonBody = json.encode(requestBody);

    var response = await http.post(
      Uri.parse(_url),
      headers: {
        'Content-Type': 'application/json'
      },
      body: jsonBody,
    );

    if (response.statusCode == 200) {
      Map<String, dynamic> jsonResponse = json.decode(response.body);
      String generateText = jsonResponse['generated_text'];

      setState(() {
        _responseText = generateText;
      });
    } else {
      setState(() {
        _responseText = 'Error: ${response.statusCode} ${response.reasonPhrase}';
      });
    }
  } else {
    setState(() {
      _responseText = 'Please enter some text.';
    });
  }
}

Future<void> _testConnection() async {
  var response = await http.get(
    Uri.parse(_url),
    headers: {'Content-Type': 'application/json'},
  );
  if (response.statusCode == 200) {
    setState(() {
      _testingText = "Connected to flask app!";
    });
  } else {
    setState(() {
      _testingText = 'Error: ${response.statusCode} ${response.reasonPhrase}';
    });
  }
}
```

</details>
