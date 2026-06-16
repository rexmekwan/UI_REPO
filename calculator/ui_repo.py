"""
Single-file Django login demo.

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
  }
  *{box-sizing:border-box;}
  html,body{height:100%;}
  body{
    margin:0;
    min-height:100vh;
    display:flex;
    align-items:center;
    justify-content:center;
    background:var(--ink-900);
    font-family:'Inter',sans-serif;
    color:var(--mist-100);
    position:relative;
    overflow:hidden;
  }
  .blob{position:absolute;border-radius:50%;filter:blur(80px);opacity:.55;pointer-events:none;}
  .blob-1{width:520px;height:520px;background:var(--violet-700);top:-160px;left:-140px;animation:drift1 16s ease-in-out infinite;}
  .blob-2{width:460px;height:460px;background:var(--teal-600);bottom:-180px;right:-120px;animation:drift2 18s ease-in-out infinite;}
  @keyframes drift1{0%,100%{transform:translate(0,0) scale(1);}50%{transform:translate(60px,40px) scale(1.08);}}
  @keyframes drift2{0%,100%{transform:translate(0,0) scale(1);}50%{transform:translate(-50px,-30px) scale(1.05);}}
  .card{position:relative;z-index:1;width:100%;max-width:380px;margin:24px;padding:40px 36px 36px;background:rgba(255,255,255,0.045);border:1px solid rgba(255,255,255,0.08);border-radius:20px;backdrop-filter:blur(18px);box-shadow:0 30px 60px -20px rgba(0,0,0,.6);animation:fadeIn .35s ease both;}
  .card.dashboard-card{max-width:420px;text-align:center;}
  @keyframes fadeIn{from{opacity:0;transform:translateY(6px);}to{opacity:1;transform:translateY(0);}}
  .mark,.avatar{border-radius:12px;background:linear-gradient(135deg,var(--gold-500),#d98f2b);display:flex;align-items:center;justify-content:center;font-family:'Sora',sans-serif;font-weight:700;color:var(--ink-900);}
  .mark{width:42px;height:42px;margin-bottom:22px;font-size:18px;}
  .avatar{width:64px;height:64px;border-radius:50%;font-size:24px;margin:0 auto 20px;}
  h1{font-family:'Sora',sans-serif;font-size:24px;font-weight:700;margin:0 0 6px;letter-spacing:-0.01em;word-break:break-word;}
  .sub{color:var(--mist-400);font-size:14px;margin:0 0 28px;line-height:1.5;}
  label{display:block;font-size:13px;font-weight:500;color:var(--mist-400);margin-bottom:7px;}
  .field{margin-bottom:18px;}
  input{width:100%;padding:13px 14px;background:var(--ink-700);border:1px solid rgba(255,255,255,0.08);border-radius:10px;color:var(--mist-100);font-family:'Inter',sans-serif;font-size:14.5px;outline:none;transition:border-color .15s, box-shadow .15s;}
  input::placeholder{color:#5b6478;}
  input:focus-visible{border-color:var(--gold-500);box-shadow:0 0 0 3px rgba(242,184,75,0.18);}
  .error{font-size:13px;color:var(--danger);margin:-6px 0 16px;}
  button.submit,button.logout{width:100%;padding:13px;border:none;border-radius:10px;font-family:'Sora',sans-serif;font-weight:600;font-size:14.5px;cursor:pointer;transition:transform .12s ease, box-shadow .12s ease, background .12s ease;}
  button.submit{margin-top:6px;background:var(--gold-500);color:var(--ink-900);}
  button.submit:hover{transform:translateY(-1px);box-shadow:0 10px 24px -10px rgba(242,184,75,0.5);}
  button.logout{background:transparent;color:var(--mist-100);border:1px solid rgba(255,255,255,0.12);}
  button.logout:hover{background:rgba(255,255,255,0.06);transform:translateY(-1px);}
  button.submit:active,button.logout:active{transform:translateY(0);}
  button.submit:focus-visible,button.logout:focus-visible{outline:2px solid var(--mist-100);outline-offset:2px;}
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

DASHBOARD_BODY = Template("""
<main class="card dashboard-card">
  <div class="avatar">$initial</div>
  <h1>Welcome, $username</h1>
  <p class="sub">You're signed in. This page is reachable only after submitting the login form.</p>
  <form method="post" action="/logout/">
    <input type="hidden" name="csrfmiddlewaretoken" value="$csrf">
    <button type="submit" class="logout">Log out</button>
  </form>
</main>
""")


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            body = LOGIN_BODY.substitute(
                csrf=get_token(request),
                username=escape(username),
                error_html='<p class="error">Please fill in both fields.</p>',
            )
            return HttpResponse(PAGE.substitute(title='Sign in', body=body))

        # No real authentication — any non-empty pair is accepted by design.
        request.session['username'] = username
        return redirect('/dashboard/')

    body = LOGIN_BODY.substitute(csrf=get_token(request), username='', error_html='')
    return HttpResponse(PAGE.substitute(title='Sign in', body=body))


def dashboard_view(request):
    username = request.session.get('username')
    if not username:
        return redirect('/')

    body = DASHBOARD_BODY.substitute(
        csrf=get_token(request),
        username=escape(username),
        initial=escape(username[0].upper()),
    )
    return HttpResponse(PAGE.substitute(title='Dashboard', body=body))


def logout_view(request):
    if request.method == 'POST':
        request.session.flush()
    return redirect('/')


urlpatterns = [
    path('', login_view),
    path('dashboard/', dashboard_view),
    path('logout/', logout_view),
]

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)