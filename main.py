import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

# Инициализация Flask приложения
app = Flask(__name__)

# Функция для получения данных с сайта
def get_product_info():
    url = 'https://www.ipp-ips.com/Products/Helmets-Hoods/'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }

    # Отправляем запрос
    response = requests.get(url, headers=headers)

    # Разбираем HTML страницу
    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим все div с классом card-body
    card_bodies = soup.find_all('div', class_='card-body')

    # Сохраняем данные о каждом товаре в список
    products = []

    for card in card_bodies:
        # Ищем название товара
        name_tag = card.find('a', class_='product-name')
        name = name_tag.text.strip() if name_tag else 'Не указано'

        # Ищем ссылку на картинку товара
        img_tag = card.find('div', class_='product-image-wrapper').find('img')
        img_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else 'Нет изображения'

        # Ищем описание товара
        description_tag = card.find('div', class_='product-description')
        description = description_tag.text.strip() if description_tag else 'Нет описания'

        # Ищем цену товара
        price_tag = card.find('div', class_='product-price-info')
        price = price_tag.text.strip() if price_tag else 'Цена не указана'

        # Добавляем данные в список
        products.append({
            'name': name,
            'image_url': img_url,
            'description': description,
            'price': price
        })

    return products

# Эндпоинт для API
@app.route('/api/products', methods=['GET'])
def get_products_api():
    products = get_product_info()
    return jsonify(products)  # Возвращаем данные как JSON

if __name__ == '__main__':
    app.run(debug=True)
