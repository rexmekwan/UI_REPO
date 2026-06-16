"""
Single-file Django login demo — Humanized Edition.

We've removed the overly technical abbreviations and added friendly,
conversational comments to explain exactly what each part of the script does.

Run this script from your terminal:
    py ui_repo.py runserver
"""
import sys
from string import Template

import django
from django.conf import settings

# -------------------------------------------------------------------------
# 1. THE SETUP: Configuring Django on the fly
# -------------------------------------------------------------------------
# Normally, Django needs a dozen files and folders. By configuring settings
# directly in the code below, we force Django to run from this single file.

settings.configure(
    DEBUG=True,  # Shows helpful error pages if something breaks
    SECRET_KEY='django-insecure-single-file-demo-key',
    ALLOWED_HOSTS=['*'],  # Allows the server to run locally
    ROOT_URLCONF=__name__,  # Tells Django to look for URLs in this exact file
    
    # Middlewares are like security guards that check requests before they reach our code
    MIDDLEWARE=[
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware', # Remembers who is logged in
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',            # Blocks cross-site hacker attacks
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ],
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.sessions',
    ],
    
    # We use 'signed_cookies' so we don't have to set up a database.
    # The user's logged-in status is securely saved right inside their browser cookie.
    SESSION_ENGINE='django.contrib.sessions.backends.signed_cookies',
    SESSION_EXPIRE_AT_BROWSER_CLOSE=True, # Logs them out when they close the tab
    DEFAULT_AUTO_FIELD='django.db.models.BigAutoField',
)

# Tell Django to wake up and apply the settings above
django.setup()

# -------------------------------------------------------------------------
# 2. IMPORTS: Bringing in the tools we need
# -------------------------------------------------------------------------
from django.urls import path                       # noqa: E402
from django.shortcuts import redirect               # noqa: E402
from django.http import HttpResponse                # noqa: E402
from django.middleware.csrf import get_token        # noqa: E402
from django.utils.html import escape                # noqa: E402

# -------------------------------------------------------------------------
# 3. THE VISUALS: Our HTML and CSS templates
# -------------------------------------------------------------------------
# We use Python's 'Template' tool to safely inject data (like usernames) 
# into our HTML using the $ symbol.

PAGE_WRAPPER = Template("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>$title</title>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  :root{
    --ink-900:#0a0e1a; --ink-700:#1c2438; --violet-700:#3d2c6b;
    --teal-600:#1f6f78; --gold-500:#f2b84b; --mist-100:#eef1f7;
    --mist-400:#9aa3b8; --danger:#ff6b6b;
  }
  *{box-sizing:border-box;}
  body{
    margin:0; min-height:100vh; display:flex; align-items:center;
    justify-content:center; background:var(--ink-900);
    font-family:'Inter',sans-serif; color:var(--mist-100);
    position:relative; overflow:hidden;
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
  h1{font-family:'Sora',sans-serif;font-size:24px;font-weight:700;margin:0 0 6px;}
  .sub{color:var(--mist-400);font-size:14px;margin:0 0 28px;line-height:1.5;}
  label{display:block;font-size:13px;font-weight:500;color:var(--mist-400);margin-bottom:7px;}
  .field{margin-bottom:18px;}
  input{width:100%;padding:13px 14px;background:var(--ink-700);border:1px solid rgba(255,255,255,0.08);border-radius:10px;color:var(--mist-100);font-family:'Inter',sans-serif;font-size:14.5px;outline:none;}
  input:focus-visible{border-color:var(--gold-500);box-shadow:0 0 0 3px rgba(242,184,75,0.18);}
  .error{font-size:13px;color:var(--danger);margin:-6px 0 16px;}
  button.submit,button.logout{width:100%;padding:13px;border:none;border-radius:10px;font-family:'Sora',sans-serif;font-weight:600;font-size:14.5px;cursor:pointer;}
  button.submit{margin-top:6px;background:var(--gold-500);color:var(--ink-900);}
  button.logout{background:transparent;color:var(--mist-100);border:1px solid rgba(255,255,255,0.12);}
  .foot{text-align:center;font-size:12.5px;color:var(--mist-400);margin-top:22px;}
</style>
</head>
<body>
  <div class="blob blob-1" aria-hidden="true"></div>
  <div class="blob blob-2" aria-hidden="true"></div>
  
  $body_content
  
</body>
</html>""")

LOGIN_SCREEN = Template("""
<main class="card">
  <div class="mark">A</div>
  <h1>Welcome back</h1>
  <p class="sub">Sign in to continue. Any username and password will work &mdash; this is a demo flow.</p>
  
  <form method="post" novalidate>
    <input type="hidden" name="csrfmiddlewaretoken" value="$security_token">
    
    <div class="field">
      <label for="username">Username</label>
      <input type="text" id="username" name="username" placeholder="Enter your name" value="$saved_username" required>
    </div>
    
    <div class="field">
      <label for="password">Password</label>
      <input type="password" id="password" name="password" placeholder="Enter your password" required>
    </div>
    
    $error_message
    
    <button type="submit" class="submit">Sign in</button>
  </form>
  <p class="foot">No account needed &mdash; this page logs you in regardless.</p>
</main>
""")

DASHBOARD_SCREEN = Template("""
<main class="card dashboard-card">
  <div class="avatar">$first_letter</div>
  
  <h1>Welcome, $username</h1>
  <p class="sub">You're signed in. This page is reachable only after submitting the login form.</p>
  
  <form method="post" action="/logout/">
    <input type="hidden" name="csrfmiddlewaretoken" value="$security_token">
    <button type="submit" class="logout">Log out</button>
  </form>
</main>
""")

# -------------------------------------------------------------------------
# 4. THE LOGIC: Handling what happens when a user visits a URL
# -------------------------------------------------------------------------

def handle_login(request):
    """Shows the login screen and handles form submissions."""
    
    # Did the user just click the 'Sign in' button?
    if request.method == 'POST':
        # Grab what they typed, stripping away accidental spaces at the ends
        typed_username = request.POST.get('username', '').strip()
        typed_password = request.POST.get('password', '').strip()

        # If they left something blank, scold them gently
        if not typed_username or not typed_password:
            login_html = LOGIN_SCREEN.substitute(
                security_token=get_token(request),
                saved_username=escape(typed_username), # Put their name back so they don't have to retype it
                error_message='<p class="error">Please fill in both fields.</p>',
            )
            final_page = PAGE_WRAPPER.substitute(title='Sign in', body_content=login_html)
            return HttpResponse(final_page)

        # Success! Log them in by saving their name into the browser's secure session cookie
        request.session['username'] = typed_username
        
        # Send them straight to the dashboard
        return redirect('/dashboard/')

    # If they just arrived at the page normally (a GET request), show a clean, empty form
    clean_login_html = LOGIN_SCREEN.substitute(
        security_token=get_token(request), 
        saved_username='', 
        error_message=''
    )
    final_page = PAGE_WRAPPER.substitute(title='Sign in', body_content=clean_login_html)
    return HttpResponse(final_page)


def handle_dashboard(request):
    """Shows the welcome screen, but only if they are logged in."""
    
    # Check the browser session to see if we remember them
    current_user = request.session.get('username')
    
    # If we don't know who they are, kick them back to the login screen
    if not current_user:
        return redirect('/')

    # Build the dashboard HTML using their name
    dashboard_html = DASHBOARD_SCREEN.substitute(
        security_token=get_token(request),
        username=escape(current_user),
        first_letter=escape(current_user[0].upper()), # Grab the very first letter and capitalize it
    )
    final_page = PAGE_WRAPPER.substitute(title='Dashboard', body_content=dashboard_html)
    return HttpResponse(final_page)


def handle_logout(request):
    """Destroys the session data and logs the user out."""
    if request.method == 'POST':
        request.session.flush() # Wipes the cookie clean
    return redirect('/')

# -------------------------------------------------------------------------
# 5. THE MAP: Connecting URLs to our logic functions
# -------------------------------------------------------------------------
urlpatterns = [
    path('', handle_login),
    path('dashboard/', handle_dashboard),
    path('logout/', handle_logout),
]

# -------------------------------------------------------------------------
# 6. THE ENGINE: Starting the actual server
# -------------------------------------------------------------------------
if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    # When you type 'py ui_repo.py runserver', this line catches the word 'runserver' and starts Django.
    execute_from_command_line(sys.argv)