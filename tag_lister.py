# %%

import requests 
import datetime
import os
from dotenv import load_dotenv
load_dotenv()

APIKEY = input("Api key?") or os.environ.get("TOGGL_KEY") or "Not Set"
session = requests.Session()
session.auth = (APIKEY, "api_token")

WORKSPACE = input("Workspace?") or os.environ.get("WORKSPACE") or 1
# %%
WEEK = int(input("WEEK? [current]") or -1)

tags = session.get(
    "https://api.track.toggl.com/api/v9/me/tags"
).json()

times = {}

today = datetime.date.today()

if WEEK < 0:
    today = today + datetime.timedelta(weeks=WEEK)
elif WEEK > 0:
    today = datetime.datetime.strptime(f"{today.year}-{WEEK}-1", "%Y-%W-%w").date()

startDate = today - datetime.timedelta(today.weekday())
endDate = startDate + datetime.timedelta(6)


print(f"Querying from {startDate} to {endDate}")

for tag in tags:

    if tag["workspace_id"] != int(WORKSPACE):
        continue

    projects = session.post(
        f"https://api.track.toggl.com/reports/api/v3/workspace/{WORKSPACE}/weekly/time_entries",
        json= {
            "tag_ids": [
		        tag["id"]
	        ],
            "start_date": startDate.isoformat(),
	        "end_date":endDate.isoformat(),
        },
        headers= {
            "Content-Type": "application/json"
        }
    ).json()

    print(tag["name"])
    seconds = 0

    for p in projects:
        seconds += sum(p["seconds"])
    print(seconds)

    times[tag["name"]] =  seconds

## %%
strTimes = {}
for (tag, seconds) in times.items():
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    time = datetime.timedelta(seconds=seconds)
    strTimes[tag] = f"{h:d}:{m:02d}:{s:02d}"
    print(f"{tag}: {strTimes[tag]}")

print(",".join(strTimes.get(k) or "0:00" for k in ["Vorlesung","Übung","Homework","Lernen","Vorbereitung","Nachbereitung","Tutoring","Gruppenarbeit","Konferenz","Research",	"Video"
]))

# %%
