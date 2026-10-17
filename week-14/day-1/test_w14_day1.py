"""Day 1 — guardrails, measured.

`test_luhn_alone_still_redacts_eighty_order_numbers_in_a_thousand` is the day.
"""

import random

from guardrails import (cards, digits, guard_answer, guard_query, issuer, luhn, luhn_cards,
                        pattern_cards, redact)

# Published test numbers from the card networks' developer documentation.
TEST_CARDS = ["4242424242424242", "4111111111111111", "4012888888881881", "4000056655665556",
              "5555555555554444", "5105105105105100", "5200828282828210", "2223003122003222",
              "378282246310005", "371449635398431", "6011111111111117", "6011000990139424"]


def order_references(n=1000):
    rng = random.Random(0)
    return ["".join(str(rng.randrange(10)) for _ in range(16)) for _ in range(n)]


def test_digits_and_luhn():
    assert digits("4242 4242-4242 4242") == "4242424242424242"
    assert all(luhn(card) for card in TEST_CARDS)
    assert not luhn("4242424242424241") and not luhn("")


def test_issuer():
    assert [issuer(c) for c in TEST_CARDS] == ["visa"] * 4 + ["mastercard"] * 4 + ["amex"] * 2 + ["discover"] * 2
    assert issuer("9999999999999995") is None


def test_written_with_spaces_and_dashes():
    assert cards("card 4242 4242 4242 4242 please") == ["4242 4242 4242 4242"]
    assert cards("card 5555-5555-5555-4444") == ["5555-5555-5555-4444"]


def test_every_test_card_is_caught_every_way():
    for card in TEST_CARDS:
        line = f"my card is {card}, why was I charged twice"
        assert pattern_cards(line) and luhn_cards(line) and cards(line)


def test_luhn_alone_still_redacts_eighty_order_numbers_in_a_thousand():
    """1,000 random sixteen-digit order references, none of them a card. The pattern
    flags all 1,000. Luhn flags 80. Luhn and the issuer flag 18."""
    lines = [f"order reference {ref} has not arrived" for ref in order_references()]
    flagged = (sum(bool(pattern_cards(l)) for l in lines), sum(bool(luhn_cards(l)) for l in lines),
               sum(bool(cards(l)) for l in lines))
    assert flagged == (1000, 80, 18)


def test_redact():
    assert redact("card 4242424242424242, mail me at a.b@example.com") == "card [CARD], mail me at [EMAIL]"
    assert redact("order 1234567812345678") == "order 1234567812345678"


def test_guard_query():
    assert guard_query("   ") == {"allowed": False, "text": "", "problems": ["empty"]}
    assert guard_query("x" * 501) == {"allowed": False, "text": "", "problems": ["longer than 500 characters"]}
    assert guard_query(" why was 4242424242424242 charged? reply to me@example.com ") == {
        "allowed": True, "text": "why was [CARD] charged? reply to [EMAIL]",
        "problems": ["contained a card number", "contained an email address"]}
    assert guard_query("what does 418 mean") == {"allowed": True, "text": "what does 418 mean", "problems": []}


def test_guard_answer():
    public = lambda chunk: not chunk.startswith("rfc-2324")
    assert guard_answer("418 is a joke [1]", ["rfc-7725#1"], public) == {
        "allowed": True, "answer": "418 is a joke [1]", "problems": []}
    hidden = guard_answer("418 is a joke [1]", ["rfc-2324#3"], public)
    assert hidden == {"allowed": False, "answer": "",
                      "problems": ["cites what this reader may not see: rfc-2324#3"]}
    assert guard_answer("no sources", [], public)["problems"] == ["cites nothing"]
    leaky = guard_answer("your card 4242424242424242 [1]", ["rfc-7725#1"], public)
    assert leaky["answer"] == "your card [CARD] [1]" and leaky["problems"] == ["contains a card number"]
