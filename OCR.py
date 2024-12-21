import os
import time
import dxcam
import win32api
import win32con
import cv2
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Инициализация камеры
camera = dxcam.create()

# Определение региона для захвата
left, top = 28, 20
right, bottom = left + 445, top + 275
region = (left, top, right, bottom)

# Относительный путь к изображению
relative_image_path = "image.png"  # Замените на ваш относительный путь
# Преобразование относительного пути в абсолютный
absolute_image_path = os.path.abspath(relative_image_path)

# Путь загрузки
download_directory = os.getcwd()

def is_caps_lock_on():  # Проверяем состояние Caps Lock
    return win32api.GetKeyState(win32con.VK_CAPITAL) & 0x0001 != 0

while True:
    if not is_caps_lock_on():  # Проверка состояния Caps Lock
        time.sleep(0.5)
        continue

    # Захват кадра
    frame = camera.grab(region=region)

    # Преобразование кадра (numpy массив) в изображение PIL
    image = Image.fromarray(frame)

    # Сохранение изображения
    image.save('image.png')

    # Настройка параметров Chrome
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("prefs", {"download.default_directory": download_directory})
    
    # Запуск браузера в фоновом режиме (headless)
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")

    # Инициализация браузера
    driver = webdriver.Chrome(options=chrome_options)

    # Переход на страницу OCR
    driver.get("https://translate.yandex.ru/ocr")

    # Явное ожидание загрузки страницы
    wait = WebDriverWait(driver, 2, poll_frequency=0.1)

    # Находим элемент для загрузки файла
    upload_input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
    )

    # Загружаем файл
    upload_input.send_keys(absolute_image_path)

    # Ожидание появления кнопки "Скачать"
    download_button = wait.until(
        EC.element_to_be_clickable((By.ID, "downloadButton"))
    )

    # Нажимаем на кнопку скачивания
    download_button.click()

    # Ожидание скачивания (по необходимости)
    time.sleep(0.5)

    # Закрытие браузера
    driver.quit()
    
    # Загрузка изображения
    image = cv2.imread('image.translated.jpg')
    
    # Получение размеров изображения
    height, width, _ = image.shape
    
    # Создание окна с нужными размерами и без рамки
    cv2.namedWindow("Окно", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Окно", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.resizeWindow("Окно", width, height)
    cv2.setWindowProperty("Окно", cv2.WND_PROP_TOPMOST, 1)
    
    # Отображение изображения
    cv2.imshow("Окно", image)
    
    # Перемещение окна
    cv2.moveWindow("Окно", 1505, 10)
    
    if is_caps_lock_on():
        cv2.waitKey(1500)  # Ожидание 1500 мс

        cv2.destroyAllWindows()  # Закрытие всех окон

        os.remove("image.translated.jpg")  # Удаление файла

        continue
    else:
        cv2.waitKey(7000)  # Ожидание 7000 мс

        cv2.destroyAllWindows()  # Закрытие всех окон

        os.remove("image.translated.jpg")  # Удаление файла
