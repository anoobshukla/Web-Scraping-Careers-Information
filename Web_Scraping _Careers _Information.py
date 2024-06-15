import requests
from bs4 import BeautifulSoup
import pandas as pd

final_data = []

home_url = "https://job-descriptions.careerplanner.com"

# Requesting and parsing the home page
response = requests.get(home_url)
response.raise_for_status()  # Raise an error for bad status codes
soup = BeautifulSoup(response.text, 'html.parser')  # Parse the HTML content

# Finding all <a> tags with href starting with 'https://Job-Descriptions.CareerPlanner.com'
all_jobs_a_tags = soup.find_all('a', href=lambda href: href and href.startswith('https://Job-Descriptions.CareerPlanner.com'))

# Initializing a list to store job descriptions
all_jobs_text_list = []

# Extracting job titles from <a> tags and appending 'NEW' if the next sibling is <span class="NewHiLight">
for job_a_tag in all_jobs_a_tags:
    job_text = job_a_tag.text.strip()
    job_a_tag_next_sibling = job_a_tag.find_next_sibling()
    if job_a_tag_next_sibling and job_a_tag_next_sibling.name == 'span' and job_a_tag_next_sibling.get('class') == ['NewHiLight']:
        if job_text.endswith('s'):
            job_text = job_text[:-1]  # Trim 's' from job title
    all_jobs_text_list.append(job_text)

# Iterating over the job titles to fetch detailed job data
count = len(all_jobs_text_list)

for i in range(0, count):
    job = all_jobs_text_list[i]
    
    # Creating a dictionary to store job data
    job_data = {
        "Career Name": job,
        "Basic Job Description": "",
        "Duties": "",
        "Activities": "",
        "Skills": "",
        "Abilities": "",
        "Knowledge": ""
    }
    
    # Generating URL variations for job details
    job_url_with_hyphen = job.replace(', ', '-').replace('/', '-').replace(' ', '-')
    url_1 = f"https://job-descriptions.careerplanner.com/{job_url_with_hyphen}.cfm"
    url_2 = f"https://job-descriptions.careerplanner.com/{job_url_with_hyphen}-2.cfm"
    url_3 = f"https://job-descriptions.careerplanner.com/{job_url_with_hyphen}-3.cfm"
    url_4 = f"https://job-descriptions.careerplanner.com/{job_url_with_hyphen}-4.cfm"
    url_5 = f"https://job-descriptions.careerplanner.com/{job_url_with_hyphen}-5.cfm"
    
    # Fetching and parsing job details from each URL
    response_1 = requests.get(url_1)
    response_1.raise_for_status()
    soup_1 = BeautifulSoup(response_1.text, 'html.parser')
    
    # Extracting basic job description from the first URL
    job_desc_div = soup_1.find('div', class_='Job-desc-table-mobile')
    job_desc_text = job_desc_div.find('p').get_text()
    job_data["Basic Job Description"] = job_desc_text.strip()
    
    # Extracting Duties from the second URL
    p_with_strong_tags = soup_1.find_all('p')
    duties_p_tags = [p_tag for p_tag in p_with_strong_tags if p_tag.strong and p_tag.strong.text.strip().startswith(tuple(map(str, range(10)))) and p_tag.strong.text.strip()[1] == ')' and len(p_tag.strong.text.strip()) < 4]
    duties_p_tags_texts = [p_tag.text.strip() for p_tag in duties_p_tags]
    duties = ' '.join(duties_p_tags_texts)
    job_data["Duties"] = duties
    
    # Extracting Activities from the third URL
    response_2 = requests.get(url_2)
    response_2.raise_for_status()
    soup_2 = BeautifulSoup(response_2.text, 'html.parser')
    p_with_strong_tags = soup_2.find_all('p')
    activities_p_tags = [p_tag for p_tag in p_with_strong_tags if p_tag.strong and p_tag.strong.text.strip().startswith(tuple(map(str, range(10)))) and p_tag.strong.text.strip()[1] == ')' and len(p_tag.strong.text.strip()) < 4]
    activities_p_tags_texts = [p_tag.text.strip() for p_tag in activities_p_tags]
    activities = ' '.join(activities_p_tags_texts)
    job_data["Activities"] = activities
    
    # Extracting Skills from the fourth URL
    response_3 = requests.get(url_3)
    response_3.raise_for_status()
    soup_3 = BeautifulSoup(response_3.text, 'html.parser')
    p_with_strong_tags = soup_3.find_all('p')
    skills_p_tags = [p_tag for p_tag in p_with_strong_tags if p_tag.strong and p_tag.strong.text.strip().startswith(tuple(map(str, range(10)))) and p_tag.strong.text.strip()[1] == ')' and len(p_tag.strong.text.strip()) < 4]
    skills_p_tags_texts = [p_tag.text.strip() for p_tag in skills_p_tags]
    skills = ' '.join(skills_p_tags_texts)
    job_data["Skills"] = skills
    
    # Extracting Abilities from the fifth URL
    response_4 = requests.get(url_4)
    response_4.raise_for_status()
    soup_4 = BeautifulSoup(response_4.text, 'html.parser')
    p_with_strong_tags = soup_4.find_all('p')
    abilities_p_tags = [p_tag for p_tag in p_with_strong_tags if p_tag.strong and p_tag.strong.text.strip().startswith(tuple(map(str, range(10)))) and p_tag.strong.text.strip()[1] == ')' and len(p_tag.strong.text.strip()) < 4]
    abilities_p_tags_texts = [p_tag.text.strip() for p_tag in abilities_p_tags]
    abilities = ' '.join(abilities_p_tags_texts)
    job_data["Abilities"] = abilities
    
    # Extracting Knowledge from the sixth URL
    response_5 = requests.get(url_5)
    response_5.raise_for_status()
    soup_5 = BeautifulSoup(response_5.text, 'html.parser')
    p_with_strong_tags = soup_5.find_all('p')
    
    # Finding and appending relevant knowledge information
    knowledge_p_tags = []
    for p_tag in p_with_strong_tags:
        knowledge_tag = p_tag.find('strong')
        if knowledge_tag and not knowledge_tag.text.strip().startswith(tuple(map(str, range(10)))):
            knowledge_p_tags.append(p_tag)
    
    knowledge_p_tags_texts = [p_tag.text.strip() for p_tag in knowledge_p_tags]
    
    # If no knowledge tags found, fallback to extracting from abilities tags
    if len(knowledge_p_tags_texts) == 0:
        knowledge_p_tags = [p_tag for p_tag in p_with_strong_tags if p_tag.strong and p_tag.strong.text.strip().startswith(tuple(map(str, range(10)))) and p_tag.strong.text.strip()[1] == ')' and len(p_tag.strong.text.strip()) < 4]
        knowledge_p_tags_texts = [p_tag.text.strip() for p_tag in knowledge_p_tags]
    
    knowledge = '.'.join(knowledge_p_tags_texts)
    job_data["Knowledge"] = knowledge
    
    # Appending job data to final_data list
    final_data.append(job_data)
    # break

# Creating a DataFrame from final_data and exporting to Excel and CSV files
df = pd.DataFrame(final_data)
df.to_excel('career_data.xlsx', index=False)
df.to_csv('career_data_csv.csv', index=False)
