# Libros con TDA

A one-tap web app for picking a book back up when you've lost the thread.

Pick a book → say how far in you are → say what you need → it opens Claude with
the question already written. Built for an adult reader with ADHD who reads
Spanish translations on a phone and loses the plot between sessions.

**Live:** https://chemasala.github.io/libros-con-tda/

---

## Why it doesn't touch your Kindle

It deliberately extracts nothing from Amazon. That isn't laziness — we checked,
and as of August 2026 there is no reliable way to get a "currently reading + %"
list off an Amazon account from a phone:

- iOS sandboxing puts the Kindle app's data out of reach entirely
- Android scoped storage has blocked `/Android/data` browsing since Android 11
- Manage Your Content has no list export and shows no reading progress
- `read.amazon.com` sorts by **purchase** date, not reading activity
- Goodreads syncs start/finish only — **never** the percentage — and its CSV
  export is desktop-only
- The Kindle app's library is a cover-art grid; a list view showing title *text*
  on mobile is unverified, and July 2026's series grouping hides volumes behind
  stacks

So the app doesn't try. You type a title once and it's remembered forever.
Three seconds, and nothing about it can break when Amazon reshuffles a page —
which they did three times in the last year.

The summaries never needed the book's text anyway: Claude already knows the
books. Title + author + how far in you are is enough.

---

## Sending someone their books

Books are seeded through the link, so no one's reading list ends up in a public
repo. Append one `add` parameter per book:

```
?add=Título|Autor|tipo
```

`tipo` is `nofic` or `novela` (default). URL-encode it. Example:

```
https://chemasala.github.io/libros-con-tda/?add=Pensar%20r%C3%A1pido%2C%20pensar%20despacio%7CDaniel%20Kahneman%7Cnofic
```

On open it adds anything new, skips duplicates, then strips the parameters from
the URL so a reload can't add them twice. Same trick works later — to add a book
to someone's phone, just send another link.

## Fiction vs non-fiction

Each book is tagged, and the tag changes what's on screen. For a novel the first
question is *Ponme al día* and *¿Quién es quién?* matters. For non-fiction
"who's who" is close to useless, so **Ideas clave** leads and *Conceptos clave*
takes its place.

The reading-position boundary changes meaning too. In a novel it prevents
spoilers. In non-fiction it stops Claude explaining something using a concept
the author hasn't introduced yet — just as unhelpful, and much easier to miss.

## Spanish translations

If "leo traducciones" is on (it is by default), every question tells Claude to
use the names and terms **as they appear in the Spanish edition**. Without it
Claude answers from the English original, the character names don't match the
page, and the recap makes things worse rather than better.

---

## Running it

Static files. No build, no dependencies, no server.

```
python -m http.server 8740      # then open http://localhost:8740
```

`index.html` is the entire app. Everything is kept in `localStorage` on the
device — no accounts, no backend, nothing leaves the phone except the question
you choose to send to Claude.

Regenerate the icons after editing `icon.svg`:

```
python tools/mkicon.py .
```

## Adding to the home screen

- **iPhone** — open in Safari, Share → *Añadir a pantalla de inicio*
- **Android** — open in Chrome, ⋮ → *Instalar aplicación*

It then launches full-screen with its own icon and behaves like a normal app.
