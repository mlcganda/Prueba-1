from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Cargar la base de datos
df = pd.read_csv('data/Compuestos.csv')

def buscar_formula(formula):
    """Busca una fórmula en la base de datos y devuelve los resultados."""
    resultados = df[df['Formula'].str.lower() == formula.lower()]
    return resultados.to_dict(orient='records') if not resultados.empty else None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar', methods=['POST'])
def buscar():
    formula = request.form['formula']
    resultados = buscar_formula(formula)
    
    if resultados:
        return render_template('resultado.html', formula=formula, resultados=resultados)
    else:
        return render_template('resultado.html', formula=formula, error="Fórmula no encontrada")

if __name__ == '__main__':
    app.run(debug=True)
