"""
Single-file Django mini-site: login + Home, About, Shopping, Services, Pricing, FAQ, Contact pages.

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
  .nav-inner{max-width:860px;margin:0 auto;padding:16px 24px;display:flex;align-items:center;gap:28px;}
  .brand{font-family:'Sora',sans-serif;font-weight:700;font-size:16px;color:var(--mist-100);margin-right:auto;}
  .nav-links{display:flex;gap:18px;flex-wrap:wrap;}
  .nav-links a{color:var(--mist-400);text-decoration:none;font-size:14px;font-weight:500;padding:6px 2px;border-bottom:2px solid transparent;transition:color .15s, border-color .15s;}
  .nav-links a:hover{color:var(--mist-100);}
  .nav-links a.active{color:var(--mist-100);border-bottom-color:var(--gold-500);}
  .nav-actions{display:flex;align-items:center;gap:14px;}
  .cart-link{position:relative;color:var(--mist-100);text-decoration:none;font-size:19px;line-height:1;display:flex;align-items:center;padding:4px;}
  .cart-badge{position:absolute;top:-6px;right:-8px;background:var(--gold-500);color:var(--ink-900);font-size:10px;font-weight:700;border-radius:999px;min-width:16px;height:16px;display:flex;align-items:center;justify-content:center;padding:0 4px;font-family:'Sora',sans-serif;}
  .nav-logout-form{margin:0;}
  button.nav-logout{padding:8px 14px;border-radius:8px;border:1px solid rgba(255,255,255,0.12);background:transparent;color:var(--mist-100);font-family:'Inter',sans-serif;font-weight:500;font-size:13px;cursor:pointer;transition:background .12s ease;}
  button.nav-logout:hover{background:rgba(255,255,255,0.06);}

  .page-content{position:relative;z-index:1;max-width:860px;margin:0 auto;padding:48px 24px 64px;display:flex;justify-content:center;}

  .card{position:relative;z-index:1;width:100%;max-width:380px;padding:40px 36px 36px;background:rgba(255,255,255,0.045);border:1px solid rgba(255,255,255,0.08);border-radius:20px;backdrop-filter:blur(18px);box-shadow:0 30px 60px -20px rgba(0,0,0,.6);animation:fadeIn .35s ease both;}
  .card.dashboard-card{max-width:420px;text-align:center;}
  .card.wide{max-width:640px;text-align:left;}
  .card.wide p{color:var(--mist-400);font-size:14.5px;line-height:1.7;margin:0 0 16px;}
  .card.wide p:last-child{margin-bottom:0;}
  @keyframes fadeIn{from{opacity:0;transform:translateY(6px);}to{opacity:1;transform:translateY(0);}}

  .page-head{width:100%;max-width:680px;margin:0 auto 28px;text-align:center;}
  .page-head h1{margin-bottom:8px;}
  .page-head p{color:var(--mist-400);font-size:14.5px;line-height:1.6;margin:0;}

  .grid-wrap{width:100%;max-width:760px;display:flex;flex-direction:column;align-items:center;gap:0;}

  .services-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:18px;width:100%;}
  .service-card{padding:26px 22px;background:rgba(255,255,255,0.045);border:1px solid rgba(255,255,255,0.08);border-radius:16px;backdrop-filter:blur(18px);animation:fadeIn .35s ease both;}
  .service-card .icon{width:38px;height:38px;border-radius:10px;background:linear-gradient(135deg,var(--teal-600),#143f45);display:flex;align-items:center;justify-content:center;font-family:'Sora',sans-serif;font-weight:700;color:var(--mist-100);margin-bottom:16px;font-size:16px;}
  .service-card h2{font-family:'Sora',sans-serif;font-size:16px;font-weight:700;margin:0 0 8px;}
  .service-card p{color:var(--mist-400);font-size:13.5px;line-height:1.6;margin:0;}

  .pricing-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:18px;width:100%;align-items:stretch;}
  .price-card{display:flex;flex-direction:column;padding:30px 24px;background:rgba(255,255,255,0.045);border:1px solid rgba(255,255,255,0.08);border-radius:16px;backdrop-filter:blur(18px);animation:fadeIn .35s ease both;}
  .price-card.featured{border-color:rgba(242,184,75,0.45);box-shadow:0 20px 50px -20px rgba(242,184,75,0.25);position:relative;}
  .price-card.featured .badge{position:absolute;top:-12px;left:50%;transform:translateX(-50%);background:var(--gold-500);color:var(--ink-900);font-family:'Sora',sans-serif;font-size:11px;font-weight:700;padding:4px 12px;border-radius:999px;white-space:nowrap;}
  .price-card h2{font-family:'Sora',sans-serif;font-size:16px;font-weight:700;margin:0 0 4px;}
  .price-card .amount{font-family:'Sora',sans-serif;font-size:30px;font-weight:700;margin:8px 0 4px;}
  .price-card .amount span{font-size:13px;font-weight:500;color:var(--mist-400);}
  .price-card .desc{color:var(--mist-400);font-size:13px;margin:0 0 20px;}
  .price-card ul{list-style:none;margin:0 0 24px;padding:0;display:flex;flex-direction:column;gap:10px;flex-grow:1;}
  .price-card li{font-size:13.5px;color:var(--mist-100);display:flex;align-items:center;gap:8px;}
  .price-card li::before{content:"";width:6px;height:6px;border-radius:50%;background:var(--gold-500);flex-shrink:0;}
  .price-card .pick-btn{width:100%;padding:11px;border:1px solid rgba(255,255,255,0.14);border-radius:9px;background:transparent;color:var(--mist-100);font-family:'Sora',sans-serif;font-weight:600;font-size:13.5px;cursor:pointer;transition:background .12s ease;}
  .price-card.featured .pick-btn{background:var(--gold-500);color:var(--ink-900);border-color:transparent;}
  .price-card .pick-btn:hover{background:rgba(255,255,255,0.08);}
  .price-card.featured .pick-btn:hover{background:#ffc869;}

  .faq-list{width:100%;display:flex;flex-direction:column;gap:12px;}
  .faq-item{background:rgba(255,255,255,0.045);border:1px solid rgba(255,255,255,0.08);border-radius:14px;backdrop-filter:blur(18px);overflow:hidden;animation:fadeIn .35s ease both;}
  .faq-item summary{list-style:none;cursor:pointer;padding:18px 20px;font-family:'Sora',sans-serif;font-size:14.5px;font-weight:600;display:flex;align-items:center;justify-content:space-between;gap:12px;}
  .faq-item summary::-webkit-details-marker{display:none;}
  .faq-item summary::after{content:"+";font-size:18px;font-weight:400;color:var(--mist-400);transition:transform .15s ease;flex-shrink:0;}
  .faq-item[open] summary::after{transform:rotate(45deg);}
  .faq-item .faq-answer{padding:0 20px 18px;color:var(--mist-400);font-size:13.5px;line-height:1.65;margin:0;}

  .shopping-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:18px;width:100%;}
  .product-card{display:block;text-decoration:none;color:inherit;padding:24px 20px;background:rgba(255,255,255,0.045);border:1px solid rgba(255,255,255,0.08);border-radius:16px;backdrop-filter:blur(18px);animation:fadeIn .35s ease both;transition:transform .15s ease, border-color .15s ease;}
  .product-card:hover{transform:translateY(-3px);border-color:rgba(242,184,75,0.35);}
  .product-card .emoji{font-size:34px;margin-bottom:14px;display:block;}
  .product-card h2{font-family:'Sora',sans-serif;font-size:15px;font-weight:700;margin:0 0 6px;}
  .product-card .blurb{color:var(--mist-400);font-size:13px;line-height:1.5;margin:0 0 14px;}
  .product-card .price{font-family:'Sora',sans-serif;font-weight:700;color:var(--gold-500);font-size:15px;}

  .product-detail{width:100%;max-width:520px;text-align:center;}
  .product-detail .emoji-lg{font-size:64px;display:block;margin-bottom:18px;}
  .product-detail .price-lg{font-family:'Sora',sans-serif;font-weight:700;color:var(--gold-500);font-size:22px;margin:6px 0 18px;}
  .product-detail .detail-text{color:var(--mist-400);font-size:14px;line-height:1.7;margin:0 0 24px;text-align:left;}
  .qty-row{display:flex;align-items:center;justify-content:center;gap:12px;margin-bottom:18px;}
  .qty-row label{margin:0;}
  .qty-row input{width:80px;text-align:center;}
  .detail-links{display:flex;justify-content:center;gap:18px;margin-top:18px;font-size:13px;}
  .detail-links a{color:var(--mist-400);text-decoration:none;}
  .detail-links a:hover{color:var(--mist-100);}

  .cart-list{width:100%;max-width:560px;display:flex;flex-direction:column;gap:12px;}
  .cart-row{display:flex;align-items:center;gap:14px;padding:16px 18px;background:rgba(255,255,255,0.045);border:1px solid rgba(255,255,255,0.08);border-radius:14px;backdrop-filter:blur(18px);animation:fadeIn .35s ease both;}
  .cart-row .emoji{font-size:26px;flex-shrink:0;}
  .cart-row .info{flex-grow:1;text-align:left;}
  .cart-row .info .name{font-family:'Sora',sans-serif;font-weight:600;font-size:14px;}
  .cart-row .info .meta{color:var(--mist-400);font-size:12.5px;margin-top:2px;}
  .cart-row .subtotal{font-family:'Sora',sans-serif;font-weight:700;font-size:14px;white-space:nowrap;}
  .cart-row form{margin:0;}
  .remove-btn{background:none;border:none;color:var(--mist-400);cursor:pointer;font-size:13px;padding:4px 6px;border-radius:6px;transition:color .12s ease, background .12s ease;}
  .remove-btn:hover{color:var(--danger);background:rgba(255,107,107,0.1);}
  .cart-total{width:100%;max-width:560px;display:flex;justify-content:space-between;align-items:center;padding:16px 18px;margin-top:6px;font-family:'Sora',sans-serif;font-weight:700;font-size:15px;}
  .cart-empty{text-align:center;color:var(--mist-400);font-size:14px;}
  .cart-empty a{color:var(--gold-500);}

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
      <a href="/shopping/" class="$shopping_cls">Shopping</a>
      <a href="/services/" class="$services_cls">Services</a>
      <a href="/pricing/" class="$pricing_cls">Pricing</a>
      <a href="/faq/" class="$faq_cls">FAQ</a>
      <a href="/contact/" class="$contact_cls">Contact</a>
    </div>
    <div class="nav-actions">
      <a href="/cart/" class="cart-link" aria-label="Cart">&#128722;<span class="cart-badge">$cart_count</span></a>
      <form method="post" action="/logout/" class="nav-logout-form">
        <input type="hidden" name="csrfmiddlewaretoken" value="$csrf">
        <button type="submit" class="nav-logout">Log out</button>
      </form>
    </div>
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

PRODUCTS = [
    {
        'id': 1, 'emoji': '🎧', 'name': 'Wireless Headphones', 'price': 59.99,
        'blurb': 'Noise-isolating, 30hr battery life.',
        'detail': 'Over-ear wireless headphones with active noise isolation, a 30-hour battery, and a fold-flat design for travel. Pairs over Bluetooth 5.0 with any phone or laptop.',
    },
    {
        'id': 2, 'emoji': '⌨️', 'name': 'Mechanical Keyboard', 'price': 89.00,
        'blurb': 'Hot-swappable switches, RGB backlight.',
        'detail': 'A compact 75% mechanical keyboard with hot-swappable switches, per-key RGB lighting, and a aluminum top plate for a solid typing feel.',
    },
    {
        'id': 3, 'emoji': '⌚', 'name': 'Smart Watch', 'price': 129.50,
        'blurb': 'Heart-rate tracking, week-long battery.',
        'detail': 'Tracks heart rate, sleep, and workouts around the clock, with up to seven days of battery on a single charge and a always-on display.',
    },
    {
        'id': 4, 'emoji': '🔊', 'name': 'Portable Speaker', 'price': 39.99,
        'blurb': 'Waterproof, 12-hour playtime.',
        'detail': 'A pocket-sized waterproof speaker rated IPX7, with 12 hours of playtime and surprisingly deep bass for its size.',
    },
]
PRODUCTS_BY_ID = {p['id']: p for p in PRODUCTS}

PRODUCT_CARD = Template("""
      <a class="product-card" href="/shopping/$id/">
        <span class="emoji">$emoji</span>
        <h2>$name</h2>
        <p class="blurb">$blurb</p>
        <span class="price">$$$price</span>
      </a>""")

SHOPPING_PAGE = Template("""
<div class="page-head">
  <h1>Shopping</h1>
  <p>Click any item to view its page and add it to your cart &mdash; nothing here actually ships.</p>
</div>
<div class="grid-wrap">
  <div class="shopping-grid">$cards</div>
</div>
""")

PRODUCT_DETAIL = Template("""
<main class="card product-detail">
  <span class="emoji-lg">$emoji</span>
  <h1>$name</h1>
  <div class="price-lg">$$$price</div>
  <p class="detail-text">$detail</p>
  <form method="post">
    <input type="hidden" name="csrfmiddlewaretoken" value="$csrf">
    <div class="qty-row">
      <label for="quantity">Qty</label>
      <input type="number" id="quantity" name="quantity" min="1" max="10" value="1">
    </div>
    $status_html
    <button type="submit" class="submit">Add to cart</button>
  </form>
  <div class="detail-links">
    <a href="/shopping/">&larr; Back to shopping</a>
    <a href="/cart/">View cart ($cart_count)</a>
  </div>
</main>
""")

CART_ROW = Template("""
      <div class="cart-row">
        <span class="emoji">$emoji</span>
        <div class="info">
          <div class="name">$name</div>
          <div class="meta">Qty $qty &times; $$$price</div>
        </div>
        <div class="subtotal">$$$subtotal</div>
        <form method="post">
          <input type="hidden" name="csrfmiddlewaretoken" value="$csrf">
          <input type="hidden" name="action" value="remove">
          <input type="hidden" name="product_id" value="$id">
          <button type="submit" class="remove-btn">Remove</button>
        </form>
      </div>""")

CART_PAGE = Template("""
<div class="page-head">
  <h1>Your cart</h1>
  <p>Items you've added while browsing the shop.</p>
</div>
<div class="grid-wrap">
  <div class="cart-list">$rows</div>
  <div class="cart-total"><span>Total</span><span>$$$total</span></div>
</div>
""")

CART_EMPTY = Template("""
<div class="page-head">
  <h1>Your cart</h1>
</div>
<div class="grid-wrap">
  <p class="cart-empty">Your cart is empty. <a href="/shopping/">Browse the shop</a> to add something.</p>
</div>
""")

SERVICE_ITEMS = [
    ('01', 'Web Design', 'Clean, fast interfaces built around what people actually need to do on the page.'),
    ('02', 'Automation', 'Scripts and tools that take repetitive manual work off your plate for good.'),
    ('03', 'Consulting', 'A second pair of eyes on architecture, performance, or anything stuck mid-build.'),
    ('04', 'Support', 'Ongoing maintenance and quick turnarounds when something needs fixing fast.'),
]

SERVICE_CARD = Template("""
      <div class="service-card">
        <div class="icon">$num</div>
        <h2>$title</h2>
        <p>$desc</p>
      </div>""")

SERVICES_PAGE = Template("""
<div class="page-head">
  <h1>Services</h1>
  <p>A few of the things this demo company would offer, if it were real.</p>
</div>
<div class="grid-wrap">
  <div class="services-grid">$cards</div>
</div>
""")

PRICING_TIERS = [
    ('Starter', '0', 'For trying things out', ['1 project', 'Community support', 'Core features'], False),
    ('Pro', '29', 'For getting serious', ['Unlimited projects', 'Priority support', 'All features', 'Team access'], True),
    ('Enterprise', '99', 'For larger teams', ['Everything in Pro', 'Dedicated support', 'Custom integrations'], False),
]

PRICE_CARD = Template("""
      <div class="price-card$featured_cls">
        $badge_html
        <h2>$name</h2>
        <p class="desc">$desc</p>
        <div class="amount">$$$amount<span>/mo</span></div>
        <ul>$features</ul>
        <button type="button" class="pick-btn">Choose $name</button>
      </div>""")

PRICING_PAGE = Template("""
<div class="page-head">
  <h1>Pricing</h1>
  <p>Simple, transparent tiers. No payment is actually processed &mdash; this is a demo.</p>
</div>
<div class="grid-wrap">
  <div class="pricing-grid">$cards</div>
</div>
""")

FAQ_ITEMS = [
    ('Is this a real product?', "No &mdash; it's a demo site to show a small multi-page Django app running from a single file."),
    ('Does the login check my password?', 'No. Any non-empty username and password combination is accepted, by design.'),
    ('Is any data saved to a database?', "No. There's no database configured at all &mdash; session data lives in a signed cookie."),
    ('Can I extend this with more pages?', 'Yes &mdash; add a view function, a URL pattern, and a nav link, following the existing pages as a template.'),
]

FAQ_ITEM = Template("""
    <details class="faq-item">
      <summary>$question</summary>
      <p class="faq-answer">$answer</p>
    </details>""")

FAQ_PAGE = Template("""
<div class="page-head">
  <h1>Frequently asked questions</h1>
  <p>Quick answers about how this demo site works.</p>
</div>
<div class="grid-wrap">
  <div class="faq-list">$items</div>
</div>
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


def cart_item_count(request):
    cart = request.session.get('cart', {})
    return sum(cart.values())


def render_nav(request, active):
    return NAV.substitute(
        csrf=get_token(request),
        home_cls='active' if active == 'home' else '',
        about_cls='active' if active == 'about' else '',
        shopping_cls='active' if active == 'shopping' else '',
        services_cls='active' if active == 'services' else '',
        pricing_cls='active' if active == 'pricing' else '',
        faq_cls='active' if active == 'faq' else '',
        contact_cls='active' if active == 'contact' else '',
        cart_count=cart_item_count(request),
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


def shopping_view(request):
    if not request.session.get('username'):
        return redirect('/')

    cards = ''.join(
        PRODUCT_CARD.substitute(
            id=p['id'], emoji=p['emoji'], name=escape(p['name']),
            blurb=escape(p['blurb']), price=f"{p['price']:.2f}",
        )
        for p in PRODUCTS
    )
    content = SHOPPING_PAGE.substitute(cards=cards)
    body = PAGE_CONTENT_WRAP.substitute(nav=render_nav(request, 'shopping'), content=content)
    return HttpResponse(PAGE.substitute(title='Shopping', body=body))


def product_detail_view(request, product_id):
    if not request.session.get('username'):
        return redirect('/')

    product = PRODUCTS_BY_ID.get(product_id)
    if not product:
        return redirect('/shopping/')

    status_html = ''
    if request.method == 'POST':
        try:
            qty = max(1, min(10, int(request.POST.get('quantity', '1'))))
        except ValueError:
            qty = 1

        cart = request.session.get('cart', {})
        key = str(product_id)
        cart[key] = cart.get(key, 0) + qty
        request.session['cart'] = cart
        request.session.modified = True
        status_html = f'<p class="success">Added {qty} &times; {escape(product["name"])} to your cart.</p>'

    card = PRODUCT_DETAIL.substitute(
        csrf=get_token(request),
        emoji=product['emoji'],
        name=escape(product['name']),
        price=f"{product['price']:.2f}",
        detail=escape(product['detail']),
        status_html=status_html,
        cart_count=cart_item_count(request),
    )
    body = PAGE_CONTENT_WRAP.substitute(nav=render_nav(request, 'shopping'), content=card)
    return HttpResponse(PAGE.substitute(title=product['name'], body=body))


def cart_view(request):
    if not request.session.get('username'):
        return redirect('/')

    cart = request.session.get('cart', {})

    if request.method == 'POST':
        if request.POST.get('action') == 'remove':
            cart.pop(request.POST.get('product_id', ''), None)
            request.session['cart'] = cart
            request.session.modified = True
        return redirect('/cart/')  # POST-redirect-GET avoids a resubmit-on-refresh prompt

    if not cart:
        content = CART_EMPTY.substitute()
    else:
        rows = ''
        total = 0.0
        for pid_str, qty in cart.items():
            product = PRODUCTS_BY_ID.get(int(pid_str))
            if not product:
                continue
            subtotal = product['price'] * qty
            total += subtotal
            rows += CART_ROW.substitute(
                csrf=get_token(request),
                emoji=product['emoji'],
                name=escape(product['name']),
                qty=qty,
                price=f"{product['price']:.2f}",
                subtotal=f"{subtotal:.2f}",
                id=pid_str,
            )
        content = CART_PAGE.substitute(rows=rows, total=f"{total:.2f}")

    body = PAGE_CONTENT_WRAP.substitute(nav=render_nav(request, 'shopping'), content=content)
    return HttpResponse(PAGE.substitute(title='Cart', body=body))


def services_view(request):
    if not request.session.get('username'):
        return redirect('/')

    cards = ''.join(
        SERVICE_CARD.substitute(num=num, title=escape(title), desc=escape(desc))
        for num, title, desc in SERVICE_ITEMS
    )
    content = SERVICES_PAGE.substitute(cards=cards)
    body = PAGE_CONTENT_WRAP.substitute(nav=render_nav(request, 'services'), content=content)
    return HttpResponse(PAGE.substitute(title='Services', body=body))


def pricing_view(request):
    if not request.session.get('username'):
        return redirect('/')

    cards = ''
    for name, amount, desc, features, featured in PRICING_TIERS:
        feature_html = ''.join(f'<li>{escape(f)}</li>' for f in features)
        cards += PRICE_CARD.substitute(
            featured_cls=' featured' if featured else '',
            badge_html='<span class="badge">Most popular</span>' if featured else '',
            name=escape(name),
            desc=escape(desc),
            amount=amount,
            features=feature_html,
        )
    content = PRICING_PAGE.substitute(cards=cards)
    body = PAGE_CONTENT_WRAP.substitute(nav=render_nav(request, 'pricing'), content=content)
    return HttpResponse(PAGE.substitute(title='Pricing', body=body))


def faq_view(request):
    if not request.session.get('username'):
        return redirect('/')

    items = ''.join(
        FAQ_ITEM.substitute(question=question, answer=answer)
        for question, answer in FAQ_ITEMS
    )
    content = FAQ_PAGE.substitute(items=items)
    body = PAGE_CONTENT_WRAP.substitute(nav=render_nav(request, 'faq'), content=content)
    return HttpResponse(PAGE.substitute(title='FAQ', body=body))


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
    path('shopping/', shopping_view),
    path('shopping/<int:product_id>/', product_detail_view),
    path('cart/', cart_view),
    path('services/', services_view),
    path('pricing/', pricing_view),
    path('faq/', faq_view),
    path('contact/', contact_view),
    path('logout/', logout_view),
]

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)