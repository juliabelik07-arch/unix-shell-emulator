import os
import socket
import getpass
import argparse
import sys

# ФУНКЦИЯ ПРИГЛАШЕНИЯ 1 этап
def priglashenie():
    user = getpass.getuser() # Имя пользователя
    host = socket.gethostname() # Имя компьютера
    papka = os.getcwd() # Текущая папка
    home = os.path.expanduser("~") # Домашняя папка
    
    papka = papka.replace("\\", "/")
    home = home.replace("\\", "/")
    
    if papka.startswith(home):# Если текущая папка внутри домашней
        papka = "~" + papka[len(home):]# Сокращаем её до вида ~/Desktop
        
    return user + "@" + host + ":" + papka + "$ "


# ФУНКЦИЯ РАСКРЫТИЯ ПЕРЕМЕННЫХ 1 этап
def raskryt(slova):
    result = []
    for slovo in slova:
        if slovo.startswith("$"):
            peremennaya = slovo[1:] # Убираем $
            if peremennaya == "HOME":
                znachenie = os.environ.get("USERPROFILE", "")
            else:
                znachenie = os.environ.get(peremennaya, "")
            result.append(znachenie)
        else:
            result.append(slovo)
    return result


# ФУНКЦИЯ ВЫПОЛНЕНИЯ ОДНОЙ КОМАНДЫ 1 этап
def execute_command(vvod):
    if not vvod.strip():
        return True
        
    slova = raskryt(vvod.split())
    komanda = slova[0] # Первое слово — команда
    argumenty = slova[1:]# Остальные — аргументы
    
    if komanda == "exit":
        print("Пока!")
        return False
        
    elif komanda == "ls":# ls (заглушка)
        print("ls: аргументы:", argumenty)
        
    elif komanda == "cd":
        # Если нет аргументов - идем домой
        if len(argumenty) == 0:
            novaya_papka = os.path.expanduser("~")
        else:
            novaya_papka = argumenty[0]
            
        # Пытаемся перейти
        try:
            os.chdir(novaya_papka)
        except:
            print("cd: нет такой папки:", novaya_papka)
            
    else:
        print(komanda + ": команда не найдена")
        
    return True


# ФУНКЦИЯ ВЫПОЛНЕНИЯ СКРИПТА 2 этап
def run_script(filepath):
    print(f"--- Запуск скрипта: {filepath} ---")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()# Убираем пробелы

                # Игнорируем пустые строки и комментарии (начинающиеся с #)
                if not line or line.startswith('#'):
                    continue

                print(priglashenie() + line) # Показываем "ввод"

                if not execute_command(line):
                    break
    except FileNotFoundError:
        print(f"Ошибка: Файл '{filepath}' не найден.")
    print("--- Скрипт завершен ---")


# ГЛАВНАЯ ФУНКЦИЯ 
def main():
     
    parser = argparse.ArgumentParser()
    parser.add_argument("--vfs", type=str, default=None, help="Путь к VFS")
    parser.add_argument("--script", type=str, default=None, help="Путь к скрипту")
    args = parser.parse_args() # запускает парсер

     
    print("=== Параметры запуска ===")
    print(f"VFS: {args.vfs}")# выводим то, что пользователь передал в параметре --vfs
    print(f"Script: {args.script}")

    # Если передан скрипт - выполняем его 
    if args.script:
        run_script(args.script)
    
    # 4. Интерактивный режим (Этап 1 + Этап 2)
    print("Эмулятор (Этап 1 + Этап 2)")
    while True:
        vvod = input(priglashenie())
        if not execute_command(vvod):
            break


# ТОЧКА ВХОДА 
if __name__ == "__main__":
    main()