#!/usr/bin/env python3
"""Generate the unlinked.store static pages. Run: python3 tools/build.py

GitHub Pages serves the generated HTML as is. STORE_URL is the Chrome Web Store
listing; set it to None to turn the install buttons back into "Coming soon" badges.
"""
import html, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://unlinked.store"
STORE_URL = "https://chromewebstore.google.com/detail/unlinked-clean-linkedin-f/mgeelmoeppnfccegklclehplkkicmcca"
LASTMOD = "2026-10-31"
EMAIL = "amarkumar.sde@gmail.com"
COFFEE = "https://buymeacoffee.com/amarxkumar"
SPONSORS = "https://github.com/sponsors/amarkum"
OG = f"{SITE}/assets/og-image.jpg"
OG_ALT = "Unlinked Chrome extension popup next to the headline: A clean LinkedIn feed"
DISCLAIMER = "Unlinked is an independent project and is not affiliated with or endorsed by LinkedIn. LinkedIn is a trademark of LinkedIn Corporation."

ICONS = {
    "eye-off": '<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/>',
    "users": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "message": '<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>',
    "repeat": '<polyline points="17 1 21 5 17 9"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/><polyline points="7 23 3 19 7 15"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/>',
    "sidebar": '<rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="9" y1="3" x2="9" y2="21"/>',
    "check": '<polyline points="20 6 9 17 4 12"/>',
    "lock": '<rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "sliders": '<line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/><line x1="1" y1="14" x2="7" y2="14"/><line x1="9" y1="8" x2="15" y2="8"/><line x1="17" y1="16" x2="23" y2="16"/>',
    "cloud-off": '<path d="M22.61 16.95A5 5 0 0 0 18 10h-1.26a8 8 0 0 0-7.05-6M5 5a8 8 0 0 0 4 15h9a5 5 0 0 0 1.7-.3"/><line x1="1" y1="1" x2="23" y2="23"/>',
    "menu": '<line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/>',
    "x": '<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>',
    "plus": '<line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
}


def icon(name, size=22, sw=2):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{ICONS[name]}</svg>')


def esc(s):
    return html.escape(s, quote=True)


def jsonld(data):
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "</script>"


def head(title, desc, path, *, og_type="website", ld=None, noindex=False):
    url = f"{SITE}{path}"
    robots = "noindex,follow" if noindex else "index,follow,max-image-preview:large,max-snippet:-1"
    parts = [
        '<!doctype html>',
        '<html lang="en">',
        '<head>',
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width,initial-scale=1">',
        f'<title>{esc(title)}</title>',
        f'<meta name="description" content="{esc(desc)}">',
        f'<meta name="robots" content="{robots}">',
        f'<link rel="canonical" href="{url}">',
        '<meta name="color-scheme" content="light">',
        '<meta name="theme-color" content="#ffffff">',
        '<link rel="icon" href="/favicon.ico" sizes="48x48">',
        '<link rel="icon" type="image/png" sizes="192x192" href="/icon-192.png">',
        '<link rel="apple-touch-icon" href="/apple-touch-icon.png">',
        '<meta name="application-name" content="Unlinked">',
        '<meta name="apple-mobile-web-app-title" content="Unlinked">',
        f'<meta property="og:type" content="{og_type}">',
        '<meta property="og:site_name" content="Unlinked">',
        '<meta property="og:locale" content="en_US">',
        f'<meta property="og:title" content="{esc(title)}">',
        f'<meta property="og:description" content="{esc(desc)}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:image" content="{OG}">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        f'<meta property="og:image:alt" content="{esc(OG_ALT)}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{esc(title)}">',
        f'<meta name="twitter:description" content="{esc(desc)}">',
        f'<meta name="twitter:image" content="{OG}">',
        f'<meta name="twitter:image:alt" content="{esc(OG_ALT)}">',
        '<link rel="stylesheet" href="/assets/site.css?v=4">',
    ]
    if ld:
        parts.append(jsonld(ld))
    parts.append('</head>')
    return "\n".join(parts)


NAV = [
    ("/#features", "Features", None),
    ("/#how", "How it works", None),
    ("/clean-linkedin-feed/", "Guide", "guide"),
    ("/#faq", "FAQ", None),
    ("/support/", "Support", "support"),
    ("/store/", "Install", "store"),
]


# Mobile menu toggle. Without JS the header falls back to a scrolling row of links.
MENU_JS = ("(function(){var h=document.querySelector('.site-header'),b=h.querySelector('.menu-btn');h.classList.add('js');"
           "function set(o){h.classList.toggle('open',o);b.setAttribute('aria-expanded',o)}"
           "b.addEventListener('click',function(){set(!h.classList.contains('open'))});"
           "h.querySelector('.nav').addEventListener('click',function(e){if(e.target.closest('a'))set(false)});"
           "document.addEventListener('keydown',function(e){if(e.key==='Escape'&&h.classList.contains('open')){set(false);b.focus()}})})();")


def header(current=None):
    links = "".join(
        f'<a href="{href}"'
        + (' class="nav-cta"' if key == "store" else "")
        + (' aria-current="page"' if key and key == current else "")
        + f'>{label}</a>'
        for href, label, key in NAV
    )
    return f'''<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
<div class="wrap">
<a class="brand" href="/"><img src="/assets/icon-48.png" width="32" height="32" alt="">Unlinked</a>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Menu">{icon("menu", 24).replace("<svg ", '<svg class="i-open" ', 1)}{icon("x", 24).replace("<svg ", '<svg class="i-close" ', 1)}</button>
<nav class="nav" id="site-nav" aria-label="Main">{links}</nav>
</div>
</header>
<script>{MENU_JS}</script>'''


def footer():
    return f'''<footer class="site-footer">
<div class="wrap">
<div class="foot">
<div>
<a class="brand" href="/"><img src="/assets/icon-48.png" width="32" height="32" alt="">Unlinked</a>
<p class="foot-about">A free Chrome extension that cleans up your LinkedIn feed: no ads, no suggestions, only the people you follow.</p>
</div>
<div>
<h4>Explore</h4>
<ul>
<li><a href="/">Home</a></li>
<li><a href="/store/">Get Unlinked for Chrome</a></li>
<li><a href="/clean-linkedin-feed/">How to clean up your LinkedIn feed</a></li>
<li><a href="/#faq">FAQ</a></li>
</ul>
</div>
<div>
<h4>Help</h4>
<ul>
<li><a href="/support/">Support</a></li>
<li><a href="/privacy/">Privacy policy</a></li>
<li><a href="{COFFEE}" rel="noopener">Buy me a coffee</a></li>
<li><a href="{SPONSORS}" rel="noopener">GitHub Sponsors</a></li>
<li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
</ul>
</div>
</div>
<p class="legal">&copy; 2026 Unlinked. {DISCLAIMER}</p>
</div>
</footer>
</body>
</html>
'''


def store_ld():
    return {"installUrl": STORE_URL, "downloadUrl": STORE_URL, "sameAs": [STORE_URL]} if STORE_URL else {}


def soon_or_install(kind="hero"):
    if STORE_URL:
        return f'<a class="btn btn-primary" href="{STORE_URL}" rel="noopener">{icon("plus", 18, 2.5)} Add to Chrome, it&rsquo;s free</a>'
    return f'<span class="btn btn-soon">{icon("clock", 18)} Coming soon to the Chrome Web Store</span>'


def crumbs(items):
    out = ['<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a>']
    for label, href in items:
        out.append(f' <span aria-hidden="true">/</span> ' + (f'<a href="{href}">{label}</a>' if href else f'<span>{label}</span>'))
    out.append('</nav>')
    return "".join(out)


def breadcrumb_ld(items):
    elems = [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}]
    for i, (label, href) in enumerate(items, start=2):
        elems.append({"@type": "ListItem", "position": i, "name": label, "item": SITE + href})
    return {"@type": "BreadcrumbList", "itemListElement": elems}


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


# ----------------------------------------------------------------------------- home
FAQ = [
    ("What is Unlinked?",
     "Unlinked is a free Chrome extension that cleans up your LinkedIn home feed. It hides promoted posts, suggested posts, “liked by” and “commented on” activity and other filler, so the feed shows posts from the people and pages you follow."),
    ("How do I clean up my LinkedIn feed?",
     "Install Unlinked, open linkedin.com and pick a filter from the toolbar popup. Recommended keeps posts from people you follow, Ads & suggestions is lighter, and Aggressive hides everything else. Under Advanced you can switch individual items on or off."),
    ("Can I hide LinkedIn ads and promoted posts?",
     "Yes. The Ads & suggestions filter hides promoted posts and LinkedIn’s suggestions, and you can switch ads and suggestions off separately under Advanced."),
    ("Can I still see the posts Unlinked hides?",
     "Yes. Turn Unlinked off at any time with the switch at the top of the popup. Or, under Advanced, turn on “Show a line where posts were hidden” to get a thin “N posts hidden” line you can click to bring them back."),
    ("Does Unlinked collect my data?",
     "No. Unlinked runs only on linkedin.com, works entirely in your browser and sends no data anywhere. Your settings are saved with Chrome sync, and recently seen author names used for muted-people suggestions stay on your device."),
    ("Which browsers does it work in?",
     "Unlinked is built for Chrome on desktop. Other Chromium-based browsers such as Edge and Brave can usually install Chrome Web Store extensions, but Chrome is the supported browser."),
    ("Is Unlinked free?",
     "Yes, it is free to use. If you find it useful, you can support the project by buying me a coffee or through GitHub Sponsors."),
    ("Is Unlinked affiliated with LinkedIn?",
     "No. Unlinked is an independent project and is not affiliated with or endorsed by LinkedIn."),
]


def faq_html():
    out = []
    for q, a in FAQ:
        if q == "Is Unlinked free?":
            a_html = f'Yes, it is free to use. If you find it useful, you can support the project by <a href="{COFFEE}" rel="noopener">buying me a coffee</a> or through <a href="{SPONSORS}" rel="noopener">GitHub Sponsors</a>.'
        elif q == "How do I clean up my LinkedIn feed?":
            a_html = esc(a) + ' Read the <a href="/clean-linkedin-feed/">full guide to cleaning up your LinkedIn feed</a>.'
        elif q == "Does Unlinked collect my data?":
            a_html = esc(a) + ' See the <a href="/privacy/">privacy policy</a>.'
        else:
            a_html = esc(a)
        out.append(f'<details><summary>{esc(q)}</summary><p>{a_html}</p></details>')
    return "\n".join(out)


def feature(ic, title, text):
    return f'<article class="card"><div class="ic">{icon(ic, 22)}</div><h3>{title}</h3><p>{text}</p></article>'


def tick(text):
    return f'<li>{icon("check", 18, 2.5)}<span>{text}</span></li>'


def home():
    title = "Unlinked: Clean LinkedIn Feed – Hide Ads & Suggested Posts"
    desc = "Unlinked is a free Chrome extension that cleans your LinkedIn feed: hide ads, suggested and “liked by” posts and see only the people you follow."
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "Unlinked", "inLanguage": "en",
             "description": "A free Chrome extension that cleans up your LinkedIn feed."},
            {"@type": "SoftwareApplication", "@id": SITE + "/#app", "name": "Unlinked - Clean LinkedIn Feed", "url": SITE + "/",
             "applicationCategory": "BrowserApplication", "operatingSystem": "Chrome",
             "description": "Clean up your LinkedIn feed: see posts from people you follow, without promoted, suggested and other noise.",
             "image": OG, "isAccessibleForFree": True,
             "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, **store_ld()},
            {"@type": "FAQPage", "@id": SITE + "/#faq",
             "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        ],
    }
    hero_alt = "Unlinked toolbar popup showing 24 posts hidden from the LinkedIn feed and four filters: Ads & suggestions, Recommended, Aggressive and Custom"
    adv_alt = "Unlinked advanced settings with switches to hide posts from people you don't follow, network likes and comments, LinkedIn suggestions, ads, reposts, celebrations, hiring posts, polls and videos"
    body = f'''{header()}
<main id="main">

<section class="hero">
<div class="wrap">
<div class="hero-copy">
<p class="eyebrow">{icon("check", 16, 3)} Free Chrome extension for LinkedIn</p>
<h1>A clean LinkedIn feed. <em>Only the people you follow.</em></h1>
<p class="lede">Unlinked is a LinkedIn feed cleaner. It hides ads, suggested posts, &ldquo;liked by&rdquo; activity and other filler, so you see posts from the people and pages you actually follow.</p>
<div class="cta">{soon_or_install()}<a class="btn btn-ghost" href="/store/">Details &amp; screenshots</a></div>
<ul class="trust">
<li>{icon("check", 18, 2.5)} No data collected</li>
<li>{icon("check", 18, 2.5)} Runs only on linkedin.com</li>
<li>{icon("check", 18, 2.5)} Free to use</li>
</ul>
</div>
<div class="shot">
<img src="/assets/presets-960.webp" srcset="/assets/presets-480.webp 480w, /assets/presets-960.webp 960w" sizes="(max-width: 900px) 90vw, 440px" width="960" height="1040" alt="{esc(hero_alt)}" fetchpriority="high">
</div>
</div>
</section>

<section id="features">
<div class="wrap">
<div class="sec-head">
<h2>Everything noisy, gone</h2>
<p>Unlinked is a LinkedIn feed filter that hides the filler and keeps the posts you came to read.</p>
</div>
<div class="grid3">
{feature("eye-off", "Ads &amp; promoted posts", "Hide promoted posts and sponsored content so your feed is made of real posts.")}
{feature("users", "Suggestions &amp; carousels", "Hide LinkedIn&rsquo;s suggested posts, plus the people and jobs carousels in the middle of the feed.")}
{feature("message", "&ldquo;Liked by&rdquo; &amp; &ldquo;commented on&rdquo;", "Skip posts that only appear because someone in your network liked or commented on them.")}
{feature("check", "Only people you follow", "Hide posts from people and pages you don&rsquo;t follow, and keep the ones you chose.")}
{feature("repeat", "Reposts, polls, videos and more", "Switch off reposts, celebrations, hiring posts, polls and videos, one by one.")}
{feature("sidebar", "Less clutter on the page", "Hide the news and puzzles sidebar, your profile sidebar, the messaging pop-up and like and comment counts.")}
</div>
</div>
</section>

<section id="how" class="soft">
<div class="wrap">
<div class="sec-head">
<h2>From cluttered to clean</h2>
<p>Install it, open LinkedIn and your feed cleans itself up. There is nothing to set up.</p>
</div>
<div class="ba" role="img" aria-label="Illustration: a feed with promoted and suggested posts next to the same feed with only posts from people you follow">
<div class="feed">
<h3>Before</h3>
<div class="post"><div class="who"><span class="av"></span><i class="m"></i></div><i></i><i class="s"></i></div>
<div class="post bad"><div class="who"><span class="av"></span><i class="m"></i></div><i></i><i class="s"></i></div>
<div class="post bad"><div class="who"><span class="av"></span><i class="m"></i></div><i></i><i class="s"></i></div>
<div class="post"><div class="who"><span class="av"></span><i class="m"></i></div><i></i><i class="s"></i></div>
</div>
<div class="feed clean">
<h3>After</h3>
<div class="post"><div class="who"><span class="av"></span><i class="m"></i></div><i></i><i class="s"></i></div>
<div class="post"><div class="who"><span class="av"></span><i class="m"></i></div><i></i><i class="s"></i></div>
</div>
</div>
<ol class="steps">
<li><b>Install Unlinked</b><span>Add the extension to Chrome. It is on by default and uses the Recommended filter.</span></li>
<li><b>Open your LinkedIn feed</b><span>Promoted, suggested and &ldquo;liked by&rdquo; posts disappear as you scroll.</span></li>
<li><b>Tune it if you like</b><span>Click the toolbar icon to pick a filter or switch individual items on and off.</span></li>
</ol>
</div>
</section>

<section id="filters">
<div class="wrap split">
<div class="copy">
<h2>Pick a LinkedIn feed filter in one click</h2>
<p class="sub">Four filters cover most feeds. Change them any time from the toolbar popup.</p>
<div class="presets">
<div class="preset"><b>Ads &amp; suggestions</b><span>Hides promoted posts and LinkedIn&rsquo;s suggestions.</span></div>
<div class="preset rec"><b>Recommended</b><span>Also hides posts from people you don&rsquo;t follow, and posts shown because someone in your network liked or commented on them.</span></div>
<div class="preset"><b>Aggressive</b><span>Hides everything except posts from people you follow, plus the clutter around the feed.</span></div>
<div class="preset"><b>Custom</b><span>Your own mix of switches, remembered for next time.</span></div>
</div>
</div>
<div class="media">
<img src="/assets/presets-960.webp" srcset="/assets/presets-480.webp 480w, /assets/presets-960.webp 960w" sizes="(max-width: 900px) 90vw, 440px" width="960" height="1040" alt="{esc(hero_alt)}" loading="lazy">
</div>
</div>
</section>

<section id="advanced" class="soft">
<div class="wrap split rev">
<div class="media">
<img src="/assets/advanced-960.webp" srcset="/assets/advanced-480.webp 480w, /assets/advanced-960.webp 960w" sizes="(max-width: 900px) 90vw, 440px" width="960" height="1190" alt="{esc(adv_alt)}" loading="lazy">
</div>
<div class="copy">
<h2>Fine-tune exactly what disappears</h2>
<p class="sub">Open Advanced to turn individual filters on or off and tidy up the rest of the page.</p>
<ul class="ticks">
{tick("Hide reposts, celebrations, hiring posts, polls and videos")}
{tick("Hide the news and puzzles sidebar, your profile sidebar, the messaging pop-up, and like and comment counts")}
{tick("Mute keywords and people, with name suggestions as you type")}
{tick("Use focus mode to hide the whole feed when you only want to post or check messages")}
{tick("Optionally show a thin &ldquo;N posts hidden&rdquo; line that brings removed posts back")}
</ul>
</div>
</div>
</section>

<section id="privacy">
<div class="wrap">
<div class="sec-head">
<h2>Private by design</h2>
<p>Unlinked collects nothing. It only changes what you see in your own browser.</p>
</div>
<div class="grid3">
{feature("globe", "Runs only on linkedin.com", "The extension is limited to www.linkedin.com and asks for a single permission: storage.")}
{feature("cloud-off", "Nothing leaves your browser", "No accounts, no analytics, no servers. Unlinked sends no data anywhere.")}
{feature("lock", "Your settings stay yours", "Settings are saved with Chrome sync. Recently seen author names, used for muted-people suggestions, stay on your device.")}
</div>
<p class="center"><a href="/privacy/">Read the privacy policy</a></p>
</div>
</section>

<section id="faq" class="soft">
<div class="wrap">
<div class="sec-head">
<h2>Frequently asked questions</h2>
<p>Short answers about cleaning up your LinkedIn feed with Unlinked.</p>
</div>
<div class="faq">
{faq_html()}
</div>
</div>
</section>

<section class="final">
<div class="wrap">
<h2>Ready for a clean LinkedIn feed?</h2>
<p>See only the people you follow. No ads, no suggestions, no filler.</p>
<div class="cta center-cta">{soon_or_install()}<a class="btn btn-ghost" href="/clean-linkedin-feed/">Read the guide</a></div>
</div>
</section>

</main>
{footer()}'''
    write("index.html", head(title, desc, "/", ld=ld) + "\n" + body)


# ----------------------------------------------------------------------------- guide
def guide():
    title = "How to Clean Up Your LinkedIn Feed (Hide Ads & Suggestions)"
    desc = "Why your LinkedIn feed is so noisy and how to clean it up: hide promoted posts, suggestions, “liked by” posts and more, by hand or automatically."
    path = "/clean-linkedin-feed/"
    items = [("How to clean up your LinkedIn feed", None)]
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Article", "@id": SITE + path + "#article", "headline": "How to clean up your LinkedIn feed",
             "description": desc, "image": OG, "datePublished": "2026-10-30", "dateModified": LASTMOD, "inLanguage": "en",
             "mainEntityOfPage": SITE + path,
             "author": {"@type": "Organization", "name": "Unlinked", "url": SITE + "/"},
             "publisher": {"@type": "Organization", "name": "Unlinked", "url": SITE + "/",
                           "logo": {"@type": "ImageObject", "url": SITE + "/icon-192.png"}}},
            breadcrumb_ld([("How to clean up your LinkedIn feed", path)]),
        ],
    }
    img_alt = "Unlinked popup with filters for cleaning up the LinkedIn feed"
    body = f'''{header("guide")}
<main id="main" class="page">
<div class="wrap">
<article class="prose">
{crumbs(items)}
<h1>How to clean up your LinkedIn feed</h1>
<p class="meta">Updated October 30, 2026</p>
<p class="lead">If your LinkedIn feed feels more like an ad board than a place to follow people you know, you are not imagining it. Here is why a LinkedIn feed gets noisy, what you can do about it by hand, and how to clean it up automatically.</p>

<h2>Why your LinkedIn feed is so noisy</h2>
<p>LinkedIn ranks your feed with an algorithm, and it mixes in much more than the posts of the people you follow:</p>
<ul>
<li><b>Promoted posts.</b> Ads that sit between regular posts.</li>
<li><b>Suggested posts.</b> Posts from people and pages you do not follow.</li>
<li><b>Network activity.</b> Posts that show up only because someone you know liked or commented on them.</li>
<li><b>Carousels.</b> &ldquo;People you may know&rdquo; and jobs modules in the middle of the feed.</li>
<li><b>Everything else.</b> Reposts, celebrations, hiring posts, polls and videos, plus the news sidebar, the messaging pop-up and reaction counts around the page.</li>
</ul>

<h2>What you can do by hand</h2>
<ul>
<li>Hide posts you do not want from the menu on each post.</li>
<li>Unfollow the people and pages whose posts you do not want to see.</li>
<li>Sort the feed by recent instead of top, if you prefer it in time order.</li>
<li>Remove connections you do not know.</li>
</ul>
<p>These help, but they work one post or one person at a time, and LinkedIn does not currently give you a setting that switches off promoted or suggested posts. LinkedIn also changes its menus often, so the exact wording may differ.</p>

<h2>Clean your LinkedIn feed automatically with Unlinked</h2>
<p><a href="/">Unlinked</a> is a free Chrome extension that does the filtering for you, inside your own browser.</p>
<ol>
<li><b>Install Unlinked.</b> {f'Add it from the <a href="{STORE_URL}" rel="noopener">Chrome Web Store</a>.' if STORE_URL else "It is coming soon to the Chrome Web Store."} It is on by default and starts with the Recommended filter.</li>
<li><b>Open linkedin.com.</b> Promoted, suggested and &ldquo;liked by&rdquo; posts are hidden as you scroll.</li>
<li><b>Pick a filter.</b> Click the Unlinked icon in the toolbar and choose Ads &amp; suggestions, Recommended, Aggressive or Custom.</li>
<li><b>Fine-tune it.</b> Under Advanced, hide reposts, celebrations, hiring posts, polls and videos, the sidebars, the messaging pop-up and reaction counts, and add muted keywords or people.</li>
</ol>
<figure class="fig">
<img src="/assets/presets-960.webp" srcset="/assets/presets-480.webp 480w, /assets/presets-960.webp 960w" sizes="(max-width: 600px) 90vw, 360px" width="960" height="1040" alt="{esc(img_alt)}" loading="lazy">
<figcaption>The Unlinked popup: pick a filter, see how many posts were hidden.</figcaption>
</figure>

<h2>Tips for a calmer LinkedIn feed</h2>
<ul>
<li>Start with <b>Recommended</b>. Move to <b>Aggressive</b> if you want only the people you follow and nothing around them.</li>
<li>Add <b>muted keywords</b> for phrases you keep seeing, and <b>muted people</b> for accounts you would rather not read.</li>
<li>Use <b>focus mode</b> when you only want to post or check messages.</li>
<li>Turn on <b>Show a line where posts were hidden</b> if you are curious what was removed.</li>
</ul>

<div class="callout">
<b>Your feed stays private.</b> Unlinked runs only on linkedin.com, works entirely in your browser and sends no data anywhere. <a href="/privacy/">Read the privacy policy</a>.
</div>

<p>Questions? Check the <a href="/#faq">FAQ</a> or <a href="/support/">contact support</a>.</p>
</article>
</div>
</main>
{footer()}'''
    write("clean-linkedin-feed/index.html", head(title, desc, path, og_type="article", ld=ld) + "\n" + body)


# ----------------------------------------------------------------------------- privacy
def privacy():
    title = "Privacy Policy | Unlinked"
    desc = "Unlinked collects no data. Read how the Chrome extension and this website handle your information."
    path = "/privacy/"
    items = [("Privacy policy", None)]
    ld = {"@context": "https://schema.org", "@graph": [breadcrumb_ld([("Privacy policy", path)])]}
    body = f'''{header()}
<main id="main" class="page">
<div class="wrap">
<article class="prose">
{crumbs(items)}
<h1>Privacy Policy</h1>
<p class="meta">Last updated: October 30, 2026</p>

<h2>The short version</h2>
<p>Unlinked does not collect, transmit, sell or share any personal data, browsing history or page content. It has no analytics, no tracking and no servers.</p>

<h2>The Chrome extension</h2>
<p>Unlinked is a Chrome extension that hides unwanted posts in the LinkedIn home feed.</p>
<ul>
<li><b>Where it runs.</b> Only on www.linkedin.com. It reads the feed in your browser to decide which posts to hide, and all of that happens on your device.</li>
<li><b>Permissions.</b> Unlinked asks for the <code>storage</code> permission and access to www.linkedin.com. It needs nothing else.</li>
<li><b>Remote code.</b> None. All of the extension&rsquo;s code is bundled in the package.</li>
<li><b>Third parties.</b> Unlinked sends no data to any third party.</li>
<li><b>Support buttons.</b> The popup has two buttons, Buy me a coffee and GitHub Sponsors, that open a Buy Me a Coffee or GitHub Sponsors page in a new tab. They are ordinary links: Unlinked sends nothing when you click them, and what you do on those pages is covered by their own privacy policies.</li>
</ul>

<h2>What is stored</h2>
<ul>
<li>Your settings (chosen filter, switches, muted keywords and muted people) are saved with Chrome&rsquo;s storage and synced through your own Chrome sync account, if you have it turned on.</li>
<li>Recently seen author names, used for muted-people suggestions, stay on your device.</li>
</ul>
<p>You can remove all of this by uninstalling the extension or clearing its data.</p>

<h2>This website</h2>
<p>unlinked.store is a static website. It has no cookies, no analytics, no advertising and no forms. It is hosted on GitHub Pages, so GitHub may process technical data such as your IP address when you visit, as described in the <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" rel="noopener">GitHub privacy statement</a>.</p>

<h2>Changes</h2>
<p>If this policy changes, the new version will be posted on this page with an updated date.</p>

<h2>Contact</h2>
<p>Questions about privacy: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
</article>
</div>
</main>
{footer()}'''
    write("privacy/index.html", head(title, desc, path, ld=ld) + "\n" + body)


# ----------------------------------------------------------------------------- support
def support():
    title = "Support & Help | Unlinked"
    desc = "Get help with Unlinked, the Chrome extension that cleans up your LinkedIn feed. Troubleshooting tips and contact details."
    path = "/support/"
    items = [("Support", None)]
    ld = {"@context": "https://schema.org", "@graph": [breadcrumb_ld([("Support", path)])]}
    body = f'''{header("support")}
<main id="main" class="page">
<div class="wrap">
<article class="prose">
{crumbs(items)}
<h1>Support</h1>
<p class="lead">Something not working, or have an idea? Email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>

<h2>Common questions</h2>
<h3>Posts are not being hidden</h3>
<p>Reload the LinkedIn tab, make sure the switch at the top of the Unlinked popup is on, and check that you are on www.linkedin.com. Then check which filter is selected.</p>
<h3>Unlinked hides too much</h3>
<p>Switch to the lighter <b>Ads &amp; suggestions</b> filter, or choose <b>Custom</b> and turn off the items you want to keep.</p>
<h3>How do I see a hidden post?</h3>
<p>Turn Unlinked off from the popup. Or, under Advanced, turn on <b>Show a line where posts were hidden</b> and click the &ldquo;N posts hidden&rdquo; line where the posts were.</p>
<h3>How do I start over?</h3>
<p>Open the popup and press <b>Reset</b> to go back to the default settings.</p>
<h3>LinkedIn changed and something slipped through</h3>
<p>LinkedIn updates its site often. If Unlinked stops hiding something, email a screenshot (with any personal details covered) and it will be fixed.</p>

<h2>What to include in a bug report</h2>
<ul>
<li>Your Chrome version and operating system</li>
<li>The filter you are using</li>
<li>What you expected and what you saw</li>
</ul>

<p>See also the <a href="/#faq">FAQ</a> and the <a href="/privacy/">privacy policy</a>.</p>
</article>
</div>
</main>
{footer()}'''
    write("support/index.html", head(title, desc, path, ld=ld) + "\n" + body)



# ----------------------------------------------------------------------------- store
def store():
    title = "Get Unlinked for Chrome | Clean LinkedIn Feed Extension"
    desc = "Get Unlinked, the free Chrome extension that hides ads, suggested posts and filler from your LinkedIn feed. Screenshots, permissions and privacy details."
    path = "/store/"
    items = [("Get Unlinked for Chrome", None)]
    shots = [
        ("/assets/store-1", "Unlinked popup showing 24 posts hidden from the LinkedIn feed with the Recommended filter selected"),
        ("/assets/store-2", "Unlinked advanced settings: choose exactly which post types and page elements to hide"),
    ]
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "SoftwareApplication", "@id": SITE + "/#app", "name": "Unlinked - Clean LinkedIn Feed", "url": SITE + path,
             "applicationCategory": "BrowserApplication", "operatingSystem": "Chrome", "softwareVersion": "1.0.0",
             "description": "Clean up your LinkedIn feed: see posts from people you follow, without promoted, suggested and other noise.",
             "image": OG, "screenshot": [SITE + s + "-1280.webp" for s, _ in shots], "isAccessibleForFree": True,
             "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, **store_ld()},
            breadcrumb_ld([("Get Unlinked for Chrome", path)]),
        ],
    }
    figs = "\n".join(
        f'<figure><img src="{s}-1280.webp" srcset="{s}-640.webp 640w, {s}-1280.webp 1280w" sizes="(max-width: 700px) 92vw, 460px" '
        f'width="1280" height="800" alt="{esc(a)}" loading="lazy"></figure>'
        for s, a in shots
    )
    body = f'''{header("store")}
<main id="main" class="page">
<div class="wrap wide">
{crumbs(items)}
<div class="store-head">
<img src="/assets/icon-128.png" width="84" height="84" alt="Unlinked icon">
<div>
<h1>Get Unlinked for Chrome</h1>
<p class="meta">Unlinked - Clean LinkedIn Feed &middot; Free Chrome extension</p>
</div>
</div>
<div class="cta">{soon_or_install()}<a class="btn btn-ghost" href="/clean-linkedin-feed/">How it works</a></div>
<p class="lead">Unlinked cleans up your LinkedIn home feed so you see posts from the people and pages you follow, without ads, suggestions and other filler.</p>

<div class="gallery">
{figs}
</div>

<h2>What you get</h2>
<ul class="ticks">
{tick("Filters you can pick in one click: Ads &amp; suggestions, Recommended, Aggressive or your own Custom mix")}
{tick("Hides promoted posts, suggested posts, &ldquo;liked by&rdquo; and &ldquo;commented on&rdquo; activity, and posts from people you don&rsquo;t follow")}
{tick("Switches for reposts, celebrations, hiring posts, polls, videos, sidebars, the messaging pop-up and like and comment counts")}
{tick("Muted keywords and muted people, with name suggestions as you type")}
{tick("Focus mode, and an optional &ldquo;N posts hidden&rdquo; line that brings removed posts back")}
</ul>

<h2>Details</h2>
<dl class="facts">
<div><dt>Price</dt><dd>Free</dd></div>
<div><dt>Category</dt><dd>Social Networking</dd></div>
<div><dt>Version</dt><dd>1.0.0</dd></div>
<div><dt>Language</dt><dd>English</dd></div>
<div><dt>Works in</dt><dd>Chrome on desktop</dd></div>
<div><dt>Runs on</dt><dd>www.linkedin.com</dd></div>
</dl>

<h2>Permissions, explained</h2>
<ul>
<li><b>storage</b>: saves your filter choice, switches, muted keywords and muted people.</li>
<li><b>Access to www.linkedin.com</b>: lets Unlinked read the feed on the page so it can hide posts. It runs nowhere else.</li>
</ul>
<p>Unlinked asks for nothing else, uses no remote code and sends no data anywhere.</p>

<div class="callout">
<b>Private by design.</b> No accounts, no analytics, no servers. Read the <a href="/privacy/">privacy policy</a>, get help on the <a href="/support/">support page</a>, or see the <a href="/clean-linkedin-feed/">guide to cleaning up your LinkedIn feed</a>.
</div>
<p>Unlinked is free. If it saves you time, you can <a href="{COFFEE}" rel="noopener">buy me a coffee</a> or <a href="{SPONSORS}" rel="noopener">sponsor it on GitHub</a>.</p>
</div>
</main>
{footer()}'''
    write("store/index.html", head(title, desc, path, ld=ld) + "\n" + body)

# ----------------------------------------------------------------------------- 404, robots, sitemap
def not_found():
    title = "Page not found | Unlinked"
    body = f'''{header()}
<main id="main" class="page">
<div class="wrap">
<div class="prose center-text">
<h1>Page not found</h1>
<p class="lead">That page does not exist. Try the <a href="/">home page</a> or the <a href="/clean-linkedin-feed/">guide to cleaning up your LinkedIn feed</a>.</p>
</div>
</div>
</main>
{footer()}'''
    write("404.html", head(title, "This page does not exist.", "/404.html", noindex=True) + "\n" + body)


def robots_sitemap():
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    urls = [("/", "1.0"), ("/store/", "0.9"), ("/clean-linkedin-feed/", "0.8"), ("/support/", "0.5"), ("/privacy/", "0.3")]
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, p in urls:
        lines.append(f"<url><loc>{SITE}{u}</loc><lastmod>{LASTMOD}</lastmod><priority>{p}</priority></url>")
    lines.append("</urlset>")
    write("sitemap.xml", "\n".join(lines) + "\n")


if __name__ == "__main__":
    home(); store(); guide(); privacy(); support(); not_found(); robots_sitemap()
    print("generated")
