---
inclusion: always
---

# Cluefin Product Guidelines

## Product Overview

Cluefin is a Korean financial investment toolkit for educational and research purposes. Focus on Korean markets (KOSPI, KOSDAQ, KONEX) with Korean language support throughout.

## Core Architecture

**cluefin-openapi** (Library Package):
- Kiwoom Securities API client with authentication, rate limiting, caching
- KRX (Korea Exchange) API client for market data
- Pydantic models for all data validation
- Domain-specific modules: account, chart, stock info, ranking, sector

**cluefin-cli** (Application):
- Technical analysis with standard indicators (RSI, MACD, Bollinger Bands)
- Terminal-based visualizations using Rich and Plotext
- AI-powered analysis via OpenAI integration
- Interactive inquiry system for market exploration

## Product Conventions

### Korean Market Focus
- All stock codes use 6-digit Korean format (e.g., "005930" for Samsung)
- Support KRW currency formatting and Korean number conventions
- Include Korean company names alongside English when available
- Market hours: 09:00-15:30 KST (Korean Standard Time)

### Data Standards
- Use Pydantic models for all external API responses
- Implement proper error handling for market closures and holidays
- Cache frequently accessed data (stock info, sector classifications)
- Rate limit API calls to respect provider limits

### User Experience
- Provide clear educational disclaimers about investment risks
- Use Rich formatting for terminal output (tables, progress bars, colors)
- Support both interactive and batch processing modes
- Include helpful error messages with suggested actions

### AI Integration
- Use OpenAI for market sentiment analysis and trend interpretation
- Provide context about Korean market characteristics in AI prompts
- Include technical indicator explanations for educational value
- Maintain objectivity - avoid specific buy/sell recommendations

## Compliance & Ethics

- Always include educational purpose disclaimers
- Never provide specific investment advice or recommendations
- Respect API rate limits and terms of service
- Handle sensitive financial data securely (no logging of account details)