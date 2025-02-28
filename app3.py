from flask import Flask,request,render_template_string

app3=Flask(__name__)

def calcule(x):
    if type(x) == int :
     for i in range(1,x):
        x=i*x
    return x
@app3.route("/",methods=["GET","POST"])
def index():
  result=""
  if request.method == "POST":
    x=int(request.form["x"])
    y=calcule(x)
    result=f"<p>le factorielle de {x} est: {y} </p>"

  return render_template_string("""
    <html>
        <head>
            <title>calcule de factorielle</title>
        </head>
        <body>
        <h2>Calcul factorielle</h2>
         <form method="POST">
            <label for="x">x :</label>
            <input type="text" name="x" required><br><br>
            <button type="submit">Calculer</button>
         </form>
         <br>
         {{ result | safe }}
        </body>
    </html>""" ,result=result)

if __name__ == "__main__":
    app3.run(debug=True)

