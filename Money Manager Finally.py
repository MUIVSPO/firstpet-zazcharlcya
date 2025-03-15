import matplotlib.pyplot as plt
from colorama import Fore, Style, init
from datetime import datetime, timedelta
import json

# Инициализация colorama
init(autoreset=True)

# Глобальные переменные для хранения данных
data = {
    "incomes": [],
    "expenses": [],
    "categories": {"Доходы": [], "Расходы": []},
    "balance": 0,
    "reminder_limit": 0,
    "rank": "Новичок-сберегатель"
}

# Определение уровней званий и порогов доходов
RANKS = [
    {"name": "Новичок-сберегатель", "threshold": 0},
    {"name": "Мастер бюджета", "threshold": 10000},
    {"name": "Капитан капитала", "threshold": 50000},
    {"name": "Инвестор-виртуоз", "threshold": 100000},
    {"name": "Финансовый магнат", "threshold": 500000}
]

def save_data():
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_data():
    global data
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(Fore.RED + "Файл данных не найден. Будет создан новый файл при сохранении данных.")
    except json.JSONDecodeError:
        print(Fore.RED + "Ошибка чтения данных. Файл данных поврежден. Будет создан новый файл при сохранении данных.")
        data = {
            "incomes": [],
            "expenses": [],
            "categories": {"Доходы": [], "Расходы": []},
            "balance": 0,
            "reminder_limit": 0,
            "rank": "Новичок-сберегатель"
        }

def display_menu():
    print(Fore.CYAN + "\n=== Менеджер расходов ===")
    print(Fore.MAGENTA + f"Ваше текущее звание: {data['rank']}")
    print(Fore.YELLOW + "1. Добавить доход")
    print(Fore.YELLOW + "2. Добавить расход")
    print(Fore.YELLOW + "3. Показать текущий баланс")
    print(Fore.YELLOW + "4. Показать статистику за период")
    print(Fore.YELLOW + "5. Управление категориями")
    print(Fore.YELLOW + "6. Построить графики")
    print(Fore.YELLOW + "7. Настройка напоминаний")
    print(Fore.YELLOW + "8. Редактировать доход")
    print(Fore.YELLOW + "9. Редактировать расход")
    print(Fore.RED + "10. Выйти из программы")
    print(Style.RESET_ALL)

def add_income():
    if not data["categories"]["Доходы"]:
        print(Fore.RED + "Сначала создайте категорию доходов.")
        return
    try:
        amount = float(input("Введите сумму дохода: "))
        category = select_category("Доходы")
        data["incomes"].append({"amount": amount, "category": category, "date": datetime.now().isoformat()})
        update_balance()
        update_rank()
        save_data()
    except ValueError:
        print(Fore.RED + "Неверный ввод. Пожалуйста, введите числовое значение.")

def add_expense():
    if not data["categories"]["Расходы"]:
        print(Fore.RED + "Сначала создайте категорию расходов.")
        return
    try:
        amount = float(input("Введите сумму расхода: "))
        category = select_category("Расходы")
        data["expenses"].append({"amount": amount, "category": category, "date": datetime.now().isoformat()})
        check_reminder(amount)
        update_balance()
        save_data()
    except ValueError:
        print(Fore.RED + "Неверный ввод. Пожалуйста, введите числовое значение.")

def edit_income():
    if not data["incomes"]:
        print(Fore.RED + "Нет доходов для редактирования.")
        return
    print(Fore.CYAN + "\nВыберите доход для редактирования:")
    for i, income in enumerate(data["incomes"], 1):
        print(f"{i}. {income['amount']} руб. - {income['category']} - {income['date']}")
    try:
        choice = int(input("Введите номер дохода: "))
        if 1 <= choice <= len(data["incomes"]):
            income = data["incomes"][choice - 1]
            new_amount = float(input(f"Введите новую сумму дохода (текущая: {income['amount']}): "))
            new_category = select_category("Доходы")
            income['amount'] = new_amount
            income['category'] = new_category
            update_balance()
            update_rank()
            save_data()
            print(Fore.GREEN + "Доход успешно обновлен.")
        else:
            print(Fore.RED + "Неверный номер дохода.")
    except ValueError:
        print(Fore.RED + "Неверный ввод. Пожалуйста, введите числовое значение.")

def edit_expense():
    if not data["expenses"]:
        print(Fore.RED + "Нет расходов для редактирования.")
        return
    print(Fore.CYAN + "\nВыберите расход для редактирования:")
    for i, expense in enumerate(data["expenses"], 1):
        print(f"{i}. {expense['amount']} руб. - {expense['category']} - {expense['date']}")
    try:
        choice = int(input("Введите номер расхода: "))
        if 1 <= choice <= len(data["expenses"]):
            expense = data["expenses"][choice - 1]
            new_amount = float(input(f"Введите новую сумму расхода (текущая: {expense['amount']}): "))
            new_category = select_category("Расходы")
            expense['amount'] = new_amount
            expense['category'] = new_category
            update_balance()
            save_data()
            print(Fore.GREEN + "Расход успешно обновлен.")
        else:
            print(Fore.RED + "Неверный номер расхода.")
    except ValueError:
        print(Fore.RED + "Неверный ввод. Пожалуйста, введите числовое значение.")

def update_balance():
    total_income = sum(item['amount'] for item in data["incomes"])
    total_expense = sum(item['amount'] for item in data["expenses"])
    data["balance"] = total_income - total_expense

def update_rank():
    total_income = sum(item['amount'] for item in data["incomes"])
    for rank in reversed(RANKS):
        if total_income >= rank["threshold"]:
            data["rank"] = rank["name"]
            break

def show_balance():
    print(Fore.GREEN + f"\nТекущий баланс: {data['balance']} руб.")

def show_statistics():
    print(Fore.CYAN + "\nВыберите период для отображения статистики:")
    print("1. День")
    print("2. Неделя")
    print("3. Месяц")
    choice = input("Введите номер периода: ")
    
    now = datetime.now()
    if choice == "1":
        period = "день"
        start_date = now - timedelta(days=1)
    elif choice == "2":
        period = "неделя"
        start_date = now - timedelta(weeks=1)
    elif choice == "3":
        period = "месяц"
        start_date = now - timedelta(days=30)
    else:
        print(Fore.RED + "Неверный выбор")
        return

    filtered_incomes = [item for item in data["incomes"] if datetime.fromisoformat(item['date']) >= start_date]
    filtered_expenses = [item for item in data["expenses"] if datetime.fromisoformat(item['date']) >= start_date]

    print(Fore.BLUE + f"\nСтатистика за {period}:")
    print(Fore.GREEN + f"Доходы: {sum(item['amount'] for item in filtered_incomes)} руб.")
    print(Fore.RED + f"Расходы: {sum(item['amount'] for item in filtered_expenses)} руб.")

def manage_categories():
    print(Fore.CYAN + "\n=== Управление категориями ===")
    print("1. Добавить категорию")
    print("2. Удалить категорию")
    print("3. Редактировать категорию")
    choice = input("Выберите действие: ")
    if choice == "1":
        category_type = select_category_type()
        category_name = input("Введите название категории: ").capitalize()
        if category_type in data["categories"]:
            data["categories"][category_type].append(category_name)
        else:
            print(Fore.RED + "Неверный тип категории")
    elif choice == "2":
        category_type = select_category_type()
        if category_type in data["categories"]:
            category_name = select_category(category_type)
            if category_name in data["categories"][category_type]:
                data["categories"][category_type].remove(category_name)
            else:
                print(Fore.RED + "Категория не найдена.")
        else:
            print(Fore.RED + "Неверный тип категории")
    elif choice == "3":
        category_type = select_category_type()
        if category_type in data["categories"]:
            old_name = select_category(category_type)
            new_name = input("Введите новое название категории: ").capitalize()
            if old_name in data["categories"][category_type]:
                index = data["categories"][category_type].index(old_name)
                data["categories"][category_type][index] = new_name
            else:
                print(Fore.RED + "Категория не найдена.")
        else:
            print(Fore.RED + "Неверный тип категории")
    else:
        print(Fore.RED + "Неверный выбор")
    save_data()

def select_category_type():
    print(Fore.CYAN + "\nВыберите тип категории:")
    print("1. Доходы")
    print("2. Расходы")
    choice = input("Введите номер типа категории: ")
    if choice == "1":
        return "Доходы"
    elif choice == "2":
        return "Расходы"
    else:
        print(Fore.RED + "Неверный выбор")
        return select_category_type()

def select_category(category_type):
    print(Fore.CYAN + f"\nВыберите категорию для {category_type}:")
    for i, category in enumerate(data["categories"][category_type], 1):
        print(f"{i}. {category}")
    try:
        choice = int(input("Введите номер категории: "))
        if 1 <= choice <= len(data["categories"][category_type]):
            return data["categories"][category_type][choice - 1]
        else:
            print(Fore.RED + "Неверный номер категории. Пожалуйста, выберите снова.")
            return select_category(category_type)
    except ValueError:
        print(Fore.RED + "Неверный ввод. Пожалуйста, введите числовое значение.")
        return select_category(category_type)

def plot_graphs():
    income_categories = {}
    expense_categories = {}

    for item in data["incomes"]:
        category = item['category']
        income_categories[category] = income_categories.get(category, 0) + item['amount']

    for item in data["expenses"]:
        category = item['category']
        expense_categories[category] = expense_categories.get(category, 0) + item['amount']

    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.bar(income_categories.keys(), income_categories.values(), color='green')
    plt.title('Доходы по категориям')
    plt.xticks(rotation=45, ha="right")

    plt.subplot(1, 2, 2)
    plt.bar(expense_categories.keys(), expense_categories.values(), color='red')
    plt.title('Расходы по категориям')
    plt.xticks(rotation=45, ha="right")

    plt.subplots_adjust(bottom=0.3)
    plt.show()

def set_reminder():
    try:
        data["reminder_limit"] = float(input("Введите лимит для напоминания о расходах: "))
        save_data()
    except ValueError:
        print(Fore.RED + "Неверный ввод. Пожалуйста, введите числовое значение.")

def check_reminder(amount):
    if amount > data["reminder_limit"]:
        print(Fore.RED + f"Внимание! Расход превышает установленный лимит: {data['reminder_limit']} руб.")

def main():
    load_data()
    while True:
        display_menu()
        choice = input("Выберите опцию: ")
        if choice == "1":
            add_income()
        elif choice == "2":
            add_expense()
        elif choice == "3":
            show_balance()
        elif choice == "4":
            show_statistics()
        elif choice == "5":
            manage_categories()
        elif choice == "6":
            plot_graphs()
        elif choice == "7":
            set_reminder()
        elif choice == "8":
            edit_income()
        elif choice == "9":
            edit_expense()
        elif choice == "10":
            print(Fore.RED + "Выход из программы...")
            break
        else:
            print(Fore.RED + "Неверный выбор. Пожалуйста, выберите снова.")

if __name__ == "__main__":
    main()
