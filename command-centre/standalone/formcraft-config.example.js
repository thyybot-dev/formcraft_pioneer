// Copy this file to formcraft-config.js and fill it in. This file holds no secrets:
// Firebase web config is public by design (security comes from firestore.rules), and AI keys are asked for on each PC.
window.FORMCRAFT_CONFIG = {
  firebase: {
    apiKey: 'PASTE', authDomain: 'PASTE.firebaseapp.com', projectId: 'PASTE', storageBucket: 'PASTE.appspot.com', appId: 'PASTE'
  },
  owners: ['owner@example.com'],           // emails with full admin rights (must match OWNER_EMAILS in firestore.rules)
  ai: {                                    // remove this block to run with no AI
    // Each model size uses its own provider. Keys are asked for once on each PC and stay there.
    // Check each provider's current model names on its website and put them here.
    tiers: {
      quick:    { provider: 'deepseek', model: 'deepseek-chat' },        // cheap: sorting, extracting, drafts
      default:  { provider: 'claude',   model: 'claude-sonnet-5-5' },    // most agent work
      complex:  { provider: 'claude',   model: 'claude-opus-5-5' },      // planning, development, review
      second:   { provider: 'grok',     model: 'grok-4' },               // second opinions and cross-checks (a different model family)
      offline:  { provider: 'ollama',   model: '<7-8B model>' }          // used automatically when the internet or a provider is down
    }
  }
};
