from pyrogram import Client, filters
from pyrogram.types import Message
import time

# Inserisci il tuo bot token qui
API_ID = "25047326"
API_HASH = "9673ea812441c77e912979cd0f8a2572"
BOT_TOKEN = "7106494895:AAGyb2xjOyj-DqbDHGlHlJEn2R9ixMo7sZ8"

admin_list = [6305317727]  # Inserisci qui gli ID degli admin
allowed_user = "TrueHatman"  # Tuo username

user_post_count = {}  # Dizionario per tenere traccia dei post inviati da ogni utente

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

print("HatmanPostbot started..")
print("#######################")


# Funzione per inviare un messaggio nel canale
def send_message(client, message):
    client.send_message("1002076625446", message)


# Funzione per contare i post di un utente
def count_user_post(user_id):
    current_time = int(time.time())
    if user_id in user_post_count:
        user_data = user_post_count[user_id]
        if current_time - user_data["timestamp"] < 86400:  # 86400 secondi in 24 ore
            if user_data["count"] < 5:
                user_data["count"] += 1
                return True
            else:
                return False
        else:
            user_data["timestamp"] = current_time
            user_data["count"] = 1
            return True
    else:
        user_post_count[user_id] = {"timestamp": current_time, "count": 1}
        return True


# Definizione del comando /send
@app.on_message(filters.command("send") & filters.user(admin_list))
def send_command(client, message: Message):
    client.send_message(message.chat.id, "Send me the text message, you can also add media")


# Definizione del comando /addadmin
@app.on_message(filters.command("addadmin") & filters.user(allowed_user))
def add_admin_command(client, message: Message):
    if len(message.command) == 2:
        try:
            new_admin_id = int(message.command[1])
            if new_admin_id not in admin_list:
                admin_list.append(new_admin_id)
                client.send_message(message.chat.id, f"User {new_admin_id} added as admin.")
            else:
                client.send_message(message.chat.id, "This user is already an admin.")
        except ValueError:
            client.send_message(message.chat.id, "Invalid user ID.")
    elif message.reply_to_message and message.reply_to_message.from_user:
        new_admin_id = message.reply_to_message.from_user.id
        if new_admin_id not in admin_list:
            admin_list.append(new_admin_id)
            client.send_message(message.chat.id, f"User {new_admin_id} added as admin.")
        else:
            client.send_message(message.chat.id, "This user is already an admin.")
    else:
        client.send_message(message.chat.id, "Reply to a user's message or use /addadmin <user_id> to add them as admin.")


# Gestisci l'input dopo il comando /send
@app.on_message(filters.text & filters.user(admin_list))
def handle_text(client, message: Message):
    if message.reply_to_message and message.reply_to_message.text == "Send me the text message, you can also add media":
        if count_user_post(message.from_user.id):
            # Incrementa il conteggio dei post dell'utente
            user_post_count[message.from_user.id]["count"] += 1

            # Crea il messaggio di conferma
            confirmation_message = (
                "✅ Post correctly sent!\n"
                f"📬 Posts Made: {user_post_count[message.from_user.id]['count']} / 5"
            )

            # Invia il messaggio di conferma
            client.send_message(message.chat.id, confirmation_message)

            # Continua con la gestione del messaggio inviato nel canale
            text = message.text
            sender_name = message.from_user.first_name
            sender_link = f'<a href="tg://user?id={message.from_user.id}">{sender_name}</a>'
            
            final_message = f"{text}\n\n📬 Posted By {sender_link}"
            
            send_message(client, final_message)
        else:
            # Cambiato il messaggio di risposta in inglese
            client.send_message(message.chat.id, "You have exceeded the limit of 5 posts per day.")

app.run()
