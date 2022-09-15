#indeed job scraping
import csv
from datetime import datetime
from datetime import timedelta
import requests
from bs4 import BeautifulSoup
from Create_Database import Connect_database, Create_table, insert_data, show_table
from Send_email import daily_report


def get_url(pos, loc):
    '''
    Return the 10 pages of urls of the destinated search words and location where scapped 3 times for entry, mid, senior level, sorted by date.
    '''
    template = 'https://www.indeed.com/jobs?q={}&l={}&sc={}&fromage=14&start={}&sort=date'
    pos = pos.replace(' ', '+')
    loc = loc.replace(' ', '+')
    url = list()
    for i in range(0, 10):
        try:
            entry_url = template.format(pos, loc, '(ENTRY_LEVEL)', str(i*10))
            mid_url = template.format(pos, loc, '(MID_LEVEL)', str(i*10))
            senior_url = template.format(pos, loc, '(SENIOR_LEVEL)', str(i*10))
            url.append(entry_url)
            url.append(mid_url)
            url.append(senior_url)
        except:
            break
    return url

# url = get_url('software engineer', 'Irvine')
# print(url)

# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'html.parser')
# cards = soup.find_all('div', 'cardOutline')

# card = cards[0]
# job_title = card.h2.a.get('jobTitle')
# url = 'https://www.indeed.com' + card.h2.a.get('href')
# company = card.find('span', 'companyName').text.strip()
# location = card.find('div', 'companyLocation').text.strip()
# salary = card.find('div', 'salaryOnly').text.strip()
# description = card.find('div', 'jobCardShelfContainer').text.strip().replace('\n', ' ')


# record = (job_title, company, location, salary, description, url)

def get_record(card, pos):
    '''
    Get all the columns for the jobs database and store into a list
    '''
    search_word = pos
    try:
        job_title = card.find('h2').text.strip()
    except AttributeError:
        job_title = ''

    try:
        url = 'https://www.indeed.com' + card.h2.a.get('href')
    except AttributeError:
        url = ''

    try:
        company = card.find('span', 'companyName').text.strip()
    except:
        company = ''
    try:
        location = card.find('div', 'companyLocation').text.strip()
    except:
        location = ''

    jobid = card.h2.a.get('data-jk')

    try:
        salary = card.find('div', 'salaryOnly').text.strip()
    except AttributeError:
        salary = ''
    try:
        description = card.find('div', 'job-snippet').text.strip().replace('\n', ' ')
    except AttributeError:
        description = ''
    timestamp = currentTime()
    try:
        date_diff = card.find('span', 'date').text.strip()
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
    except AttributeError:
        post_date = currentDate()
    record = [jobid, post_date, search_word, timestamp, job_title, company, location, salary, description, url]
    return record

# records = []
# for card in cards:
#     record = get_record(card)
#     records.append(record)

# while True:
#     try:
#         url = 'https://www.indeed.com' + soup.find('a', {'aria-label': 'Next'}).get('href')
#     except AttributeError:
#         break
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     cards = soup.find_all('div', 'cardOutline')
#     for card in cards:
#         record = get_record(card)
#         records.append(record)
def currentTime():
    now = datetime.now()
 
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    return dt_string

def currentDate():
    now = datetime.today()
    today = now.strftime("%Y-%m-%d")
    return today

def search_nested(records, jobid):
    for i in range(len(records)):
        if records[i][0] == jobid:
            return i
    return 0

def form_records(url, pos, pastRecords):
    records = list()
    jobids = []
    repeated = [0, 0, 0]    
    index = -1
    
    for i in url:
        if repeated == [1,1,1]:     #once entrylevel, mid level, senior level all have more than 10 repetitions, stop
            break
        index += 1
        while True:
        
            response = requests.get(i)
            soup = BeautifulSoup(response.text, 'html.parser')
            cards = soup.find_all('div', 'cardOutline')
            count = 0
            for card in cards:
                if count >10:
                    repeated[index%3] = 1
                    break
                record = get_record(card, pos)
                if record[0] in pastRecords:
                    count += 1
                
                if record[0] not in jobids:
                    jobids.append(record[0])
                    record.append([])
                    if '(ENTRY_LEVEL)' in i and 'Entry Level' not in record[-1]:
                        record[-1].append('Entry Level')
                    elif '(MID_LEVEL)' in i and 'Mid Level' not in record[-1]:
                        record[-1].append('Mid Level')
                    elif '(SENIOR_LEVEL)' in i and 'Senior Level' not in record[-1]:
                        record[-1].append('Senior Level')
                    #TODO: create a list of states to recognize states in the location
                    if 'Remote' != record[6] and record[6] != "United States":
                        detail = record[6].split(',')
                        record.append(detail[0])
                        if len(detail) > 1:
                            record.append(detail[1][:3])
                        else:
                            record.append('')
                        records.append(record)
                    else:
                        record.append('')
                        record.append('')
                        records.append(record)
                else:
                    index = search_nested(records, record[0])
                    if '(ENTRY_LEVEL)' in i and 'Entry Level' not in records[index][-3]:
                        records[index][-3].append('Entry Level')
                    elif '(MID_LEVEL)' in i and 'Mid Level' not in records[index][-3]:
                        records[index][-3].append('Mid Level')
                    elif '(SENIOR_LEVEL)' in i and 'Senior Level' not in records[index][-3]:
                        records[index][-3].append('Senior Level')
                
                    # print(tuple(record))
            try:
                url = 'https://www.indeed.com' + soup.find('a', {'aria-label': 'Next'}).get('href')
            except AttributeError:
                break
    for record in records:    
        record[-3] = ",".join(record[-3])
        record = tuple(record)
    return records

def mergeSearchWords(sum_job_ids, current_search_words_records, sum_records):
    for i in range(len(current_search_words_records)):
        if current_search_words_records[i][0] in sum_job_ids:
            sum_records[search_nested(sum_records, current_search_words_records[i][0])][2] += ", " + (current_search_words_records[i][2])
        else:
            sum_records.append(current_search_words_records[i])
    

def main(Search_words, loc):
    connect = Connect_database("indeed_jobs")
    pastRecords = set()
    for i in Search_words:
        pastRecords = pastRecords.union(show_table(connect, i))
    sum_records = list()
    email_str = ""
    total_job_scrapped = 0
    sum_job_ids = set()
    for pos in Search_words:
        url = get_url(pos, loc)
        current_search_words_records = form_records(url, pos, pastRecords)
        mergeSearchWords(sum_job_ids, current_search_words_records, sum_records)
        for i in current_search_words_records:
            sum_job_ids.add(i[0])
        email_str += pos + ": "
        email_str += str(len(current_search_words_records)) + "\n"
        total_job_scrapped += len(current_search_words_records)
    email_str += "Total Job Scrapped On " + str(currentDate()) + " : " + str(total_job_scrapped) + "\n"
    email_str += "Unique Job Scrapped On " + str(currentDate()) + " : " + str(len(sum_job_ids)) + "\n"
    daily_report(email_str)
    
    
    # fname = 'swe'+ currentDate() +'.csv'
    # with open(fname, 'w', newline='', encoding='utf-8') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(['JobID', 'TimeStamp', 'JobTitle', 'Company', 'Location', 'Salary', 'Description', 'jobURL', 'Experience Level', 'City', "State"])
    #     writer.writerows(records)
    
    insert_data(connect, sum_records)
    
    
    

Search_words = ["Business Analyst", "Software Engineer", "Backend Software Engineer", "Front End Engineer",
                    "Electrical Engineer", "Data Analytics", "Mechanical Engineer", "Data Scientist", 
                    "Financial Analyst", "Accountant", "Machine Learning Engineer", "Marketing Analyst",
                    "Civil Engineer", "Chemical Engineer", "Biological Engineer", "Biostatistician", "Statistician",
                    "Quantitative Analyst", "Industrial Engineer", "Full-stack Engineer", "Supply Chain Engineer"]

main(Search_words, "Irvine")


        