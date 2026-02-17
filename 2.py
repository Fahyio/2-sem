import re
from typing import List, Dict, Optional


# ===== 1. Валидация логина =====
def validate_login(login: str) -> bool:
    """
    Валидация логина по критериям:
    - Начинается с буквы
    - Содержит только латиницу, цифры и _
    - Длина 5-20 символов
    - Не заканчивается _
    """
    if len(login) < 5 or len(login) > 20:
        return False

    if not login[0].isalpha():
        return False

    if login[-1] == '_':
        return False

    # Проверяем, что все символы допустимы
    pattern = r'^[a-zA-Z0-9_]+$'
    if not re.match(pattern, login):
        return False

    # Проверяем, что есть хотя бы одна буква (логин начинается с буквы, но мог состоять только из цифр и _)
    if not any(c.isalpha() for c in login):
        return False

    return True


# ===== 2. Поиск дат в тексте =====
def find_dates(text: str) -> List[str]:
    """
    Поиск дат в форматах:
    - DD.MM.YYYY
    - DD-MM-YYYY
    - DD/MM/YYYY
    День и месяц могут быть 1-2 цифры, год 2 или 4 цифры
    """
    # Регулярное выражение для всех форматов дат
    pattern = r'\b(\d{1,2})[./-](\d{1,2})[./-](\d{2,4})\b'

    dates = []
    for match in re.finditer(pattern, text):
        day, month, year = match.groups()

        # Проверяем валидность даты (базовая проверка)
        try:
            day_int = int(day)
            month_int = int(month)
            year_int = int(year)

            # Базовые проверки
            if 1 <= day_int <= 31 and 1 <= month_int <= 12:
                # Форматируем год
                if len(year) == 2:
                    year_full = f"20{year}" if int(year) <= 50 else f"19{year}"
                else:
                    year_full = year

                # Форматируем день и месяц
                day_formatted = f"{day_int:02d}"
                month_formatted = f"{month_int:02d}"

                # Восстанавливаем оригинальный формат с разделителем
                separator = match.group(0)[len(day):len(day) + 1]
                date_str = f"{day_formatted}{separator}{month_formatted}{separator}{year_full}"
                dates.append(date_str)
        except ValueError:
            continue

    return dates


# ===== 3. Парсинг логов =====
def parse_log(log_line: str) -> Dict[str, str]:
    """
    Парсинг строки лога в формате:
    2024-02-10 14:23:01 INFO user=ada action=login ip=192.168.1.15
    """
    result = {}

    # Разбиваем строку по пробелам
    parts = log_line.split()

    if len(parts) >= 6:
        # Дата и время
        result['date'] = parts[0]
        result['time'] = parts[1]

        # Парсим остальные параметры
        for part in parts[3:]:
            if '=' in part:
                key, value = part.split('=', 1)
                result[key] = value

    return result


# ===== 4. Проверка пароля =====
def validate_password(password: str) -> bool:
    """
    Проверка пароля по критериям:
    - Минимум 8 символов
    - Хотя бы одна заглавная буква
    - Хотя бы одна строчная буква
    - Хотя бы одна цифра
    - Хотя бы один спецсимвол !@#$%^&*
    """
    if len(password) < 8:
        return False

    # Проверяем наличие заглавных букв
    if not re.search(r'[A-Z]', password):
        return False

    # Проверяем наличие строчных букв
    if not re.search(r'[a-z]', password):
        return False

    # Проверяем наличие цифр
    if not re.search(r'\d', password):
        return False

    # Проверяем наличие спецсимволов
    if not re.search(r'[!@#$%^&*]', password):
        return False

    return True


# ===== 5. E-mail с ограниченными доменами =====
def validate_email_with_domains(email: str, domains: List[str]) -> bool:
    """
    Проверка email с ограничением доменов
    """
    # Базовый паттерн для email
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if not re.match(email_pattern, email):
        return False

    # Извлекаем домен
    domain = email.split('@')[1]

    # Проверяем, что домен в списке допустимых
    if domain not in domains:
        return False

    return True


# ===== 6. Нормализация телефонных номеров =====
def normalize_phone(phone: str) -> str:
    """
    Нормализация телефонного номера в формат +79991234567
    """
    # Удаляем все символы, кроме цифр
    digits = re.sub(r'\D', '', phone)

    # Если номер начинается с 7 или 8 (российский номер)
    if digits.startswith('8'):
        digits = '7' + digits[1:]

    # Если номер начинается не с 7, добавляем 7
    if not digits.startswith('7'):
        digits = '7' + digits

    # Проверяем длину номера
    if len(digits) != 11:
        # Если номер короче, добавляем нули
        if len(digits) < 11:
            digits = digits.ljust(11, '0')
        # Если номер длиннее, обрезаем
        else:
            digits = digits[:11]

    return f"+{digits}"


# ===== Функции для ввода с клавиатуры =====
def input_validate_login():
    """Ввод и проверка логина с клавиатуры"""
    print("\n--- Проверка логина ---")
    print("\nГотовые примеры для тестирования:")
    print("  Корректные: User123, john_doe, admin_1, Python123")
    print("  Некорректные: 123user (начинается с цифры), user_ (заканчивается _), a (слишком короткий)")

    login = input("\nВведите логин для проверки: ")
    result = validate_login(login)
    print(f"Результат: {'✓ Корректный' if result else '✗ Некорректный'} логин")
    return result


def input_find_dates():
    """Ввод текста и поиск дат"""
    print("\n--- Поиск дат в тексте ---")
    print("\nГотовые примеры для тестирования:")
    print("  Текст 1: Сегодня 10.02.2024, а завтра 11-02-24. Встреча 5/12/2023")
    print("  Текст 2: Срок сдачи 25.12.2023 и 01-01-24. План на 30/02/2023")

    text = input("\nВведите текст для поиска дат: ")
    dates = find_dates(text)
    if dates:
        print(f"Найденные даты: {dates}")
    else:
        print("Даты не найдены")
    return dates


def input_parse_log():
    """Ввод строки лога и её парсинг"""
    print("\n--- Парсинг лога ---")
    print("Формат: YYYY-MM-DD HH:MM:SS LEVEL key=value key=value ...")
    print("\nГотовые примеры:")
    print("  1. 2024-02-10 14:23:01 INFO user=ada action=login ip=192.168.1.15")
    print("  2. 2024-02-10 15:30:45 ERROR user=bob action=upload file=doc.pdf size=1024")
    print("  3. 2024-02-10 16:15:22 WARNING user=charlie action=delete status=partial")

    log_line = input("\nВведите строку лога: ")
    result = parse_log(log_line)
    if result:
        print("Результат парсинга:")
        for key, value in result.items():
            print(f"  {key}: {value}")
    else:
        print("Не удалось распарсить лог (недостаточно данных)")
    return result


def input_validate_password():
    """Ввод и проверка пароля"""
    print("\n--- Проверка пароля ---")
    print("Требования: минимум 8 символов, заглавная буква, строчная буква, цифра, спецсимвол (!@#$%^&*)")
    print("\nГотовые примеры:")
    print("  Корректные: Pass123!, StrongP@ss1, MyP@ssw0rd, Test123#")
    print("  Некорректные: password (нет заглавных и спецсимволов), PASSWORD123 (нет строчных), Pass! (короткий)")

    password = input("\nВведите пароль для проверки: ")
    result = validate_password(password)
    if result:
        print("✓ Пароль соответствует требованиям")
    else:
        print("✗ Пароль НЕ соответствует требованиям")
    return result


def input_validate_email():
    """Ввод email и проверка с доменами"""
    print("\n--- Проверка email ---")
    print("Допустимые домены: gmail.com, yandex.ru, edu.ru, mail.ru, outlook.com")
    print("\nГотовые примеры:")
    print("  Корректные: user@gmail.com, student@edu.ru, test@yandex.ru")
    print("  Некорректные: invalid@mail.ru (домен не в списке), bad-email (неверный формат)")

    email = input("\nВведите email для проверки: ")

    # Список допустимых доменов
    valid_domains = ['gmail.com', 'yandex.ru', 'edu.ru', 'mail.ru', 'outlook.com']

    result = validate_email_with_domains(email, valid_domains)
    if result:
        print(f"✓ Email '{email}' корректен и домен допустим")
    else:
        print(f"✗ Email '{email}' НЕ корректен или домен не в списке допустимых")
    return result


def input_normalize_phone():
    """Ввод и нормализация телефонного номера"""
    print("\n--- Нормализация телефона ---")
    print("Примеры форматов: 8(999)123-45-67, +7 999 123 45 67, 89991234567")
    print("\nГотовые примеры:")
    print("  1. 8(999)123-45-67 -> +79991234567")
    print("  2. +7 999 123 45 67 -> +79991234567")
    print("  3. 89991234567 -> +79991234567")
    print("  4. 8-999-123-45-67 -> +79991234567")

    phone = input("\nВведите телефонный номер: ")
    normalized = normalize_phone(phone)
    print(f"Исходный: {phone}")
    print(f"Нормализованный: {normalized}")
    return normalized


def show_examples():
    """Показать все готовые примеры"""
    print("\n" + "=" * 60)
    print("ГОТОВЫЕ ПРИМЕРЫ ДЛЯ ВСЕХ ФУНКЦИЙ")
    print("=" * 60)

    print("\n1. Валидация логина:")
    print("   Корректные: User123, john_doe, admin_1, Python123")
    print("   Некорректные: 123user (начинается с цифры), user_ (заканчивается _), a (слишком короткий)")

    print("\n2. Поиск дат в тексте:")
    print("   Текст 1: Сегодня 10.02.2024, а завтра 11-02-24. Встреча 5/12/2023")
    print("   Текст 2: Срок сдачи 25.12.2023 и 01-01-24. План на 30/02/2023")
    print("   Текст 3: Важные даты: 1.1.23, 31/12/2024, 15-05-22")

    print("\n3. Парсинг логов:")
    print("   1. 2024-02-10 14:23:01 INFO user=ada action=login ip=192.168.1.15")
    print("   2. 2024-02-10 15:30:45 ERROR user=bob action=upload file=doc.pdf size=1024")
    print("   3. 2024-02-10 16:15:22 WARNING user=charlie action=delete status=partial")

    print("\n4. Проверка пароля:")
    print("   Корректные: Pass123!, StrongP@ss1, MyP@ssw0rd, Test123#")
    print("   Некорректные: password (нет заглавных и спецсимволов), PASSWORD123 (нет строчных), Pass! (короткий)")

    print("\n5. Проверка email (допустимые домены: gmail.com, yandex.ru, edu.ru, mail.ru, outlook.com):")
    print("   Корректные: user@gmail.com, student@edu.ru, test@yandex.ru")
    print("   Некорректные: invalid@mail.ru (домен не в списке), bad-email (неверный формат)")

    print("\n6. Нормализация телефона:")
    print("   1. 8(999)123-45-67 -> +79991234567")
    print("   2. +7 999 123 45 67 -> +79991234567")
    print("   3. 89991234567 -> +79991234567")
    print("   4. 8-999-123-45-67 -> +79991234567")
    print("   5. 9991234567 -> +79991234567")


def interactive_menu():
    """Интерактивное меню для выбора функций"""
    while True:
        print("\n" + "=" * 60)
        print("ВЫБЕРИТЕ ФУНКЦИЮ ДЛЯ ТЕСТИРОВАНИЯ:")
        print("=" * 60)
        print("1. Проверка логина")
        print("2. Поиск дат в тексте")
        print("3. Парсинг лога")
        print("4. Проверка пароля")
        print("5. Проверка email")
        print("6. Нормализация телефона")
        print("7. Показать все готовые примеры")
        print("8. Запустить все тесты (автоматические)")
        print("0. Выход")
        print("-" * 60)

        choice = input("Ваш выбор (0-8): ").strip()

        if choice == '1':
            input_validate_login()
        elif choice == '2':
            input_find_dates()
        elif choice == '3':
            input_parse_log()
        elif choice == '4':
            input_validate_password()
        elif choice == '5':
            input_validate_email()
        elif choice == '6':
            input_normalize_phone()
        elif choice == '7':
            show_examples()
        elif choice == '8':
            test_all_functions()
        elif choice == '0':
            print("Программа завершена.")
            break
        else:
            print("Неверный выбор. Пожалуйста, введите число от 0 до 8.")

        if choice != '0':
            input("\nНажмите Enter для продолжения...")


# ===== Тестирование функций =====
def test_all_functions():
    """Тестирование всех функций"""
    print("\n=== Тестирование функций ===")

    # 1. Тест валидации логина
    print("\n1. Валидация логина:")
    test_logins = ["User123", "user_123", "123user", "u", "very_long_username_here", "user_", "_user"]
    for login in test_logins:
        print(f"  {login}: {validate_login(login)}")

    # 2. Тест поиска дат
    print("\n2. Поиск дат:")
    test_text = "Сегодня 10.02.2024, а завтра 11-02-24. Встреча 5/12/2023, дата 01.1.23"
    dates = find_dates(test_text)
    print(f"  Текст: {test_text}")
    print(f"  Найденные даты: {dates}")

    # 3. Тест парсинга логов
    print("\n3. Парсинг логов:")
    test_log = "2024-02-10 14:23:01 INFO user=ada action=login ip=192.168.1.15"
    parsed = parse_log(test_log)
    print(f"  Лог: {test_log}")
    print(f"  Результат: {parsed}")

    # 4. Тест проверки пароля
    print("\n4. Проверка пароля:")
    test_passwords = ["Pass123!", "password", "PASSWORD123", "Pass!", "Pass1234", "VeryStrongPass123!"]
    for pwd in test_passwords:
        print(f"  '{pwd}': {validate_password(pwd)}")

    # 5. Тест email с доменами
    print("\n5. Проверка email:")
    valid_domains = ['gmail.com', 'yandex.ru', 'edu.ru']
    test_emails = ["user@gmail.com", "test@yandex.ru", "invalid@mail.ru", "bad-email", "student@edu.ru"]
    for email in test_emails:
        print(f"  {email}: {validate_email_with_domains(email, valid_domains)}")

    # 6. Тест нормализации телефонов
    print("\n6. Нормализация телефонов:")
    test_phones = ["8(999)123-45-67", "+7 999 123 45 67", "89991234567", "9991234567", "8-999-123-45-67"]
    for phone in test_phones:
        normalized = normalize_phone(phone)
        print(f"  {phone} -> {normalized}")


# ===== Пример использования =====
if __name__ == "__main__":
    print("=" * 60)
    print("ПРОГРАММА ДЛЯ ТЕСТИРОВАНИЯ ФУНКЦИЙ")
    print("=" * 60)

    # Запуск интерактивного меню
    interactive_menu()

    # Примеры использования отдельных функций (оставлено для справки)
    print("\n=== Примеры использования ===")

    # Пример 1: Валидация логина
    login = "John_Doe123"
    print(f"\nВалидация логина '{login}': {validate_login(login)}")

    # Пример 2: Поиск дат
    text = "Встреча назначена на 25.12.2023 и 01-01-24"
    print(f"\nПоиск дат в тексте: {find_dates(text)}")

    # Пример 3: Парсинг лога
    log = "2024-02-10 14:23:01 INFO user=ada action=login ip=192.168.1.15"
    print(f"\nПарсинг лога: {parse_log(log)}")

    # Пример 4: Проверка пароля
    password = "MyPass123!"
    print(f"\nПроверка пароля '{password}': {validate_password(password)}")

    # Пример 5: Проверка email
    email = "student@edu.ru"
    domains = ['gmail.com', 'yandex.ru', 'edu.ru']
    print(f"\nПроверка email '{email}': {validate_email_with_domains(email, domains)}")

    # Пример 6: Нормализация телефона
    phone = "8 (999) 123-45-67"
    print(f"\nНормализация телефона '{phone}': {normalize_phone(phone)}")
