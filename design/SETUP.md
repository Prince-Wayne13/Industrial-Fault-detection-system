# Setting up Fault-Detect in VS Code

Follow these in order. Each step is small.

## Once only: install three things

1. **Node.js** (version 20 or newer) from nodejs.org. It runs the React part.
2. **Python** (version 3.11 or newer) from python.org. It runs the Flask part. On Windows, tick "Add Python to PATH" in the installer.
3. **Git for Windows**. It also gives you Git Bash, the terminal used below.

## Make the project

1. Open the project folder in VS Code (File, Open Folder).
2. Open a terminal: Terminal, New Terminal. In the small arrow next to the plus sign, pick **Git Bash**.
3. Type this and press Enter:

   ```
   bash setup.sh
   ```

   It takes a few minutes. It makes the `backend` and `frontend` folders with a starter file for every part, and installs what they need. You can run it again safely. It never overwrites a file that already exists.

## Run it

You need two terminals open side by side. Use the plus sign in the terminal panel to open a second one.

**Terminal 1, the Flask part:**

```
cd backend
source venv/Scripts/activate
python app.py
```

**Terminal 2, the React part:**

```
cd frontend
npm run dev
```

Open http://localhost:5173 in the browser. The page will say Fault-Detect and show the starter screens. To check the two parts are talking, open http://localhost:5173/api/health. You should see `{"ok":true}`.

To stop either one, click in its terminal and press Ctrl and C together.

## Handy VS Code add-ons

Search for these in the Extensions panel (the four squares on the left): **Python**, **ES7+ React/Redux/React-Native snippets**, **ESLint**.

## Secure connection (FR-28e)

The requirement is that the dashboard and server talk over https. On a laptop this needs a local certificate. We will set it up in step 10 of `docs/design/build-plan.md`. Until then the project runs on plain http.

## If something goes wrong

- "bash: command not found": you are not in Git Bash. Change the terminal type as in step 2.
- "Python is not installed": install it, then close and reopen VS Code.
- The page stays blank: check Terminal 1 is still running and shows no red error text.
