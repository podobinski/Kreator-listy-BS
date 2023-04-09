from selenium.webdriver.common.by import By

def find_facebook_profile(www_address, driver):
    try:
        if not www_address.startswith("http://") and not www_address.startswith("https://"):
            www_address = "https://" + www_address

        driver.get(www_address)
        facebook_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'facebook.com')]")
        if facebook_links:
            return facebook_links[0].get_attribute('href')
    except Exception as e:
        print(f"Error finding Facebook profile for {www_address}: {e}")
    return None
