import requests
import time
from bs4 import BeautifulSoup
import csv

product = input("Enter product name to crawl on Amazon: ")

url = f"https://www.amazon.in/s?k={product}"
print(f"Search URL: {url}")

# Crawl the product page
headers = {
        'authority': 'www.amazon.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9','accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        #'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

try:
    response = requests.get(url, headers=headers)
    print(f"Response status code: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Error occurred while making the request: {e}")
    exit(1)

# If the response is 503, try again
while response.status_code == 503:
    print("Server is busy. Waiting and trying again...")
    time.sleep(5)

    try:
        response = requests.get(url, headers=headers)
        print(f"Response status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while making the request: {e}")
        exit(1)

soup = BeautifulSoup(response.content, "html.parser")
product_links = soup.find_all("a", class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")

# Checking if the product was found 
if len(product_links) > 0:
    # up to 10 related products
    related_products = product_links[:10]

    # Looping through the related products and crawling the titles, prices, and reviews
    for related_product in related_products:
        related_product_url = "https://www.amazon.in" + related_product["href"]
        print(f"Product URL : {related_product_url}")
        related_product_response = requests.get(related_product_url, headers=headers)
        #print(f"Response status code: {response.status_code}")

        related_product_soup = BeautifulSoup(related_product_response.content, "html.parser")
        related_product_title_elem = related_product_soup.find("div", {'id':"titleSection"})

        if related_product_title_elem:
            related_product_title = related_product_title_elem.text.strip()
        else:
            related_product_title = "Title not found"

        related_product_price_elem= related_product_soup.find("span", class_="a-offscreen")
        if related_product_price_elem:
            related_product_price = related_product_price_elem.text.strip() 

        else:
            related_product_price = "Price not found"

        print(f"\nProduct Title: {related_product_title}\nPrice: {related_product_price}\n")

       # Crawling the reviews page for the related product

        reviews_response = requests.get(related_product_url, headers=headers)
        reviews_soup = BeautifulSoup(reviews_response.content, "html.parser")
        reviews = reviews_soup.find_all("a", class_="a-link-emphasis a-text-bold")

        if len(reviews) > 0:
          print(f"Reviews for {related_product_url}:")
          review_counter = 0
          review_list=[]
          with open(f'product_reviews.csv', mode='a', newline='', encoding='utf-8') as file:
           writer = csv.writer(file)

           for review in reviews:
             review_url = "https://www.amazon.in" + review['href'] + related_product_url.split("/")[-2]
             #print(f"review_page_url: {review_url}")
             review_response = requests.get(review_url, headers=headers)
             review_soup = BeautifulSoup(review_response.content, "html.parser")
             review_usernames = []
             review_body = []
             try:
              for UN in review_soup.find_all("span", class_="a-profile-name"):
               username = UN.text.strip()
               review_usernames.append(username)
             except AttributeError:
               review_usernames = ["N/A"]

             try:
              for reviews_bd in review_soup.find_all("span", {'data-hook':"review-body"}):
               body = reviews_bd.text.strip()
               review_body.append(body)
             except AttributeError:
              review_body = ["N/A"]
             for i in range(0, min(len(review_usernames), len(review_body))):
               #writer = csv.writer(file)
               writer.writerow([related_product_title, review_usernames[i], review_body[i]])
          print(f"\n{review_usernames}\n{review_body}\n\n")
             #review_counter += 1
             #if review_counter == 10:
              #break
        # Process the reviews in review_list as needed
        #for review in review_list:
          #print(review)
               #if len(reviews_list) > 0:
                # print(f"Reviews for {related_product_url}:")
               #for review in reviews_list:
                # print(f"\n{review['username']}\n{review['body']}\n\n")
    else:
     print(f"No reviews found for {related_product_url}.\n")

else:
    print(f"\nProduct '{product}' not found on Amazon.\n")
 
