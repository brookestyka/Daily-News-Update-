# Daily Briefing

A free, installable news app for your iPhone. Every day at 10am ET it:

1. pulls the latest headlines from NPR, BBC, The Guardian, NYT, WSJ, CNBC, Fox News, Politico, Al Jazeera and Ars Technica (RSS feeds),
2. has Google's Gemini pick the top 3 stories each for **US politics, economy, tech and foreign affairs**, then write a 2-sentence summary and a "why it matters" line in its own words,
3. publishes them to your app, and
4. pings your phone with a notification that opens it.

Total cost: **$0**. No App Store and no Apple developer account. The app is a website you add to your Home Screen, and it opens full-screen like a normal app.

---

## One-time setup (about 20 minutes)

### 1. Put the project on GitHub
1. Install **GitHub Desktop** (desktop.github.com) and sign in with your GitHub account.
2. In GitHub Desktop: **File > Add Local Repository**, choose this folder. If it says it isn't a repository, click **create a repository**, then **Create Repository**.
3. Click **Publish repository**. **Uncheck "Keep this code private"**. The free version of GitHub Pages needs a public repo. Nothing secret is stored in the code.
4. Name it `daily-briefing` (any name works, but the address below uses it).

> Prefer the command line? `git init -b main && git add . && git commit -m "first commit"`, create an empty public repo on github.com, then `git remote add origin <url> && git push -u origin main`.

### 2. Get a free Gemini key
Go to **aistudio.google.com/apikey**, sign in, click **Create API key**, and copy it.

### 3. Set up notifications (ntfy)
1. On your iPhone, install the free **ntfy** app from the App Store.
2. Invent a long, random topic name, like `brooke-briefing-7f3k29xq81`. Anyone who knows the topic name can send you notifications, so treat it like a password.
3. In the app tap **+**, and subscribe to that topic. Allow notifications when iOS asks.

### 4. Add your two secrets to GitHub
On your repo page: **Settings > Secrets and variables > Actions > New repository secret**. Add:

| Name | Value |
|---|---|
| `GEMINI_API_KEY` | the key from step 2 |
| `NTFY_TOPIC` | your topic name from step 3 |

### 5. Turn on GitHub Pages
**Settings > Pages > Build and deployment > Source: GitHub Actions.**

### 6. Run it once
Go to the **Actions** tab, click **Daily briefing** in the left list, then **Run workflow**. After about a minute your phone should buzz and the app will have real stories. If the run is red, click into it to see the error (see Troubleshooting).

### 7. Install it on your iPhone
1. In **Safari**, open `https://YOUR-GITHUB-USERNAME.github.io/daily-briefing/`
2. Tap **Share**, then **Add to Home Screen**, then **Add**.

From now on it runs by itself every day, weekends included.

---

## How the schedule works
GitHub's timer runs in UTC, so the workflow is scheduled for both 14:00 and 15:00 UTC and only the run that lands on 10am in New York does the work. That handles daylight saving automatically. GitHub's scheduler can start a few minutes late, so expect it between 10:00 and 10:15.

## Changing things
- **Sources or stories per section:** edit `CATEGORIES` and `STORIES_PER_CATEGORY` at the top of `scripts/build_briefing.py`.
- **Tone of the summaries:** edit the prompt in `build_prompt()` in the same file.
- **Look and feel:** everything visual is in `index.html`.
- **Test the feeds on your laptop:** `python3 scripts/build_briefing.py --check-feeds` (on Windows, run `pip install tzdata` once first).

## Troubleshooting
- **The run says some feed failed:** the script skips broken feeds and keeps going. Run `--check-feeds` (or read the "Build today's briefing" log) to see which ones. RSS addresses occasionally change; replace the URL in `CATEGORIES`.
- **The briefing shows headlines but no summaries:** the Gemini call failed. The log shows why. The most common causes are a wrong key or a retired model name. Check the current model names at ai.google.dev and set `GEMINI_MODEL` in the workflow's `env:` block.
- **No notification:** check that `NTFY_TOPIC` exactly matches the topic you subscribed to, and that ntfy notifications are allowed in iPhone Settings.
- **The app is blank:** make sure Pages is set to **GitHub Actions** (step 5) and that the first run finished green.
- **GitHub pauses scheduled runs** on repos with no activity for 60 days. The daily save of the briefing should count as activity, but if the notifications ever stop, open the Actions tab and re-enable the workflow.

## Good to know
- Summaries are written by AI and can be wrong, so every story links to the original articles.
- AP and Reuters don't offer free public feeds, so they aren't included.
- Google's free Gemini tier may use your prompts to improve its products. The only thing sent is public news headlines.
