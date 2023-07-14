import vk_scripts
import datetime


def main():
    print("Добро пожаловать! Это программа со скриптами для VK!\nСоздатель: damvih\n")
    token = input("Введите токен: ")
    print("Токен введен!")
    while True:
        n = int(input("Меню:\n1. Фотоконкурс\n\n0. Выход из программы\nВыберите функцию: "))
        if n == 1:
            link = input("Введите ссылку на альбом: ")
            time_start = datetime.datetime.now()
            print(f"[INFO] Время запуска: {time_start}")
            result = vk_scripts.photo_contest.get_winner(token, link)
            while result == "0/0 ошибка...":
                print("[INFO] '0/0' ошибка! Перезапуск скрипта...")
                result = vk_scripts.photo_contest.get_winner(token, link)
            print(f"[INFO] Выводим результат...\n{result}")
        elif n == 0:
            print("[INFO] Выход из программы...")
            break
        else:
            print(f"Функции с номером '{n}' не существует! Попробуйте еще раз!")
    return


if __name__ == "__main__":
    main()
