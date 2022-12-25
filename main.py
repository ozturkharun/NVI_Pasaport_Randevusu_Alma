from selenium import webdriver
import time

print("Randevu alma modülüne hoşgeldiniz.")

isim="HARUN"
soyisim="...."
tc="585...."
dt_gun=".."
dt_ay=".."
dt_yil="...."
tel="546..."

# --------Driver Kurulumu--------

browser_path = "C:\Drivers\chromedriver.exe"
driver = webdriver.Chrome(executable_path=browser_path)
driver.get("https://randevu.nvi.gov.tr/")

# --------Web sitesi içindeki xpath ler (baş)--------

# Açılış Sayfası
pasaport_path = '/html/body/div[1]/div[1]/div/div/div[2]/form/div/a[3]/div/div/div/p'
kabul_ediyorum_path = '/html/body/div[2]/div[2]/div/div/div/div/div/div/div/div[4]/button[1]'
bordo_pasaport_path = '/html/body/div[1]/div[1]/div/div/div/form/div[1]/div/div/div/div/div[1]/div/button'

# Bilgi Giriş Sayfası
isim_path = '/html/body/div[1]/div[1]/div/div/div/form/div[2]/div[1]/div[1]/div/input'
soyisim_path = '/html/body/div[1]/div[1]/div/div/div/form/div[2]/div[1]/div[2]/div/input'
tc_path = '//*[@id="IdentityNo"]'
dt_gun_path = '/html/body/div[1]/div[1]/div/div/div/form/div[2]/div[1]/div[4]/div/div/div[1]/input'
dt_ay_path = '/html/body/div[1]/div[1]/div/div/div/form/div[2]/div[1]/div[4]/div/div/div[2]/input'
dt_yil_path = '/html/body/div[1]/div[1]/div/div/div/form/div[2]/div[1]/div[4]/div/div/div[3]/input'
tel_path = '/html/body/div[1]/div[1]/div/div/div/form/div[2]/div[1]/div[5]/div/input'

# step2 (İl İlçe Seçim) Sayfası
istanbul_path = '/html/body/div[1]/form/section/div/div[2]/div[3]/div/div/a[2]/span'
il_path =       '/html/body/div[1]/form/section/div/div[2]/div[3]/div/div/a[2]/span'

# step3 () Sayfası


# --------Web sitesi içindeki xpath ler (son)--------


# --------Driver İşlemleri--------

# İlk Tıklamalar
driver.find_element("xpath", pasaport_path).click()
time.sleep(1)
driver.find_element("xpath", kabul_ediyorum_path).click()
time.sleep(2)
driver.find_element("xpath", bordo_pasaport_path).click()
time.sleep(1)
print("Bordo pasaport seçildi!")
# Bilgilerin Doldurulması
driver.find_element("xpath", isim_path).send_keys(isim)
driver.find_element("xpath", soyisim_path).send_keys(soyisim)
driver.find_element("xpath", tc_path).send_keys(tc)
driver.find_element("xpath", dt_gun_path).send_keys(dt_gun)
driver.find_element("xpath", dt_ay_path).send_keys(dt_ay)
driver.find_element("xpath", dt_yil_path).send_keys(dt_yil)
driver.find_element("xpath", tel_path).send_keys(tel)
print("Bilgiler dolduruldu, güvenlik kodunu girin!")

# !!! Güvenlik kodu manuel girilip "Devam Et" butonuna basılacak
# Kullanıcının Butona basmasını bekleme
poll_rate = 1
current_url = driver.current_url
while driver.current_url == current_url:
    time.sleep(poll_rate)
print("Güvenlik kodu girildi, işleme devam ediliyor...")

# Seçilen İlin Belirlenen İlçelerinde Boşluk Kontrolü
ilce_listesi = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41]
tarih_listesi = ["27.12.2022" , "28.12.2022" , "24.12.2022"]
yenileme_sayisi = 0

while True:
    # !!!---Aşağıdaki xpath il_path ile değişiecek---!!!
    driver.find_element("xpath", il_path).click()
    time.sleep(1)
    print("İstenen şehre tıklandı!")

    for i in ilce_listesi:
        # Bu döngü while loop için True ya da False üretmeli

        try:
            # İlçede randevu var demek
            driver.find_element("xpath",'/html/body/div[1]/form/section/div/div[2]/div[5]/div/div/a[{0}]/div/div/label'.format(i))
            uygun_tarih = driver.find_element("xpath",'/html/body/div[1]/form/section/div/div[2]/div[5]/div/div/a[{0}]/div/span'.format(i)).text
            print(i, "Numaralı ilçe için en erken randevu tarihi:", uygun_tarih)

            if uygun_tarih in tarih_listesi:
                print(uygun_tarih, "istenen tarihler içerisinde mevcut.")
                # Randevu günü talep edilen gün ile uyuşuyorsa
                driver.find_element("xpath","/html/body/div[1]/form/section/div/div[2]/div[5]/div/div/a[{0}]/div/div/label".format(i)).click()
                time.sleep(0.5)
                driver.find_element("xpath", "/html/body/div[1]/form/section/div/div[3]/div/div[2]/button").click()
                time.sleep(1)
                driver.find_element("xpath", "/html/body/div[1]/form/section/div/div[2]/div[3]/div/div/a[1]/div/i").click()
                time.sleep(1)
                driver.find_element("xpath", "/html/body/div[1]/form/section/div/div[3]/div/span[2]/button").click()
                time.sleep(1)

                try:
                    # Randevu saati hala varsa

                    #Randevu saati kontrolü:
                    driver.find_element("xpath","/html/body/div[1]/form/section/div[1]/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div")
                    #Randevu saati çekme:
                    randevu_saati = driver.find_element("xpath","/html/body/div[1]/form/section/div[1]/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div").text
                    # Kişi seçimi:
                    driver.find_element("xpath","/html/body/div[1]/form/section/div[1]/div[2]/div[3]/div[1]/div[1]/div/a/div/div/label").click()
                    time.sleep(0.2)
                    #Randevu saati seçimi:
                    driver.find_element("xpath","/html/body/div[1]/form/section/div[1]/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div").click()
                    print("Randevu saati (", randevu_saati, ") bulundu ve seçildi.")
                    time.sleep(0.5)
                    # !!!---Telefonla doğrulama aşamasına gelmemek için aşağıdaki kod deaktif edilir
                    #driver.find_element("xpath","/html/body/div[1]/form/section/div[1]/div[2]/div[3]/div[2]/div/div[2]/button").click()

                    sonuc = True
                    break
                except:
                    # Randevu saati kaybolmuşsa
                    print("Randevu saati seçilemedi, İşlemler tekrarlanacak!")
                    driver.get("https://randevu.nvi.gov.tr/default/step2")
                    sonuc = False
                    # burada ne olacak?
            else:
                # Randevu günü talep edilen gün ile uyuşmuyorsa
                print(uygun_tarih, "istenen tarihler içerisinde yok.")
                raise Exception

        except:
            # İlçede randevu yok demek
            hata_sebebi = "Seçilen ilçelerde uygun bir randevu bulunamadı!"
            sonuc = False

    if sonuc == True:
        print(uygun_tarih,"tarihindeki saat", randevu_saati, "randevusunu almak için telefonunuza gelen sms onay kodunu girin!")
        break

    else:
        # İlçede randevu yok, while loop ile yenileyip devam et
        print(hata_sebebi)
        yenileme_sayisi += 1
        print("Randevu alınamadı, yeniden deneniyor! Yenilenme sayısı:", yenileme_sayisi)




"""
tercih edilen ilçeler seçilecek üsküdar-beykoz vb
tercih edilen tarihler verilecek
"""