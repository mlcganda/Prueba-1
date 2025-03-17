from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)
app.config['DEBUG'] = True  # Habilita el modo depuración

# Cargar la base de datos correctamente
db_path = os.path.join(os.path.dirname(__file__), 'Compuestos.csv')

try:
    df = pd.read_csv(db_path)  # Intenta cargar la base de datos
except FileNotFoundError:
    df = None
    print("⚠️ Error: No se encontró 'Compuestos.csv'.")

# Función para buscar una fórmula en el DataFrame
def buscar_formula(formula):
    if df is None:
        return None  # No hay base de datos cargada
    resultados = df[df['Formula'] == formula]
    return resultados if not resultados.empty else None

# Página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para la búsqueda
@app.route('/buscar', methods=['POST'])
def buscar():
    try:
        formula = request.form.get('formula')  # Evita errores de KeyError
        if not formula:
            return render_template('resultado.html', error="⚠️ Debes ingresar una fórmula.")

        resultados = buscar_formula(formula)

        return render_template('resultado.html', formula=formula, 
                               resultados=resultados.to_html() if resultados is not None else None,
                               error="Fórmula no encontrada" if resultados is None else None)
    except Exception as e:
        return f"❌ Error interno: {str(e)}", 500  # Manejo de errores

# Ejecutar en local
if __name__ == '__main__':
    app.run(debug=True)
