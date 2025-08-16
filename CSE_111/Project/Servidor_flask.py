from flask import Flask, render_template_string, request, redirect
import csv, os
from datetime import datetime

app = Flask(__name__)

FILENAME = "SmartBudget.csv"

CATEGORIES_EXPENSE = {
    'Growth': {'Rate': 0.25, 'Phrase': "The 25% That Works For You!"},
    'Stability': {'Rate': 0.15, 'Phrase': "The 15% That Keeps You In The Game!"},
    'Essential': {'Rate': 0.5, 'Phrase': "The 50% That Feed You, Not Your Ego!"},
    'Reward': {'Rate': 0.1, 'Phrase': "The 10% That Keeps You Sane!"}
}
CATEGORIES_INCOME = {
    'Employment Income': {'Phrase': 'Salary, wages, bonuses, commissions'},
    'Business / Self-Employment Income': {'Phrase': 'Product sales, service fees'},
    'Investment & Passive Income': {'Phrase': 'Rentals, dividends, interest, royalties'},
    'Other Income': {'Phrase': 'Gifts, inheritances, asset sales, prizes'}
}

# --------------------------
# Funciones CSV
# --------------------------
def read_csv():
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        entries = list(reader)
        for e in entries:
            try:
                e["Amount"] = float(e["Amount"])
            except:
                e["Amount"] = 0
        return entries

def save_csv(data):
    file_exists = os.path.isfile(FILENAME)
    with open(FILENAME, "a", newline='') as csvfile:
        fieldnames = ['Date', 'Type', 'Category', 'Description', 'Amount']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

# --------------------------
# Funciones Summary
# --------------------------
def filter_transaction(entries, year=None, month=None, day=None):
    return [
        e for e in entries if
        (year is None or int(e['Date'][:4]) == year) and
        (month is None or int(e['Date'][5:7]) == month) and
        (day is None or int(e['Date'][8:10]) == day)
    ]

def generate_summary(entries, year, month):
    transacciones = filter_transaction(entries, year=year, month=month)
    total_income = sum(t['Amount'] for t in transacciones if t['Type'] == 'Income')
    total_expense = sum(t['Amount'] for t in transacciones if t['Type'] == 'Expense')

    resumen = {'Total Income': total_income, 'Total Expenses': total_expense}

    for cat in CATEGORIES_EXPENSE.keys():
        gasto_cat = sum(t['Amount'] for t in transacciones if t['Type'] == 'Expense' and t['Category'] == cat)
        asignacion = total_income * CATEGORIES_EXPENSE[cat]['Rate'] if total_income else 0
        resumen[cat] = gasto_cat
        resumen[f'Alloc_{cat}'] = asignacion

    return resumen, transacciones

# --------------------------
# Rutas Flask
# --------------------------
@app.route("/")
def index():
    entries = read_csv()
    return render_template_string(TEMPLATE, entries=entries,
                                  CATEGORIES_INCOME=CATEGORIES_INCOME,
                                  CATEGORIES_EXPENSE=CATEGORIES_EXPENSE,
                                  resumen=None)

@app.route("/add", methods=["POST"])
def add():
    tipo = request.form.get("type")
    categoria = request.form.get("category")
    desc = request.form.get("description")
    dt_str = request.form.get("date_in")  
# Ejemplo: "2025-08-15T14:30"

    dt_obj = datetime.fromisoformat(dt_str)  
# dt_obj = datetime.datetime(2025, 8, 15, 14, 30)

# Guardar como ISO completo en CSV/SQLite
    moment = dt_obj.isoformat()  
    amount = request.form.get("amount")
    try:
        amount = float(amount)
    except:
        amount = 0
    save_csv({
        'Date': moment,
        'Type': tipo,
        'Category': categoria,
        'Description': desc,
        'Amount': amount
    })
    return redirect("/")

@app.route("/summary", methods=["POST"])
def summary():
    date_str = request.form.get("summary_month")
    try:
        year, month = map(int, date_str.split("-"))
    except:
        year, month = datetime.now().year, datetime.now().month

    entries = read_csv()
    resumen, rows = generate_summary(entries, year, month)
    return render_template_string(TEMPLATE, entries=rows,
                                  CATEGORIES_INCOME=CATEGORIES_INCOME,
                                  CATEGORIES_EXPENSE=CATEGORIES_EXPENSE,
                                  resumen=resumen, year=year, month=month)

# --------------------------
# HTML
# --------------------------
TEMPLATE = """
<!doctype html>
<html>
<head>
<title>SmartBudget</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
<script>
document.addEventListener("DOMContentLoaded", function() {
    const typeSelect = document.querySelector("select[name='type']");
    const categorySelect = document.querySelector("select[name='category']");

    // Categorías pre-cargadas desde Flask (JSON)
    const categoriesIncome = {{ CATEGORIES_INCOME | tojson }};
    const categoriesExpense = {{ CATEGORIES_EXPENSE | tojson }};

    function updateCategories() {
        const type = typeSelect.value;
        categorySelect.innerHTML = ""; // Limpiar opciones

        let categories;
        if (type === "Income") {
            categories = categoriesIncome;
        } else {
            categories = categoriesExpense;
        }

        for (let key in categories) {
            let option = document.createElement("option");
            option.value = key;
            option.textContent = key;
            categorySelect.appendChild(option);
        }
    }

    // Inicializar y escuchar cambios
    typeSelect.addEventListener("change", updateCategories);
    updateCategories();
});
</script>
</head>
<body class="p-4">
<h1>SmartBudget</h1>

<form action="/add" method="post" class="mb-3">
  <div class="row g-2">
    <div class="col-md-1">
      <select name="type" class="form-select" required>
        <option value="Income">Income</option>
        <option value="Expense">Expense</option>
      </select>
    </div>
    <div class="col-md-3">
      <select name="category" class="form-select" required></select>
    </div>
    <div class="col-md-3">
      <input type="text" name="description" placeholder="Description" class="form-control" required>
    </div>
    
    <div class="col-md-2">
       <input type="datetime-local" name="date_in" class="form-control" required>
    </div>
    <div class="col-md-2">
      <input type="number" step="0.01" name="amount" placeholder="Amount" class="form-control" required>
    </div>
    <div class="col-md-1">
      <button class="btn btn-primary w-100">Add</button>
    </div>
  </div>
</form>

<!-- Formulario resumen mensual -->
<form action="/summary" method="post" class="mb-3">
  <div class="input-group">
    <input type="month" name="summary_month" class="form-control" required>
    <button class="btn btn-success">Show Summary</button>
  </div>
</form>

{% if resumen %}
<h3>Summary for {{year}}-{{'%02d' % month}}</h3>
<p><strong>Total Income:</strong> {{ "%.2f"|format(resumen["Total Income"]) }} |
   <strong>Total Expenses:</strong> {{ "%.2f"|format(resumen["Total Expenses"]) }} |
   <strong>Balance:</strong> {{ "%.2f"|format(resumen["Total Income"] - resumen["Total Expenses"]) }}</p>

<table class="table table-bordered">
<tr><th>Category</th><th>Spent</th><th>Allocated</th><th>Status</th></tr>
{% for cat in CATEGORIES_EXPENSE.keys() %}
<tr>
<td>{{cat}}</td>
<td>{{ "%.2f"|format(resumen[cat]) }}</td>
<td>{{ "%.2f"|format(resumen["Alloc_"+cat]) }}</td>
<td>
{% if resumen[cat] > resumen["Alloc_"+cat] %}
<span class="text-danger">Exceeded by {{ "%.2f"|format(resumen[cat]-resumen["Alloc_"+cat]) }}</span>
{% else %}
<span class="text-success">Under by {{ "%.2f"|format(resumen["Alloc_"+cat]-resumen[cat]) }}</span>
{% endif %}
</td>
</tr>
{% endfor %}
</table>
{% endif %}


<table class="table table-striped">
  <thead><tr><th>Date</th><th>Type</th><th>Category</th><th>Description</th><th>Amount</th></tr></thead>
  <tbody>
    {% for e in entries %}
    <tr>
      <td>{{e.Date}}</td>
      <td>{{e.Type}}</td>
      <td>{{e.Category}}</td>
      <td>{{e.Description}}</td>
      <td>{{e.Amount}}</td>
    </tr>
    {% endfor %}
  </tbody>
</table>
</body>
</html>
"""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
