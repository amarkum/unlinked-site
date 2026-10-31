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
OG_ALT = "The Unlinked popup next to the headline: See only the people you follow on LinkedIn."
DISCLAIMER = "Unlinked is an independent project and is not affiliated with or endorsed by LinkedIn. LinkedIn is a trademark of LinkedIn Corporation."

ICONS = {
    "menu": '<line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/>',
    "x": '<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>',
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
        '<link rel="stylesheet" href="/assets/site.css?v=6">',
    ]
    if ld:
        parts.append(jsonld(ld))
    parts.append('</head>')
    return "\n".join(parts)


NAV = [
    ("/#hides", "What it hides", None),
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


# Google's own "Available in the Chrome Web Store" badge, unmodified, as its branding guidelines ask.
def install_badge():
    if STORE_URL:
        return (f'<a class="store-badge" href="{STORE_URL}" rel="noopener">'
                '<img src="/assets/chrome-web-store.png" width="206" height="62" alt="Available in the Chrome Web Store"></a>')
    return '<span class="soon">Coming soon to the Chrome Web Store</span>'


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


# Product images, rendered by tools/shots/render.py at 1x and 2x.
def shot(name, w, h, alt, sizes, eager=False):
    return (f'<img src="/assets/{name}-{w}.webp" srcset="/assets/{name}-{w}.webp {w}w, /assets/{name}-{w * 2}.webp {w * 2}w" '
            f'sizes="{sizes}" width="{w}" height="{h}" alt="{esc(alt)}"' + (' fetchpriority="high"' if eager else ' loading="lazy"') + '>')


POPUP_ALT = "The Unlinked popup: 31 posts hidden and four filters, with Recommended selected"
ADVANCED_ALT = "Unlinked's advanced settings, with a switch for each kind of post and page element"


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
    body = f'''{header()}
<main id="main">

<section class="hero">
<div class="wrap hero-grid">
<div class="hero-copy">
<h1>See only the people you follow on LinkedIn.</h1>
<p class="lede">Unlinked is a free Chrome extension. It clears ads, suggested posts and &ldquo;so-and-so liked this&rdquo; posts out of your LinkedIn feed before you see them.</p>
<div class="cta">{install_badge()}<a href="#hides">What it hides</a></div>
<p class="fine">Free &middot; No account &middot; Works in every LinkedIn language &middot; Nothing leaves your browser</p>
</div>
<div class="hero-shot">
{shot("popup", 560, 587, POPUP_ALT, "(max-width: 900px) 92vw, 460px", eager=True)}
</div>
</div>
</section>

<section id="hides">
<div class="wrap">
<div class="sec-head">
<h2>What Unlinked hides</h2>
<p>LinkedIn mixes your feed with posts you never asked for. Unlinked takes them out as the page loads, so the feed appears already clean.</p>
</div>
<dl class="hides">
<div><dt>Ads</dt><dd>Promoted posts from companies and pages.</dd></div>
<div><dt>Posts your network reacted to</dt><dd>Posts that only show up because someone you know liked or commented on them.</dd></div>
<div><dt>Suggestions</dt><dd>Posts and carousels from people and pages you don&rsquo;t follow, like &ldquo;Jobs recommended for you&rdquo;.</dd></div>
<div><dt>Clutter around the feed</dt><dd>The news sidebar, the messaging pop-up and like counts, if you want those gone too.</dd></div>
</dl>
</div>
</section>

<section id="filters">
<div class="wrap">
<div class="sec-head">
<h2>Choose how strict it is</h2>
<p>Pick a filter from the toolbar. Recommended is on from the start.</p>
</div>
<dl class="hides">
<div><dt>Ads &amp; suggestions</dt><dd>Hides promoted and suggested posts only.</dd></div>
<div><dt>Recommended</dt><dd>Also hides posts from people you don&rsquo;t follow and posts your network reacted to.</dd></div>
<div><dt>Aggressive</dt><dd>Hides everything but the people you follow, plus the clutter around the feed.</dd></div>
<div><dt>Custom</dt><dd>Your own mix of switches, remembered for next time.</dd></div>
</dl>
</div>
</section>

<section id="advanced">
<div class="wrap split rev">
<div class="media">
{shot("popup-advanced", 560, 1040, ADVANCED_ALT, "(max-width: 900px) 92vw, 440px")}
</div>
<div class="copy">
<h2>Or decide for each kind of post</h2>
<p class="sub">Open Advanced for a switch per kind of post.</p>
<ul class="plain">
<li>Reposts, celebrations, hiring posts, polls, videos and games</li>
<li>The news sidebar, your profile sidebar, the messaging pop-up and like counts</li>
<li>Muted keywords and people, with name suggestions as you type</li>
<li>Sort the feed by Recent, so posts come in the order they were written</li>
<li>Focus mode, which hides the whole feed when you only want to post</li>
</ul>
</div>
</div>
</section>

<section id="privacy">
<div class="wrap">
<div class="sec-head">
<h2>Nothing leaves your browser</h2>
<p>Unlinked runs only on linkedin.com and does all of its work on your computer. There are no accounts, no analytics and no servers. Your settings sync through your own Chrome profile.</p>
</div>
<ul class="facts-line">
<li>No data collected</li>
<li>One permission: storage</li>
<li><a href="/privacy/">Privacy policy</a></li>
</ul>
</div>
</section>

<section id="faq">
<div class="wrap">
<div class="sec-head">
<h2>Questions</h2>
</div>
<div class="faq">
{faq_html()}
</div>
</div>
</section>

<section class="final">
<div class="wrap">
<h2>Try it on your own feed</h2>
<p>It&rsquo;s free, and you can switch it off from the toolbar any time.</p>
<div class="cta">{install_badge()}<a href="/clean-linkedin-feed/">Read the guide</a></div>
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
{shot("popup", 560, 587, img_alt, "(max-width: 600px) 92vw, 400px")}
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
    shots = [("popup", 587, POPUP_ALT, "Pick a filter"),
             ("popup-advanced", 1040, ADVANCED_ALT, "Or switch each kind of post on or off")]
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "SoftwareApplication", "@id": SITE + "/#app", "name": "Unlinked - Clean LinkedIn Feed", "url": SITE + path,
             "applicationCategory": "BrowserApplication", "operatingSystem": "Chrome", "softwareVersion": "2.0.0",
             "description": "Clean up your LinkedIn feed: see posts from people you follow, without promoted, suggested and other noise.",
             "image": OG, "screenshot": [f"{SITE}/assets/{name}-1120.webp" for name, *_ in shots], "isAccessibleForFree": True,
             "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, **store_ld()},
            breadcrumb_ld([("Get Unlinked for Chrome", path)]),
        ],
    }
    figs = "\n".join(f'<figure>{shot(name, 560, h, alt, "(max-width: 620px) 92vw, 440px")}<figcaption>{caption}</figcaption></figure>'
                     for name, h, alt, caption in shots)
    body = f'''{header("store")}
<main id="main" class="page">
<div class="wrap wide">
{crumbs(items)}
<div class="store-head">
<img src="/assets/icon-128.png" width="72" height="72" alt="Unlinked icon">
<div>
<h1>Get Unlinked for Chrome</h1>
<p class="meta">Unlinked - Clean LinkedIn Feed &middot; Free Chrome extension</p>
</div>
</div>
<div class="cta">{install_badge()}<a href="/clean-linkedin-feed/">How it works</a></div>
<p class="lead">Unlinked cleans up your LinkedIn home feed so you see posts from the people and pages you follow, without ads, suggestions and other filler.</p>

<div class="gallery">
{figs}
</div>

<h2>What you get</h2>
<ul>
<li>Filters you can pick in one click: Ads &amp; suggestions, Recommended, Aggressive or your own Custom mix</li>
<li>Hides promoted posts, suggested posts, &ldquo;liked by&rdquo; and &ldquo;commented on&rdquo; activity, and posts from people you don&rsquo;t follow</li>
<li>Switches for reposts, celebrations, hiring posts, polls, videos, games, sidebars, the messaging pop-up and like and comment counts</li>
<li>Muted keywords and muted people, with name suggestions as you type</li>
<li>Sorting by Recent, focus mode, and an optional &ldquo;N posts hidden&rdquo; line that brings removed posts back</li>
</ul>

<h2>Details</h2>
<dl class="facts">
<div><dt>Price</dt><dd>Free</dd></div>
<div><dt>Category</dt><dd>Social Networking</dd></div>
<div><dt>Version</dt><dd>2.0.0</dd></div>
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
