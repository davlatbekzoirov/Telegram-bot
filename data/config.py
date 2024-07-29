from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  
ADMINS = list(map(int, env.list("ADMINS"))) 
IP = env.str("ip")  

CLICK_PAYMENT_TOKEN = env.str("CLICK_PAYMENT_TOKEN")
PAYME_PAYMENT_TOKEN = env.str("PAYME_PAYMENT_TOKEN")
VIDEO_PRICES = env.str("VIDEO_PRICES")