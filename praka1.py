import os
import socket
import getpass

# 1. ФУНКЦИЯ ПРИГЛАШЕНИЯ
def priglashenie():
    user = getpass.getuser()
    host = socket.gethostname()
    papka = os.getcwd()
    home = os.path.expanduser("~")
    
    
    papka = papka.replace("\\", "/")
    home = home.replace("\\", "/")
    
    
    if papka.startswith(home):
        papka = "~" + papka[len(home):]
        
    return user + "@" + host + ":" + papka + "$ "


def raskryt(slova):
    result = []
    for slovo in slova:
        if slovo.startswith("$"):
            peremennaya = slovo[1:] # Убираем $
            result.append(os.environ.get(peremennaya, ""))
        else:
            result.append(slovo)
    return result


def main():
    print("Мой эмулятор (Этап 1)")
    
    while True:
        vvod = input(priglashenie())
        
        if vvod == "":
            continue
            
        # Разбиваем строку на слова
        slova = vvod.split()
        
        # Раскрываем переменные
        slova = raskryt(slova)
        
        komanda = slova[0]
        argumenty = slova[1:]
        
        if komanda == "exit":
            print("Пока!")
            break
            
        elif komanda == "ls":
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


main()