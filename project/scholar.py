import requests
import csv

API_KEY = "97e4b85da6ffc4d324ce7fbbd168739c0b19bdc1aa8b0d08474678edc1069566"  

url = "https://serpapi.com/search"

params = {
    "engine": "google_scholar_profiles",  
    "hl": "en",  
    "mauthors": "label:computational_neuroscience",  
    "api_key": API_KEY  
}


session = requests.Session()


with open("scholar_profiles.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

 
    writer.writerow(["Author Name", "Affiliation", "Google Scholar Link", "Research Interests", "Email Domain", "Citations"])

    while True:

        response = session.get(url, params=params)

        if response.status_code == 200:
            data = response.json()

            profiles = data.get("profiles", [])  


            for author in profiles:

                author_name = author.get("name", "N/A")

                affiliation = author.get("affiliations", "N/A")

                scholar_link = author.get("link", "N/A")

                interests = ", ".join([interest.get("title", "") for interest in author.get("interests", [])])

                email = author.get("email", "N/A")
                if email != "N/A":
                    email_domain = email.split(" at ")[-1]  
                else:
                    email_domain = "N/A"

                citations = author.get("cited_by", 0)  

                writer.writerow([author_name, affiliation, scholar_link, interests, email_domain, citations])


            profiles_last = profiles[-1]  
            last_citations = profiles_last.get("cited_by", 0)  

            if last_citations > 1000:
                next_page = data.get("pagination", {}).get("next")
                if next_page:

                    url = next_page  
                else:
                    print("No more pages")
                    break
            else:
                print("stop")
                break
        else:
            print(f"Request Failed: {response.status_code}")
            break
