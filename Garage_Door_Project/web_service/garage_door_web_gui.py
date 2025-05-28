from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return(render_template('web_template.html'))

if __name__ == __name__:
    app.run(host='192.168.30.4', port=9000)