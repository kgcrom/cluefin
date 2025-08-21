# Project Overview

## About Cluefin

Cluefin is a Korean financial investment toolkit organized as a **uv workspace monorepo** that provides OpenAPI clients for Korean financial services. The project focuses on providing Python clients for:
- Kiwoom Securities API
- Korea Exchange (KRX) API  
- CLI tools for Korean stock market analysis
- ML-powered stock prediction and AI analysis

**Current Development Status**: Phase 2 (DART integration and fundamental analysis enhancement) with active development of machine learning capabilities and interactive inquiry systems.

## Vision & Goals

> **"Clearly Looking U Entered Financial Information"**
> 
> Empowering individual investors with professional-grade analysis tools

### Primary Problems We Solve

1. **Information Fragmentation**: Consolidating scattered financial data from multiple platforms
2. **Technical Barriers**: Simplifying complex Korean financial APIs into intuitive CLI commands
3. **Analysis Overwhelm**: Providing AI-powered insights and objective investment analysis
4. **Time Inefficiency**: Reducing analysis time from 30-60 minutes to under 5 minutes

### Target Users

- Individual investors seeking comprehensive market analysis
- Python developers building financial applications
- Researchers studying Korean financial markets
- Trading algorithm developers

## Key Features

### Core Capabilities
- **Type-Safe API Clients**: Complete OpenAPI clients for Korean financial services
- **Interactive CLI**: Rich terminal interface with menu-driven stock inquiry
- **Technical Analysis**: 20+ built-in indicators via TA-Lib integration
- **AI-Powered Insights**: GPT-4 integration for market analysis and explanations
- **ML Predictions**: LightGBM-based stock movement prediction with SHAP explainability

### Supported Data Sources
- **Kiwoom Securities**: Real-time quotes, account management, order execution
- **Korea Exchange (KRX)**: Market data, indices, sector information
- **OpenAI**: AI-powered analysis and natural language insights
- **Technical Indicators**: RSI, MACD, Bollinger Bands, and more

## Project Philosophy

### Design Principles
1. **Type Safety First**: Extensive Pydantic models with Korean field aliases
2. **Developer Experience**: Intuitive CLI with beautiful Rich UI
3. **Financial Domain Focus**: Korean market timezone and trading hour awareness
4. **Open Source**: Democratizing access to professional-grade financial tools

### Korean Market Specialization
- Market timezone: Korea Standard Time (KST)
- Trading hours: 9:00-15:30 KST consideration in ML models
- Korean field name aliases: `cont_yn: Literal["Y", "N"] = Field(..., alias="cont-yn")`
- Realistic mock data using actual Korean stock codes (e.g., "005930" for Samsung Electronics)
