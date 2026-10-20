# このリポジトリでの作業ルール

AIエンジニアリング実践講座（AIE2026）の演習・宿題用リポジトリ（講座 repo matsuolab/lecture-ai-engineering-2026 の fork）。

## 提出（ブランチと PR）
- 回ごとに作業ブランチ `lecNN`（例: `lec01`）を作り、そこで作業する。`main` に直接コミットしない。
- PR は必ず **自分の fork の main 向け** に作る。講座本体（matsuolab）には絶対に PR を出さない。
  - `gh pr create --repo khiroshi110621/lecture-ai-engineering-2026 --base main --head lecNN`
  - `gh` が無い場合は push までにして、PR は GitHub の画面で作るよう伝える。
- push・PR 作成の前に、何をするかを説明して確認を取る。

## 環境
- 依存パッケージの版は講座期間中固定。`uv sync --frozen` を使い、`pyproject.toml` / `uv.lock` は変更しない。
- コミット前に `uv run pytest -q` でテストが通ることを確かめる（API キー不要）。
- アプリが呼ぶ LLM は Gemini（`GEMINI_API_KEY`、Codespaces secret）。API キーをコード・コミット・チャットに書かない。
- `ANTHROPIC_API_KEY` は設定しない（Claude Code はサブスクリプションで使う）。

## 学習の進め方
- これは自分の学習のための宿題。答えやコードを丸ごと書かず、まずヒントや読むべき箇所を示す。
- `lectures/NN/answer.md` は自分の言葉で書く。Claude は添削や確認にとどめる。
- コードを変えたときは、何をなぜ変えたかを短く説明する。
