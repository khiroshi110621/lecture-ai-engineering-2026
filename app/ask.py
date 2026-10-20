"""第1回: 素のLLMに1回だけ質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする
    uv run python -m app.ask --chat     # 宿題（実装）: 会話履歴を保ったまま続けて質問する

ツールも会話履歴も持たない「素の」呼び出し。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def print_usage(response) -> None:
    """第1回 演習: 入力トークン数と出力トークン数を表示する。"""
    usage = response.usage_metadata
    if usage is None:
        print("[tokens] 取得できませんでした")
        return
    print(f"[tokens] 入力 {usage.prompt_token_count} / 出力 {usage.candidates_token_count}")


def ask(question: str) -> str:
    client = genai.Client(api_key=get_api_key())
    response = client.models.generate_content(model=MODEL, contents=question)
    print_usage(response)
    return response.text


def chat(client=None, read=input) -> None:
    """第1回 宿題（実装）: 会話履歴を保ったまま続けて質問する。空行か exit で終了。

    client.chats.create で作ったチャットは、それまでのやりとりを毎回まとめてモデルに送る。
    そのため、ターンが進むほど入力トークン数が増える。
    """
    client = client or genai.Client(api_key=get_api_key())
    session = client.chats.create(model=MODEL)
    print("続けて質問できます（空行か exit で終了）\n")
    while True:
        try:
            question = read("あなた> ").strip()
        except EOFError:
            break
        if question in ("", "exit", "quit"):
            break
        response = session.send_message(question)
        print(f"\nAI> {response.text}")
        print_usage(response)
        print()


def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMに質問する")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    parser.add_argument("--chat", action="store_true", help="会話履歴を保ったまま続けて質問する")
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    try:
        if args.chat:
            chat()
            return
        print(f"[質問] {args.question}\n")
        print(ask(args.question))
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
