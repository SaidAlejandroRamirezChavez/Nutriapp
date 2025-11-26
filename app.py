
from flask import Flask, render_template, request, redirect, url_for, session
import os
import requests

app = Flask(__name__)

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

@app.route("/resultados", methods=["GET", "POST"])
def Resultados():

    if request.method == "POST":
        form = request.form

        kg_imc = form.get("kgIMC") or form.get("kg")
        m_imc = form.get("mIMC") or form.get("m")


        kg_tmb = form.get("kgtmb") or form.get("kg") or form.get("peso")
        cm_tmb = form.get("mtmb") or form.get("cm") or form.get("estatura")
        años_tmb = form.get("añostmb") or form.get("sñostmb") or form.get("edad")
        sexo = form.get("sexo")

        if kg_imc and m_imc:
            try:
                peso = float(kg_imc)
                estatura = float(m_imc)
                if estatura > 10:
                    estatura = estatura / 100
                imc = round(peso / (estatura ** 2), 2)


                if imc < 18.5:
                    categoria = 'Bajo peso'
                elif imc < 25:
                    categoria = 'Normal'
                elif imc < 30:
                    categoria = 'Sobrepeso'
                else:
                    categoria = 'Obesidad'

                # Compute simple 'peso ideal' using BMI target = 22
                try:
                    peso_ideal = round(22 * (estatura ** 2), 1)
                except Exception:
                    peso_ideal = None

                return render_template("Resultados.html", imc=imc, categoria=categoria, peso_ideal=peso_ideal)
            except (TypeError, ValueError, ZeroDivisionError):
                error_message = "Valores inválidos para IMC."
                return render_template("Herramientas.html", error=error_message)

        if kg_tmb and cm_tmb and años_tmb:
            try:
                peso = float(kg_tmb)
                altura_cm = float(cm_tmb)
                edad = float(años_tmb)

                sexo_norm = (sexo or '').lower()
                if sexo_norm.startswith('h') or sexo_norm == 'male':
                    add = 5
                else:
                    add = -161

                tmb = int(round(10 * peso + 6.25 * altura_cm - 5 * edad + add))

                # peso ideal (BMI target 22)
                altura_m = altura_cm / 100.0
                peso_ideal = round(22 * (altura_m ** 2), 1)

                # default maintenance (assume sedentary if no activity provided)
                maintenance = int(round(tmb * 1.2))

                # macros 50% carbs / 20% protein / 30% fat (kcal -> grams)
                kcal = maintenance
                carbs_g = int(round((kcal * 0.5) / 4))
                protein_g = int(round((kcal * 0.2) / 4))
                fat_g = int(round((kcal * 0.3) / 9))

                # also give a protein recommendation per kg (1.6 g/kg)
                protein_per_kg = int(round(1.6 * peso))

                return render_template("Resultados.html", tmb=tmb, peso_ideal=peso_ideal,
                                       mantenimiento=maintenance, carbs_g=carbs_g,
                                       protein_g=protein_g, fat_g=fat_g, protein_per_kg=protein_per_kg)
            except (TypeError, ValueError):
                error_message = "Valores inválidos para TMB."
                return render_template("Herramientas.html", error=error_message)

        # GCT (calorías diarias según actividad) expects 'actGCT' (actividad) and 'kgIMC' field
        act = form.get('actGCT')
        base_tmb = form.get('kgIMC') or form.get('kg') or form.get('tmb')
        if act and base_tmb:
            try:
                tmb_val = float(base_tmb)
                activity = act.strip().lower()
                # activity factors commonly used
                factors = {
                    'sedentario': 1.2,
                    'ligero': 1.375,
                    'moderado': 1.55,
                    'intenso': 1.725,
                    'muy intenso': 1.9,
                    'muy intenso/option>': 1.9
                }
                factor = factors.get(activity, 1.2)
                mantenimiento = int(round(tmb_val * factor))

                # macros based on maintenance calories (50/20/30)
                kcal = mantenimiento
                carbs_g = int(round((kcal * 0.5) / 4))
                protein_g = int(round((kcal * 0.2) / 4))
                fat_g = int(round((kcal * 0.3) / 9))

                return render_template("Resultados.html", gct=mantenimiento, activity=act,
                                       base_tmb=round(tmb_val), carbs_g=carbs_g,
                                       protein_g=protein_g, fat_g=fat_g)
            except (TypeError, ValueError):
                error_message = "Valores inválidos para GCT."
                return render_template("Herramientas.html", error=error_message)

        return render_template("Herramientas.html", error="Formulario no reconocido. Usa el formulario de la página Herramientas.")

    return redirect(url_for("Herramientas"))



if __name__ == "__main__":
    app.run(debug = True)
