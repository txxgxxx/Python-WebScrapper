from requests import get

websites = (
    "google.com",
    "airbnb.com",
    "twitter.com",
    "facebook.com",
    "tiktok.com",
)

for website in websites:
  if not website.startswith("https://"):
    website = f"https://{website}"
  print(website)