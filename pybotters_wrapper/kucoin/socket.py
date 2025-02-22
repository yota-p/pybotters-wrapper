from __future__ import annotations

import uuid

from pybotters_wrapper.core import WebsocketChannels


class KuCoinWebsocketChannels(WebsocketChannels):
    def subscribe(self, topic: str, *args, **kwargs) -> KuCoinWebsocketChannels:
        return super().subscribe(topic, *args, **kwargs)

    def make_subscribe_request(self, topic: str, *args, **kwargs) -> str:
        return {
            "id": str(uuid.uuid4()),
            "type": "subscribe",
            "topic": topic,
            "response": True,
        }

    def _join_symbols(self, symbols):
        if isinstance(symbols, str):
            return symbols
        else:
            return ",".join(symbols)


class KuCoinSpotWebsocketChannels(KuCoinWebsocketChannels):
    def ticker(self, symbol: str, **kwargs) -> KuCoinSpotWebsocketChannels:
        return self.market_ticker(symbol)

    def trades(self, symbol: str, **kwargs) -> KuCoinSpotWebsocketChannels:
        return self.market_match(symbol)

    def orderbook(self, symbol: str, **kwargs) -> KuCoinSpotWebsocketChannels:
        return self.spot_market_level2depth50(symbol)

    def order(self, **kwargs) -> KuCoinSpotWebsocketChannels:
        return self.spot_market_trade_orders()

    def execution(self, **kwargs) -> KuCoinSpotWebsocketChannels:
        return self.spot_market_trade_orders()

    def market_ticker(self, *symbols: str) -> KuCoinSpotWebsocketChannels:
        return self.subscribe("/market/ticker:" + self._join_symbols(symbols))

    def market_match(self, *symbols: str) -> KuCoinSpotWebsocketChannels:
        return self.subscribe("/market/match:" + self._join_symbols(symbols))

    def spot_market_level2depth50(self, *symbols: str) -> KuCoinSpotWebsocketChannels:
        return self.subscribe(
            "/spotMarket/level2Depth50:" + self._join_symbols(symbols)
        )

    def spot_market_trade_orders(self) -> KuCoinSpotWebsocketChannels:
        return self.subscribe("/spotMarket/tradeOrders")


class KuCoinFuturesWebsocketChannels(KuCoinWebsocketChannels):
    def ticker(self, symbol: str, **kwargs) -> KuCoinFuturesWebsocketChannels:
        return self.contract_market_ticker_v2(symbol)

    def trades(self, symbol: str, **kwargs) -> KuCoinFuturesWebsocketChannels:
        return self.contract_market_execution(symbol)

    def orderbook(self, symbol: str, **kwargs) -> KuCoinFuturesWebsocketChannels:
        return self.contract_market_level2depth50(symbol)

    def order(self, **kwargs) -> KuCoinFuturesWebsocketChannels:
        return self.contract_market_trade_orders()

    def execution(self, **kwargs) -> KuCoinFuturesWebsocketChannels:
        return self.contract_market_trade_orders()

    def position(self, symbol: str, **kwargs) -> KuCoinFuturesWebsocketChannels:
        return self.contract_position(symbol)

    def contract_market_ticker_v2(self, symbol: str) -> KuCoinFuturesWebsocketChannels:
        return self.subscribe(f"/contractMarket/tickerV2:{symbol}")

    def contract_market_execution(self, symbol: str) -> KuCoinFuturesWebsocketChannels:
        return self.subscribe(f"/contractMarket/execution:{symbol}")

    def contract_market_level2depth50(
        self, symbol: str
    ) -> KuCoinFuturesWebsocketChannels:
        return self.subscribe(f"/contractMarket/level2Depth50:{symbol}")

    def contract_market_trade_orders(self) -> KuCoinFuturesWebsocketChannels:
        return self.subscribe("/contractMarket/tradeOrders")

    def contract_position(self, symbol: str) -> KuCoinFuturesWebsocketChannels:
        return self.subscribe(f"/contract/position:{symbol}")
