from datetime import datetime, timedelta
import json

routes = []

# Создать маршрут
def create_route():
    new_route = []
    n = int(input("введите количество станций в маршруте: "))
    for i in range(n):
        station = input(f"введите название {i+1}-й станции: ")
        if i == n-1: # Последняя станция
            arr_time = input(f"введите время прибытия в {station} (чч:мм): ")
            new_route.append({"station": station, "arr_time": arr_time})
        elif i == 0: # Первая станиция
            dep_time = input("введите время отправления (чч:мм): ")
            new_route.append({"station": station, "dep_time": dep_time}) 
        else: # Не первая и не последняя
            arr_time = input(f"введите время прибытия в {station} (чч:мм): ")
            dep_time = input(f"введите время отправления из {station} (чч:мм): ")
            new_route.append({"station": station, "arr_time": arr_time, "dep_time": dep_time})
    routes.append(new_route)

# Сохранить маршрут
def save_routes():
    with open('routes.json', 'w') as f:
        json.dump(routes, f)

# Загрузить маршрут
def load_routes():
    global routes
    try:
        with open('routes.json', 'r') as file:
            routes = json.load(file)
    except FileNotFoundError:
        print("файл с маршрутами не найден.")

# Редактировать
def edit_route():
    if not routes:
        print("маршруты отсутствуют")
        return
    for i, route in enumerate(routes):
        print(f"\nмаршрут {i+1}:")
        show_route(route)
    route_index = int(input("\nвыберите номер маршрута для редактирования: ")) - 1
    if route_index >= len(routes):
        print("маршрут с таким номером не найден.")
        return
    selected_route = routes[route_index]

    print("\n1. добавить станцию\n2. удалить станцию\n3. изменить станцию")
    choice = input("> ")

    if choice == "1":
        station = input("введите название новой станции: ")
        arr_time = input("введите время прибытия (чч:мм): ")
        if len(selected_route) > 1:
            dep_time = input("введите время отправления (чч:мм): ")
            selected_route.insert(-1, {"station": station, "arr_time": arr_time, "dep_time": dep_time})
        else:
            selected_route.append({"station": station, "arr_time": arr_time})
    elif choice == "2":
        for i, part in enumerate(selected_route):
            print(f"{i+1}. {part['station']}")
        station_index = int(input("выберите номер станции для удаления: ")) - 1
        if station_index >= len(selected_route) or station_index < 0:
            print("станция с таким номером не найдена.")
            return
        del selected_route[station_index]
    elif choice == "3":
        for i, part in enumerate(selected_route):
            print(f"{i+1}. {part['station']}")
        station_index = int(input("выберите номер станции для изменения: ")) - 1
        if station_index >= len(selected_route) or station_index < 0:
            print("станция с таким номером не найдена.")
            return
        station = input("введите новое название станции: ")
        selected_route[station_index]['station'] = station
        if 'arr_time' in selected_route[station_index]:
            arr_time = input("введите новое время прибытия (чч:мм): ")
            selected_route[station_index]['arr_time'] = arr_time
        if 'dep_time' in selected_route[station_index]:
            dep_time = input("введите новое время отправления (чч:мм): ")
            selected_route[station_index]['dep_time'] = dep_time

# Рассчитать разницу по времени между станциями
def calculate_time_diff(start_time, end_time):
    fmt = '%H:%M'
    start = datetime.strptime(start_time, fmt)
    end = datetime.strptime(end_time, fmt)
    # Если время прибытия меньше времени отправления, считаем, что прибытие на следующий день
    if end < start:
        end += timedelta(days=1)
    return (end - start)

# Показать информацию о маршруте
def show_route(route):
    for i, part in enumerate(route):
        if i == 0:
            print(f"Отправление с {part['station']} в {part['dep_time']}")
        else:
            time_in_way = calculate_time_diff(route[i-1]['dep_time'], part['arr_time'])
            print(f"В пути до {part['station']}: {time_in_way}")
            if 'dep_time' in part:
                stay_time = calculate_time_diff(part['arr_time'], part['dep_time'])
                print(f"Стоянка на {part['station']}: {stay_time}")
            else:
                print(f"Конечная на {part['station']} в {part['arr_time']}")

# Главная
def main_menu():
    load_routes()
    while True:
        try:
            print("\n1. новый маршрут\n2. все маршруты\n3. сохранить маршруты\n4. редактировать маршруты")
            choice = input("> ")
            if choice == "1":
                create_route()
            elif choice == "2":
                for i, route in enumerate(routes):
                    print(f"\nМаршрут {i+1}:")
                    show_route(route)
            elif choice == "3":
                save_routes()
            elif choice == "4":
                edit_route()
        except Exception as e:
            print(e)
            
# Вхождение
if __name__ == "__main__":
    main_menu()