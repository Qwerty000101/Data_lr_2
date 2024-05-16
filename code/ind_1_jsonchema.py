#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Необходимо реализовать валидацию загруженных данных
# в примере 1 и в индивидуальном задании с помощью спецификации JSON Schema


import sys
import json
import jsonschema


def add():
    '''
    Добавить маршрут
    '''
    name_start = input("Начальный пункт маршрута? ")
    name_end = input("Конечный пункт маршрута? ")
    number = int(input("Номер маршрута? "))

    route = {
        'name_start': name_start,
        'name_end': name_end,
        'number': number
    }
    return route


def list(routes):
    '''
    Вывести список маршрутов
    '''
    if routes:
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 30,
            '-' * 8
        )
        print(line)

        print('| {:^4} | {:^30} | {:^30} | {:^8} |'.format(
            "№",
            "Начальный пункт",
            "Конечный пункт",
            "Номер"
        )
        )
        print(line)

        for idx, route in enumerate(routes, 1):
            print('| {:>4} | {:<30} | {:<30} | {:>8} |'.format(
                idx,
                route.get('name_start', ''),
                route.get('name_end', ''),
                route.get('number', 0)
            )
            )
            print(line)
    else:
        print("Список маршрутов пуст.")


def save_routes(file_name, staff):
    """
    Сохранить все маршруты в файл JSON.
    """
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(staff, fout, ensure_ascii=False, indent=4)


def load_routes(file_name):
    """
    Загрузить все маршруты из файла JSON.
    """
    # Открыть файл с заданным именем для чтения.
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "name_start": {"type": "string"},
                "name_end": {"type": "string"},
                "number": {"type": "integer"}
            },
            "required": ["name_start", "name_end", "number"]
        }
    }

    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8") as fin:
        data = json.load(fin)

    try:
        jsonschema.validate(data, schema)
        print(">>> Данные получены")

    except jsonschema.exceptions.ValidationError as e:
        print(">>> Ошибка:")
        print(e.message)
    return data


def select(routes, command):
    '''
    Вывести выбранные маршруты
    '''
    parts = command.split(' ', maxsplit=1)
    station = parts[1]
    count = 0

    for route in routes:
        if (station == route["name_start"].lower() or
                station == route["name_end"].lower()):

            count += 1
            print('{:>4}: {}-{}, номер маршрута: {}'.format(count,
                  route["name_start"], route["name_end"], route["number"]))

    if count == 0:
        print("Маршрут не найден.")


def help():
    '''
    Вывести список команд
    '''
    print("Список команд:\n")
    print("add - добавить маршрут;")
    print("load - загрузить данные из файла;")
    print("save - сохранить данные в файл;")
    print("list - вывести список маршрутов;")
    print("select <пункт> - запросить информацию" +
          " о маршруте с указанным пунктом;")
    print("help - отобразить справку;")
    print("exit - завершить работу с программой.")


def main():
    '''
    Основная функция
    '''
    routes = []

    while True:

        command = input(">>> ").lower()

        if command == 'exit':
            break

        elif command == 'add':
            route = add()
            routes.append(route)

            if len(routes) > 1:
                routes.sort(key=lambda item: item.get('number', ''))

        elif command == 'list':
            list(routes)

        elif command.startswith("load "):
            parts = command.split(maxsplit=1)
            file_name = parts[1]
            routes = load_routes(file_name)

        elif command.startswith("save "):
            parts = command.split(maxsplit=1)
            file_name = parts[1]
            save_routes(file_name, routes)

        elif command.startswith('select '):
            select(routes, command)

        elif command == 'help':
            help()

        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)


if __name__ == '__main__':
    main()
