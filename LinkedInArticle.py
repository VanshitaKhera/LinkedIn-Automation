from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import google.generativeai as genai
from webdriver_manager.chrome import ChromeDriverManager
import time


def login_linkedin(username, password):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.linkedin.com/login")

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "username"))
    )

    email_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    email_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "global-nav-typeahead"))
    )

    return driver


def write_article(driver, title, content):
    driver.get("https://www.linkedin.com/post/new/")
    print("Navigated to LinkedIn post creation page")

    # try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='article-editor-headline__textarea']"))
    )
    print("Title input field located")

    title_field = driver.find_element(By.XPATH, "//*[@id='article-editor-headline__textarea']")
    content_field = driver.find_element(By.XPATH, "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/div/div[4]/div[2]/p")
    title_field.send_keys(title)
    content_field.send_keys(content)
    content_field.send_keys(Keys.RETURN)

    next_button = driver.find_element(By.XPATH, "//*[@id='ember573']")
    next_button.click()
    print("Article content submitted")


    print("Article content published")

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "ember573"))
    )

    time.sleep(5)

    print("Next button pressed")

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, ""))
    )
    print("Article published successfully!")


def generate_article(prompt):
    genai.configure(api_key="****")
    generation_config = {"temperature": 0.9, "top_p": 1, "top_k": 1, "max_output_tokens": 2048}
    model = genai.GenerativeModel("gemini-pro", generation_config=generation_config)
    response = model.generate_content(prompt)
    answer = response.text

    return answer



def main():
    username = ""
    password = ""

    driver = login_linkedin(username, password)

    article_prompt = "Write an article about the importance of AI." 
    article_title = "The Importance of AI"
    article_content = generate_article(article_prompt)
    write_article(driver, article_title, article_content)


    driver.quit()

if __name__ == "__main__":
    main()
