from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
from time import sleep
from discord_webhook import DiscordWebhook, DiscordEmbed
import requests

class PS5Bot():
    def __init__(self):
        self.options = Options()
        #self.options.add_argument("--headless")
        #self.options.headless = True
        self.driver = webdriver.Chrome(options=self.options)

            #CONFIG :
        self.logs = True  #True pour activer les logs discord du bot et False pour désactiver
        self.nblogs = 10  #Logs toutes les combien de fois. (10 ici)

            #DISCORD
        self.wh = 'https://discordapp.com/api/webhooks/792801512417001573/9dKW7BMdP-F9XtnvBIsiEvo0TSImOw_aHrL3IY6PF4OHB2TeUVwdk5u2IyJFQZKNXs_E'
        self.whlogs = 'https://discordapp.com/api/webhooks/793114381176143893/7TtSLnR_-r0q4uLjj_9Lr2R7l_zRb0mRhFOm3FHJ-VOoyAt9bWjVaFeiLIVkx3By29xh'

            #TELEGRAM
        self.token = '1474222921:AAELAQiydgFOn05cJvxVc44qVeK9WMsaS2k'
        self.id = '1041095687'

        #NE PAS MODIFIER.
        self.stores = ['amazon','auchan','darty','boulanger','leclerc','fnac','micromania']

        self.lien_amazon = 'https://www.amazon.fr/PlayStation-%C3%89dition-Standard-DualSense-Couleur/dp/B08H93ZRK9'
        self.amazon_stock = False

        self.lien_auchan = 'https://www.auchan.fr/sony-console-ps5-edition-standard/p-c1315865?awc=7728_1609098128_0bfd4d18f5709f6f5057204fa35122fe&utm_medium=affiliation&utm_source=zanox&utm_campaign=generique&utm_content=0&utm_term=285077'
        self.auchan_stock = False

        self.lien_darty = 'https://www.darty.com/nav/achat/informatique/ps4/consoles_ps4/sony_sony_ps5_standard.html'
        self.darty_stock = False

        self.lien_boulanger = 'https://www.boulanger.com/ref/1147567'
        self.boulanger_stock = False

        self.lien_leclerc = 'https://www.culture.leclerc/jeux-video-u/playstation-5-u/consoles-u/console-playstation-5---edition-standard-ps5-0711719395201-pr'
        self.leclerc_stock = False

        self.lien_fnac = 'https://www.fnac.com/Console-Sony-PS5-Edition-Standard/a14119956/w-4'
        self.fnac_stock = False

        self.lien_micromania = 'https://www.micromania.fr/playstation-5-105642.html?kwkuniv=P3CB04A8B6100-vef1ef37u61svlw81322pzplm78xy-cnjgpey3gf&utm_source=netaffiliation&utm_campaign=deeplinks'
        self.micromania_stock = False

    def amazon(self):
        self.amazon_stock = False
        self.driver.get(self.lien_amazon)

        self.src = self.driver.page_source
        self.text_found = re.findall(r'Ajouter au panier', self.src)
        if len(self.text_found)>0:
            self.amazon_stock = True
        else:
            self.amazon_stock = False
    def auchan(self):
        self.auchan_stock = False
        self.driver.get(self.lien_auchan)

        self.src2 = self.driver.page_source
        self.text_found = re.findall(r'product-price--formattedValue', self.src2)
        if len(self.text_found)>3:
            self.auchan_stock=True
        else:
            self.auchan_stock = False

    def darty(self):
        self.darty_stock = False
        self.driver.get(self.lien_darty)

        self.src = self.driver.page_source
        self.text_found = re.findall(r'Ajouter au panier', self.src)
        if len(self.text_found)>0:
            self.darty_stock=True
        else:
            self.darty_stock = False

    def boulanger(self):
        self.boulanger_stock = False
        self.driver.get(self.lien_boulanger)

        self.src = self.driver.page_source
        self.text_found = re.findall(r'onlinePurchase dynamic-onlinePurchase-1650... on', self.src)
        if len(self.text_found)>0:
            self.boulanger_stock = True
        else:
            self.boulanger_stock = False

    def leclerc(self):
        self.leclerc_stock = False
        self.driver.get(self.lien_leclerc)

        self.src = self.driver.page_source
        self.text_found = re.findall(r'Ajouter au panier', self.src)
        if len(self.text_found)>0:
            self.leclerc_stock = True
        else:
            self.leclerc_stock = False

    def fnac(self):
        self.fnac_stock = False
        self.driver.get(self.lien_fnac)

        self.src = self.driver.page_source
        self.text_found = re.findall(r'ff-button ff-button--block ff-button--medium ff-button--orange js-ProductBuy-add', self.src)
        if len(self.text_found)>0:
            self.fnac_stock = True
        else:
            self.fnac_stock = False

    def micromania(self):
        self.micromania_stock = False
        self.driver.get(self.lien_micromania)

        self.src = self.driver.page_source
        self.text_found = re.findall(r'"add-to-cart-container "', self.src)
        if len(self.text_found)>0:
            self.micromania_stock = True
        else:
            self.micromania_stock = False

    def check(self):

        for i in self.stores:


            if eval('self.' + i + '_stock') == True:
                print('\033[94m['+i.upper()+'] ',end='')
                print("\033[92m\033[1mPS5 DISPO !!!")
                exec('bot.' + i + '()')

            else:
                exec('bot.'+i+'()')
                print('\033[94m[' + i.upper() + '] ', end='')
                if eval('self.' + i + '_stock') == True:

                    #DISCORD
                    webhook = DiscordWebhook(url=self.wh)
                    embed = DiscordEmbed(title="PS5 Disponible!",
                                          url=eval('self.lien_'+i),
                                          description="Ps5 chez : "+i, color=0xff0000)
                    embed.set_thumbnail(
                        url="https://img-0.journaldunet.com/T0ZCObyIswIsSyVvO5QU8wq9OBY=/540x/smart/7e026db30a6844fc838c65c2554f8a0a/ccmcms-jdn/20320220.jpg")

                    webhook.add_embed(embed)
                    response = webhook.execute()

                    #TELEGRAM
                    self.mes = 'PS5 disponible chez '+i+' : '+eval('self.lien_'+i)
                    URL = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.id}&text={self.mes}"
                    dark = requests.get(URL)

                    print("\033[92m\033[1mPS5 DISPO !!!")
                else:
                    print("\x1b[31mPS5 indisponible...")



open = True

bot = PS5Bot()

webhook = DiscordWebhook(url=bot.whlogs)
embed = DiscordEmbed(title="BOT Started", description="Sites : "+', '.join(bot.stores), color=0xff0000)
embed.set_thumbnail(url="https://image.flaticon.com/icons/png/512/60/60473.png")
embed.add_embed_field(name="Tourre#0001", value="v1.1", inline=False)

webhook.add_embed(embed)
response = webhook.execute()
v = 0
while open:
    print('[SYSTEM] CHECKING')
    v += 1
    if v%bot.nblogs == 0 and bot.logs:
        # DISCORD
        webhook = DiscordWebhook(url=bot.whlogs)
        embed = DiscordEmbed(title="LOGS",description="STILL RUNING : " + str(v)+' time.', color=0xff0000)
        embed.add_embed_field(name="Tourre#0001", value="v1.1", inline=False)
        embed.set_thumbnail(url="https://image.flaticon.com/icons/png/512/60/60473.png")
        webhook.add_embed(embed)
        response = webhook.execute()

    bot.check()


