import requests
from bs4 import BeautifulSoup
URL = f"https://stackoverflow.com/jobs?q="

def extract_job(html):
  title = html.find("h2",{"class":"mb4"}).find("a")["title"]
  company,location = html.find("h3",{"class":"mb4"}).find_all("span", recursive=False)
  company = company.get_text(strip=True)
  location = location.get_text(strip=True)
  job_id = html["data-jobid"]
  
  return {'title': title , 'company' : company, 'location' : location, 'link' : f"https://stackoverflow.com/jobs/{job_id}"}

def extract_jobs(job_name_searching):
  jobs = []
  result = requests.get(URL+job_name_searching)
  soup = BeautifulSoup(result.text, "html.parser")
  if not soup.find("div",{"class":"s-pagination"}):
    last_page = 1
  else:
    pages = soup.find("div",{"class":"s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
  
  for page in range(int(last_page)):
    result = requests.get(f"{URL}{job_name_searching}&pg={page+1}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div",{"class":"-job"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs

def get_jobs(job_name_searching):
  jobs = extract_jobs(job_name_searching)
  return jobs