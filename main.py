import os
import logging
import random
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from jokes import JOKES, TRIVIA, FUN_FACTS
from config import BOT_TOKEN

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Categories for jokes
CATEGORIES = ["general", "dad", "pun", "programming", "animals"]

# Command Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when /start is issued."""
    user = update.effective_user
    welcome_text = (
        f"🎭 *Welcome to JokerBot, {user.first_name}!* \n\n"
        "I'm your personal comedy assistant! Here's what I can do:\n\n"
        "😂 `/joke` - Get a random joke\n"
        "😂 `/joke [category]` - Get a joke by category (dad, pun, programming, animals, general)\n"
        "🎲 `/roll` - Roll a dice\n"
        "🪙 `/flip` - Flip a coin\n"
        "📊 `/trivia` - Test your knowledge\n"
        "💡 `/fact` - Get a fun fact\n"
        "📋 `/menu` - Show all commands\n\n"
        "🤖 Made with ❤️ by your JokerBot team!"
    )
    
    keyboard = [
        [InlineKeyboardButton("😂 Random Joke", callback_data="random_joke")],
        [InlineKeyboardButton("📚 Categories", callback_data="show_categories")],
        [InlineKeyboardButton("📊 Trivia", callback_data="trivia")],
        [InlineKeyboardButton("💡 Fun Fact", callback_data="fact")],
        [InlineKeyboardButton("📋 Full Menu", callback_data="menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show all available commands."""
    menu_text = (
        "📋 *JokerBot Command Menu*\n\n"
        "😂 `/joke` - Random joke\n"
        "😂 `/joke dad` - Dad joke\n"
        "😂 `/joke pun` - Pun\n"
        "😂 `/joke programming` - Programming joke\n"
        "😂 `/joke animals` - Animal joke\n"
        "😂 `/joke general` - General joke\n"
        "🎲 `/roll [sides]` - Roll dice (default 6)\n"
        "🪙 `/flip` - Flip a coin\n"
        "📊 `/trivia` - Random trivia question\n"
        "💡 `/fact` - Fun fact\n"
        "📋 `/menu` - Show this menu\n"
        "ℹ️ `/about` - About JokerBot\n"
        "👋 `/start` - Welcome message\n\n"
        "_All jokes are handpicked from our growing collection!_"
    )
    await update.message.reply_text(menu_text, parse_mode="Markdown")

async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a joke based on category or random."""
    try:
        if context.args and context.args[0].lower() in CATEGORIES:
            category = context.args[0].lower()
            jokes_list = JOKES.get(category, JOKES["general"])
            joke_text = random.choice(jokes_list)
            await update.message.reply_text(f"😂 *{category.capitalize()} Joke:*\n\n{joke_text}", parse_mode="Markdown")
        else:
            category = random.choice(CATEGORIES)
            jokes_list = JOKES.get(category, JOKES["general"])
            joke_text = random.choice(jokes_list)
            await update.message.reply_text(f"😂 *Random Joke:*\n\n{joke_text}", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text("Oops! Something went wrong. Try again! 😅")

async def roll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Roll a dice with custom sides."""
    try:
        if context.args and context.args[0].isdigit():
            sides = int(context.args[0])
            if sides < 2:
                await update.message.reply_text("❌ Please choose a number greater than 1.")
                return
        else:
            sides = 6
        
        result = random.randint(1, sides)
        await update.message.reply_text(f"🎲 Rolling a {sides}-sided die...\n\n*Result: {result}!*", parse_mode="Markdown")
    except ValueError:
        await update.message.reply_text("❌ Please provide a valid number for the dice sides.")

async def flip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Flip a coin."""
    result = random.choice(["Heads 🪙", "Tails 🪙"])
    await update.message.reply_text(f"🪙 Flipping a coin...\n\n*{result}!*", parse_mode="Markdown")

async def trivia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a trivia question."""
    question = random.choice(TRIVIA)
    await update.message.reply_text(f"📊 *Trivia Time!*\n\n{question}\n\n_Reply with your answer!_", parse_mode="Markdown")

async def fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a fun fact."""
    fact_text = random.choice(FUN_FACTS)
    await update.message.reply_text(f"💡 *Fun Fact:*\n\n{fact_text}", parse_mode="Markdown")

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """About the bot."""
    about_text = (
        "🤖 *About JokerBot*\n\n"
        "JokerBot is your go-to comedy companion on Telegram!\n\n"
        "✨ *Features:*\n"
        "• 100+ handpicked jokes across 5 categories\n"
        "• Fun trivia questions\n"
        "• Interesting facts\n"
        "• Dice rolling & coin flipping\n\n"
        "📈 *Stats:*\n"
        f"• {sum(len(jokes) for jokes in JOKES.values())} jokes in database\n"
        f"• {len(TRIVIA)} trivia questions\n"
        f"• {len(FUN_FACTS)} fun facts\n\n"
        "🚀 *Deployed with:* GitHub + Railway\n\n"
        "_Made with ❤️ for Telegram users worldwide!_"
    )
    await update.message.reply_text(about_text, parse_mode="Markdown")

# Callback Query Handlers
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks."""
    query = update.callback_query
    await query.answer()
    
    if query.data == "random_joke":
        category = random.choice(CATEGORIES)
        jokes_list = JOKES.get(category, JOKES["general"])
        joke_text = random.choice(jokes_list)
        await query.edit_message_text(f"😂 *Random Joke:*\n\n{joke_text}", parse_mode="Markdown")
    
    elif query.data == "show_categories":
        keyboard = []
        for cat in CATEGORIES:
            keyboard.append([InlineKeyboardButton(f"😂 {cat.capitalize()}", callback_data=f"cat_{cat}")])
        keyboard.append([InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("📚 *Choose a category:*", reply_markup=reply_markup, parse_mode="Markdown")
    
    elif query.data.startswith("cat_"):
        category = query.data.replace("cat_", "")
        jokes_list = JOKES.get(category, JOKES["general"])
        joke_text = random.choice(jokes_list)
        await query.edit_message_text(f"😂 *{category.capitalize()} Joke:*\n\n{joke_text}", parse_mode="Markdown")
    
    elif query.data == "trivia":
        question = random.choice(TRIVIA)
        await query.edit_message_text(f"📊 *Trivia Time!*\n\n{question}\n\n_Reply with your answer!_", parse_mode="Markdown")
    
    elif query.data == "fact":
        fact_text = random.choice(FUN_FACTS)
        await query.edit_message_text(f"💡 *Fun Fact:*\n\n{fact_text}", parse_mode="Markdown")
    
    elif query.data == "menu":
        await menu(update, context)
    
    elif query.data == "back_to_menu":
        keyboard = [
            [InlineKeyboardButton("😂 Random Joke", callback_data="random_joke")],
            [InlineKeyboardButton("📚 Categories", callback_data="show_categories")],
            [InlineKeyboardButton("📊 Trivia", callback_data="trivia")],
            [InlineKeyboardButton("💡 Fun Fact", callback_data="fact")],
            [InlineKeyboardButton("📋 Full Menu", callback_data="menu")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("🎭 *Welcome back to JokerBot!*\n\nWhat would you like to do?", reply_markup=reply_markup, parse_mode="Markdown")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors."""
    logger.error(f"Update {update} caused error {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text("⚠️ Something went wrong! Please try again later.")

def main():
    """Start the bot."""
    try:
        print("🤖 JokerBot is starting...")
        print(f"📡 Bot Token: {'*' * 10} (hidden for security)")
        
        # Create the Application
        application = Application.builder().token(BOT_TOKEN).build()

        # Add command handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("menu", menu))
        application.add_handler(CommandHandler("joke", joke))
        application.add_handler(CommandHandler("roll", roll))
        application.add_handler(CommandHandler("flip", flip))
        application.add_handler(CommandHandler("trivia", trivia))
        application.add_handler(CommandHandler("fact", fact))
        application.add_handler(CommandHandler("about", about))

        # Add callback query handler
        application.add_handler(CallbackQueryHandler(button_callback))

        # Add error handler
        application.add_error_handler(error_handler)

        # Start the bot with polling
        print("✅ Bot is running and polling for updates...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        logger.error(f"Error starting bot: {e}")
        raise

if __name__ == "__main__":
    main()
