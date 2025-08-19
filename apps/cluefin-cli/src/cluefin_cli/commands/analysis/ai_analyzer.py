import asyncio
from typing import Any, Dict

import pandas as pd
from openai import AsyncOpenAI

from cluefin_cli.config.settings import settings


class AIAnalyzer:
    """AI-powered stock analysis using OpenAI."""

    def __init__(self):
        if settings.openai_api_key:
            self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        else:
            self.client = None

    async def analyze_stock(
        self,
        stock_code: str,
        stock_data: pd.DataFrame,
        indicators: pd.DataFrame,  # foreign_data: Dict[str, Any]
    ) -> str | None:
        """
        Generate AI-powered stock analysis.

        Args:
            stock_code: Korean stock code
            stock_data: Historical price data
            indicators: Technical indicators
            foreign_data: Foreign trading data

        Returns:
            Natural language analysis
        """
        if not self.client:
            return "OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."

        try:
            # Prepare data summary
            analysis_data = self._prepare_analysis_data(stock_code, stock_data, indicators)  # , foreign_data)

            # Create prompt
            prompt = self._create_analysis_prompt(analysis_data)

            # Get AI analysis
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional Korean stock market analyst. Provide concise, actionable insights based on technical analysis and market data. Use Korean stock market terminology and context.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=1000,
                temperature=0.7,
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Error generating AI analysis: {str(e)}"

    def _prepare_analysis_data(
        self,
        stock_code: str,
        stock_data: pd.DataFrame,
        indicators: pd.DataFrame,  # foreign_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Prepare data for AI analysis."""
        if stock_data.empty:
            return {}

        latest = stock_data.iloc[-1]
        previous = stock_data.iloc[-2] if len(stock_data) > 1 else latest

        # Price analysis
        price_change = latest["close"] - previous["close"]
        price_change_pct = (price_change / previous["close"] * 100) if previous["close"] != 0 else 0

        # Volume analysis
        avg_volume = stock_data["volume"].tail(20).mean()
        volume_ratio = latest["volume"] / avg_volume if avg_volume > 0 else 1

        # Technical indicators summary
        indicators_summary = {}
        if not indicators.empty:
            latest_indicators = indicators.iloc[-1]

            if not pd.isna(latest_indicators.get("rsi")):
                indicators_summary["rsi"] = latest_indicators["rsi"]

            if not pd.isna(latest_indicators.get("macd")):
                indicators_summary["macd"] = {
                    "value": latest_indicators["macd"],
                    "signal": latest_indicators.get("macd_signal", 0),
                }

            # Moving averages
            sma_20 = latest_indicators.get("sma_20")
            sma_50 = latest_indicators.get("sma_50")
            if not pd.isna(sma_20):
                indicators_summary["sma_20"] = sma_20
                indicators_summary["price_vs_sma20"] = latest["close"] / sma_20 if sma_20 > 0 else 1

            if not pd.isna(sma_50):
                indicators_summary["sma_50"] = sma_50
                indicators_summary["price_vs_sma50"] = latest["close"] / sma_50 if sma_50 > 0 else 1

        return {
            "stock_code": stock_code,
            "current_price": latest["close"],
            "price_change": price_change,
            "price_change_pct": price_change_pct,
            "volume": latest["volume"],
            "volume_ratio": volume_ratio,
            "indicators": indicators_summary,
            # "foreign_trading": foreign_data,
            "data_period": len(stock_data),
        }

    def _create_analysis_prompt(self, data: Dict[str, Any]) -> str:
        """Create analysis prompt for AI."""
        stock_code = data.get("stock_code", "Unknown")
        current_price = data.get("current_price", 0)
        price_change = data.get("price_change", 0)
        price_change_pct = data.get("price_change_pct", 0)
        volume_ratio = data.get("volume_ratio", 1)

        prompt = f"""
Analyze the following Korean stock data for {stock_code}:

Price Information:
- Current Price: ₩{current_price:,.0f}
- Price Change: ₩{price_change:+,.0f} ({price_change_pct:+.2f}%)
- Volume Ratio: {volume_ratio:.2f}x (vs 20-day average)

Technical Indicators:
"""

        indicators = data.get("indicators", {})
        if "rsi" in indicators:
            prompt += f"- RSI (14): {indicators['rsi']:.2f}\n"

        if "macd" in indicators:
            macd_data = indicators["macd"]
            prompt += f"- MACD: {macd_data['value']:.4f} (Signal: {macd_data['signal']:.4f})\n"

        if "price_vs_sma20" in indicators:
            ratio = indicators["price_vs_sma20"]
            prompt += f"- Price vs SMA(20): {ratio:.2f}x\n"

        if "price_vs_sma50" in indicators:
            ratio = indicators["price_vs_sma50"]
            prompt += f"- Price vs SMA(50): {ratio:.2f}x\n"

        # foreign_data = data.get("foreign_trading", {})
        # if foreign_data:
        #     net_foreign = foreign_data.get("buy", 0) - foreign_data.get("sell", 0)
        #     prompt += f"""
        # Foreign Trading:
        # - Foreign Buy: ₩{foreign_data.get("buy", 0):,.0f}
        # - Foreign Sell: ₩{foreign_data.get("sell", 0):,.0f}
        # - Net Foreign: ₩{net_foreign:+,.0f}
        # """

        prompt += """
Please provide a concise analysis including:
1. Current market sentiment and trend direction
2. Key technical signals and their implications
3. Support and resistance levels to watch
4. Short-term outlook and potential catalysts
5. Risk factors to consider

Keep the analysis practical and actionable for Korean retail investors.
"""

        return prompt
