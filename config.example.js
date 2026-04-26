// Copy this file to `config.js` and fill in your Supabase project credentials.
// `config.js` is gitignored so it will not be committed to the repository.
//
// Where to find these values:
//   Supabase Dashboard > Project Settings > API
//     - Project URL          -> SUPABASE_URL
//     - Project API keys     -> anon / public  -> SUPABASE_ANON_KEY
//
// The anon key is safe to expose in browsers as long as you have proper
// Row Level Security (RLS) policies in place. See supabase/schema.sql.

window.SUPABASE_CONFIG = {
  SUPABASE_URL: "https://YOUR-PROJECT-REF.supabase.co",
  SUPABASE_ANON_KEY: "YOUR_PUBLIC_ANON_KEY",
};
