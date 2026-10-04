import os
import socket
import getpass
import argparse
import sys

# Приглашение (как в этапе 1)
def priglashenie():
    user = getpass.getuser()
    host = socket.gethostname()
    papka = os.getcwd().replace("\\", "/")
    home = os.path.expanduser("~").replace("\\", "/")
    if papka.startswith(home):
        papka = "~" + papka[len(home):]
    return user + "@" + host + ":" + papka + "$ "

# Раскрытие переменных (как в этапе 1)
def raskryt(slova):
    result = []
    for slovo in slova:
        if slovo.startswith("$"):
            result.append(os.environ.get(slovo[1:], ""))
        else:
            result.append(slovo)
    return result

# Выполнение одной команды
def execute_command(vvod):
    if not vvod.strip():
        return True
    slova = raskryt(vvod.split())
    komanda = slova[0]
    argumenty = slova[1:]
    
    if komanda == "exit":
        print("Пока!")
        return False
    elif komanda == "ls":
        print("ls: аргументы:", argumenty)
    elif komanda == "cd":
        try:
            os.chdir(argumenty[0] if argumenty else os.path.expanduser("~"))
        except:
            print("cd: нет такой папки")
    else:
        print(komanda + ": команда не найдена")
    return True

# Выполнение скрипта из файла
def run_script(filepath):
    print(f"--- Запуск скрипта: {filepath} ---")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Игнорируем пустые строки и комментарии (начинающиеся с #)
                if not line or line.startswith('#'):
                    continue
                print(priglashenie() + line) # Показываем "ввод"
                if not execute_command(line):
                    break
    except FileNotFoundError:
        print(f"Ошибка: Файл '{filepath}' не найден.")
    print("--- Скрипт завершен ---")

# Главная функция
def main():
    # Настройка параметров командной строки
    parser = argparse.ArgumentParser()
    parser.add_argument("--vfs", type=str, default=None, help="Путь к VFS")
    parser.add_argument("--script", type=str, default=None, help="Путь к скрипту")
    args = parser.parse_args()

    # Отладочный вывод параметров (требование задания)
    print("=== Параметры запуска ===")
    print(f"VFS: {args.vfs}")
    print(f"Script: {args.script}")
    print("=========================")

    # Если передан скрипт - выполняем его
    if args.script:
        run_script(args.script)
    
    # Интерактивный режим
    print("Эмулятор (Этап 2)")
    while True:
        vvod = input(priglashenie())
        if not execute_command(vvod):
            break

if __name__ == "__main__":
    main()