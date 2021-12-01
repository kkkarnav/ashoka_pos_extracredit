from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep
import requests
import shutil


def setup():
    # needs a geckodriver.exe in the same folder as a script,
    # as well as a firefox exe in the specified location
    options = Options()
    options.binary_location = (
        "C:\\Users\\KARNAV\\AppData\\Local\\Firefox Developer Edition\\firefox.exe"
    )

    driver_object = webdriver.Firefox(options=options)
    driver_object.implicitly_wait(0.5)

    # for convenience, runs fine in headless too
    driver_object.maximize_window()
    return driver_object


def toggle_animation(driver):
    toggle = wait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "uom-playpause"))
    )
    toggle.click()


def download_image(image_url, time_period, measurement):

    filename = (
        "./pos_images/" + str(time_period) + str(measurement) + image_url.split("/")[-1]
    )

    r = requests.get(image_url, stream=True)

    if r.status_code == 200:
        r.raw.decode_content = True

        with open(filename, "wb") as f:
            shutil.copyfileobj(r.raw, f)

        print("Image sucessfully downloaded: ", filename)
    else:
        print("Image couldn't be retreived")


def grab_image(driver):
    image_element = driver.find_element(By.CLASS_NAME, "uom-image")
    image_url = image_element.get_attribute("src")
    return image_url


def scrape(driver, time_period, measurement):

    driver.get(
        f"http://www.buildyourownearth.com/byoe.html?e1={time_period}&c1={measurement}&v=pm"
    )
    toggle_animation(driver)

    for month in range(12):
        download_image(grab_image(driver), time_period, measurement)
        toggle_animation(driver)
        sleep(0.5)
        toggle_animation(driver)


def main():

    current_day = 0
    last_glacial = 33
    late_permian = 39
    mean_temp = 0

    # get the data from source
    driver = setup()
    scrape(driver, current_day, mean_temp)
    scrape(driver, last_glacial, mean_temp)
    scrape(driver, late_permian, mean_temp)


if __name__ == "__main__":
    main()
