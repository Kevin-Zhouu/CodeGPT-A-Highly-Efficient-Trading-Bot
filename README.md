# CodeGPT Trading Bot (Winner of 2023 Jane Street Trading Competition)

## Overview

CodeGPT's Trading Bot is a sophisticated algorithm designed for high-frequency trading, tailored to operate in fast-paced financial environments. It won the 2023 Jane Street Trading Competition by implementing a unique strategy that capitalises on market inefficiencies through real-time data analysis and order execution. The bot's architecture is built for performance, with a focus on minimising response times and maximising throughput.

## High-Level Design

The trading bot operates by continuously analysing market data, identifying profitable trading opportunities based on predefined strategies, and executing trades with precision. The system is divided into several key components:

- **Market Data Listener:** Constantly listens for market updates and adjusts the bot's internal state to reflect the current market conditions.
- **Trading Strategy Analyser:** Implements the core logic of the trading bot, analysing market data to identify profitable opportunities and deciding on the actions to take.
- **Order Execution System:** Manages the sending of orders to the market, ensuring they are executed at the best possible prices and times.
- **Risk Management:** Monitors the bot's positions and market conditions to manage and mitigate financial risk.

## Strategy Breakdown: Step3function

The `Step3function` is a pivotal part of the trading bot's strategy. It focuses on arbitrage opportunities in the ETF market, specifically targeting discrepancies in the price of a basket of stocks compared to the price of their corresponding ETF. Here's how it works:

1. **Market Analysis:** The function begins by calculating the implied price of the ETF based on the current prices of the underlying stocks. It compares this with the actual market price of the ETF.
2. **Opportunity Identification:** If the price difference between the calculated ETF price and the market price is significant, the bot identifies an arbitrage opportunity.
3. **Trade Execution:**
   - If the ETF is undervalued compared to the basket, the bot buys the ETF and sells the underlying stocks.
   - If the ETF is overvalued, it does the opposite by selling the ETF and buying the stocks.
4. **Profit Realisation:** The trades are structured to lock in profit due to the price discrepancy, assuming the market corrects this inefficiency.

This strategy capitalises on temporary market inefficiencies that occur due to the lag in the adjustment of the ETF's price to the prices of its constituent stocks. It requires precise execution and fast decision-making to be profitable.

## Running the Bot

To run the bot, follow these steps:

1. **Configuration:** Set up your initial configuration in the `CONFIGURATION` section of the script.
2. **Permissions:** Change the script's permissions to make it executable: `chmod +x bot.py`.
3. **Execution:** Run the bot in a continuous loop to keep it active: `while true; do ./bot.py --test prod-like; sleep 1; done`.

Ensure you have a stable and fast internet connection to minimise latency, which is critical for the success of high-frequency trading strategies.

