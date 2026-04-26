# Mini X

X (旧 Twitter) 風のとてもシンプルなつぶやき投稿アプリです。

- フロントエンド: 素の HTML / CSS / JavaScript（フレームワーク不使用）
- バックエンド: [Supabase](https://supabase.com)（Auth + Postgres）
- 認証: メール + パスワード（2段階認証なし）
- 機能: 新規登録 / ログイン / つぶやき投稿 / タイムライン表示

## ファイル構成

```
.
├── index.html              # 画面
├── style.css               # スタイル
├── app.js                  # アプリ本体（Supabase クライアント）
├── config.example.js       # Supabase 認証情報のテンプレ（コピーして config.js に）
├── config.js               # 実際の認証情報（gitignore 済み・コミットされない）
├── supabase/schema.sql     # DB スキーマ + RLS ポリシー
└── .github/workflows/      # GitHub Pages へのデプロイ
```

## セットアップ手順

### 1. Supabase プロジェクトを用意

1. <https://supabase.com> でプロジェクトを作成
2. **SQL Editor** を開き、`supabase/schema.sql` の内容を貼り付けて実行
3. **Authentication > Providers > Email** を有効化
   - 動作確認だけ手早く済ませたい場合は **"Confirm email"** をオフにすると、確認メールなしですぐログインできます
4. **Project Settings > API** から以下を控える
   - `Project URL`
   - `anon` `public` key

### 2. ローカルで動かす

```bash
cp config.example.js config.js
# config.js を開いて URL と anon key を貼り付け
```

任意の静的ファイルサーバで開きます（`file://` 直接だと ES Modules が読めません）。

```bash
# 例: Python が入っているなら
python3 -m http.server 8000
# ブラウザで http://localhost:8000 を開く
```

### 3. GitHub Pages にデプロイ

このリポジトリには `.github/workflows/deploy.yml` が含まれており、`main` への push で自動的に GitHub Pages にデプロイされます。

設定手順:

1. GitHub のリポジトリで **Settings > Pages > Build and deployment > Source** を **GitHub Actions** に変更
2. **Settings > Secrets and variables > Actions > Variables** タブで以下のリポジトリ変数を追加
   - `SUPABASE_URL`: 例 `https://xxxx.supabase.co`
   - `SUPABASE_ANON_KEY`: anon public key
3. `main` に push、もしくは Actions タブから手動で `Deploy to GitHub Pages` を実行

ワークフローはビルド時に `config.js` を生成し、Pages にだけ含めます。Git 履歴・リポジトリ本体には `config.js` は含まれません。

> **メモ**: Supabase の `anon` key はブラウザに公開する前提のキーです（公式ドキュメント参照）。実際のアクセス制御は本リポジトリの `schema.sql` で設定する Row Level Security (RLS) ポリシーで行います。`service_role` key は絶対に公開しないでください。

## シークレットの取り扱い

- `.env`、`.env.local`、`config.js`、`config.local.js` は `.gitignore` 済み
- リポジトリにコミットされるのは `config.example.js`（プレースホルダのみ）だけです
- Pages にデプロイされる `config.js` は GitHub Actions 内で Variables から動的に生成されます

## ライセンス

MIT
