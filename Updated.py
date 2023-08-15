import time
from bs4 import BeautifulSoup
import csv
import pandas as pd
import nltk
from textblob import TextBlob
import os
from flask import Flask, render_template, request
import chardet
from sklearn.metrics import precision_score, recall_score, f1_score
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import requests

app = Flask(__name__)

"""
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/quickshop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    __tablename__ = 'users'  # Update the table name to 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)






@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the login form data
        name = request.form['name']
        password = request.form['password']

        # Check if the user exists in the database
        user = User.query.filter_by(name=name, password=password).first()

        if user:
            # User authentication successful
            # Redirect to the appropriate page
            return render_template('index.html')  # Replace 'index.html' with the appropriate page

        else:
            # User authentication failed
            # Show an error message
            return render_template('login.html', error_message='Authentication failed')  # Replace 'login.html' with the appropriate login page


    # Handle GET requests or other cases
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get the signup form data
        name = request.form['name']
        password = request.form['password']

        # Check if the username already exists in the database
        existing_user = User.query.filter_by(name=name).first()

        if existing_user:
            # Username already exists
            # Show an error message
            return render_template('login.html')

        else:
            # Create a new user object and insert it into the database
            new_user = User(name=name, password=password)
            db.session.add(new_user)
            db.session.commit()

            # User registration successful
            # Redirect to the appropriate page
            # ...

            # Add a success message if desired
            success_message = 'Registration successful! Please log in.'
            return render_template('login.html', success_message=success_message)

    # Handle GET requests or other cases
    return render_template('signup.html')

   
"""
@app.route('/', methods=['GET'])
def home():
    #return render_template('index.html')
    return render_template('test.html')

@app.route('/home', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        product = request.form['product']
        if product:
            url = f"https://www.amazon.com/s?k={product}"
            # print(f"Search URL: {url}")

        headers = {
            'Host': 'www.amazon.in',
            'Connection': 'close',
            'device-memory': '8',
            'sec-ch-device-memory': '8',
            'dpr': '1',
            'sec-ch-dpr': '1',
            'viewport-width': '1366',
            'sec-ch-viewport-width': '1366',
            'rtt': '100',
            'downlink': '10',
            'ect': '4g',
            'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"10.0.0"',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Cookie': 'session-id=262-6671822-5304245; session-id-time=2082787201l; i18n-prefs=INR; ubid-acbin=260-3024353-3077152; session-token=bR4LC6G2XH0uJFryM1vNLcKRcn3J8idAHkzKz2QjI2JXO9UKtHzkMJJBiCguiBiUpxUzwJ0HDnaAC+ViN6j1ZLbBI3+4tBqGpjZktLipz7vD9WEyanPPLUiTZrS1eUKFK8zPsSG4twlZ73F8TaaI8MMxqgNe/R6NV1hyeGX9IKDW7BRVncFc/zSUbDg6x8P7CH6KmhgUDQsPjsyskrSQCz6cPXMKpbluOFpbjNYlReE=; csm-hit=tb:PWY7RKK25BQBSVCZZY9J+s-PWY7RKK25BQBSVCZZY9J|1692073540944&t:1692073540944&adb:adblk_unk'
                    
        }
        
        try:
            response = requests.get(url,headers=headers)
            print(f"Response status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error occurred while making the request: {e}")
            exit(1)

        # If the response is 503
        while response.status_code == 503:
            print("Server is busy. Waiting and trying again...")
            time.sleep(5)

            try:
                response = requests.get(url,headers=headers)
                print(f"Response status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Error occurred while making the request: {e}")
                exit(1)

        soup = BeautifulSoup(response.content, "html.parser")
        product_links = soup.find_all("a", class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")

        columnname = ['Product', 'Price', 'Review', 'url']
        with open('product_reviews.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(columnname)

        # Checking if the product was found
        if len(product_links) > 0:
            related_products = product_links[:2] 
            related_product_url1 = []

            for related_product in related_products:
                related_product_url = "https://www.amazon.com" + related_product["href"]
                related_product_url1.append(related_product_url)

                related_product_response = requests.get(related_product_url, headers=headers)
                related_product_soup = BeautifulSoup(related_product_response.content, "html.parser")
                related_product_title_elem = related_product_soup.find("span", {'id': "productTitle"})

                if related_product_title_elem:
                    related_product_title = related_product_title_elem.text.strip()
                else:
                    related_product_title = "Title not found"

                related_product_price_elem = related_product_soup.find("span", class_="a-price-whole")
                if related_product_price_elem:
                    related_product_price = related_product_price_elem.text.strip()
                else:
                    related_product_price = "Price not found"

                # print(f"\nProduct Title: {related_product_title}\nPrice: {related_product_price}\n")

                # Crawling the reviews page for the related product
                reviews_response = requests.get(related_product_url, headers=headers)
                reviews_soup = BeautifulSoup(reviews_response.content, "html.parser")
                reviews = reviews_soup.find_all("a", class_="a-link-emphasis a-text-bold")

                if len(reviews) > 0:
                    print(f"Reviews for {related_product_url}:")
                    # review_counter = 0
                    # review_list = []

                    for review in reviews:
                        review_url = "https://www.amazon.com" + review['href'] + related_product_url.split("/")[-2]
                        # print(f"review_page_url: {review_url}")
                        review_response = requests.get(review_url, headers=headers)
                        review_soup = BeautifulSoup(review_response.content, "html.parser")
                        # review_usernames = []
                        review_body = []
                        try:
                            for reviews_bd in review_soup.find_all("span", {'data-hook': "review-body"}):
                                body = reviews_bd.text.strip()
                                review_body.append(body)
                        except AttributeError:
                            review_body = ["N/A"]
                        # Open the CSV- append mode
                        with open('product_reviews.csv', mode='a', newline='', encoding='utf-8') as file:
                            writer = csv.writer(file)
                            for i in range(0, min(len(review_body), len(related_product_price))):
                                writer.writerow(
                                    [related_product_title, related_product_price, review_body[i], related_product_url])

                else:
                    print(f"No reviews found for {related_product_url}.\n")

        else:
            print(f"\nProduct '{product}' not found on Amazon.\n")

        ## SENTIMENT ANALYSIS ##--------------------

        df = pd.read_csv("product_reviews.csv")
        df['Review'] = df['Review'].str.replace('[^\w\s]', '', regex=False)
        df['Review'] = df['Review'].str.lower()

        # Define the path to the folder
        folder_path = 'D:/Start/StopWords'
        file_names = os.listdir(folder_path)

        stop_words = []

        for file_name in file_names:
            with open(os.path.join(folder_path, file_name), 'rb') as f:
                raw_bytes = f.read()
                encoding = chardet.detect(raw_bytes)['encoding']
                text = raw_bytes.decode(encoding)
                stop_words += [line.strip() for line in text.split('\n')]

        ##print(stop_words)

        df['Review'] = df.iloc[1:, ]['Review'].apply(
            lambda x: ' '.join([word for word in str(x).split() if word.lower() not in stop_words]))

        positive_words = []
        negative_words = []

        # Read the positive words
        with open('positive-words.txt', 'rb') as f:
            raw_bytes = f.read()
            encoding = chardet.detect(raw_bytes)['encoding']
            text = raw_bytes.decode(encoding)
            positive_words += [line.strip() for line in text.split('\n')]

        # Read the negative words
        with open('negative-words.txt', 'rb') as f:
            raw_bytes = f.read()
            encoding = chardet.detect(raw_bytes)['encoding']
            text = raw_bytes.decode(encoding)
            negative_words += [line.strip() for line in text.split('\n')]

        ##print(positive_words)
        ##print(negative_words)

        # sentiment Analysis

        def get_sentiment(Review):
            analysis = TextBlob(str(Review))
            # positive_score = sum(word in positive_words for word in analysis.words)
            # negative_score = sum(word in negative_words for word in analysis.words)
            sentiment_score = analysis.sentiment.polarity
            if sentiment_score > 0:
                sentiment_label = 'Positive'
            elif sentiment_score < 0:
                sentiment_label = 'Negative'
            else:
                sentiment_label = 'Neutral'
            return sentiment_label, sentiment_score

        df['sentiment'], df['sentiment_score'] = zip(*df['Review'].map(get_sentiment))

        # df['sentiment'] = df['Review'].apply(get_sentiment)
        true_labels = df['sentiment']
        predicted_labels = df['sentiment']

        precision = precision_score(true_labels, predicted_labels, average='macro')
        recall = recall_score(true_labels, predicted_labels, average='macro')
        f1 = f1_score(true_labels, predicted_labels, average='macro')

        df['Precision'] = precision
        df['Recall'] = recall
        df['F1 Score'] = f1

        unique_products = df['Product'].unique()

        product_positive_counts = {}

        for product in unique_products:
          product_df = df[df['Product'] == product]
          positive_reviews = product_df[product_df['sentiment'] == 'Positive']
          product_positive_counts[product] = len(positive_reviews)
  
        sorted_products = sorted(product_positive_counts.items(), key=lambda x: x[1], reverse=True)
        sorted_products_df = pd.DataFrame(sorted_products, columns=['Product', 'Positive Count'])
        df_merged = pd.merge(sorted_products_df, df, on='Product', how='left')

        #print(sorted_products)
        #df.to_csv("product_reviews.csv", index=False)


        # Pass the sorted_products variable along with the reviews DataFrame to the template
    return render_template('home.html', reviews=df_merged[['Product', 'Price', 'Review', 'sentiment', 'url']].to_dict(orient='records'))


if __name__ == '__main__':
    app.run(debug=True)

