from export import save_to_file
from stackoverflow import get_jobs as so_jobs
from remote import get_jobs as rt_jobs
from weworkremotely import get_jobs as wwk_jobs
from flask import Flask, render_template, request, redirect,send_file

db = {}
def get_jobs(job_searching):
  jobs = so_jobs(job_searching)+rt_jobs(job_searching)+wwk_jobs(job_searching)
  return jobs
#save_to_file(jobs)

app = Flask("SuperScrapper")

@app.route("/")
def home():
  return render_template("template.html")

@app.route("/report")
def report():
  word = request.args.get('word')
  if word:
    word = word.lower()
    fromDB = db.get(word)
    if fromDB: 
      jobs = fromDB
    else:
      jobs = get_jobs(word)
      db[word] = jobs
  else:
    return redirect("/")
  return render_template(
    "report.html",
    searchingBy=word,
    resultsNumber=len(jobs),
    jobs = jobs
    )

@app.route("/export")
def export():
  try:
    word = request.args.get('word')
    if not word:
      raise Exception()
    word = word.lower()
    jobs = db.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs)
    return send_file("jobs.csv")
  except:
    return redirect("/")

  
app.run(host="0.0.0.0")