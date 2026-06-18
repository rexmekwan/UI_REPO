"""
Single-file Django mini-site: login + Home, About, Contact pages.

Run:
    pip install django
    python ui_repo.py runserver

Then open http://127.0.0.1:8000/
"""
import sys
from string import Template

import django
from django.conf import settings

settings.configure(
    DEBUG=True,
    SECRET_KEY='django-insecure-single-file-demo-key',
    ALLOWED_HOSTS=['*'],
    ROOT_URLCONF=__name__,
    MIDDLEWARE=[
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ],
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.sessions',
    ],
    # Cookie-backed sessions — no database/migrations required.
    SESSION_ENGINE='django.contrib.sessions.backends.signed_cookies',
    SESSION_EXPIRE_AT_BROWSER_CLOSE=True,
    DEFAULT_AUTO_FIELD='django.db.models.BigAutoField',
)
django.setup()

from django.urls import path                       # noqa: E402
from django.shortcuts import redirect               # noqa: E402
from django.http import HttpResponse                # noqa: E402
from django.middleware.csrf import get_token        # noqa: E402
from django.utils.html import escape                # noqa: E402

# $ has special meaning in string.Template, CSS/HTML below has none,
# so plain $placeholder substitution is used instead of str.format()
# to avoid clashing with the literal { } braces in the CSS.
PAGE = Template("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>$title</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  :root{
    --ink-900:#0a0e1a;
    --ink-700:#1c2438;
    --violet-700:#3d2c6b;
    --teal-600:#1f6f78;
    --gold-500:#f2b84b;
    --mist-100:#eef1f7;
    --mist-400:#9aa3b8;
    --danger:#ff6b6b;
    --success:#5fd99a;
  }
  *{box-sizing:border-box;}
  html{overflow-x:hidden;}
  body{
    margin:0;
    min-height:100vh;
    background:var(--ink-900);
    font-family:'Inter',sans-serif;
    color:var(--mist-100);
    position:relative;
  }
  .blob{position:absolute;border-radius:50%;filter:blur(80px);opacity:.55;pointer-events:none;}
  .blob-1{width:520px;height:520px;background:var(--violet-700);top:-160px;left:-140px;animation:drift1 16s ease-in-out infinite;}
  .blob-2{width:460px;height:460px;background:var(--teal-600);bottom:-180px;right:-120px;animation:drift2 18s ease-in-out infinite;}
  @keyframes drift1{0%,100%{transform:translate(0,0) scale(1);}50%{transform:translate(60px,40px) scale(1.08);}}
  @keyframes drift2{0%,100%{transform:translate(0,0) scale(1);}50%{transform:translate(-50px,-30px) scale(1.05);}}

  .center-wrap{position:relative;z-index:1;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px;}

  .nav{position:sticky;top:0;z-index:2;background:rgba(10,14,26,0.72);backdrop-filter:blur(14px);border-bottom:1px solid rgba(255,255,255,0.08);}
  .nav-inner{max-width:760px;margin:0 auto;padding:16px 24px;display:flex;align-items:center;gap:28px;}
  .brand{font-family:'Sora',sans-serif;font-weight:700;font-size:16px;color:var(--mist-100);margin-right:auto;}
  .nav-links{display:flex;gap:20px;}
  .nav-links a{color:var(--mist-400);text-decoration:none;font-size:14px;font-weight:500;padding:6px 2px;border-bottom:2px solid transparent;transition:color .15s, border-color .15s;}
  .nav-links a:hover{color:var(--mist-100);}
  .nav-links a.active{color:var(--mist-100);border-bottom-color:var(--gold-500);}
  .nav-logout-form{margin:0;}
  button.nav-logout{padding:8px 14px;border-radius:8px;border:1px solid rgba(255,255,255,0.12);background:transparent;color:var(--mist-100);font-family:'Inter',sans-serif;font-weight:500;font-size:13px;cursor:pointer;transition:background .12s ease;}
  button.nav-logout:hover{background:rgba(255,255,255,0.06);}

  .page-content{position:relative;z-index:1;max-width:760px;margin:0 auto;padding:48px 24px 64px;display:flex;justify-content:center;}

  .card{position:relative;z-index:1;width:100%;max-width:380px;padding:40px 36px 36px;background:rgba(255,255,255,0.045);border:1px solid rgba(255,255,255,0.08);border-radius:20px;backdrop-filter:blur(18px);box-shadow:0 30px 60px -20px rgba(0,0,0,.6);animation:fadeIn .35s ease both;}
  .card.dashboard-card{max-width:420px;text-align:center;}
  .card.wide{max-width:640px;text-align:left;}
  .card.wide p{color:var(--mist-400);font-size:14.5px;line-height:1.7;margin:0 0 16px;}
  .card.wide p:last-child{margin-bottom:0;}
  @keyframes fadeIn{from{opacity:0;transform:translateY(6px);}to{opacity:1;transform:translateY(0);}}

  .mark,.avatar{border-radius:12px;background:linear-gradient(135deg,var(--gold-500),#d98f2b);display:flex;align-items:center;justify-content:center;font-family:'Sora',sans-serif;font-weight:700;color:var(--ink-900);}
  .mark{width:42px;height:42px;margin-bottom:22px;font-size:18px;}
  .avatar{width:64px;height:64px;border-radius:50%;font-size:24px;margin:0 auto 20px;}

  h1{font-family:'Sora',sans-serif;font-size:24px;font-weight:700;margin:0 0 6px;letter-spacing:-0.01em;word-break:break-word;}
  .sub{color:var(--mist-400);font-size:14px;margin:0 0 28px;line-height:1.5;}

  label{display:block;font-size:13px;font-weight:500;color:var(--mist-400);margin-bottom:7px;}
  .field{margin-bottom:18px;}
  input,textarea{width:100%;padding:13px 14px;background:var(--ink-700);border:1px solid rgba(255,255,255,0.08);border-radius:10px;color:var(--mist-100);font-family:'Inter',sans-serif;font-size:14.5px;outline:none;transition:border-color .15s, box-shadow .15s;}
  textarea{resize:vertical;min-height:110px;}
  input::placeholder,textarea::placeholder{color:#5b6478;}
  input:focus-visible,textarea:focus-visible{border-color:var(--gold-500);box-shadow:0 0 0 3px rgba(242,184,75,0.18);}

  .error{font-size:13px;color:var(--danger);margin:-6px 0 16px;}
  .success{font-size:13px;color:var(--success);margin:-6px 0 16px;}

  button.submit{width:100%;padding:13px;margin-top:6px;border:none;border-radius:10px;background:var(--gold-500);color:var(--ink-900);font-family:'Sora',sans-serif;font-weight:600;font-size:14.5px;cursor:pointer;transition:transform .12s ease, box-shadow .12s ease;}
  button.submit:hover{transform:translateY(-1px);box-shadow:0 10px 24px -10px rgba(242,184,75,0.5);}
  button.submit:active{transform:translateY(0);}
  button.submit:focus-visible{outline:2px solid var(--mist-100);outline-offset:2px;}

  .foot{text-align:center;font-size:12.5px;color:var(--mist-400);margin-top:22px;}

  @media (prefers-reduced-motion: reduce){.blob-1,.blob-2{animation:none;}.card{animation:none;}}
</style>
</head>
<body>
  <div class="blob blob-1" aria-hidden="true"></div>
  <div class="blob blob-2" aria-hidden="true"></div>
  $body
</body>
</html>""")

LOGIN_BODY = Template("""
<main class="card">
  <div class="mark">A</div>
  <h1>Welcome back</h1>
  <p class="sub">Sign in to continue. Any username and password will work &mdash; this is a demo flow.</p>
  <form method="post" novalidate>
    <input type="hidden" name="csrfmiddlewaretoken" value="$csrf">
    <div class="field">
      <label for="username">Username</label>
      <input type="text" id="username" name="username" placeholder="Enter your name" autocomplete="username" value="$username" required>
    </div>
    <div class="field">
      <label for="password">Password</label>
      <input type="password" id="password" name="password" placeholder="Enter your password" autocomplete="current-password" required>
    </div>
    $error_html
    <button type="submit" class="submit">Sign in</button>
  </form>
  <p class="foot">No account needed &mdash; this page logs you in regardless.</p>
</main>
""")

NAV = Template("""
<nav class="nav">
  <div class="nav-inner">
    <span class="brand">DemoCo</span>
    <div class="nav-links">
      <a href="/dashboard/" class="$home_cls">Home</a>
      <a href="/about/" class="$about_cls">About</a>
      <a href="/contact/" class="$contact_cls">Contact</a>
    </div>
    <form method="post" action="/logout/" class="nav-logout-form">
      <input type="hidden" name="csrfmiddlewaretoken" value="$csrf">
      <button type="submit" class="nav-logout">Log out</button>
    </form>
  </div>
</nav>
""")

PAGE_CONTENT_WRAP = Template("""$nav
<div class="page-content">
  $content
</div>""")

HOME_CARD = Template("""
<main class="card dashboard-card">
  <div class="avatar">$initial</div>
  <h1>Welcome, $username</h1>
  <p class="sub">You're signed in. Use the nav above to look around.</p>
</main>
""")

ABOUT_CARD = Template("""
<main class="card wide">
  <h1>About this site</h1>
  <p>This is a small demo site that runs entirely from one Python file using Django. There's no database and no real accounts &mdash; the login screen accepts any username and password and starts a session.</p>
  <p>It exists to show a minimal multi-page flow: a login gate, a home screen, and a couple of content pages, all wired together with plain Django views and inline templates.</p>
</main>
""")

CONTACT_CARD = Template("""
<main class="card wide">
  <h1>Contact</h1>
  <p>Send a message below. Nothing is actually emailed &mdash; this just echoes it back to show the form works end to end.</p>
  <form method="post" novalidate>
    <input type="hidden" name="csrfmiddlewaretoken" value="$csrf">
    <div class="field">
      <label for="name">Name</label>
      <input type="text" id="name" name="name" placeholder="Your name" value="$name" required>
    </div>
    <div class="field">
      <label for="email">Email</label>
      <input type="email" id="email" name="email" placeholder="you@example.com" value="$email" required>
    </div>
    <div class="field">
      <label for="message">Message</label>
      <textarea id="message" name="message" placeholder="Say something...">$message</textarea>
    </div>
    $status_html
    <button type="submit" class="submit">Send message</button>
  </form>
</main>
""")


def render_nav(request, active):
    return NAV.substitute(
        csrf=get_token(request),
        home_cls='active' if active == 'home' else '',
        about_cls='active' if active == 'about' else '',
        contact_cls='active' if active == 'contact' else '',
    )


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            card = LOGIN_BODY.substitute(
                csrf=get_token(request),
                username=escape(username),
                error_html='<p class="error">Please fill in both fields.</p>',
            )
            return HttpResponse(PAGE.substitute(title='Sign in', body=f'<div class="center-wrap">{card}</div>'))

        # No real authentication — any non-empty pair is accepted by design.
        request.session['username'] = username
        return redirect('/dashboard/')

    card = LOGIN_BODY.substitute(csrf=get_token(request), username='', error_html='')
    return HttpResponse(PAGE.substitute(title='Sign in', body=f'<div class="center-wrap">{card}</div>'))


def dashboard_view(request):
    username = request.session.get('username')
    if not username:
        return redirect('/')

    card = HOME_CARD.substitute(username=escape(username), initial=escape(username[0].upper()))
    body = PAGE_CONTENT_WRAP.substitute(nav=render_nav(request, 'home'), content=card)
    return HttpResponse(PAGE.substitute(title='Home', body=body))


def about_view(request):
    if not request.session.get('username'):
        return redirect('/')

    body = PAGE_CONTENT_WRAP.substitute(nav=render_nav(request, 'about'), content=ABOUT_CARD.substitute())
    return HttpResponse(PAGE.substitute(title='About', body=body))


def contact_view(request):
    if not request.session.get('username'):
        return redirect('/')

    name = email = message = ''
    status_html = ''

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        if not name or not email or not message:
            status_html = '<p class="error">Please fill in all fields.</p>'
        else:
            status_html = f'<p class="success">Thanks, {escape(name)} &mdash; your message has been received.</p>'
            name = email = message = ''  # clear the form after a successful "send"

    card = CONTACT_CARD.substitute(
        csrf=get_token(request),
        name=escape(name),
        email=escape(email),
        message=escape(message),
        status_html=status_html,
    )
    body = PAGE_CONTENT_WRAP.substitute(nav=render_nav(request, 'contact'), content=card)
    return HttpResponse(PAGE.substitute(title='Contact', body=body))


def logout_view(request):
    if request.method == 'POST':
        request.session.flush()
    return redirect('/')


urlpatterns = [
    path('', login_view),
    path('dashboard/', dashboard_view),
    path('about/', about_view),
    path('contact/', contact_view),
    path('logout/', logout_view),
]

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)