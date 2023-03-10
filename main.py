import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

print("Randevu alma modülüne hoşgeldiniz.")

load_dotenv()
isim = os.getenv("isim")
soyisim = os.getenv("soyisim")
tc = os.getenv("tc")
dt_gun = os.getenv("dt_gun")
dt_ay = os.getenv("dt_ay")
dt_yil = os.getenv("dt_yil")
tel = os.getenv("tel")

# İl, ilçe ve tarih belirleme
il_index = 2  # İstanbul=2 Kocaeli=52 Bursa=23
ilce_listesi = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41]
tarih_listesi = ["29.12.2022", "30.12.2022", "31.12.2022", "02.01.2023", "03.01.2023", "04.01.2023", "05.01.2023", "06.01.2023", "07.01.2023"]

# --------------------------Web sitesi içindeki xpath ler (baş)--------------------------
# Açılış Sayfası
pasaport_path = '/html/body/div[1]/div[1]/div/div/div[2]/form/div/a[3]/div/div/div/p'
kabul_ediyorum_path = '/html/body/div[2]/div[2]/div/div/div/div/div/div/div/div[4]/button[1]'
bordo_pasaport_button_path = '/html/body/div[1]/div[1]/div/div/div/form/div[1]/div/div/div/div/div[1]/div/button'
bordo_pasaport_isim_path = '/html/body/div[1]/div[1]/div/div/div/form/div[1]/div/div/div/div/div[1]/div/h4'

# Bilgi Giriş Sayfası
isim_path = '/html/body/div[1]/div[1]/div/div/div/form/div[2]/div[1]/div[1]/div/input'
soyisim_path = '/html/body/div[1]/div[1]/div/div/div/form/div[2]/div[1]/div[2]/div/input'
tc_path = '//*[@id="IdentityNo"]'
dt_gun_path = '/html/body/div[1]/div[1]/div/div/div/form/div[2]/div[1]/div[4]/div/div/div[1]/input'
dt_ay_path = '/html/body/div[1]/div[1]/div/div/div/form/div[2]/div[1]/div[4]/div/div/div[2]/input'
dt_yil_path = '/html/body/div[1]/div[1]/div/div/div/form/div[2]/div[1]/div[4]/div/div/div[3]/input'
tel_path = '/html/body/div[1]/div[1]/div/div/div/form/div[2]/div[1]/div[5]/div/input'
guvenlik_kodu_path = '/html/body/div/div[1]/div/div/div/form/div[2]/div[1]/div[6]/div/input'

# step2 (İl İlçe Seçim) Sayfası
il_path = '/html/body/div[1]/form/section/div/div[2]/div[3]/div/div/a[{0}]/span'.format(il_index)  # a[x] il indeksi
bos_randevu_butonu_path = '/html/body/div[1]/form/section/div/div[2]/div[5]/div/div/a[{0}]/div/div/label'  # a[x] İlçe indeksi
en_erken_rand_tarihi_path = '/html/body/div[1]/form/section/div/div[2]/div[5]/div/div/a[{0}]/div/span'  # a[x] İlçe indeksi
ilce_path = '/html/body/div/form/section/div/div[2]/div[5]/div/div/a[{0}]/span'  # a[x] İlçe indeksi
step_2_ileri_button_path = '/html/body/div[1]/form/section/div/div[3]/div/div[2]/button'

# step3 (Kişi Seçim) Sayfası
ilk_kisi_ekleme_path = '/html/body/div[1]/form/section/div/div[2]/div[3]/div/div/a[4]/div/i'  # a[x] diğer aile bireylerine randevu almak için
ilk_kisi_path = '/html/body/div/form/section/div/div[2]/div[3]/div/div/a[1]/span'
step_3_ileri_button_path = '/html/body/div[1]/form/section/div/div[3]/div/span[2]/button'

# step4 (Randevu Seçim) Sayfası
randevu_saati_path = '/html/body/div[1]/form/section/div[1]/div[2]/div[3]/div[1]/div[2]/div[2]/div/div[1]/div'
kisi_secimi_path = '/html/body/div[1]/form/section/div[1]/div[2]/div[3]/div[1]/div[1]/div/a/div/div/label'
step_4_ileri_button_path = '/html/body/div[1]/form/section/div[1]/div[2]/div[3]/div[2]/div/div[2]/button'
# --------------------------Web sitesi içindeki xpath ler (son)--------------------------


# --------------------------Randevu Alma Fonksiyonu--------------------------
def randevu_alma():

    global yenileme_sayisi
    yenileme_sayisi = 0

    # --------Driver Kurulumu--------
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))
    driver.get("https://randevu.nvi.gov.tr/")
    driver.set_window_rect(x=760, y=5)
    driver.set_window_size(990, 900)

    # Login Ekranının Açılması
    driver.find_element("xpath", pasaport_path).click()
    time.sleep(0.5)
    driver.find_element("xpath", kabul_ediyorum_path).click()
    time.sleep(2)
    driver.find_element("xpath", bordo_pasaport_button_path).click()
    time.sleep(0.5)
    bordo_pasaport_isim = "".join(driver.find_element("xpath", bordo_pasaport_isim_path).text.splitlines())
    print(bordo_pasaport_isim, "seçildi!")

    # Bilgilerin Doldurulması
    print("Bilgiler dolduruluyor...")
    driver.find_element("xpath", isim_path).send_keys(isim)
    driver.find_element("xpath", soyisim_path).send_keys(soyisim)
    driver.find_element("xpath", tc_path).send_keys(tc)
    driver.find_element("xpath", dt_gun_path).send_keys(dt_gun)
    driver.find_element("xpath", dt_ay_path).send_keys(dt_ay)
    driver.find_element("xpath", dt_yil_path).send_keys(dt_yil)
    driver.find_element("xpath", tel_path).send_keys(tel)
    driver.find_element("xpath", guvenlik_kodu_path).click()
    print("Bilgiler dolduruldu, güvenlik kodunu girin!")

    # !!! Güvenlik kodu manuel girilip "Devam Et" butonuna basılacak
    # Kullanıcının Butona basmasını bekleme
    poll_rate = 1
    current_url = driver.current_url
    while driver.current_url == current_url:
        time.sleep(poll_rate)
    print("Güvenlik kodu girildi, işleme devam ediliyor...")

    sonuc = False
    while not sonuc:
        driver.find_element("xpath", il_path).click()
        il = driver.find_element("xpath", il_path).text
        print(il, "şehrine tıklandı!")
        time.sleep(0.7)
        hata_sebebi = "Seçilen ilçelerde uygun bir randevu bulunamadı!"

        for i in ilce_listesi:
            try:  # İlçede randevu varsa gerçekleşir
                driver.find_element("xpath", bos_randevu_butonu_path.format(i))
                en_erken_rand_tarihi = driver.find_element("xpath", en_erken_rand_tarihi_path.format(i)).text
                ilce = driver.find_element("xpath", ilce_path.format(i)).text.partition('\n')[0]
                print(ilce, "için uygun randevu tarihi:", en_erken_rand_tarihi)

                if en_erken_rand_tarihi in tarih_listesi:  # Randevu günü talep edilen gün ile uyuşuyorsa
                    print(en_erken_rand_tarihi, "istenen tarihler içerisinde mevcut.")
                    driver.find_element("xpath", bos_randevu_butonu_path.format(i)).click()
                    print(ilce, "seçildi!")
                    time.sleep(0.2)
                    driver.find_element("xpath", step_2_ileri_button_path).click()
                    print("Kişi seçim ekranına geçildi!")
                    time.sleep(0.5)
                    ilk_kisi = driver.find_element("xpath", ilk_kisi_path).text
                    driver.find_element("xpath", ilk_kisi_ekleme_path).click()
                    print(ilk_kisi, "seçildi!")
                    time.sleep(0.5)
                    driver.find_element("xpath", step_3_ileri_button_path).click()
                    print("Randevu seçim ekranına geçildi!")
                    time.sleep(1)

                    try:  # Randevu saati seçilebilirse gerçekleşir
                        # Kişi seçimi:
                        driver.find_element("xpath", kisi_secimi_path).click()
                        time.sleep(0.1)
                        # Randevu saati seçimi:
                        driver.find_element("xpath", randevu_saati_path).click()
                        randevu_saati = driver.find_element("xpath", randevu_saati_path).text
                        print("Randevu saati (", randevu_saati, ") bulundu ve seçildi.")
                        time.sleep(1)
                        # !!!---Telefonla doğrulama aşamasına gelmemek için aşağıdaki kod deaktif edilir
                        # driver.find_element("xpath", step_4_ileri_button_path).click()
                        sonuc = True
                        break

                    except:  # Randevu saati kaybolmuşsa veya randevu seçim ekranında bir hata oluşmuşsa gerçekleşir
                        hata_sebebi = "Randevu saati kayboldu, işlemler tekrarlanacak!"
                        driver.get("https://randevu.nvi.gov.tr/default/step2")
                        break  # For looptan çıkması için

                else:  # Randevu günü talep edilen gün ile uyuşmuyorsa gerçekleşir
                    print(ilce, "içerisindeki uygun randevu tarihi (", en_erken_rand_tarihi,
                          ") talep edilen tarihler arasında yok!")

            except:  # İlçede randevu yoksa veya alınamadıysa gerçekleşir
                pass

        if sonuc:
            print(il, ilce, "'nde", en_erken_rand_tarihi, "tarihindeki saat", randevu_saati,
                  "randevusunu almak için telefonunuza gelen sms onay kodunu girin!")
            break  # While looptan çıkmak için

        else:
            yenileme_sayisi += 1
            print(hata_sebebi, "İşlemler tekrarlanıyor... Yenilenme sayısı:", yenileme_sayisi)


max_tekrar_sayilari_listesi = []
randevu_durumu = False
while not randevu_durumu:
    try:
        randevu_alma()
        randevu_durumu = True
    except:
        max_tekrar_sayilari_listesi.append(yenileme_sayisi)
        print("Randevu alma işleminde hata çıktı. Süreç yeniden başlatılıyor...")
        print("Döngülerdeki maksimum tekrarlar:", max_tekrar_sayilari_listesi_listesi)