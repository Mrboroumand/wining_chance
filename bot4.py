from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import requests
import multiprocessing as mp

#################################################### PEPERATION ################################################################
edge_Options = Options()
edge_Options.add_argument("--headless")

service = Service(executable_path="msedgedriver.exe")
driver = webdriver.Edge(service=service)
#driver = webdriver.Edge(service=service, options=edge_Options)
wait = WebDriverWait(driver, 10)

################################################################################################################################
#################################################### FIND THE LSIT #############################################################

def step1():
    global driver
    driver.get("https://www.digikala.com/treasure-hunt/")

    driver.execute_script("return document.readyState") == 'complete'
    sleep(2)
    driver.execute_script("scrollBy(0,600);")
    sleep(5)

    enter = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div[4]/div[2]/div[2]/div[2]/div[2]/div/div[3]/div/div[3]")
    enter.click()
    sleep(3)
    tabs = driver.window_handles
    driver.switch_to.window(tabs[1])
    url = driver.current_url
    driver.quit()
    return url

################################################################################################################################
######################################################## SEARCHING #############################################################
# LOAD THE PAGE
def step2(url ,starting_page, counter):
    global driver, wait
    page_counter = starting_page
    while True:
        try:
            # make sure the product liast is loaded
            tabs = driver.window_handles
            if len(tabs) > 1:
                for i in range(1, len(tabs)):   
                    driver.switch_to.window(tabs[i])
                    driver.close()
            driver.switch_to.window(tabs[0])
            driver.get(f"{url}&page={page_counter}")
            sleep(5)
            driver.execute_script("return document.readyState") == 'complete'
            products = driver.find_elements(By.CLASS_NAME, "product-list_ProductList__item__LiiNI")
            if len(products) == 0:
                continue
            proc_number = 0
            # start getting the products one by one
            while proc_number < len(products):
                    try:
                        products[proc_number].click()
                        sleep(5)
                        tabs = driver.window_handles
                        driver.switch_to.window(tabs[1])
                        image = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, r"#__next > div.h-full.flex.flex-col.bg-neutral-000.items-center > div.grow.bg-neutral-000.flex.flex-col.w-full.items-center.shrink-0 > div.grow.bg-neutral-000.flex.flex-col.w-full.items-center.styles_BaseLayoutDesktop__content__hfHD1.container-4xl-w > div.lg\:px-5 > div.flex.flex-col.lg\:flex-row.overflow-hidden.styles_PdpProductContent__sectionBorder--mobile__J7liJ > div.lg\:ml-4.shrink-0.flex.flex-col-reverse.lg\:flex-col.styles_InfoSection__rightSection__PiYpa > div.flex.flex-col.items-center.lg\:max-w-92.xl\:max-w-145.lg\:block > div.flex.relative > div.relative.flex.items-center > div")))
                        image.click()
                        
                        all_images = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, r"#modal-root > div > div > div > div > div > div > div.relative.flex.flex-col.justify-between.select-none.touch-none > div.relative.w-full.py-4.z-2.flex.justify-start.items-center.relative.duration-300.opacity-100.styles_Modal__thumbnailContainer__BHMqe > button > div")))
                        all_images.click()

                        sleep(2)
                        pictures = driver.find_element(By.XPATH, r"/html/body/div[2]/div[2]/div/div/div/div/div/div/div[2]/div/div[2]/div[2]/div").find_elements(By.CSS_SELECTOR, "img")
                        for pic in pictures:
                            try :
                                image_url = pic.get_attribute('src')
                            except NoSuchElementException:
                                print("error in copying img url")
                                continue
                            respunce = requests.get(image_url)
                            with open (f"images/image{counter}.png", "wb") as file:
                                file.write(respunce.content)
                            counter += 1    
                        driver.close()
                        driver.switch_to.window(tabs[0])
                        proc_number += 1
                    except NoSuchElementException:
                        tabs = driver.window_handles
                        if len(tabs) > 1:
                            for i in tabs[1:]:   
                                driver.switch_to.window(i)
                                driver.close()
                        driver.switch_to.window(tabs[0])
                        driver.refresh()
                        products = driver.find_elements(By.CLASS_NAME, "product-list_ProductList__item__LiiNI")
                        print("cloud not find the product element")
                        print(e)
                    except Exception as e:
                        tabs = driver.window_handles
                        if len(tabs) > 1:
                            for i in tabs[1:]:   
                                driver.switch_to.window(i)
                                driver.close()
                        driver.switch_to.window(tabs[0])
                        print("failed to load product page")
                        print(e)
                    
                        
            page_counter += 1
        except Exception as e:
            print(f"failed to load page{page_counter}")
            print(e)

if __name__ == "__main__":
    print("starting bot...")
    url = "https://www.digikala.com/search/personal-appliance/?th_no_track=1"
    print(url)
    proc0 = mp.Process(target=step2, args=[url, 1, 1])
    proc1 = mp.Process(target=step2, args=[url, 10, 1000])
    proc2 = mp.Process(target=step2, args=[url, 20, 2000])
    proc3 = mp.Process(target=step2, args=[url, 30, 3000])
    #proc4 = mp.Process(target=step2, args=[url, 40, 4000])



    proc0.start()
    proc1.start()
    proc2.start()
    proc3.start()
    #proc4.start()

#2360
