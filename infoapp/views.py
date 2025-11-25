from django.http import HttpResponse, HttpResponseRedirect
from .data import storage
from django.views.decorators.http import require_GET
import html

def html_page(title: str, body: str, status: int = 200) -> HttpResponse:
    full = f"""
    <!doctype html>
    <html lang="uk">
    <head>
      <meta charset="utf-8">
      <title>{html.escape(title)}</title>
      <meta name="viewport" content="width=device-width,initial-scale=1">
      <style>
        table {{ border-collapse: collapse; width: 100%; }}
        td, th {{ border: 1px solid #444; padding: 8px; text-align: left; }}
        thead {{ background: #f0f0f0; }}
        a {{ color: #06c; }}
      </style>
    </head>
    <body>
      <h1>{html.escape(title)}</h1>
      {body}
      <hr>
      <small>Demo Django app — відображення та маршрутизація</small>
    </body>
    </html>
    """
    return HttpResponse(full, status=status)

@require_GET
def home(request):
    bloggers = storage.list_all()
    rows = []
    for b in bloggers:
        latest = b.get('posts', [])[:2]
        latest_html = '<ul>' + ''.join(f"<li>{html.escape(p['title'])} ({html.escape(p['type'])})</li>" for p in latest) + '</ul>'
        rows.append(f"<tr><td><a href=\"/profiles/{html.escape(str(b['slug']))}/\">{html.escape(b['name'])}</a></td><td>{html.escape(b['category'])}</td><td>{latest_html}</td></tr>")

    table = """
    <h2>Останні публікації</h2>
    <table>
      <thead><tr><th>Ім'я</th><th>Категорія</th><th>Останні пости</th></tr></thead>
      <tbody>
        %s
      </tbody>
    </table>
    <p><a href='/profiles/'>Переглянути всі профілі</a> | <a href='/news/list/'>Новини (список)</a> | <a href='/news/'>Новини (redirect)</a></p>
    """ % ('\n'.join(rows))

    return html_page('Головна — Блогери', table)

@require_GET
def profiles_list(request):
    bloggers = storage.list_all()
    rows = []
    for b in bloggers:
        rows.append(
            "<tr>"
            f"<td><a href=\"/profiles/{html.escape(str(b['slug']))}/\">{html.escape(b['name'])}</a></td>"
            f"<td>{html.escape(b['category'])}</td>"
            f"<td>{html.escape(b['short'])}</td>"
            "</tr>"
        )

    table = """
    <table>
      <thead><tr><th>Ім'я</th><th>Категорія</th><th>Коротко</th></tr></thead>
      <tbody>
        %s
      </tbody>
    </table>
    """ % ('\n'.join(rows))

    return html_page('Сторінка профілів', table)

@require_GET
def profile_detail(request, key):
    b = storage.get_by_slug_or_id(key)
    if not b:
        body = f"<p>Блогер з ідентифікатором <strong>{html.escape(key)}</strong> не знайдений.</p>"
        body += "<p><a href='/profiles/'>Повернутися до списку профілів</a></p>"
        return html_page('404 — Не знайдено блогера', body, status=404)

    socials_rows = ''.join(f"<li>{html.escape(k)}: <a href=\"{html.escape(v)}\">{html.escape(v)}</a></li>" for k, v in b.get('socials', {}).items())
    posts_rows = ''.join(f"<li>{html.escape(p['title'])} ({html.escape(p['type'])})</li>" for p in b.get('posts', []))

    body = f"""
    <h2>{html.escape(b['name'])}</h2>
    <table>
      <tr><th>Категорія</th><td>{html.escape(b['category'])}</td></tr>
      <tr><th>Коротко</th><td>{html.escape(b['short'])}</td></tr>
      <tr><th>Соціальні мережі</th><td><ul>{socials_rows}</ul></td></tr>
      <tr><th>Пости</th><td><ul>{posts_rows}</ul></td></tr>
    </table>
    <p><a href='/profiles/'>Назад до списку профілів</a></p>
    """

    return html_page(f"Профіль — {b['name']}", body)

@require_GET
def news_redirect(request):
    return HttpResponseRedirect('/')

@require_GET
def news_list(request):
    bloggers = storage.list_all()
    items = []
    for b in bloggers:
        for p in b.get('posts', []):
            items.append({'who': b['name'], 'title': p['title'], 'type': p['type']})

    rows = ''.join(f"<tr><td>{html.escape(i['who'])}</td><td>{html.escape(i['title'])}</td><td>{html.escape(i['type'])}</td></tr>" for i in items)
    table = f"""
    <h2>Новини зі світу блогерів</h2>
    <table>
      <thead><tr><th>Блогер</th><th>Заголовок</th><th>Тип</th></tr></thead>
      <tbody>
        {rows}
      </tbody>
    </table>
    """
    return html_page('Новини — Блогери', table)
