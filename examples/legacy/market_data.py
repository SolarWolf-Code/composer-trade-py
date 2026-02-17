"""
Example: Market data for options.

This example shows how to retrieve options chain, contract market data,
and options overview for a given underlying symbol.
"""

from composer import ComposerClient
from composer.models.market_data import ContractType, OptionSortBy, SortOrder
import os
from dotenv import load_dotenv

load_dotenv()


def main():
    client = ComposerClient(
        api_key=os.getenv("COMPOSER_API_KEY"),
        api_secret=os.getenv("COMPOSER_API_SECRET"),
    )

    symbol = "AAPL"

    print("=" * 60)
    print(f"OPTIONS OVERVIEW: {symbol}")
    print("=" * 60)
    overview = client.market_data.get_options_overview(symbol)
    print(f"  Symbol: {overview.symbol}")
    print(f"  Available Expiries: {overview.calendar[:5]}...")
    print()

    print("=" * 60)
    print(f"OPTIONS CHAIN: {symbol}")
    print("=" * 60)
    chain = client.market_data.get_options_chain(
        underlying=symbol,
        contract_type=ContractType.CALL,
        limit=5,
        sort_by=OptionSortBy.EXPIRY,
    )
    print(f"  Total results: {len(chain.results)}")
    print(
        f"  Next cursor: {chain.next_cursor[:50]}..."
        if chain.next_cursor
        else "  Next cursor: None"
    )
    print()

    print("  First page contracts:")
    for contract in chain.results[:2]:
        print(
            f"    - {contract.symbol} (Strike: ${contract.contract_details.strike_price})"
        )
    print()

    if chain.next_cursor:
        print("  Fetching next page...")
        chain_page2 = client.market_data.get_options_chain(
            underlying=symbol,
            next_cursor=chain.next_cursor,
        )
        print(f"  Second page results: {len(chain_page2.results)}")
        for contract in chain_page2.results[:2]:
            print(
                f"    - {contract.symbol} (Strike: ${contract.contract_details.strike_price})"
            )
    print()

    if chain.results:
        contract_symbol = chain.results[0].symbol
        print("=" * 60)
        print(f"OPTIONS CONTRACT: {contract_symbol}")
        print("=" * 60)
        contract = client.market_data.get_options_contract(contract_symbol)
        print(f"  Symbol: {contract.symbol}")
        print(f"  Name: {contract.name}")
        print(f"  Underlying: {contract.underlying_asset_symbol}")
        print(f"  Underlying Price: ${contract.underlying_asset_price}")
        print(f"  Expiry: {contract.contract_details.expiry}")
        print(f"  Strike: ${contract.contract_details.strike_price}")
        print(f"  Type: {contract.contract_details.contract_type.value}")
        print(
            f"  Payoff Status: {contract.payoff_status.value if contract.payoff_status else 'N/A'}"
        )
        print(
            f"  Bid: ${contract.bid.price or 'N/A'} (size: {contract.bid.size or 'N/A'})"
        )
        print(
            f"  Ask: ${contract.ask.price or 'N/A'} (size: {contract.ask.size or 'N/A'})"
        )
        print(
            f"  Last Trade: ${contract.last_trade.price or 'N/A'} (size: {contract.last_trade.size or 'N/A'})"
        )
        print(
            f"  Today's Change: ${contract.todays_change or 'N/A'} ({contract.todays_change_percent or 'N/A'})"
        )
        print(f"  Open Interest: {contract.open_interest}")
        print(f"  Implied Volatility: {contract.implied_volatility or 'N/A'}")
        print(f"  Notional Value: ${contract.notional_value:,.2f}")
        print(f"  Delta Dollars: ${contract.delta_dollars or 'N/A'}")
        print(f"  Greeks:")
        print(f"    Delta: {contract.greeks.delta}")
        print(f"    Gamma: {contract.greeks.gamma}")
        print(f"    Theta: {contract.greeks.theta}")
        print(f"    Vega: {contract.greeks.vega}")
        if contract.greeks.rho:
            print(f"    Rho: {contract.greeks.rho}")
        print(f"  Day Data:")
        print(f"    Open: {contract.day.open or 'N/A'}")
        print(f"    High: {contract.day.high or 'N/A'}")
        print(f"    Low: {contract.day.low or 'N/A'}")
        print(f"    Close: {contract.day.close or 'N/A'}")
        print(f"    Volume: {contract.day.volume or 'N/A'}")


if __name__ == "__main__":
    main()
