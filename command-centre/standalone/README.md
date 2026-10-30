# Formcraft Command Centre: many PCs, one dataset

This is the same Command Centre app, running on Formcraft's own Firebase project instead of inside claude.ai. With it:

- **Many PCs, one dataset.** Every PC and phone that signs in sees the same live data. A change on one shows on the others within a second.
- **Offline.** Each device keeps a local copy. Work continues without internet, and changes sync when the connection comes back.
- **Windows app and phone app.** Open the site in Edge or Chrome and choose **Install app**. On Windows it then runs in its own window from the Start menu. On a phone, use **Add to Home screen**. No separate packaging is needed.
- **Each person signs in.** An admin gives each person a role on the Access page. Firestore rules enforce the same access as in claude.ai: money, people, contracts and licences are admin only.
- **Any AI, or none.** Set the provider in `formcraft-config.js`:
  - online: Anthropic, OpenAI, Gemini or Mistral
  - offline: Ollama or LM Studio
  - remove the `ai` block to run with no AI.
  
  API keys are asked for on each PC and stay on that PC. They are never stored in the shared database.

## Set up (about one hour, once)

1. **Create a new Firebase project**, for example `formcraft-command-centre`. Keep it separate from the website's Firebase project, so that client accounts on the website can never reach company data.
2. **Turn on the services** in the Firebase console:
   - **Authentication:** Google and Email/Password.
   - **Firestore:** production mode. Pick the region closest to Kampala that Firebase offers.
   - **Storage.**
3. **Add a web app** to the project and copy its config.
4. **Fill in the config.** Copy `formcraft-config.example.js` to `formcraft-config.js`. Paste in the config, put the founders' sign-in emails in `owners`, and choose the AI provider.
5. **Put the same founders' emails in the rules files.** Replace `owner@example.com` in `firestore.rules` and in `storage.rules`.
6. **Build and deploy.** From the repository folder:

   ```
   python tools/build_standalone.py
   cd command-centre/standalone
   npm install -g firebase-tools
   firebase login
   firebase use --add        # pick the new project
   firebase deploy
   ```

   The app is then live at `https://<project>.web.app`. You can also connect a subdomain such as `app.formcraftdesignconstruction.com` under Hosting.
7. **Move the data.** In the claude.ai Command Centre, go to **Access → Download full backup (JSON)**. Then sign in to the new app as an owner, go to **Access → Restore**, choose the file and type RESTORE.
8. **Add the team.** Each person signs in once. They then appear on the Access page, where an admin gives them a role. Until they have a role, they see nothing.

## Costs

- The free Spark plan is enough to start.
- Each open device keeps live listeners on about 60 collections. As data grows, switch to the pay-as-you-go Blaze plan and set a budget alert (for example USD 10 a month).
- At three founders and a small team, expect a few dollars a month.

## How it works

- `formcraft-runtime.js` gives the app the same five services it uses in claude.ai, backed by Firebase. Because of this, the app code is unchanged:
  - `db`: Firestore with offline cache
  - `user`: Firebase Auth plus the roles collection
  - `assets`: Firebase Storage
  - `downloads`: browser downloads
  - `sample`: the AI adapter, which runs the tool loop for Anthropic and OpenAI-compatible APIs
- AI proposals go into the shared `pending` collection, so any founder can approve them from any device.
- Firestore cannot store a list inside a list. The runtime stores those as JSON and restores them when reading.
- `sw.js` keeps the app itself available offline. Firestore keeps the data offline.
- Rebuild with `tools/build_standalone.py` whenever `command-centre/index.html` changes, then deploy again.

## Tested here

Tested with a mock of the Firebase SDK and a mock AI endpoint:
- sign-in
- all 60 pages
- writes, approvals and usage tracking
- restore from a backup
- the AI tool loop

It has not yet been run against a real Firebase project or a live AI provider. Do that first, on a test project.
