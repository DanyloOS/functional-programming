
from __future__ import annotations

from functools import reduce
from itertools import islice
from typing import Callable, Iterable, Iterator, TypedDict


class Transaction(TypedDict, total=False):
    amount: float
    type: str


class Account(TypedDict, total=False):
    id: int
    name: str
    city: str
    transactions: list[float] | list[Transaction]
    turnover: float


def compose(*functions: Callable):
    """Композиція: compose(f, g)(x) виконує спочатку g, потім f."""
    def composed(value):
        for function in reversed(functions):
            value = function(value)
        return value
    return composed


def pipe(value, *functions):
    """Послідовно передає результат кожної функції наступній."""
    for function in functions:
        value = function(value)
    return value


def normalize_names() -> Callable[[Iterable[Account]], Iterator[Account]]:
    """Створює нові записи з іменами у форматі Title Case."""
    return lambda accounts: (
        {**account, "name": str(account.get("name", "")).strip().title()}
        for account in accounts
    )


def with_turnover() -> Callable[[Iterable[Account]], Iterator[Account]]:
    """Обчислює оборот рахунку як суму всіх транзакцій."""
    def get_amount(transaction) -> float:
        if isinstance(transaction, dict):
            return float(transaction.get("amount", 0.0))
        return float(transaction)

    return lambda accounts: (
        {
            **account,
            "turnover": sum(
                get_amount(transaction)
                for transaction in (account.get("transactions", []) or [])
            ),
        }
        for account in accounts
    )


def boost_city(city: str, factor: float) -> Callable[[Iterable[Account]], Iterator[Account]]:
    """Застосовує коефіцієнт до обороту рахунків у вибраному місті."""
    def transform(accounts: Iterable[Account]) -> Iterator[Account]:
        for account in accounts:
            turnover = float(account.get("turnover", 0.0))
            new_turnover = turnover * factor if account.get("city") == city else turnover
            yield {**account, "turnover": new_turnover}
    return transform


def filter_min_turnover(minimum: float) -> Callable[[Iterable[Account]], Iterator[Account]]:
    """Залишає рахунки з оборотом не меншим за minimum."""
    return lambda accounts: (
        account for account in accounts
        if float(account.get("turnover", 0.0)) >= minimum
    )


def sort_by_turnover_desc() -> Callable[[Iterable[Account]], list[Account]]:
    """Сортує за оборотом за спаданням, а за однакового обороту — за id."""
    return lambda accounts: sorted(
        accounts,
        key=lambda account: (
            -float(account.get("turnover", 0.0)),
            int(account.get("id", 0)),
        ),
    )


def take(top_n: int) -> Callable[[Iterable[Account]], list[Account]]:
    """Повертає не більше top_n перших записів."""
    if top_n < 0:
        raise ValueError("top_n не може бути від'ємним")
    return lambda accounts: list(islice(accounts, top_n))


def reduce_stats(accounts: Iterable[Account]) -> dict[str, float]:
    """Обчислює count, turnover і avg_turnover через reduce."""
    initial = {"count": 0.0, "turnover": 0.0}
    result = reduce(
        lambda acc, account: {
            "count": acc["count"] + 1,
            "turnover": acc["turnover"] + float(account.get("turnover", 0.0)),
        },
        accounts,
        initial,
    )
    average = result["turnover"] / result["count"] if result["count"] else 0.0
    return {
        "count": result["count"],
        "turnover": result["turnover"],
        "avg_turnover": average,
    }


def build_pipeline(
    top_n: int = 3,
    city: str = "Kyiv",
    factor: float = 1.1,
    min_turnover: float = 0.0,
):
    """Будує конвеєр обробки банківських рахунків."""
    return compose(
        take(top_n),
        sort_by_turnover_desc(),
        filter_min_turnover(min_turnover),
        boost_city(city, factor),
        with_turnover(),
        normalize_names(),
    )


def process_accounts(
    accounts: list[Account],
    top_n: int = 3,
    city: str = "Kyiv",
    factor: float = 1.1,
    min_turnover: float = 0.0,
) -> list[Account]:
    """Запускає конвеєр і повертає Top-N рахунків."""
    return build_pipeline(top_n, city, factor, min_turnover)(accounts)
