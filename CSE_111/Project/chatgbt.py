# smartbudget.py
# SmartBudget: Income and Expense Tracker with 4-category allocation
# Enhancements: interactive menu, CSV persistence, summary report, percentage notifications

import csv
import os
from datetime import datetime
from typing import List, Dict

FILENAME = 'entries.csv'
CATEGORIES = {
    'Crecimiento': 0.25,
    'Estabilidad': 0.15,
    'Esenciales': 0.50,
    'Recompensa': 0.10
}

# 1. calculate_allocations
def calculate_allocations(income: float) -> Dict[str, float]:
    """
    Reparte el ingreso en montos para cada categoría según sus porcentajes.
    """
    return {cat: round(income * pct, 2) for cat, pct in CATEGORIES.items()}

# 2. register_income
def register_income(amount: float) -> Dict:
    """
    Crea un registro de ingreso con fecha y tipo 'Ingreso'.
    """
    return {
        'fecha': datetime.now().isoformat(),
        'tipo': 'Ingreso',
        'categoria': '',
        'descripcion': '',
        'monto': amount
    }

# 3. validate_expense
def validate_expense(category: str, amount: float, allocations: Dict[str, float]) -> bool:
    """
    Verifica que el gasto no exceda la asignación de la categoría.
    """
    if category not in allocations:
        return False
    return amount <= allocations[category]

# 4. register_expense
def register_expense(amount: float, category: str, description: str) -> Dict:
    """
    Crea un registro de gasto con fecha, categoría y descripción.
    """
    return {
        'fecha': datetime.now().isoformat(),
        'tipo': 'Gasto',
        'categoria': category,
        'descripcion': description,
        'monto': amount
    }

# 5. save_entry
def save_entry(entry: Dict, filename: str = FILENAME) -> None:
    """
    Añade un registro al archivo CSV.
    """
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['fecha','tipo','categoria','descripcion','monto'])
        if not file_exists:
            writer.writeheader()
        writer.writerow(entry)

# 6. load_entries
def load_entries(filename: str = FILENAME) -> List[Dict]:
    """
    Lee todos los registros del archivo CSV.
    """
    entries = []
    if not os.path.isfile(filename):
        return entries
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['monto'] = float(row['monto'])
            entries.append(row)
    return entries

# 7. summarize_budget
def summarize_budget(entries: List[Dict]) -> Dict[str, float]:
    """
    Resume totales de ingresos y gastos por categoría.
    """
    summary = {cat: 0.0 for cat in CATEGORIES}
    total_income = 0.0
    for e in entries:
        if e['tipo'] == 'Ingreso':
            total_income += e['monto']
        else:
            summary[e['categoria']] += e['monto']
    # Añadir ingreso total y asignaciones
    allocations = calculate_allocations(total_income)
    summary['Total Income'] = total_income
    summary.update({f'Alloc_{cat}': amt for cat, amt in allocations.items()})
    return summary

# 8. print_summary
def print_summary(summary: Dict[str, float]) -> None:
    """
    Muestra el resumen en pantalla con notificaciones de excedentes.
    """
    print("\n--- Resumen de Presupuesto ---")
    print(f"Total Ingresos: {summary['Total Income']:.2f}")
    for cat in CATEGORIES:
        spent = summary[cat]
        alloc = summary[f'Alloc_{cat}']
        status = ''
        if spent > alloc:
            status = f" (Excedido {spent - alloc:.2f})"
        print(f"{cat}: Gastado {spent:.2f} / Asignado {alloc:.2f}{status}")
    print("-----------------------------\n")

# 9. main
def main():
    # Cargar datos
    entries = load_entries()
    # Solicitar ingreso inicial si no hay
    if not any(e['tipo']=='Ingreso' for e in entries):
        amt = float(input("Ingresa tu ingreso total: "))
        save_entry(register_income(amt))
        entries = load_entries()
    # Calcular asignaciones basadas en ingreso acumulado
    total_income = sum(e['monto'] for e in entries if e['tipo']=='Ingreso')
    allocations = calculate_allocations(total_income)

    while True:
        print("\nMenú SmartBudget:\n1) Registrar gasto\n2) Ver resumen\n3) Salir")
        choice = input("Elige una opción: ")
        if choice == '1':
            desc = input("Descripción del gasto: ")
            cat = input(f"Categoría {list(CATEGORIES.keys())}: ")
            amt = float(input("Monto del gasto: "))
            if not validate_expense(cat, amt, allocations):
                print("Error: monto excede la asignación o categoría inválida.")
            else:
                save_entry(register_expense(amt, cat, desc))
                entries = load_entries()
                print("Gasto registrado.")
        elif choice == '2':
            summary = summarize_budget(entries)
            print_summary(summary)
        elif choice == '3':
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida.")

if __name__ == '__main__':
    main()
