from selenium import webdriver
import time

print("Randevu alma modülüne hoşgeldiniz.")

isim = "HARUN"
soyisim = "...."
tc = "585...."
dt_gun = ".."
dt_ay = ".."
dt_yil = "...."
tel = "546..."

ildeki_ilce_sayisi = 41

# --------Driver Kurulumu--------

browser_path = "C:\Drivers\chromedriver.exe"
driver = webdriver.Chrome(executable_path=browser_path)
driver.get("https://randevu.nvi.gov.tr/")

# --------Web sitesi içindeki xpath ler--------

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

# --------Web sitesi içindeki xpath ler--------


# --------Driver İşlemleri--------

# İlk Tıklamalar
driver.find_element("xpath", pasaport_path).click()
time.sleep(1)
driver.find_element("xpath", kabul_ediyorum_path).click()
time.sleep(2)
driver.find_element("xpath", bordo_pasaport_path).click()
time.sleep(1)

# Bilgilerin Doldurulması
driver.find_element("xpath", isim_path).send_keys(isim)
driver.find_element("xpath", soyisim_path).send_keys(soyisim)
driver.find_element("xpath", tc_path).send_keys(tc)
driver.find_element("xpath", dt_gun_path).send_keys(dt_gun)
driver.find_element("xpath", dt_ay_path).send_keys(dt_ay)
driver.find_element("xpath", dt_yil_path).send_keys(dt_yil)
driver.find_element("xpath", tel_path).send_keys(tel)

# !!! Güvenlik kodu manuel girilip "Devam Et" butonuna basılacak
# Kullanıcının Butona basmasını bekleme
poll_rate = 1
current_url = driver.current_url
while driver.current_url == current_url:
    time.sleep(poll_rate)

# İstanbul Seçimi ve İlçelerde Boşluk Kontrolü
driver.find_element("xpath", istanbul_path).click()
time.sleep(1)
