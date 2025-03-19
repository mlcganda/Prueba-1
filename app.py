# abrir base de datos compuestos.csv con pandas
df = pd.read_csv('Compuestos.csv')
from IPython.display import display
from ipywidgets import Dropdown, Output, Text

# definimos función para buscar en la columna Fórmula

def buscar_formula(formula,dfdatos):
  """
  Busca una fórmula específica en la columna 'Fórmula' del DataFrame df.

  Args:
    formula: La fórmula a buscar.

  Returns:
    Un DataFrame con las filas que contienen la fórmula especificada, o None si no se encuentra.
  """
  resultados = dfdatos[dfdatos['Formula'] == formula]
  if not resultados.empty:
      return resultados
  else:
      return None

# Crear un widget Dropdown con opciones de nomenclatura
nomenclatura_options = {
    'Todas': 'Todas',
    'Nomenclatura Tradicional': 'Tradicional',
    'Nomenclatura Sistemática': 'Sistematica',
    'Nomenclatura Stock': 'Stock'
}
nomenclatura_dropdown = Dropdown(options=nomenclatura_options, description='Nomenclatura:')
formula_input = Text(value='', description='Fórmula:')  # Input para la fórmula
output = Output()

# Define a function to update the output when the dropdown value changes
def on_value_change(change):
    with output:
        output.clear_output()
        selected_nomenclatura = nomenclatura_dropdown.value
        formula = formula_input.value
        resultados = buscar_formula(formula, df)
        if resultados is not None:
            if selected_nomenclatura == 'Todas':
              display(resultados[['Tradicional', 'Sistematica', 'Stock']])
            elif selected_nomenclatura in resultados.columns:
                if not resultados[selected_nomenclatura].isnull().all():
                    display(resultados[selected_nomenclatura])
                else:
                    print(f"No hay información disponible para la nomenclatura {nomenclatura_dropdown.label} de la formula {formula}")
            else:
                print("Nomenclatura no válida.")
        else:
            print(f"No se encontró la fórmula: {formula}")

nomenclatura_dropdown.observe(on_value_change, names='value')
formula_input.observe(on_value_change, names='value')

display(formula_input)
display(nomenclatura_dropdown)
display(output)
