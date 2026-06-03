import os
import requests
from datetime import datetime

API_KEY = os.environ["YOUTUBE_API_KEY"]

with open("streams.txt", "r", encoding="utf-8") as f:
video_ids = [x.strip() for x in f.readlines() if x.strip()]

url = (
"https://www.googleapis.com/youtube/v3/videos"
"?part=snippet,liveStreamingDetails"
"&id=" + ",".join(video_ids) +
"&key=" + API_KEY
)

data = requests.get(url).json()

rows = []

for item in data.get("items", []):

```
title = item["snippet"]["title"]

viewers = int(
    item.get("liveStreamingDetails", {})
        .get("concurrentViewers", 0)
)

rows.append({
    "title": title,
    "viewers": viewers
})
```

rows.sort(
key=lambda x: x["viewers"],
reverse=True
)

table_rows = ""

rank = 1

for row in rows:

```
table_rows += f"""
```

<tr>
<td>{rank}</td>
<td>{row['title']}</td>
<td>{row['viewers']}</td>
</tr>
"""

```
rank += 1
```

html = f"""

<!DOCTYPE html>

<html>
<head>

<meta charset="utf-8">

<meta http-equiv="refresh" content="300">

<title>YouTube Counter</title>

<style>

body {{
    background:#000;
    color:#fff;
    font-family:Arial;
    margin:0;
    padding:5px;
}}

table {{
    width:100%;
    border-collapse:collapse;
}}

td {{
    padding:2px 6px;
    font-size:12px;
    border-bottom:1px solid #111;
}}

tr:hover {{
    background:#111;
}}

td:nth-child(1) {{
    width:40px;
}}

td:nth-child(3) {{
    text-align:right;
    width:80px;
}}

</style>

</head>

<body>

<table>

{table_rows}

</table>

</body>

</html>
"""

with open("dashboard.html", "w", encoding="utf-8") as f:
f.write(html)

print(
f"Updated {datetime.utcnow().isoformat()} UTC"
)
