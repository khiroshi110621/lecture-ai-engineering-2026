"""第1回: トークン数の表示と、会話履歴を保つチャットのテスト（APIは呼ばない）。"""

from types import SimpleNamespace

from app import ask


def _response(text, prompt_tokens, output_tokens):
    usage = SimpleNamespace(prompt_token_count=prompt_tokens, candidates_token_count=output_tokens)
    return SimpleNamespace(text=text, usage_metadata=usage)


class FakeSession:
    """送られた質問を記録し、履歴の長さに応じて入力トークン数を増やす偽チャット。"""

    def __init__(self):
        self.sent = []

    def send_message(self, message):
        self.sent.append(message)
        return _response(f"回答{len(self.sent)}", prompt_tokens=10 * len(self.sent), output_tokens=5)


class FakeClient:
    def __init__(self):
        self.created = 0
        self.session = FakeSession()
        self.chats = self

    def create(self, model):
        self.created += 1
        return self.session


def test_print_usage_shows_input_and_output_tokens(capsys):
    ask.print_usage(_response("x", prompt_tokens=12, output_tokens=34))
    assert "入力 12 / 出力 34" in capsys.readouterr().out


def test_print_usage_without_metadata(capsys):
    ask.print_usage(SimpleNamespace(usage_metadata=None))
    assert "取得できませんでした" in capsys.readouterr().out


def test_chat_keeps_one_session_until_exit(capsys):
    client = FakeClient()
    inputs = iter(["私の名前はヒロシです", "私の名前は？", "exit", "届かない質問"])
    ask.chat(client=client, read=lambda _prompt: next(inputs))

    assert client.created == 1  # 同じチャット（＝同じ履歴）に送り続ける
    assert client.session.sent == ["私の名前はヒロシです", "私の名前は？"]
    out = capsys.readouterr().out
    assert "回答2" in out and "入力 20 / 出力 5" in out
