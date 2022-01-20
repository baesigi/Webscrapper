import requests
from bs4 import BeautifulSoup

URL = "https://remoteok.com/remote-" 

def extract_job(html):
  title = html.find("h2",{"itemprop":"title"}).text.replace("\n","")
  company = html.find("h3",{"itemprop":"name"}).text.replace("\n","").replace(" ","")
  location = html.find("div",{"class":"location"}).text.replace("\n","").replace(" ","")
  if "$" in location:
    location = "No office location"
  else:
    pass
  job_id = html["data-url"]
  return {
          'title' : title,
          'company' : company,
          'location' : location,
          'link' : "https://remoteok.com/"+job_id
         }

def extract_jobs(job_name_searching):
  jobs = []
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',}
  result = requests.get(f"{URL}{job_name_searching}-jobs",headers=headers)
  soup = BeautifulSoup(result.text, "html.parser")
  results = soup.find_all("tr", {"class":"job"})
  print(len(results))
  for result in results:
    job = extract_job(result)
    jobs.append(job)
  return jobs
  
def get_jobs(job_name_searching):
  jobs = extract_jobs(job_name_searching)
  return jobs