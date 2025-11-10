from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("Registro.html")

@app.route("/verificacion", methods=["GET", "POST"])
def verificacion():
    # Leer correctamente los valores enviados por el formulario
    contraseña = request.form.get("contraseña")
    confirmar = request.form.get("confirmar")

    if contraseña != confirmar:
        error_message = "Las contraseñas no coinciden. Por favor, inténtalo de nuevo."
        return render_template("Registro.html", error=error_message)
    else:
        # Redirigir al endpoint /inicio después de un registro/verificación exitosa
        return redirect(url_for('inicio'))



@app.route("/inicio")
def inicio():
    return render_template("inicio.html")  


if __name__ == "__main__":
    app.run(debug = True)
