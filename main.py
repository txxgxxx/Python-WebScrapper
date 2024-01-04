from requests import get

websites = (
    "google.com",
    "httpstat.us/502",
    "httpstat.us/404",
    "httpstat.us/300",
    "httpstat.us/200",
    "httpstat.us/101",
)

results = {}

for website in websites:
  if not website.startswith("https://"):
    website = f"https://{website}"
  response = get(website)
  code = response.status_code
  if code >= 500:
    results[website] = "5xx/ server error"
  elif code >= 400:
    results[website] = "4xx / client error"
  elif code >= 300:
    results[website] = "3xx / redirection"
  elif code >= 200:
    results[website] = "2xx / successful"
  elif code >= 100:
    results[website] = "1xx / informational response"
  
print(results)
