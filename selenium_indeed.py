import csv
from datetime import datetime
from datetime import timedelta
from operator import indexOf
from sys import breakpointhook
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
import time
from Create_Database import Connect_database, show_table, insert_data

REPEATED_LIMIT = 10 #Limit for repetition in different experience level
SEARCH_WORDS = ["Business Analyst", "Software Engineer", "Backend Software Engineer", "Front End Engineer",
                    "Electrical Engineer", "Data Analytics", "Mechanical Engineer", "Data Scientist", 
                    "Financial Analyst", "Accountant", "Machine Learning Engineer", "Marketing Analyst",
                    "Civil Engineer", "Chemical Engineer", "Biological Engineer", "Biostatistician", "Statistician",
                    "Quantitative Analyst", "Industrial Engineer", "Full-stack Engineer", "Supply Chain Engineer"]


past_repete_count = 0
repetition_lvl_count = 0


def get_url(position, location):
    """Generate url from position and location"""
    template = 'https://www.indeed.com/jobs?q={}&l={}&sc={}&sort=date'
    position = position.replace(' ', '+')
    location = location.replace(' ', '+')
    entry_url = template.format(position, location, '(ENTRY_LEVEL)')
    mid_url = template.format(position, location, '(MID_LEVEL)')
    senior_url = template.format(position, location, '(SENIOR_LEVEL)')
    
    return [entry_url, mid_url, senior_url]


def get_record(card, pos, driver):
    """Extract job data from single card"""
    
    job_id = card.find_element(By.CLASS_NAME, 'jcs-JobTitle').get_attribute('data-jk')
    # time.sleep(3)

    job_title = card.find_element(By.CLASS_NAME, 'jobTitle').text
    # time.sleep(3)

    company = card.find_element(By.CLASS_NAME, 'companyName').text
    # time.sleep(3)

    location = card.find_element(By.CLASS_NAME, 'companyLocation').text
    # time.sleep(3)

    if location != 'Remote' and location != 'United States':
        detail = location.split(',')
        city = detail[0]
        if len(detail) > 1:
            state = detail[1]
        else:
            state = ''
    else:
        city = ''
        state = ''
    
    try:
        summary = card.find_element(By.CLASS_NAME, 'job-snippet').text
    except:
        summary = ""
    # time.sleep(3)

    timestamp = currentTime()

    job_url = card.find_element(By.CLASS_NAME, 'jcs-JobTitle').get_attribute('href')
    # time.sleep(3)

    try:
        salary = salary = card.find_element(By.CLASS_NAME, "salaryOnly").text
    except:
        salary = ""
    # time.sleep(3)

    try:
        jobType = card.find_element(By.XPATH, """//*[@id="mosaic-provider-jobcards"]/ul/li[4]/div/div[1]/div/div[1]/div/table[1]/tbody/tr/td/div[3]/div[2]/div""").text.strip()
    except:
        jobType = "Not Specified"
    # time.sleep(3)

    try:
        date_diff = card.find_element(By.CLASS_NAME, 'date').text.strip()
        if "Today" in date_diff or "Just" in date_diff:
            post_date = str(currentDate())
        else:
            diff = ''
            for i in range(len(date_diff)):
                if date_diff[i].isdigit():
                    diff += date_diff[i]
            if diff == '':
                post_date = str(currentDate())
            else:
                post_date = str(datetime.today() - timedelta(days=int(diff))).split()
                post_date = post_date[0]
        # time.sleep(3)
    except AttributeError:
        post_date = currentDate()

    return [job_id, pos, post_date, timestamp, job_title, company, location, city, state, salary, jobType, summary, job_url]


def currentDate():
    now = datetime.today()
    today = now.strftime("%Y-%m-%d")
    return today

def currentTime():
    now = datetime.now()
 
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    return dt_string

def search_nested(records, jobid):
    '''
    Find the Index of the record in the records list which has the jobid.
    '''
    for i in range(len(records)):
        if records[i][0] == jobid:
            return i
    return 0

def mergeSearchWords(sum_job_ids, current_search_words_records, sum_records):
    '''
    Merge the job found in the current search word to the total records which contains all the records from
    the previous search words. If the job already exists in the previosu ids, append the new found search word
    into the search word field of the orginal record.
    '''
    for i in range(len(current_search_words_records)):
        if current_search_words_records[i][0] in sum_job_ids:
            sum_records[search_nested(sum_records, current_search_words_records[i][0])][1] += ", " + (current_search_words_records[i][1])
        else:
            sum_records.append(current_search_words_records[i])
            sum_job_ids.add(current_search_words_records[i][0])

def get_page_records(cards, job_list, id_set, pos, level, records, driver, past_records):
    """Extract all cards from the page"""
    global past_repete_count
    global repetition_lvl_count
    for card in cards:
        record = get_record(card, pos, driver)
        # add if job title exists and not duplicate
        job_title = record[4]
        company = record[5]
        if record[0] in past_records:
            past_repete_count += 1
        if job_title != "" and company != "":
            if record[0] not in id_set:
                record.append(level)
                job_list.append(record)
                id_set.add(record[0])
            else:
                index = search_nested(records, record[0])
                if level not in records[index][-1]:
                    records[index][-1] += " " + level
                    repetition_lvl_count += 1



def save_data_to_file(records, connection):
    """Save data to csv file"""
    # with open('results.csv', 'w', newline='', encoding='utf-8') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(['JobID', 'Search_Word', 'Post_Date', 'Timestamp', 'Job_Title', 'Company', 'Location', 'City', 'State', 'Salary', 'JobType', 'Summary', 'JobUrl', 'ExperienceLevel'])
    #     writer.writerows(records)
    insert_data(connection, records)


def main(position, location):
    """Run the main program routine"""
    global past_repete_count
    global repetition_lvl_count
    sum_scraped_jobs = []
    
    sum_ids = set()
    connect = Connect_database("indeed_jobs")
    pastRecords = set()
    for position in SEARCH_WORDS:
        pastRecords = pastRecords.union(show_table(connect, position))
    # setup web driver
    
    driver = webdriver.Chrome(executable_path='/Users/shiliangyao/Documents/GitHub/indeed_scrapper/chromedriver')
    
    driver.implicitly_wait(5)

    for position in SEARCH_WORDS:
        driver.quit()
        driver = webdriver.Chrome(executable_path='/Users/shiliangyao/Documents/GitHub/indeed_scrapper/chromedriver')
        urlsForExperienceLevel = get_url(position, location)
        scraped_jobs = []
        scraped_ids = set()
        for url in urlsForExperienceLevel:
            
            repetition_lvl_count = 0 
            past_repete_count = 0
            driver.quit()
            driver = webdriver.Chrome(executable_path='/Users/shiliangyao/Documents/GitHub/indeed_scrapper/chromedriver')
            driver.implicitly_wait(5)
            driver.get(url)        
            exp_lvl = indexOf(urlsForExperienceLevel, url)
            if exp_lvl == 0:
                exp_lvl = 'entry'
            elif exp_lvl == 1:
                exp_lvl = 'mid'
            else:
                exp_lvl = 'senior'
            # extract the job data
            while True:
                if repetition_lvl_count >= REPEATED_LIMIT or past_repete_count >= REPEATED_LIMIT:
                    break
                cards = driver.find_elements(By.CLASS_NAME, 'cardOutline')
                get_page_records(cards, scraped_jobs, scraped_ids, position, exp_lvl, scraped_jobs, driver, pastRecords)
                try:
                    driver.find_element(By.XPATH, '//a[@aria-label="Next"]').click()
                except NoSuchElementException:
                    break
                except ElementNotInteractableException:
                    driver.find_element(By.ID, 'popover-x').click()  # to handle job notification popup
                    get_page_records(cards, scraped_jobs, scraped_ids, position, exp_lvl, scraped_jobs, driver, pastRecords)
                    continue
        
        mergeSearchWords(sum_ids, scraped_jobs, sum_scraped_jobs)

        # shutdown driver and save file
        driver.quit()
    save_data_to_file(sum_scraped_jobs, connect)


if __name__ == '__main__':

    main('Software Engineer', 'Irvine')