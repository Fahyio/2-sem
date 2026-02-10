import requests
import matplotlib.pyplot as plt
import pandas as pd

# ================== 1. Получение данных по API ==================
base_url = 'https://pokeapi.co/api/v2/'
limit = 10
url = f'{base_url}pokemon?limit={limit}'

response = requests.get(url)
pokemon_list = response.json()['results']  # список покемонов

# ================== 2. Парсинг JSON ==================
data = []

for idx, pokemon in enumerate(pokemon_list, start=1):
    pokemon_url = pokemon['url']
    pokemon_response = requests.get(pokemon_url)
    pokemon_details = pokemon_response.json()

    # Получаем характеристики
    stats = {stat['stat']['name']: stat['base_stat'] for stat in pokemon_details['stats']}

    pokemon_data = {
        'id': idx,
        'name': pokemon['name'],
        'height': pokemon_details['height'],
        'weight': pokemon_details['weight'],
        'hp': stats.get('hp', 0),
        'attack': stats.get('attack', 0),
        'defense': stats.get('defense', 0),
        'speed': stats.get('speed', 0),  # дополнительно
        'special-attack': stats.get('special-attack', 0),  # дополнительно
        'special-defense': stats.get('special-defense', 0)  # дополнительно
    }
    data.append(pokemon_data)

# Преобразуем в DataFrame для удобства
df = pd.DataFrame(data)

# ================== 3. Визуализация ==================
# График 1: Линейный график - рост покемонов
plt.figure(figsize=(12, 8))

plt.subplot(2, 3, 1)
plt.plot(df['name'], df['height'], marker='o', color='green', linewidth=2)
plt.title('Рост покемонов (height)')
plt.xticks(rotation=45)
plt.ylabel('Рост')
plt.grid(True, linestyle='--', alpha=0.5)

# График 2: Точечная диаграмма - вес vs рост (с подписями точек)
plt.subplot(2, 3, 2)
plt.scatter(df['height'], df['weight'], color='blue', s=100, alpha=0.7)
plt.xlabel('Рост')
plt.ylabel('Вес')
plt.title('Вес vs Рост покемонов')
plt.grid(True, linestyle='--', alpha=0.5)

# Добавляем подписи для каждой точки
for i, (name, height, weight) in enumerate(zip(df['name'], df['height'], df['weight'])):
    plt.annotate(
        name,
        (height, weight),
        textcoords="offset points",
        xytext=(0, 10),  # смещение подписи от точки
        ha='center',
        fontsize=8,
        alpha=0.8
    )

# График 3: Столбчатая диаграмма - атака
plt.subplot(2, 3, 3)
plt.bar(df['name'], df['attack'], color='red', edgecolor='black')
plt.title('Уровень атаки покемонов')
plt.xticks(rotation=45)
plt.ylabel('Атака')
plt.grid(axis='y', linestyle='--', alpha=0.5)

# График 4: Горизонтальная столбчатая диаграмма - здоровье (HP)
plt.subplot(2, 3, 4)
plt.barh(df['name'], df['hp'], color='orange', edgecolor='black')
plt.title('Здоровье (HP) покемонов')
plt.xlabel('HP')
plt.grid(axis='x', linestyle='--', alpha=0.5)

# График 5: Гистограмма распределения защиты
plt.subplot(2, 3, 5)
plt.hist(df['defense'], bins=5, color='purple', edgecolor='black', alpha=0.7)
plt.title('Распределение защиты покемонов')
plt.xlabel('Защита')
plt.ylabel('Количество')
plt.grid(True, linestyle='--', alpha=0.5)

# График 6: Круговая диаграмма - соотношение скоростей (дополнительно)
plt.subplot(2, 3, 6)
plt.pie(df['speed'], labels=df['name'], autopct='%1.1f%%', startangle=90, colors=plt.cm.tab20.colors)
plt.title('Доля скорости покемонов')

plt.tight_layout()
plt.show()