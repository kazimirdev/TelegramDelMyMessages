<!-- prettier-ignore-start -->
<h1 align="center">🧹 Telegram&nbsp;&mdash; Delete <em>Your</em> Messages</h1>
<p align="center">
  <strong>Clean up any chat— even after you’ve left it.</strong><br>
  <code>TelegramDelMyMessages</code> is a tiny CLI that bulk-deletes <em>your own</em> messages from one or more channels, groups, or PMs, with optional rate control and dry-run preview.
</p>

<p align="center">
  <img alt="PyPI - Python" src="https://img.shields.io/badge/python-3.9%2B-blue">
  <img alt="Telethon" src="https://img.shields.io/badge/telethon-≥1.34-orange">
  <img alt="License" src="https://img.shields.io/github/license/yourname/TelegramDelMyMessages">
</p>
<!-- prettier-ignore-end -->

---

## ✨ Features
- ⚡ **Fast** asynchronous deletion (user-configurable _messages-per-second_)
- 🗑️ Works even if you **left the chat** &nbsp;— supply `id:access_hash`
- 🏷️ Smart log flags  
  ` [M]` media &nbsp; ` [R]` reply &nbsp; ` [Voice]` voice note
- 🕶️ **Dry-run** mode to preview without deleting
- 🛠️ Minimal dependencies: **Telethon + python-dotenv**

---

## 📦 Installation

```bash
git clone https://github.com/kazimirdev/TelegramDelMyMessages.git
cd TelegramDelMyMessages
python -m venv .venv && source .venv/bin/activate   # optional
pip install -r requirements.txt
```

---

## 🔑 API credentials

1. Log in to [https://my.telegram.org/apps](https://my.telegram.org/apps)
2. Create an application and grab your **API ID** and **API HASH**
3. Copy `.env.example` ➜ `src/.env` (or project root) and fill in:

```dotenv
API_ID=123456
API_HASH=abcdef0123456789abcdef0123456789
```

---

## 🚀 Usage

```bash
python app.py --chat -1001222222220 --speed 2 --limit 100
```

| Flag (shorthand) | Description                                                                                                                 | Default |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------- | :-----: |
| `--chat`, `-c`   | Chat identifier. Repeat for multiple chats.<br>Supports `@username`, `t.me/...`, raw `-100…`, plain ID, or `id:access_hash` |    —    |
| `--speed`, `-s`  | Messages **per second** to delete                                                                                           |   `1`   |
| `--limit`, `-l`  | Max messages scanned **per chat**                                                                                           |  `1000` |
| `--dry-run`      | Show what would be deleted, but **don’t** delete                                                                            |   off   |

### Common examples

```bash
# Delete my last 50 messages from a super-group I’m still in
python app.py -c -100999888777 -l 50

# Clean two chats at 5 msg/s
python app.py -c @mygroup -c -100123456 -s 5

# I’ve left the channel – include access-hash
python app.py -c 1222222220:987654321098765432
```

---

## 🛠️ Folder structure

```
TelegramDelMyMessages/
├─ src/
│  ├─ config.py      # .env loader  &  APIError
│  ├─ cli.py         # argparse interface
│  ├─ core.py        # entity resolution & deletion loop
│  └─ __init__.py
├─ app.py            # asyncio entry point
├─ requirements.txt
└─ README.md
```

---

## 🤓 How access-hash works (quick note)

When you **leave** a channel, Telegram still requires its *access-hash* to address
that chat.

* If you **ever** opened the chat on the same account + session, Telethon caches it automatically — the script will fetch it for you.
* Otherwise, either *re-join for a second* (hash is cached), or run a lookup bot such as `@getidsbot` while still inside.

Then call:

```bash
python app.py -c <id>:<access_hash>
```

---

## 🧑‍💻 Contributing

1. Fork ➜ create feature branch (`feat/my-awesome-thing`)
2. Commit using **conventional commits** (`fix(core): …`, `feat(cli): …`)
3. PRs are welcome 🙂

---

## 📄 License

This project is released under the **MIT License** — see `LICENSE` for details.

---
