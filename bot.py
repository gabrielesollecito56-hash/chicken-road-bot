import telebot
from telebot import types
import json
import os

TOKEN = os.environ.get('BOT_TOKEN')
CPA_LINK = 'https://track.betmenaffiliates.com/visit/?bta=43378&nci=5903&utm_campaign=new_traffic_source&afp10=Facebook&afp1={click_id}'
STATS_FILE = 'stats.json'

bot = telebot.TeleBot(TOKEN)
ADMIN_ID = 520076361

def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r') as f:
            return json.load(f)
    return {'total_users': 0, 'started': 0, 'deposited': 0, 'users': []}

def save_stats(stats):
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f, indent=2)

@bot.message_handler(commands=['start'])
def start(message):
    stats = load_stats()
    user_id = message.from_user.id
    
    if user_id not in stats['users']:
        stats['total_users'] += 1
        stats['users'].append(user_id)
        save_stats(stats)
    
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('🎮 Inizia Ora', callback_data='start_now')
    btn2 = types.InlineKeyboardButton('👤 Parla con un Agente', callback_data='talk_agent')
    markup.add(btn1, btn2)
    
    text = (
        '🐔 *Benvenuto in Chicken Road VIP!* 🐔\n\n'
        '🎰 Il gioco più redditizio del momento!\n\n'
        '💰 Vinci migliaia di euro con la strategia giusta!\n\n'
        'Scegli un\'opzione:'
    )
    
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == 'start_now':
        stats = load_stats()
        stats['started'] += 1
        save_stats(stats)
        
        user_id = call.from_user.id
        link = CPA_LINK.replace('{click_id}', str(user_id))
        
        text = (
            '🎯 *Perfetto! Segui questi passaggi:*\n\n'
            '1️⃣ Clicca sul link qui sotto\n'
            '2️⃣ Registrati sul casino\n'
            '3️⃣ Effettua un deposito\n'
            '4️⃣ Inviami lo screenshot del deposito\n'
            '5️⃣ Riceverai la strategia vincente! 🎁\n\n'
            '🔗 *Link registrazione:*\n' + link + '\n\n'
            '📸 Dopo il deposito, inviami lo screenshot!'
        )
        
        bot.edit_message_text(text, call.message.chat.id, call.message.id)
    
    elif call.data == 'talk_agent':
        text = (
            '👤 *Supporto Clienti*\n\n'
            'Per parlare con un agente, contattaci:\n\n'
            '📱 Telegram: @Servic362\n'
            '⏰ Disponibili 24/7'
        )
        
        bot.edit_message_text(text, call.message.chat.id, call.message.id)

@bot.message_handler(content_types=['photo'])
def photo(message):
    stats = load_stats()
    stats['deposited'] += 1
    save_stats(stats)
    
    text = (
        '✅ *Screenshot ricevuto!*\n\n'
        '🎉 Verifico il deposito...\n\n'
        '📊 *Strategia Chicken Road VIP*\n\n'
        '1️⃣ Inizia con puntate basse (0.50€-1€)\n'
        '2️⃣ Usa il sistema Martingala modificato\n'
        '3️⃣ Raddoppia dopo 2 perdite consecutive\n'
        '4️⃣ Ritorna alla puntata base dopo ogni vincita\n'
        '5️⃣ Mai superare il 20% del bankroll\n\n'
        '💡 *Pro Tip:* Gioca 20:00-00:00 per vincite più alte!\n\n'
        '🎰 Buona fortuna! 🍀'
    )
    
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['stats'])
def stats_cmd(message):
    stats = load_stats()
    conversion = round(stats['deposited'] / max(stats['started'], 1) * 100, 1)
    
    text = (
        '📊 *Statistiche Bot*\n\n'
        '👥 Utenti: ' + str(stats['total_users']) + '\n'
        '🎮 Iniziati: ' + str(stats['started']) + '\n'
        '💰 Depositi: ' + str(stats['deposited']) + '\n\n'
        '📈 Conversione: ' + str(conversion) + '%'
    )
    
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['reply'])
def reply_to_user(message):
    if message.chat.id != ADMIN_ID:
        return
    
    try:
        parts = message.text.split(maxsplit=2)
        if len(parts) < 3:
            bot.reply_to(message, "Uso corretto: /reply ID_UTENTE messaggio")
            return
        
        user_id = int(parts[1])
        reply_text = parts[2]
        
        bot.send_message(user_id, reply_text)
        bot.reply_to(message, f"✅ Messaggio inviato a {user_id}")
    except Exception as e:
        bot.reply_to(message, f"❌ Errore nell'invio: {e}")

@bot.message_handler(func=lambda message: True)
def forward_to_admin(message):
    try:
        username = message.from_user.username or 'Nessun username'
        user_id = message.from_user.id
        first_name = message.from_user.first_name or 'Utente'
        
        text_to_forward = f"💬 Nuovo messaggio da {first_name} (@{username} - ID: {user_id}):\n\n{message.text}"
        
        bot.send_message(ADMIN_ID, text_to_forward)
    except:
        pass

if __name__ == '__main__':
    print('🚀 Bot Chicken Road VIP avviato!')
    bot.infinity_polling()
