from flask import Flask, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return "This is the first view of this project <h1> Hi there! </h1>"

@app.route('/<name>')
def user(name):

    if name =='Admin!':
        return "This is the boss Bitch!"
    return f" Helloooo this is {name}!!!"

@app.route('/admin')
def admin():
    return redirect(url_for("home"))

# the same as admin but with the default name
@app.route('/interface')
def interface():
    return redirect(url_for("user", name="Admin!"))

if __name__ == "__main__":
    app.run()