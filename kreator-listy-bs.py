import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_website_data(url, driver_path):
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service)
    driver.get(url)

    data = []

    try:
        print("Waiting for the company elements to be visible...")
        WebDriverWait(driver, 30).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "#entityTable dl"))
        )
        print("Company elements are visible.")

        company_list = driver.find_elements(By.CSS_SELECTOR, "#entityTable dl")
        print(f"Found {len(company_list)} company elements.")
        
        for company in company_list:
            name_element = company.find_element(By.XPATH, "./dd[1]/h3")
            name = re.sub(r'<span.*?>Nazwa<\/span>', '', name_element.get_attribute("innerHTML")).strip()
            try:
                www_address = company.find_element(By.XPATH, "./dd[2]/ul/li[6]/a").text.strip()
                if "otwiera się w nowej karcie" in www_address:
                    www_address = www_address.replace("otwiera się w nowej karcie", "").strip()
            except Exception as e:
                print(f"Error extracting wwwAddress for {name}: {e}")
                www_address = ""
            print(f"Extracted name: {name}, wwwAddress: {www_address}")
            data.append({"Name": name, "WWW Address": www_address})
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
        output_file = "output.xlsx"
        save_to_excel(data, output_file)
