import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const config = window.SUPABASE_CONFIG;

const els = {
  authSection: document.getElementById("auth-section"),
  authForm: document.getElementById("auth-form"),
  authMessage: document.getElementById("auth-message"),
  email: document.getElementById("email"),
  password: document.getElementById("password"),
  signinBtn: document.getElementById("signin-btn"),
  signupBtn: document.getElementById("signup-btn"),
  postSection: document.getElementById("post-section"),
  postForm: document.getElementById("post-form"),
  postContent: document.getElementById("post-content"),
  postBtn: document.getElementById("post-btn"),
  charCount: document.getElementById("char-count"),
  feedSection: document.getElementById("feed-section"),
  feed: document.getElementById("feed"),
  feedEmpty: document.getElementById("feed-empty"),
  userArea: document.getElementById("user-area"),
  userEmail: document.getElementById("user-email"),
  signoutBtn: document.getElementById("signout-btn"),
  configWarning: document.getElementById("config-warning"),
};

if (!config || !config.SUPABASE_URL || !config.SUPABASE_ANON_KEY) {
  els.configWarning.hidden = false;
  throw new Error("Supabase config is missing. Copy config.example.js to config.js and fill in your credentials.");
}

const supabase = createClient(config.SUPABASE_URL, config.SUPABASE_ANON_KEY);

function setMessage(text, isError = false) {
  els.authMessage.textContent = text;
  els.authMessage.classList.toggle("error", isError);
}

function formatTimestamp(iso) {
  const date = new Date(iso);
  return date.toLocaleString("ja-JP", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function renderPosts(posts) {
  els.feed.innerHTML = "";
  if (!posts.length) {
    els.feedEmpty.hidden = false;
    return;
  }
  els.feedEmpty.hidden = true;
  for (const post of posts) {
    const li = document.createElement("li");
    li.className = "post";

    const meta = document.createElement("div");
    meta.className = "post-meta";

    const author = document.createElement("span");
    author.textContent = post.author_email ?? "anonymous";

    const time = document.createElement("span");
    time.textContent = formatTimestamp(post.created_at);

    meta.append(author, time);

    const content = document.createElement("p");
    content.className = "post-content";
    content.textContent = post.content;

    li.append(meta, content);
    els.feed.append(li);
  }
}

async function loadFeed() {
  const { data, error } = await supabase
    .from("posts")
    .select("id, content, created_at, author_email")
    .order("created_at", { ascending: false })
    .limit(100);

  if (error) {
    console.error("Failed to load feed:", error);
    els.feedEmpty.hidden = false;
    els.feedEmpty.textContent = "投稿の取得に失敗しました。";
    return;
  }
  renderPosts(data ?? []);
}

function showSignedIn(user) {
  els.authSection.hidden = true;
  els.postSection.hidden = false;
  els.feedSection.hidden = false;
  els.userArea.hidden = false;
  els.userEmail.textContent = user.email ?? "";
  setMessage("");
}

function showSignedOut() {
  els.authSection.hidden = false;
  els.postSection.hidden = true;
  els.feedSection.hidden = true;
  els.userArea.hidden = true;
  els.userEmail.textContent = "";
  els.feed.innerHTML = "";
}

els.authForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  await signIn();
});

els.signupBtn.addEventListener("click", async () => {
  await signUp();
});

async function signIn() {
  setMessage("ログイン中...");
  const { data, error } = await supabase.auth.signInWithPassword({
    email: els.email.value,
    password: els.password.value,
  });
  if (error) {
    setMessage(`ログイン失敗: ${error.message}`, true);
    return;
  }
  if (data.user) {
    showSignedIn(data.user);
    await loadFeed();
  }
}

async function signUp() {
  setMessage("登録中...");
  const { data, error } = await supabase.auth.signUp({
    email: els.email.value,
    password: els.password.value,
  });
  if (error) {
    setMessage(`登録失敗: ${error.message}`, true);
    return;
  }
  if (data.session) {
    showSignedIn(data.user);
    await loadFeed();
  } else {
    setMessage("確認メールを送信しました。メール内のリンクから認証してください。");
  }
}

els.signoutBtn.addEventListener("click", async () => {
  await supabase.auth.signOut();
  showSignedOut();
});

els.postContent.addEventListener("input", () => {
  els.charCount.textContent = `${els.postContent.value.length} / 280`;
});

els.postForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const content = els.postContent.value.trim();
  if (!content) return;

  els.postBtn.disabled = true;
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) {
    els.postBtn.disabled = false;
    return;
  }

  const { error } = await supabase.from("posts").insert({
    content,
    user_id: user.id,
    author_email: user.email,
  });

  els.postBtn.disabled = false;

  if (error) {
    console.error("Failed to post:", error);
    alert(`投稿に失敗しました: ${error.message}`);
    return;
  }

  els.postContent.value = "";
  els.charCount.textContent = "0 / 280";
  await loadFeed();
});

supabase.auth.onAuthStateChange((_event, session) => {
  if (session?.user) {
    showSignedIn(session.user);
    loadFeed();
  } else {
    showSignedOut();
  }
});

const { data: { session } } = await supabase.auth.getSession();
if (session?.user) {
  showSignedIn(session.user);
  await loadFeed();
} else {
  showSignedOut();
}
