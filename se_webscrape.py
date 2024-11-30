import requests
from bs4 import BeautifulSoup # bs4

# Function to fetch recent questions from the Gardening Stack Exchange
def fetch_questions_and_answers(pagesize=5, tagged=None):
    # Base URL for questions
    questions_url = "https://api.stackexchange.com/2.3/questions"
    
    # Set up parameters for the question request
    params = {
        "order": "desc",
        "sort": "creation",
        "site": "gardening.stackexchange.com",
        "pagesize": pagesize,
        "filter": "withbody"  # Include the question body
    }
    
    # Add optional tagged filter
    if tagged:
        params["tagged"] = tagged
    
    try:
        # Get recent questions
        response = requests.get(questions_url, params=params)
        response.raise_for_status()
        
        # Parse the JSON response for questions
        questions_data = response.json().get("items", [])
        
        # Process each question and fetch its answers
        for question in questions_data:
            question_id = question["question_id"]
            title = question["title"]
            body_html = question["body"]
            link = question["link"]
            tags = question["tags"]
            score = question["score"]
            
            # Convert HTML body to plain text
            body_text = BeautifulSoup(body_html, "html.parser").get_text()
            
            print(f"Title: {title}")
            print(f"Link: {link}")
            print(f"Tags: {', '.join(tags)}")
            print(f"Score: {score}")
            print(f"Question: {body_text}\n")
            
            # Fetch answers for the current question
            fetch_answers(question_id)
            
            print("-" * 50)
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching questions: {e}")

# Function to fetch answers for a specific question
def fetch_answers(question_id):
    # Base URL for answers
    answers_url = f"https://api.stackexchange.com/2.3/questions/{question_id}/answers"
    
    # Set up parameters for the answers request
    params = {
        "order": "desc",
        "sort": "votes",
        "site": "gardening.stackexchange.com",
        "filter": "withbody"  # Include the answer body
    }
    
    try:
        # Get answers for the question
        response = requests.get(answers_url, params=params)
        response.raise_for_status()
        
        # Parse the JSON response for answers
        answers_data = response.json().get("items", [])
        
        if answers_data:
            print("Answers:")
            for answer in answers_data:
                answer_body_html = answer["body"]
                answer_score = answer["score"]
                
                # Convert HTML body to plain text
                answer_text = BeautifulSoup(answer_body_html, "html.parser").get_text()
                
                print(f"Score: {answer_score}")
                print(f"Answer: {answer_text}\n")
        else:
            print("No answers found for this question.\n")
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching answers for question {question_id}: {e}")

# Fetch questions and answers related to the 'planting' tag
fetch_questions_and_answers(pagesize=10, tagged="planting")
