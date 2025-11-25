from typing import Dict, List

class BloggerStorage:
    def __init__(self):
        self._by_slug: Dict[str, Dict] = {}
        self._order: List[str] = []
        self._init_sample_data()

    def _init_sample_data(self):
        bloggers = [
            {
                'id': 1,
                'slug': 'anna-travels',
                'name': 'Анна Мандрівниця',
                'category': 'Подорожі',
                'short': 'Блоги про бюджетні подорожі та лайфхаки.',
                'socials': {
                    'instagram': 'https://instagram.com/anna_travels',
                    'youtube': 'https://youtube.com/annatravels',
                },
                'posts': [
                    {'title': 'Як зібрати рюкзак на 7 днів', 'type': 'article'},
                    {'title': 'Топ 10 локацій в Україні', 'type': 'video'},
                ],
            },
            {
                'id': 2,
                'slug': 'tech-ivan',
                'name': 'Іван Техно',
                'category': 'Технології',
                'short': 'Огляди ґаджетів, розбори та корисні поради.',
                'socials': {'twitter': 'https://twitter.com/tech_ivan'},
                'posts': [
                    {'title': 'Огляд смартфона X', 'type': 'article'},
                    {'title': 'Розбираємо материнські плати', 'type': 'video'},
                ],
            },
            {
                'id': 3,
                'slug': 'cooking-maria',
                'name': 'Марія Кухарка',
                'category': 'Кулінарія',
                'short': 'Рецепти домашньої кухні та швидкі сніданки.',
                'socials': {'facebook': 'https://facebook.com/cooking.maria'},
                'posts': [
                    {'title': '7 рецептів на сніданок', 'type': 'article'},
                ],
            },
        ]

        for b in bloggers:
            slug_key = str(b['slug'])
            self._by_slug[slug_key] = b
            self._order.append(slug_key)

    def list_all(self):
        return [self._by_slug[s] for s in self._order]

    def get_by_slug_or_id(self, key):
        try:
            int_key = int(key)
        except Exception:
            int_key = None

        if int_key is not None:
            for b in self._by_slug.values():
                if b.get('id') == int_key:
                    return b
        return self._by_slug.get(str(key))


storage = BloggerStorage()
