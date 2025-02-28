from flask import Flask,request,render_template_string

app2= Flask(__name__)

@app2.route("/")
def index():
    return "hello world"

if __name__ == "__main__":
    app2.run(debug=True)
