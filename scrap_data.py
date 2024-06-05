from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

def get_youtube_comments(video_url, max_comments=16000):
    # Set up Selenium options
    firefox_options = Options()
    # Commenting out headless mode for better debugging
    # firefox_options.add_argument("--headless")  

    # Set up the WebDriver (assume GeckoDriver is in the PATH)
    service = Service('./common/geckodriver.exe')  # Update with the actual path
    driver = webdriver.Firefox(service=service, options=firefox_options)
    
    print("Opening YouTube video URL...")
    driver.get(video_url)
    time.sleep(5)  # Let the page load

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'ytd-comments'))
        )
        print("Comments section found.")
    except Exception as e:
        print(f"Failed to find comments section. Error: {e}")
        driver.quit()
        return []

    comments = []
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    
    start_time = time.time()
    scroll_count = 0
    print("Starting to scroll and scrape comments...")

    while len(comments) < max_comments:
        scroll_count += 1
        print(f"Scroll iteration: {scroll_count}")
        
        # Scroll to load comments
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(5)  # Wait for comments to load
        print("Scrolled to bottom, loading comments...")

        # Wait for the comments to load
        try:
            comment_elements = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#contents #content-text"))
            )
        except Exception as e:
            print(f"Comments did not load in the expected time. Error: {e}")
            break

        # Scrape comments
        new_comments = [elem.text for elem in comment_elements if elem.text not in comments]
        print(f"Found {len(new_comments)} new comments in this batch.")

        comments.extend(new_comments)
        print(f"Total comments scraped so far: {len(comments)}")

        # Break if no new comments are loaded
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            print("No new comments loaded, breaking the loop.")
            break
        last_height = new_height

        # Avoid infinite loop, if necessary
        if len(comments) >= max_comments:
            print("Reached the maximum number of comments to scrape.")
            break

    end_time = time.time()
    driver.quit()
    print(f"Time taken to scrape {len(comments)} comments: {end_time - start_time} seconds")
    return comments[:max_comments]

# Example usage
video_url = 'https://www.youtube.com/watch?v=EzFXDvC-EwM'
comments = get_youtube_comments(video_url, max_comments=300)

# Save comments to a CSV file
df = pd.DataFrame(comments, columns=['Comment'])
df.to_csv('youtube_comments.csv', index=False)
print(f"Scraped {len(comments)} comments and saved to youtube_comments.csv")
