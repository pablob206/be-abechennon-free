"""Binance test layer module"""
# Third-Party
import pytest

# App
from app.service.binance import build_stream_name


@pytest.mark.parametrize(
    "pair_list, socket_name, interval_list, expected_result",
    [
        (
            ["BTCUSDT", "ETHUSDT", "ADAUSDT"],
            "kline",
            ["1m", "5m", "15m"],
            [
                "btcusdt@kline_1m",
                "btcusdt@kline_5m",
                "btcusdt@kline_15m",
                "ethusdt@kline_1m",
                "ethusdt@kline_5m",
                "ethusdt@kline_15m",
                "adausdt@kline_1m",
                "adausdt@kline_5m",
                "adausdt@kline_15m",
            ],
        ),
        (
            ["BTCUSDT", "ETHUSDT", "ADAUSDT"],
            "trade",
            None,
            ["btcusdt@trade", "ethusdt@trade", "adausdt@trade"],
        ),
        (
            ["BTCUSDT", "ETHUSDT", "ADAUSDT"],
            "aggTrade",
            None,
            ["btcusdt@aggTrade", "ethusdt@aggTrade", "adausdt@aggTrade"],
        ),
        (
            ["BTCUSDT", "ETHUSDT", "ADAUSDT"],
            "depth",
            None,
            ["btcusdt@depth", "ethusdt@depth", "adausdt@depth"],
        ),
    ],
)
def test_build_stream_name(
    pair_list: list,
    socket_name: str,
    interval_list: list,
    expected_result: list,
):
    """
    Test build_stream_name function
    """

    assert (
        build_stream_name(
            pair_list=pair_list, socket_name=socket_name, interval_list=interval_list
        )
        == expected_result
    )
