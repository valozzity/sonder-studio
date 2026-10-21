# Claude Code setup for Gallery Sonder

Claude Code is an assistant that works on the files in this folder. You type what you want in plain English, for example "make the Closer Look email for the new show from this catalogue PDF", and it builds it, previews it, and packages it for Mailchimp. It can also create pages on the website (Prismic) as drafts for you to review.

The first setup takes about 15 minutes. After that, you open the folder and start typing.

---

## 1. What you need

- A Mac running macOS 13 or newer.
- A paid Claude plan: **Pro** or **Max** at claude.ai. The free plan doesn't include Claude Code.
- A free **GitHub** account (github.com). Carlo will invite it to the private `sonder-studio` repository.

## Get the folder (one time)

The folder lives in a private GitHub repository, so updates from Carlo reach you with one click.

1. Accept the invite email from GitHub ("valozzity invited you to valozzity/sonder-studio").
2. Download **GitHub Desktop** from https://desktop.github.com and sign in with your GitHub account.
3. In GitHub Desktop: **File → Clone Repository**, then the **GitHub.com** tab. Pick `valozzity/sonder-studio` and click **Clone**.

The folder is now at `Documents/GitHub/sonder-studio`.

### Getting updates

When Carlo says there's an update, open GitHub Desktop and click **Fetch origin**, then **Pull origin**. Do this before you start work.

If GitHub Desktop says you have local changes, those are your own show folders and edits. Type a short summary (for example "Spring show emails") and click **Commit to main**, then **Push origin**. That saves your work to the repository, and it also backs it up.

## 2. Install Claude Code

There are two ways to use it. Install both; it's quick.

### A. The Claude desktop app (easiest for day-to-day work)

1. Download it from https://claude.com/download and drag it into Applications.
2. Open it and sign in with your Claude account.
3. Click the **Code** tab, then choose the `Documents/GitHub/sonder-studio` folder as your project.

You can now type requests the same way you'd chat with Claude.

### B. The terminal version (needed once, to connect the website)

1. Open **Terminal**: press Cmd + Space, type "Terminal", then Enter.
2. Paste this line and press Enter:

   ```bash
   curl -fsSL https://claude.ai/install.sh | bash
   ```

   It shows no progress while it downloads. Wait for the prompt to return.
3. Close Terminal and open a new window, then check the install:

   ```bash
   claude --version
   ```

   You should see a version number. If you get "command not found", see Troubleshooting at the end.

## 3. First run

In Terminal, go to the folder and start Claude Code:

```bash
cd ~/Documents/GitHub/sonder-studio
claude
```

(Change the path if you put the folder somewhere else.)

- A browser window opens to sign in. Use the same Claude account.
- Claude Code asks whether you **trust this folder**. Say yes.
- It also asks whether to use the **prismic** server from `.mcp.json`. Say yes; see step 5.

Then type this so Claude installs the two small Python tools the scripts use:

> Install the Python packages the scripts in this folder need (PyMuPDF and Pillow).

It asks permission before running each command. Read the request and approve it.

## 4. How permissions work

Claude Code asks before it runs a command or changes a file. You'll see the exact action and can:

- **Allow once**: for this one action.
- **Allow always**: for that kind of action in this folder, so it stops asking about the same thing.
- **Deny**: it stops and asks you what to do instead.

Nothing goes to Mailchimp or publishes on the website unless you do it or explicitly tell Claude to.

## 5. Connect the website (Prismic), one time

**Do this first, as a Prismic Admin:** in Prismic, open **Settings → Prismic MCP** and switch it on for the `gallerysonder` repository. Activation can take a few minutes.

Then in Terminal, inside the folder:

```bash
claude
```

1. Type `/mcp` and press Enter.
2. Select **prismic**, then **Authenticate**.
3. Sign in to Prismic in the browser that opens.

Claude can now read the site's exhibitions and create or update pages. **Everything it writes goes into a Prismic Release**, which is a draft area. Nothing goes live until you publish that release in Prismic, or tell Claude in so many words "publish the release".

## 6. Everyday use

Open the folder in the desktop app (Code tab) or run `claude` in it, then just ask. Examples:

- "Here's the catalogue PDF for the new show: [drag the file in]. Pull out the works and images."
- "Make the Closer Look email for this show. Feature *Coral Stack*, and put six works in the grid."
- "Swap Snow Stack for Untitled Seed and show prices as 'Price on request'."
- "Change the opening to Saturday, November 14, 7–9 pm everywhere."
- "Package it for Mailchimp."
- "Create the exhibition page in Prismic as a draft, matching the Euphorbia page."

Tips:
- **Drag files straight into the chat** (PDFs, images) instead of typing paths.
- Copy you give it (press text, statements) is kept **word for word**. If you want it edited, say so.
- Ask "show me the email" to preview it in a browser before packaging.
- If something looks off, say what's wrong in plain words: "the cover crop cuts off the title". It will fix it.

## 7. Sending through Mailchimp

1. Ask Claude to **package the email**. It makes a `..._MAILCHIMP.zip` with exactly one HTML file plus the images it uses.
2. In Mailchimp: **Create → Email → Code your own → Import zip**, then choose that zip.
3. Set the subject line, preview text and audience, send yourself a test, then schedule.

Don't zip the folder yourself. Mailchimp can pick up the wrong file if a zip holds more than one `.html` file.

Every link to gallerysonder.com already carries tracking tags (`utm_source=mailchimp&utm_medium=email&utm_campaign=<show>-<email>`), so each email appears separately in Google Analytics under the Email channel.

## 8. What's in this folder

```
sonder-studio/
  README_CLAUDE_CODE_SETUP.md   this file
  .mcp.json                     connects Claude Code to Prismic
  scripts/
    extract_catalogue.py        reads a pre-catalogue PDF: works, prices, images
    package_mailchimp_zip.sh    builds the clean Mailchimp import zip
  shows/
    euphorbia/
      catalogue/                everything pulled out of the Euphorbia PDF
      closer-look/              the Closer Look email (index.html + images)
```

Each new show gets its own folder under `shows/`.

## Troubleshooting

- **"command not found: claude"**: close Terminal fully (Cmd + Q), open it again and retry. If it still fails, run `claude doctor` or see https://code.claude.com/docs/en/troubleshoot-install
- **Prismic says MCP isn't enabled**: a repository Admin has to switch it on (step 5), and it takes a few minutes.
- **Prismic connection stopped working**: in Claude Code, run `/mcp`, choose prismic, and authenticate again.
- **Stuck or confused**: type what you see. For example: "the zip import in Mailchimp shows a blank email, what's wrong?"
- **Help with Claude Code itself**: https://code.claude.com/docs
