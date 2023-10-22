from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN_TEST")  # Bot toekn
ADMINS = [1849953640]
# ADMINS = env.list("ADMINS")  # adminlar ro'yxati
IP = env.str("ip")  # Xosting ip manzili
DEVELOPER = env.str("DEVELOPER")
# CHANNELS = [-1001569759901,]
CHANNELS = [-1001208742794,]
