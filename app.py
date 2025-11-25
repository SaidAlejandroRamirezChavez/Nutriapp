from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "cambiar_por_una_clave_secreta_en_produccion"

@app.route("/")
def index():
    return render_template("inicio.html")

@app.route("/registro")
def registro():
    return render_template("Registro.html")

@app.route("/verificacion", methods=["GET", "POST"])
def verificacion():
    contraseña = request.form.get("contraseña")
    confirmar = request.form.get("confirmar")
    edad = request.form.get("edad")
    nombre = request.form.get("nombre")
    apellidos = request.form.get("apellidos")
    altura = request.form.get("altura")
    peso = request.form.get("peso")
    actividad = request.form.get("actividad")
    objetivo = request.form.get("objetivo")
    alergias = request.form.get("alergias")
    alimentacion = request.form.get("alimentacion")
    intolerancias = request.form.get("intolerancias")



    if contraseña != confirmar:
        error_message = "Las contraseñas no coinciden. Por favor, inténtalo de nuevo."
        return render_template("Registro.html", error=error_message)
    else:
        session['nombre'] = nombre
        session['apellidos'] = apellidos
        session['edad'] = edad
        session['altura'] = altura
        session['peso'] = peso
        session['actividad'] = actividad
        session['objetivo'] = objetivo
        session['alergias'] = alergias
        session['alimentacion'] = alimentacion
        session['intolerancias'] = intolerancias

        return redirect(url_for('perfil'))



@app.route("/perfil" , methods=["GET", "POST"])
def perfil():
    nombre = session.get('nombre')
    apellidos = session.get('apellidos')
    edad = session.get('edad')
    altura = session.get('altura')
    peso = session.get('peso')
    actividad = session.get('actividad')
    objetivo = session.get('objetivo')
    alergias = session.get('alergias')
    alimentacion = session.get('alimentacion')
    intolerancias = session.get('intolerancias')

    return render_template("perfil.html", nombre=nombre, apellidos=apellidos,
                           edad=edad, altura=altura, peso=peso, actividad=actividad,
                           objetivo=objetivo, alergias=alergias,
                           alimentacion=alimentacion, intolerancias=intolerancias)

@app.route("/educacion")
def Educacion():    
    return render_template("Educacion.html")

@app.route("/herramientas", methods=["GET", "POST"]) 
def Herramientas():   
    return render_template("Herramientas.html") 


if __name__ == "__main__":
    app.run(debug = True)
