import copy

from lab2 import build_pipeline, process_accounts, reduce_stats, with_turnover


def sample():
    return [
        {"id": 3, "name": "iryna melnyk", "city": "Kyiv", "transactions": [100, 200]},
        {"id": 1, "name": "anna kovalenko", "city": "Lviv", "transactions": [300]},
        {"id": 2, "name": "bohdan shevchenko", "city": "Kyiv", "transactions": [100, 100]},
    ]


def test_top_n_and_sorting():
    result = process_accounts(sample(), top_n=2, city="Kyiv", factor=1.1)
    assert [account["id"] for account in result] == [3, 1]
    assert result[0]["turnover"] == 330


def test_input_is_not_mutated():
    accounts = sample()
    original = copy.deepcopy(accounts)
    process_accounts(accounts, top_n=3, city="Kyiv", factor=1.1)
    assert accounts == original


def test_reduce_stats():
    stats = reduce_stats([
        {"id": 1, "turnover": 10},
        {"id": 2, "turnover": 20},
    ])
    assert stats == {"count": 2.0, "turnover": 30.0, "avg_turnover": 15.0}


def test_empty_reduce_stats():
    assert reduce_stats([]) == {"count": 0.0, "turnover": 0.0, "avg_turnover": 0.0}


def test_pipeline_composition():
    result = build_pipeline(top_n=1, city="Kyiv", factor=1.0)(sample())
    assert len(result) == 1
    assert result[0]["id"] == 1
