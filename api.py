from classes.animal import Animal
from classes.field import Field

import csv
import json


from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/api/")
# run the game
def api():
    field = Field(8)
    history = field.play()
    return json.dumps(history)

@app.route("/api/generate-testdata/")
# generate testdata
def generate():
    field = Field(8)
    field.learn()
    return 'Generated!'

@app.route("/api/learn/")
# learn NN
def learn():
    field = Field(8)
    field.go_train()
    return 'Learned!'
