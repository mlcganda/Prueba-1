import os
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['DEBUG'] = True  # Modo depuración activado

# Título personalizado
TITULO = "PROYECTO PERSONAL - MATEO MARTÍN"

# Definir la ruta correcta para `Compuestos.csv`
db_path = os.path.join(os.path.dirname(__file__), 'data', 'Compuestos.csv')

# Verificar si el archivo existe antes de cargarlo
if os.path.exists(db_path):
    try:
        df = pd.read_csv(db_path)
        # Verificar que el archivo tenga las columnas necesarias
        columnas_requeridas = {'Formula', 'Sistematica', 'Stock', 'Tradicional'}
        if not columnas_requeridas.issubset(df.columns):
            df = None
            print(f"⚠️ Error: El archivo '{db_path}' no tiene las columnas requeridas: {columnas_requeridas}.")
    except Exception as e:
        df = None
        print(f"⚠️ Error al leer el archivo CSV: {str(e)}")
else:
    df = None
    print(f"⚠️ Error: No se encontró '{db_path}'. Verifica que el archivo esté en la carpeta 'data/'.")

# Función para buscar compuestos
def buscar_compuesto(tipo_busqueda, valor_busqueda):
    if df is None or df.empty:
        return None  # Si no hay base de datos cargada o está vacía, devuelve None
    
    if tipo_busqueda == "formula":
        # Buscar por fórmula
        resultados = df[df['Formula'].str.lower() == valor_busqueda.lower()]
    elif tipo_busqueda == "nomenclatura":
        # Buscar por nomenclatura (en las tres columnas)
        resultados = df[
            (df['Sistematica'].str.lower() == valor_busqueda.lower()) |
            (df['Stock'].str.lower() == valor_busqueda.lower()) |
            (df['Tradicional'].str.lower() == valor_busqueda.lower())
        ]
    else:
        return None  # Tipo de búsqueda no válido
    
    return resultados if not resultados.empty else None

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html', titulo=TITULO)

# Ruta para la búsqueda
@app.route('/buscar', methods=['POST'])
def buscar():
    try:
        tipo_busqueda = request.form.get('tipo_busqueda')  # Obtiene el tipo de búsqueda
        formula = request.form.get('formula')  # Obtiene la fórmula (si se seleccionó)
        nomenclatura = request.form.get('nomenclatura')  # Obtiene la nomenclatura (si se seleccionó)

        if tipo_busqueda == "formula":
            if not formula:
                return render_template('resultados.html', titulo=TITULO, error="⚠️ Debes ingresar una fórmula.")
            valor_busqueda = formula
        elif tipo_busqueda == "nomenclatura":
            if not nomenclatura:
                return render_template('resultados.html', titulo=TITULO, error="⚠️ Debes seleccionar una nomenclatura.")
            valor_busqueda = nomenclatura
        else:
            return render_template('resultados.html', titulo=TITULO, error="⚠️ Tipo de búsqueda no válido.")

        # Realizar la búsqueda
        resultados = buscar_compuesto(tipo_busqueda, valor_busqueda)

        return render_template('resultados.html', titulo=TITULO, tipo_busqueda=tipo_busqueda,
                               valor_busqueda=valor_busqueda,
                               resultados=resultados.to_html(classes="tabla-resultados", index=False) if resultados is not None else None,
                               error="No se encontraron resultados." if resultados is None else None)
    except Exception as e:
        return render_template('resultados.html', titulo=TITULO, error=f"❌ Error interno: {str(e)}"), 500

# Ejecutar en local
if __name__ == '__main__':
    app.run(debug=True)
