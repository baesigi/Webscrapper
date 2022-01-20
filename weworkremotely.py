import requests
from bs4 import BeautifulSoup

URL = "https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term=" 

def extract_job(html):
  title = html.find("span",{"class":"title"}).text
  company = html.find("span",{"class":"company"}).text
  if not html.find("span",{"class":"region company"}):
    location = "None"
  else:
    location = html.find("span",{"class":"region company"}).text
  job_id = html.find('a')['href']
  return {
          'title':title ,
           'company' : company,
            'location' : location,
             'link' : "https://weworkremotely.com/"+job_id
          }

def extract_jobs(job_name_searching):
  jobs = []
  result = requests.get(URL+job_name_searching)
  soup = BeautifulSoup(result.text, "html.parser")
  results = soup.find_all("li", {"class":"feature"})
  for result in results:
    job = extract_job(result)
    jobs.append(job)
  return jobs

def get_jobs(job_name_searching):
  jobs = extract_jobs(job_name_searching)
  return jobs