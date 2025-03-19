import os
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

# Función para buscar compuestos
def buscar_compuesto(tipo_busqueda, valor_busqueda):
    if df is None:
        return None  # Si no hay base de datos cargada, devuelve None
    
    if tipo_busqueda == "formula":
        # Buscar por fórmula
        resultados = df[df['Formula'] == valor_busqueda]
    elif tipo_busqueda == "nomenclatura":
        # Buscar por nomenclatura (en las tres columnas)
        resultados = df[
            (df['Sistematica'] == valor_busqueda) |
            (df['Stock'] == valor_busqueda) |
            (df['Tradicional'] == valor_busqueda)
        ]
    else:
        return None  # Tipo de búsqueda no válido
    
    return resultados if not resultados.empty else None

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para la búsqueda
@app.route('/buscar', methods=['POST'])
def buscar():
    try:
        tipo_busqueda = request.form.get('tipo_busqueda')  # Obtiene el tipo de búsqueda
        formula = request.form.get('formula')  # Obtiene la fórmula (si se seleccionó)
        nomenclatura = request.form.get('nomenclatura')  # Obtiene la nomenclatura (si se seleccionó)

        if tipo_busqueda == "formula":
            if not formula:
                return render_template('resultados.html', error="⚠️ Debes ingresar una fórmula.")
            valor_busqueda = formula
        elif tipo_busqueda == "nomenclatura":
            if not nomenclatura:
                return render_template('resultados.html', error="⚠️ Debes seleccionar una nomenclatura.")
            valor_busqueda = nomenclatura
        else:
            return render_template('resultados.html', error="⚠️ Tipo de búsqueda no válido.")

        # Realizar la búsqueda
        resultados = buscar_compuesto(tipo_busqueda, valor_busqueda)

        return render_template('resultados.html', tipo_busqueda=tipo_busqueda,
                               valor_busqueda=valor_busqueda,
                               resultados=resultados.to_html() if resultados is not None else None,
                               error="No se encontraron resultados." if resultados is None else None)
    except Exception as e:
        return f"❌ Error interno: {str(e)}", 500  # Mensaje de error más claro

# Ejecutar en local
if __name__ == '__main__':
    app.run(debug=True)
