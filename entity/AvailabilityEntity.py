import asyncio
from entity.BrowserEntity import BrowserEntity
from utils.css_selectors import Selectors
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.configuration import load_config

class AvailabilityEntity:

    config = load_config()
    search_element_timeOut = config.get('project_options', {}).get('search_element_timeOut', 15)
    sleep_time = config.get('project_options', {}).get('sleep_time', 15)

    def __init__(self):
        self.browser_entity = BrowserEntity()


    async def check_availability(self, url: str, date_str=None, timeout=search_element_timeOut):
        try:
            # Use BrowserEntity to navigate to the URL
            self.browser_entity.navigate_to_website(url)

            # Get selectors for the given URL
            selectors = Selectors.get_selectors_for_url(url)

            # Perform date selection (optional)
            if date_str:
                try:
                    await asyncio.sleep(self.sleep_time)  # Wait for updates to load
                    print(selectors['date_field'])
                    date_field = self.browser_entity.driver.find_element(By.CSS_SELECTOR, selectors['date_field'])
                    date_field.click()
                    await asyncio.sleep(self.sleep_time)
                    date_button = self.browser_entity.driver.find_element(By.CSS_SELECTOR, f"{selectors['select_date']} button[aria-label*=\"{date_str}\"]")
                    date_button.click()
                except Exception as e:
                    return f"Failed to select the date: {str(e)}"

            await asyncio.sleep(self.sleep_time)  # Wait for updates to load

            # Initialize flags for select_time and no_availability elements
            select_time_seen = False
            no_availability_seen = False
            try:
                # Check if 'select_time' is available within the given timeout
                WebDriverWait(self.browser_entity.driver, timeout).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selectors['select_time']))
                )
                select_time_seen = True  # If found, set the flag to True
            except:
                select_time_seen = False  # If not found within timeout
            try:
                # Check if 'no_availability' is available within the given timeout
                WebDriverWait(self.browser_entity.driver, timeout).until(
                    lambda driver: len(driver.find_elements(By.CSS_SELECTOR, selectors['show_next_available_button'])) > 0
                )
                no_availability_seen = True  # If found, set the flag to True
            except:
                no_availability_seen = False  # If not found within timeout

            # Logic to determine availability
            if select_time_seen:
                return f"Selected or default date {date_str if date_str else 'current date'} is available for booking."
            elif no_availability_seen:
                return "No availability for the selected date."
            else:
                return "Unable to determine availability. Please try again."
            
        except Exception as e:
            return f"Failed to check availability: {str(e)}"
