# indeed_scrapper

Indeed Scarping is a job scraping program for MentorX to scrap the daily jobs appeared on Indeed.com

The program uses requests and beautifulsoup as python extensions to scrap the jobs into a MySQL database, and the fields of the job scrapped is showed in the below chart:

<img width="753" alt="image" src="https://user-images.githubusercontent.com/72479312/177077985-8d087f3a-1c27-4308-bf91-0945afbad00b.png">

In the diagram, JobID is a unique id existed in every job, Once the program fetched jobs with repetitive jobID which existed the amount of the threshold, the program will terminate and return all the jobs it scrapped for the day. JobIDs fetched in one day will be stored in a particular file for tomorrow to use and avoid repetiive scraping.

TimeStamp is the time that the job information is being fetched, in the format of dd-mm-yyyy hh:mm:ss.

JobTitle is the title of the job appeared on the indeed website.

Company is the company of the job

Location is splitted into two parts: state and city.

Salary is scrapped if provided.

Description is scrapped if provided.

JobUrl is also unique to every job, but not used as an identifier.

Experience Level is a tuple which might include Entry, mid, or senior level. One job might appear in multiple experience level. This is fetched in 3 times, and the informatio will be filtered and combined to form a complete output.

MySQL Database: Mark Jobs as Entities, with Job id as its unique indentifier/primary key. All other fields are attributes of the jobs.

To be implemented:
MYSQL database: Currently the program returns a csv file. Future plan is to store the job information into a mysql database for query.

Job Keyword field: The keyword searched to get this job will be stored as a field.

Algotithm to avoid conflicts between no-repetition algorithm in experience level and no-repetition between days.


