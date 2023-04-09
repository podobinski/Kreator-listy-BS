import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def find_facebook_profile(www_address, driver):
    try:
        driver.get(www_address)
        facebook_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'facebook.com')]")
        if facebook_links:
            return facebook_links[0].get_attribute('href')
    except Exception as e:
        print(f"Error finding Facebook profile for {www_address}: {e}")
    return None

def extract_website_data(url, driver_path):
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service)
    driver.get(url)

    data = []

    try:
        while True:
            print("Waiting for the company elements to be visible...")
            WebDriverWait(driver, 5).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "#entityTable dl"))
            )
            print("Company elements are visible.")

            company_list = driver.find_elements(By.CSS_SELECTOR, "#entityTable dl")
            print(f"Found {len(company_list)} company elements.")
            
            for i in range(len(company_list)):
                companies_on_page = driver.find_elements(By.CSS_SELECTOR, "#entityTable dl")
                if i >= len(companies_on_page):
                    print(f"Index {i} is out of range. Skipping this iteration.")
                    continue
                
                company = companies_on_page[i]

                name_element = company.find_element(By.XPATH, "./dd[1]/h3")
                name = re.sub(r'<span.*?>Nazwa<\/span>', '', name_element.get_attribute("innerHTML")).strip()
                try:
                    www_address = company.find_element(By.XPATH, "./dd[2]/ul/li[6]/a").text.strip()
                    if "otwiera się w nowej karcie" in www_address:
                        www_address = www_address.replace("otwiera się w nowej karcie", "").strip()
                except Exception as e:
                    print(f"Error extracting wwwAddress for {name}: {e}")
                    www_address = ""

                facebook_url = find_facebook_profile(www_address, driver) if www_address else None
                print(f"Extracted name: {name}, wwwAddress: {www_address}, Facebook URL: {facebook_url}")
                data.append({"Name": name, "WWW Address": www_address, "Facebook URL": facebook_url})

            next_page_buttons = driver.find_elements(By.CSS_SELECTOR, "#nextPage")
            if next_page_buttons:
                print("Clicking the 'next' button...")
                next_page_button = next_page_buttons[0]
                
                driver.execute_script("arguments[0].click();", next_page_button)

                WebDriverWait(driver, 30).until(
                    EC.staleness_of(company_list[-1])
                )
                print("Proceeding to the next page...")
            else:
                print("No more pages found. Exiting loop...")
                break

    except Exception as e:
        print(f"Error extracting data: {e}")
    finally:
        driver.quit()

    return data

def save_to_excel(data, output_file):
    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False, engine="openpyxl")
    print(f"Data saved to {output_file}")

if __name__ == "__main__":
    url = "https://www.knf.gov.pl/podmioty/Podmioty_sektora_bankowego/banki_spoldzielcze"
    driver_path = "/path/to/chromedriver"  # Replace this with the path to your Chrome WebDriver
    data = extract_website_data(url, driver_path)
    if data:
        output_file = "bs-lista.xlsx"
        save_to_excel(data, output_file)
