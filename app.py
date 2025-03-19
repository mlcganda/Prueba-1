import os
import re
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['DEBUG'] = True  # Modo depuración activado

# Definir la ruta correcta para `Compuestos.csv`
db_path = os.path.join(os.path.dirname(__file__), 'data', 'Compuestos.csv')

# Verificar si el archivo existe antes de cargarlo
if os.path.exists(db_path):
    df = pd.read_csv(db_path)
else:
    df = None
    print(f"⚠️ Error: No se encontró '{db_path}'. Verifica que el archivo esté en la carpeta 'data/'.")

# Función para validar fórmulas químicas
def validar_formula(formula):
    patron = re.compile(r'^[A-Z][a-z]?\d*([A-Z][a-z]?\d*)*$')
    return bool(patron.match(formula))

# Función para buscar una fórmula
def buscar_formula(formula):
    if df is None:
        return None  # Si no hay base de datos cargada, devuelve None
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
        formula = request.form.get('formula')  # Obtiene la fórmula del formulario
        if not formula:
            return render_template('resultados.html', error="⚠️ Debes ingresar una fórmula.")
        
        # Validar el formato de la fórmula
        if not validar_formula(formula):
            return render_template('resultados.html', error="⚠️ La fórmula no tiene un formato válido.")

        resultados = buscar_formula(formula)

        return render_template('resultados.html', formula=formula, 
                               resultados=resultados.to_html() if resultados is not None else None,
                               error="Fórmula no encontrada" if resultados is None else None)
    except Exception as e:
        return f"❌ Error interno: {str(e)}", 500  # Mensaje de error más claro

# Ejecutar en local
if __name__ == '__main__':
    app.run(debug=True)
