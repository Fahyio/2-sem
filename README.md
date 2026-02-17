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


# ===== Тестирование функций =====
def test_all_functions():
    """Тестирование всех функций"""
    print("=== Тестирование функций ===")

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
    # Запуск тестов
    test_all_functions()

    # Примеры использования отдельных функций
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
