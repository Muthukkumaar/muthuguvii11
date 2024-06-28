from selenium import webdriver
import os
import time

# Function to handle downloading files
def download_file(url, folder_path):
    driver.execute_script("window.open('" + url + "');")
    # Switch to the new window
    driver.switch_to.window(driver.window_handles[-1])
    # Download file
    driver.get(url)
    time.sleep(2)  # Add a delay to ensure the file downloads completely
    # Move downloaded file to the specified folder
    file_name = url.split('/')[-1]
    os.rename(os.path.join(os.path.expanduser('~'), 'Downloads', file_name), os.path.join(folder_path, file_name))
    # Close the window
    driver.close()
    # Switch back to the main window
    driver.switch_to.window(driver.window_handles[0])

# Function to create folder
def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Function to download photos from the photo gallery
def download_photos(photo_links, folder_path):
    for idx, link in enumerate(photo_links):
        driver.execute_script("window.open('" + link + "');")
        # Switch to the new window
        driver.switch_to.window(driver.window_handles[-1])
        # Download photo
        driver.get(link)
        time.sleep(2)  # Add a delay to ensure the photo downloads completely
        # Move downloaded photo to the specified folder
        file_name = f"photo_{idx+1}.jpg"
        os.rename(os.path.join(os.path.expanduser('~'), 'Downloads', 'image.jpeg'), os.path.join(folder_path, file_name))
        # Close the window
        driver.close()
        # Switch back to the main window
        driver.switch_to.window(driver.window_handles[0])

# Set up Chrome options to handle file downloads
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": os.path.expanduser('~') + "/Downloads/",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
})

# Initialize Chrome driver
driver = webdriver.Chrome(chrome_options=chrome_options)

# Task 1: Visit https://www.cowin.gov.in/
driver.get("https://www.cowin.gov.in/")
# Click on "FAQ" and "Partners" links to open new windows
faq_link = driver.find_element_by_link_text("FAQ")
faq_link.click()
partners_link = driver.find_element_by_link_text("Partners")
partners_link.click()
# Get and display the window/frame IDs
window_ids = [window_handle for window_handle in driver.window_handles]
print("Window/Frame IDs:", window_ids)

# Close the new windows and come back to the home page
for window_id in window_ids[1:]:
    driver.switch_to.window(window_id)
    driver.close()
driver.switch_to.window(window_ids[0])

# Task 2: Visit https://labour.gov.in/
driver.get("https://labour.gov.in/")
# Task 1: Download the Monthly Progress Report from the "Documents" menu
documents_menu = driver.find_element_by_xpath("//a[contains(text(),'Documents')]")
documents_menu.click()
monthly_progress_report_link = driver.find_element_by_link_text("Monthly Progress Report")
monthly_progress_report_url = monthly_progress_report_link.get_attribute('href')
download_file(monthly_progress_report_url, "Monthly_Progress_Report")

# Task 2: Download 10 photos from the "Photo Gallery" in the "Media" menu
media_menu = driver.find_element_by_xpath("//a[contains(text(),'Media')]")
media_menu.click()
photo_gallery_submenu = driver.find_element_by_xpath("//a[contains(text(),'Photo Gallery')]")
photo_gallery_submenu.click()

# Create folder to store downloaded photos
create_folder("Photo_Gallery")

# Fetching photo links
photo_links = []
photos = driver.find_elements_by_xpath("//div[@class='zoom-box']/a/img")
for photo in photos[:10]:  # Downloading only first 10 photos
    photo_links.append(photo.get_attribute("src"))

# Download photos
download_photos(photo_links, "Photo_Gallery")

# Quit the driver
driver.quit()