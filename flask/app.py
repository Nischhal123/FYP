from flask import Flask

app = Flask(name)

@app.route('/hello')
def helloIndex():
    return 'Hello World from Python Flask!'

app.run(host='0.0.0.0', port=5000)