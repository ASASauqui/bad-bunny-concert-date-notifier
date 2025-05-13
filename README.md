# 🐰 Bad Bunny Concert Date Notifier

**A fun little Python project to stay updated on Bad Bunny concert dates — without having to refresh event pages every day.**

<br>

## 📌 What does this do?

This script monitors [depuertoricopalmundo.com](https://depuertoricopalmundo.com/) and checks if new concert dates for **Bad Bunny** are added in the countries you care about. If it finds a new date that hasn't been seen before, it sends an email notification to one or more recipients.

<br>

## 🎯 Why?

Just for fun — and because checking different pages every few hours isn't it 😅

<br>

## ⚠️ Important Notes

- **Only works with Gmail.** Sending emails from other providers hasn’t been tested and might not work.
- You **must use an App Password** for Gmail — not your regular account password.
- This is a **temporary project**, only useful during this tour cycle.
- The script scrapes **depuertoricopalmundo.com**, not Ticketmaster, because:
  - Their site consolidates all dates in one place
  - Avoids making too many requests to Ticketmaster and risking **IP bans** or bot detection (which... is fair, because this *is* a bot 😅)

<br>

## ⚙️ How to set it up

### 1. Clone the repo and install dependencies

```bash
git clone https://github.com/ASASauqui/bad-bunny-concert-date-notifier.git
cd bad-bunny-concert-date-notifier
pip install -r requirements.txt
```

> Make sure you’re using Python 3.7+.

### 2. Configure your environment variables

Create a file named `.env` in the root directory. Here's a template (`.env.example`) you can copy and edit:

```
SOURCE_EMAIL=source@email.com
DESTINATION_EMAILS=destination1@email.com,destination2@email.com
EMAIL_PASSWORD=asdf dfgh hjkl qwer
```

- `SOURCE_EMAIL`: The Gmail address you’ll use to send the notifications.
- `DESTINATION_EMAILS`: One or more emails (comma-separated) that will receive alerts.
- `EMAIL_PASSWORD`: Gmail **App Password**, not your normal Gmail password.

<br>

## 📧 How to get your Gmail App Password

Gmail doesn’t let you send emails from scripts using your normal password anymore. You need to generate an App Password:

1. Go to your Google Account > [Security](https://myaccount.google.com/security)
2. Turn on **2-Step Verification** (if not already enabled)
3. Go to **App passwords**
4. Select "Mail" as the app and "Other" as the device — name it like `BadBunnyNotifier`
5. Copy the 16-character password (e.g. `asdf dfgh hjkl qwer`) and paste it in `.env` under `EMAIL_PASSWORD`

<br>

## ✏️ Example of how it works

When you run the script:

```bash
python main.py
```

It will prompt:

```
Supported countries: mexico, colombia, chile, argentina, ...
Which countries do you want to monitor? (comma-separated): mexico, colombia
```

Then it’ll check those countries every 20 minutes, and if it finds a new date, you'll get an email like this:

> **Subject:** New Bad Bunny Date in MEXICO! Dec 15 2025  
> **Body:**  
> A new Bad Bunny concert date was detected in Mexico!  
> Date: Dec 15 2025  
> Venue: Estadio GNP Seguros  
> Tickets: https://www.ticketmaster.com.mx/event/...  

<br>

## 🗃 About the `known_dates.txt` file

This is where the script keeps track of which concert dates have already been processed. It looks like this:

```
mexico_dec_10_2025
mexico_dec_11_2025
colombia_jan_23_2026
```

If you delete this file, it will re-send notifications for previously seen dates.

<br>

## 🧠 Things to keep in mind

- This script only works as long as the HTML structure of the site doesn’t change.
- Not designed for heavy traffic or production use — just a light, personal script.
- Works best when running in the background on your local machine or a personal server.

<br>

Made with ❤️ for Bad Bunny fans.  
_“Baby la vida es un ciclo...”_ 🎶
