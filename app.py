
from flask import Flask, render_template, request, redirect, url_for, session
import json


app = Flask(__name__)

# Load local secrets from secrets.json (keeps configuration out of source code)
def _load_secrets(path='secrets.json'):
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            return json.load(fh)
    except FileNotFoundError:
        return {}
    except Exception:
        return {}

_SECRETS = _load_secrets()
# Ensure a secret key is set so Flask sessions work
app.secret_key = _SECRETS.get('FLASK_SECRET', 'dev-secret')

@app.route("/")
def index():
    return render_template("inicio.html")

@app.route("/iniciar")
def iniciar():
    return render_template("iniciar.html")


@app.route('/iniciar_sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'GET':
        return render_template('iniciar.html')


    username = (request.form.get('username') or '').strip()
    password = (request.form.get('password') or '').strip()


    registered_name = session.get('nombre')

    if registered_name and username and username == registered_name:
        session['usuario'] = username

        session['registered'] = True
        session['message'] = 'Bienvenido de nuevo, ' + username
        return redirect(url_for('perfil'))

    if username == 'admin' and password == 'secret':
        session['usuario'] = 'admin'
        session['nombre'] = 'admin'

        return redirect(url_for('perfil'))


    error = 'Usuario o contraseña incorrectos. Prueba admin / secret o regístrate primero.'
    return render_template('iniciar.html', error=error)


@app.route('/cerrar_sesion')
def cerrar_sesion():
    session.pop('usuario', None)
    session.pop('registered', None)

    return redirect(url_for('index'))

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


        session['usuario'] = nombre
        session['registered'] = True

        return redirect(url_for('perfil'))



@app.route("/perfil" , methods=["GET", "POST"])
def perfil():

    if not session.get('registered'):

        return redirect(url_for('iniciar'))

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

        form_type = (form.get('form_type') or '').strip().lower()

        kg_imc = form.get("kgIMC") or form.get("kg")
        m_imc = form.get("mIMC") or form.get("m")


        kg_tmb = form.get("kgtmb") or form.get("kg") or form.get("peso")
        cm_tmb = form.get("mtmb") or form.get("cm") or form.get("estatura")
        años_tmb = form.get("añostmb") or form.get("sñostmb") or form.get("edad")
        sexo = form.get("sexo")

        if form_type == 'imc' and kg_imc and m_imc:
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


                return render_template("Resultados.html", form_type='imc', imc=imc, categoria=categoria)
            except (TypeError, ValueError, ZeroDivisionError):
                error_message = "Valores inválidos para IMC."
                return render_template("Herramientas.html", error=error_message)

        if form_type == 'tmb' and kg_tmb and cm_tmb and años_tmb:
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

                return render_template("Resultados.html", form_type='tmb', tmb=tmb)
            except (TypeError, ValueError):
                error_message = "Valores inválidos para TMB."
                return render_template("Herramientas.html", error=error_message)


        act = form.get('actGCT')
        base_tmb = form.get('kgIMC') or form.get('kg') or form.get('tmb')
        if form_type == 'gct' and act and base_tmb:
            try:
                tmb_val = float(base_tmb)
                activity = act.strip().lower()

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
                return render_template("Resultados.html", form_type='gct', gct=mantenimiento, activity=act,
                                       base_tmb=round(tmb_val))
            except (TypeError, ValueError):
                error_message = "Valores inválidos para GCT."
                return render_template("Herramientas.html", error=error_message)

        # peso ideal form
        if form_type == 'peso_ideal':
            m_pi = form.get('mPi')
            try:
                altura_m = float(m_pi)
                if altura_m > 10:  # si se envió en cm
                    altura_m = altura_m / 100.0
                peso_ideal = round(22 * (altura_m ** 2), 1)
                return render_template('Resultados.html', form_type='peso_ideal', peso_ideal=peso_ideal)
            except Exception:
                return render_template('Herramientas.html', error='Altura inválida para calcular peso ideal.')

        # macros form
        if form_type == 'macros':
            tmb_kcal = form.get('tmb_kcal') or form.get('kgIMC')
            goal = form.get('macro_goal') or ''
            try:
                kcal = int(round(float(tmb_kcal)))
                carbs_g = int(round((kcal * 0.5) / 4))
                protein_g = int(round((kcal * 0.2) / 4))
                fat_g = int(round((kcal * 0.3) / 9))
                return render_template('Resultados.html', form_type='macros', kcal=kcal, carbs_g=carbs_g, protein_g=protein_g, fat_g=fat_g, macro_goal=goal)
            except Exception:
                return render_template('Herramientas.html', error='Valor inválido para calcular macronutrientes.')

        return render_template("Herramientas.html", error="Formulario no reconocido. Usa el formulario de la página Herramientas.")

    return redirect(url_for("Herramientas"))



if __name__ == "__main__":
    app.run(debug = True)
