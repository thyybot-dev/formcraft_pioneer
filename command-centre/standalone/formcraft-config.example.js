// Copy this file to formcraft-config.js and fill it in. This file holds no secrets:
// Firebase web config is public by design (security comes from firestore.rules), and AI keys are asked for on each PC.
window.FORMCRAFT_CONFIG = {
  firebase: {
    apiKey: 'PASTE', authDomain: 'PASTE.firebaseapp.com', projectId: 'PASTE', storageBucket: 'PASTE.appspot.com', appId: 'PASTE'
  },
  owners: ['owner@example.com'],           // emails with full admin rights (must match OWNER_EMAILS in firestore.rules)
  ai: {                                    // remove this block to run with no AI
    provider: 'anthropic',                 // 'anthropic' | 'openai' | 'gemini' | 'mistral' | 'ollama' | 'lmstudio'
    // baseUrl: 'https://generativelanguage.googleapis.com/v1beta/openai',  // Gemini; Mistral: 'https://api.mistral.ai/v1'
    models: { quick: 'claude-haiku-5-5', default: 'claude-sonnet-5-5', complex: 'claude-opus-5-5' }
    // Offline (Formcraft target: 16 GB RAM, 4 GB VRAM): provider: 'ollama', models: { quick: '<3-4B model>', default: '<7-8B model>', complex: '<7-8B model>' }
    // Pick the 7-8B model with tools/offline-model-test (it must pass tool calls reliably). Deep work goes to a cloud model when online.
  }
};
