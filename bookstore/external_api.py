import requests

def fetch_book_details(title, author):
    # Replace with your Google Books API key
    api_key = 'your_api_key'
    base_url = 'https://www.googleapis.com/books/v1/volumes'
    params = {'q': f'intitle:{title}+inauthor:{author}', 'key': api_key}

    response = requests.get(base_url, params=params)
    data = response.json()

    if 'items' in data and data['items']:
        book_info = data['items'][0]['volumeInfo']
        return {
            'summary': book_info.get('description', ''),
            'cover_url': book_info['imageLinks']['thumbnail'] if 'imageLinks' in book_info else ''
            
        }
    else:
        return {}