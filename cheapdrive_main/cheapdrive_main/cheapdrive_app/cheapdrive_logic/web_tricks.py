
def driver_setup():
    """
    Sets up and returns a Selenium WebDriver with pre-configured options.
    """
    chrome_options = Options()
    chrome_options.add_argument("--disable-search-engine-choice-screen")
    new_driver = webdriver.Chrome(options=chrome_options)
    return new_driver

def go_through_cookies(driver):
    """
    Accepts cookies on the website if the cookie banner is present.
    """
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "form:nth-child(2) > div > div > button")
    )).click()