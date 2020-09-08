import csv
from flask import Flask, render_template, request, redirect
from indeed_scrapper import get_indeed_jobs

app = Flask("Job Scraper")
db = {}

def save_to_file(jobs):
  file = open("jobs.csv", mode="w")
  writer = csv.writer(file)
  writer.writerow(["Title", "Company", "Location", "Link"])

  for i in range(len(jobs)):
    writer.writerow(list(jobs[i].values()))

  return None

@app.route("/")
def home():
  return render_template("main_page.html")

@app.route("/report")
def report():
  word = request.args.get('word')
  if word is not None:
    word = word.lower()
    fromDb = db.get(word)
    if fromDb is not None:
      jobs = fromDb
    else:
      jobs = get_indeed_jobs(word)
      db[word] = jobs
    save_to_file(jobs)
    return render_template("report.html",
      search=word,
      resultsLen=len(jobs),
      jobs=jobs
    )
  else:
    return redirect("/")

app.run(host="0.0.0.0")