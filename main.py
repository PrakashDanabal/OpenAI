from openai import OpenAI
from dotenv import load_dotenv
import requests
import os
from bs4 import BeautifulSoup

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/90.0.4430.212 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

def get_reviews(url):
  # Make a GET request to the website
  response = requests.get(url,headers=HEADERS)
  data=''


  # Check if the request was successful (status code 200)
  if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup)
    # Find HTML elements containing reviews (modify this based on the website structure)
    review_elements = soup.find_all('span',
                                    class_='a-size-base review-text review-text-content')  # Change 'review-class' to the actual class used for reviews

    # Extract and print the reviews
    for review in review_elements:
      review_text = review.get_text(strip=True)
      # print(review_text+'\n----------\n')
      data=data +review_text+'\n----------\n'
  else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
  return data


# Replace 'https://example.com' with the actual URL of the website containing reviews
# url = 'https://www.amazon.in/product-reviews/B077BFH786/&reviewerType=all_reviews30'
url = 'https://www.amazon.in/product-reviews/B077BFH786/&reviewerType=all_reviews/ref=cm_cr_arp_d_viewpnt_rgt?filterByStar=critical&pageNumber=1'
# url = 'https://www.amazon.in/SOFTSPUN-Microfiber-Cleaning-Detailing-Polishing/product-reviews/B077BFH786?ie=UTF8&pageNumber=2'
get_reviews(url)




load_dotenv()


OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')
# print(OPENAI_API_KEY)
# api_key=os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)


# completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
#     {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
#   ]
# )

# print(completion.choices[0].message)
# check git commands
# check2 
# check4 divya
# check5
# check6 divya
# test 2
#test prakash branch 1 checkin at 5:09pm
#is it woking?