from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from tkinter import messagebox
import os

def open_browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def login(my_driver):
    login = my_driver.find_element(By.CLASS_NAME, value="main__sign-in-link")
    login.click()
    linkedin_email = os.environ.get("LINKEDIN_EMAIL")
    linkedin_pw = os.environ.get("LINKEDIN_PW")
    email_input = my_driver.find_element(By.ID, value="username")
    pw_input = my_driver.find_element(By.ID, value="password")
    submit = my_driver.find_element(By.XPATH,value='//*[@id="organic-div"]/form/div[3]/button')
    email_input.send_keys(linkedin_email)
    pw_input.send_keys(linkedin_pw)
    submit.click()

def get_linkedin_listing(my_driver):
    my_driver.get("https://www.linkedin.com/jobs/search/?currentJobId="
                  "3831668246&distance=25&f_AL=true&f_E=2%2C3&geoId="
                  "104428936&keywords=junior%20software%20developer&location="
                  "St%20Louis%2C%20Missouri%2C%20United%20States&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&"
                  "refresh=true&sortBy=R")

    jobs_ul = my_driver.find_element(By.CLASS_NAME, value="jobs-search__results-list")
    jobs_li = jobs_ul.find_elements(By.TAG_NAME,value="li")
    return jobs_li


def check_jobs(my_driver, jobs_li, phrase_1, phrase_2):
    formatted_phrase_1 = phrase_1.title()
    formatted_phrase_2 = phrase_2.title()
    suitable_job_found = False
    jobs = [job.text.split('\n')[0] for job in jobs_li]
    for job in jobs:
        if job.find(formatted_phrase_1) != -1 or job.find(formatted_phrase_2) != -1 or job.find(" I") != -1:
            suitable_job_found = True
            index = jobs.index(job)
            messagebox.showinfo(title="Job Found", message="There is an opportunity that requires your attention.")
            break
    if suitable_job_found == False:
        messagebox.showinfo(title="No Job Found", message="No jobs of interest at the moment.")
        index = -1
    return index


def apply_for_job(my_driver, jobs_li, index):
    if index != -1:
        desired_job = jobs_li[index]
        desired_job.click()
        apply = my_driver.find_element(
            By.XPATH, value='//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/div/button[1]')
        apply.click()
        login(my_driver)
    else:
        my_driver.quit()


chrome_driver = open_browser()
jobs_li = get_linkedin_listing(chrome_driver)
desired_job_index = check_jobs(chrome_driver, jobs_li, "junior", "entry level")
apply_for_job(chrome_driver, jobs_li, desired_job_index)

