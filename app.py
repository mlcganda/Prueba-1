from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)
app.config['DEBUG'] = True  # Habilita el modo depuración

# Cargar la base de datos
df = pd.read_csv('Compuestos.csv')

# Función para buscar una fórmula
def buscar_formula(formula):
    resultados = df[df['Formula'] == formula]
    return resultados if not resultados.empty else None

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para la búsqueda
@app.route('/buscar', methods=['POST'])
def buscar():
    try:
        formula = request.form['formula']  # Recibe la fórmula ingresada
        resultados = buscar_formula(formula)

        if resultados is not None:
            return render_template('resultado.html', formula=formula, resultados=resultados.to_html())
        else:
            return render_template('resultado.html', formula=formula, error="Fórmula no encontrada")
    except Exception as e:
        return f"Error interno: {str(e)}", 500  # Muestra el error en pantalla

# Ejecutar en local
if __name__ == '__main__':
    app.run(debug=True)
