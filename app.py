from numpy import log as Ln
from numpy import exp as e
from flask import Flask, request, render_template_string

app =Flask(__name__)
# Constantes
V_exp = 1.33e-05
aBA = 194.5302
aAB = -10.7575
rA = 1.4311
rB = 0.92
qA = 1.432
qB = 1.4
lambda_A = 1.127
lambda_B = 0.973
D_AB = 2.1e-5
D_BA = 2.67e-5

def calcul_diffusion(Xa, T):
    if 0 <= Xa <= 1 and T > 0:
        Xb = 1 - Xa
        phiA = (Xa * lambda_A) / (Xa * lambda_A + Xb * lambda_B)
        phiB = (Xb * lambda_B) / (Xa * lambda_A + Xb * lambda_B)
        tauxAB, tauxBA = e(-aAB / T), e(-aBA / T)
        tetaA = (Xa * qA) / (Xa * qA + Xb * qB)
        tetaB = (Xb * qB) / (Xa * qA + Xb * qB)
        tetaAA = tetaA / (tetaA + tetaB * tauxBA)
        tetaBB = tetaB / (tetaB + tetaA * tauxAB)
        tetaAB = (tetaA * tauxAB) / (tetaA * tauxAB + tetaB)
        tetaBA = (tetaB * tauxBA) / (tetaB * tauxBA + tetaA)

        # Calcul des termes
        première_terme = Xb * Ln(D_AB) + Xa * Ln(D_BA) + 2 * (Xa * Ln(Xa / phiA) + Xb * Ln(Xb / phiB))
        deuxième_terme = 2 * Xb * Xa * ((phiA / Xa) * (1 - (lambda_A / lambda_B)) + (phiB / Xb) * (1 - (lambda_B / lambda_A)))
        troisième_terme = Xb * qA * ((1 - (tetaBA) ** 2) * Ln(tauxBA) + (1 - (tetaBB) ** 2) * tauxAB * Ln(tauxAB))
        quatrième_terme = Xa * qB * ((1 - (tetaAB) ** 2) * Ln(tauxAB) + (1 - (tetaAA) ** 2) * tauxBA * Ln(tauxBA))

        # Résultats
        solution1 = première_terme + deuxième_terme + troisième_terme + quatrième_terme
        solution2 = e(solution1)
        erreur = (abs(solution2 - V_exp) / V_exp) * 100
        return solution1,solution2,erreur
    else:
        return None, None, None

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        try:
            Xa = float(request.form["Xa"])
            T = float(request.form["T"])
            lnDab, Dab, erreur = calcul_diffusion(Xa, T)
            if lnDab is not None:
                result = f"""
                    <p><strong>ln(Dab) :</strong> {lnDab:.5f}</p>
                    <p><strong>Dab :</strong> {Dab:.5e}</p>
                    <p><strong>Erreur :</strong> {erreur:.2f} %</p>
                """
            else:
                result = "<p style='color:red;'>Les valeurs de Xa ou T ne sont pas correctes.</p>"
        except ValueError:
            result = "<p style='color:red;'>Veuillez entrer des valeurs numériques valides.</p>"

    return render_template_string("""
        <html>
        <head>
            <title>Calcul de la Diffusion</title>
        </head>
        <body>
            <h2>Calcul de la Diffusion</h2>
            <form method="POST">
                <label for="Xa">Xa (entre 0 et 1) :</label>
                <input type="text" name="Xa" required><br><br>
                <label for="T">Température (K) :</label>
                <input type="text" name="T" required><br><br>
                <button type="submit">Calculer</button>
            </form>
            <br>
            {{ result | safe }}
        </body>
        </html>
    """, result=result)

if __name__ == "__main__":
    app.run(debug=True)

