from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import yfinance as yf

import os
from telegram import Bot

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TOKEN)

# Simple in-memory storage
watchlist = []
portfolio = {}

# ---------- BASIC COMMANDS ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to StockAI Bot!\nUse /help to see all commands."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Available commands:\n\n"
        "/start - Start the bot\n"
        "/help - Show help\n"
        "/price HAL - Get stock price\n"
        "/analyze HAL - Analyze stock\n"
        "/fairvalue HAL - Estimate fair value\n"
        "/market - Nifty & Sensex update\n"
        "/watchadd HAL - Add to watchlist\n"
        "/watchlist - Show watchlist\n"
        "/addstock HAL 10 4500 - Add to portfolio\n"
        "/portfolio - Show portfolio"
    )

# ---------- STOCK PRICE ----------
async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /price HAL")
        return

    symbol = context.args[0].upper() + ".NS"

    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")

        if data.empty:
            await update.message.reply_text("Stock not found.")
            return

        price = data["Close"].iloc[-1]
        await update.message.reply_text(
            f"{symbol}\nCurrent Price: ₹{price:.2f}"
        )
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# ---------- STOCK ANALYSIS ----------
async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /analyze HAL")
        return

    symbol = context.args[0].upper() + ".NS"

    try:
        stock = yf.Ticker(symbol)
        info = stock.info

        name = info.get("longName", symbol)
        market_cap = info.get("marketCap", "N/A")
        pe = info.get("trailingPE", "N/A")
        roe = info.get("returnOnEquity", "N/A")

        await update.message.reply_text(
            f"📊 Analysis of {name}\n\n"
            f"Market Cap: {market_cap}\n"
            f"P/E Ratio: {pe}\n"
            f"ROE: {roe}"
        )
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# ---------- FAIR VALUE ----------
async def fairvalue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /fairvalue HAL")
        return

    symbol = context.args[0].upper() + ".NS"

    try:
        stock = yf.Ticker(symbol)
        info = stock.info

        current_price = info.get("currentPrice") or info.get("regularMarketPrice")
        pe = info.get("trailingPE")

        if current_price and pe:
            fair = current_price * (20 / pe)
            await update.message.reply_text(
                f"💰 Fair Value of {symbol}\n\n"
                f"Current Price: ₹{current_price:.2f}\n"
                f"Estimated Fair Value: ₹{fair:.2f}"
            )
        else:
            await update.message.reply_text("Fair value data not available.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# ---------- MARKET OVERVIEW ----------
async def market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        nifty = yf.Ticker("^NSEI").history(period="1d")["Close"].iloc[-1]
        sensex = yf.Ticker("^BSESN").history(period="1d")["Close"].iloc[-1]

        await update.message.reply_text(
            f"📈 Market Overview\n\n"
            f"Nifty 50: {nifty:.2f}\n"
            f"Sensex: {sensex:.2f}"
        )
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# ---------- WATCHLIST ----------
async def watchadd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /watchadd HAL")
        return

    symbol = context.args[0].upper()
    if symbol not in watchlist:
        watchlist.append(symbol)
        await update.message.reply_text(f"{symbol} added to watchlist.")
    else:
        await update.message.reply_text(f"{symbol} is already in watchlist.")

async def show_watchlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not watchlist:
        await update.message.reply_text("Watchlist is empty.")
    else:
        await update.message.reply_text(
            "📋 Watchlist:\n" + "\n".join(watchlist)
        )

# ---------- PORTFOLIO ----------
async def addstock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 3:
        await update.message.reply_text(
            "Usage: /addstock HAL 10 4500"
        )
        return

    symbol = context.args[0].upper()
    qty = int(context.args[1])
    buy_price = float(context.args[2])

    portfolio[symbol] = {"qty": qty, "buy_price": buy_price}

    await update.message.reply_text(
        f"Added {qty} shares of {symbol} at ₹{buy_price}"
    )

async def show_portfolio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not portfolio:
        await update.message.reply_text("Portfolio is empty.")
        return

    message = "📊 Portfolio:\n\n"
    total_value = 0

    for symbol, data in portfolio.items():
        try:
            stock = yf.Ticker(symbol + ".NS")
            current_price = stock.history(period="1d")["Close"].iloc[-1]
            value = current_price * data["qty"]
            total_value += value

            message += (
                f"{symbol}: {data['qty']} shares\n"
                f"Current: ₹{current_price:.2f}\n"
                f"Value: ₹{value:.2f}\n\n"
            )
        except:
            message += f"{symbol}: Data unavailable\n\n"

    message += f"Total Portfolio Value: ₹{total_value:.2f}"
    await update.message.reply_text(message)

# ---------- APP SETUP ----------
app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("price", price))
app.add_handler(CommandHandler("analyze", analyze))
app.add_handler(CommandHandler("fairvalue", fairvalue))
app.add_handler(CommandHandler("market", market))
app.add_handler(CommandHandler("watchadd", watchadd))
app.add_handler(CommandHandler("watchlist", show_watchlist))
app.add_handler(CommandHandler("addstock", addstock))
app.add_handler(CommandHandler("portfolio", show_portfolio))

print("Bot is running...")
app.run_polling()
