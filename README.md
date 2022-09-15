# indeed_scrapper

Indeed Scarping is a job scraping program for MentorX to scrap the daily jobs appeared on Indeed.com

The program uses requests and beautifulsoup as python extensions to scrap the jobs into a MySQL database, and the fields of the job scrapped is showed in the below chart:

<img width="614" alt="截屏2022-09-03 下午1 47 31" src="https://user-images.githubusercontent.com/72479312/188287256-02c56534-e662-4c4c-9c70-f57e61ae95d0.png">
<img width="1340" alt="截屏2022-09-03 下午1 47 16" src="https://user-images.githubusercontent.com/72479312/188287258-eef96356-d149-4879-aaa7-90d04933be9c.png">


In the diagram, JobID is a unique id existed in every job, Once the program fetched jobs with repetitive jobID which existed the amount of the threshold, the program will terminate and return all the jobs it scrapped for the day. 

SearchWord is the search term used to find the job.

PostDate is the date that the job is posted on the website.

TimeStamp is the time that the job information is being fetched, in the format of dd-mm-yyyy hh:mm:ss.

JobTitle is the title of the job appeared on the indeed website.

Company is the company of the job

Location is splitted into two parts: state and city.

Salary is scrapped if provided.

JobType is to show if the job is fulltime, parttime, or contract.

Description is scrapped if provided.

JobUrl is also unique to every job, but not used as an identifier.

Experience Level is a tuple which might include Entry, mid, or senior level. One job might appear in multiple experience level. This is fetched in 3 times, and the informatio will be filtered and combined to form a complete output.

MySQL Database: Mark Jobs as Entities, with Job id as its unique indentifier/primary key. All other fields are attributes of the jobs.

The program will go over each search term and use selenium to browse the jobs on indeed.com sorted by date. When the jobs are scraped, the program will check if it is repeated with the job id it scrapped today ot if it is repeated with the recent jobs it scrapped. Once the repetition reaches at certain limit, the program will terminate and go to the next search term. 

To be implemented:

Solve the problem that there might be multiple job type, which will only show elements such as Fulltime/n+1 in the cart. This can be solved by click into each cart and find the full type list under the detailed information tab on the right side.

Split the salary field to hourly salary and min/max salary.

Scrape the Preferred skills and experience field by click into each cart and find the information under the detailed information tab on the right side.

Create company info such as company id, company name, company url, company review courts and average starts and make it as a foreign key in the job table.

Enhance the searching technique by using prefix and postfix to distinguish the experience level instead of the automatic parameter of indeed, which is inaccurate.

Add proxy layer.


