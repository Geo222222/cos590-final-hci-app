import streamlit as st
import matplotlib.pyplot as plt
from src.risk.simulation import get_full_market_data

def render_market_data_chart():
    st.subheader("Historical Market Data (ETH/USDT)")
    market_data = get_full_market_data()
    
    fig = plt.figure(figsize=(12, 6))
    plt.plot(market_data['Datetime'], market_data['Close'])
    plt.title("ETH/USDT 1-Hour Price")
    plt.xlabel("Date")
    plt.ylabel("Price (USDT)")
    fig.autofmt_xdate()
    st.pyplot(fig)
