import pandas as pd

from pybotters.models.gmocoin import GMOCoinDataStore
from pybotters_wrapper.common import (
    DataStoreWrapper,
    TickerStore,
    TradesStore,
    OrderbookStore,
)
from pybotters_wrapper.gmocoin import GMOWebsocketChannels


class GMOCoinTickerStore(TickerStore):
    def _normalize(self, d: dict, op: str) -> "TickerItem":
        return self._itemize(d["symbol"].name, float(d["last"]))


class GMOCoinTradesStore(TradesStore):
    def _normalize(self, d: dict, op: str) -> "TradesItem":
        return self._itemize(
            hash(tuple(d)),
            d["symbol"].name,
            d["side"].name,
            float(d["price"]),
            float(d["size"]),
            pd.to_datetime(d["timestamp"]),
        )


class GMOCoinOrderbookStore(OrderbookStore):
    def _normalize(self, d: dict, op: str) -> "OrderbookItem":
        return self._itemize(
            d["symbol"].name, d["side"].name, float(d["price"]), float(d["size"])
        )


class GMOCoinDataStoreWrapper(DataStoreWrapper[GMOCoinDataStore]):
    _NAME = "gmocoin"
    _WRAP_STORE = GMOCoinDataStore
    _WEBSOCKET_CHANNELS = GMOWebsocketChannels
    _TICKER_STORE = (GMOCoinTickerStore, "ticker")
    _TRADES_STORE = (GMOCoinTradesStore, "trades")
    _ORDERBOOK_STORE = (GMOCoinOrderbookStore, "orderbooks")
