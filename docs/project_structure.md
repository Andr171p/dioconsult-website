## Пример структуры проекта

```text
dio_website/                  ← корень репозитория (git repo)
├── config/                    ← вся конфигурация проекта (вместо mysite/settings)
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── dev.py
│   │   ├── test.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
│
├── core/                      ← общие утилиты, миксины, абстрактные модели, wagtail хуки
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── abstract.py        ← AbstractPage, AbstractStreamBlock и т.д.
│   ├── templatetags/
│   ├── utils/
│   └── wagtail_hooks.py
│
├── home/                      ← главная страница + часто используемые базовые страницы
│   ├── __init__.py
│   ├── models.py
│   ├── blocks.py              (если есть специфические блоки только для home)
│   └── templates/
│       └── home/
│           └── home_page.html
│
├── pages/                     ← самые важные страницы сайта (Blog, Article, Landing и т.д.)
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── blog.py
│   │   ├── article.py
│   │   └── landing.py
│   └── templates/
│       └── pages/
│           ├── blog_page.html
│           └── article_page.html
│
├── blog/                      ← если блог — очень важная и большая часть проекта
│   ├── __init__.py
│   ├── models.py
│   ├── blocks.py
│   ├── views.py               (если нужны кастомные списки/архивы)
│   └── templates/
│       └── blog/
│
├── components/   или   blocks/   ← переиспользуемые StreamField-блоки
│   ├── __init__.py
│   ├── hero.py
│   ├── cta.py
│   ├── rich_text.py
│   ├── cards/
│   │   ├── __init__.py
│   │   └── teaser_card.py
│   └── templates/
│       └── components/
│           └── hero.html
│
├── snippets/                  ← wagtail.snippets (авторы, теги, контакты, промо-баннеры…)
│   ├── __init__.py
│   ├── models.py
│   └── templates/
│       └── snippets/
│
├── search/                    ← поиск (часто оставляют как в wagtail start)
│   ├── __init__.py
│   ├── views.py
│   └── templates/
│       └── search/
│           └── search.html
│
├── static/                    ← или src/static, если используете vite/esbuild
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/                 ← глобальные шаблоны
│   ├── base.html
│   ├── 404.html
│   ├── 500.html
│   └── includes/
│       ├── header.html
│       └── footer.html
│
├── media/                     ← пользовательские файлы (git ignore)
├── manage.py
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── production.txt
├── .env
├── .gitignore
└── pyproject.toml   или   setup.cfg   (black, ruff, isort настройки)
```


```text
myproject/
├── config/
│   ├── settings/
│   │   └── base.py
│   └── urls.py
├── core/                  ← общие вещи
├── home/
├── pages/
├── tickets/               ← ← ← наше приложение с тикетами
│   ├── migrations/
│   ├── templatetags/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py           ← TicketForm, CommentForm
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── templates/
│       └── tickets/
│           ├── base.html
│           ├── ticket_list.html
│           ├── ticket_detail.html
│           ├── ticket_create.html
│           └── comment_form.html
├── components/
├── snippets/
├── templates/
└── manage.py
```

