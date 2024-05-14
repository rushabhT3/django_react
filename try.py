import google.generativeai as genai
import json

# Replace with your actual API key
API_KEY = "AIzaSyCPfJmtlfLRcduARGQCEoA6fUN3ja8oZ0M"

# History length to consider
HISTORY_LENGTH = 4

def extract_companies(text):
    model = genai.GenerativeModel(model_name="gemini-pro")
    response = model.generate_content([f"Extract just the company names from {text} and if any of the company names are incorrect, correct them and replace the wrong ones with them before extracting."])
    # print(response)
    generated_text = response._result.candidates[0].content.parts[0].text
    # Split the text by newline characters
    companies = generated_text.strip().split("\n")
    # Remove the hyphen from each company name
    companies = [company.split('- ')[1] for company in companies if company.startswith('- ')]
    # print(companies)
    return companies

def extract_matrix(text):
    model = genai.GenerativeModel(model_name="gemini-pro")
    response = model.generate_content([f"Extract all the performance metrics from {text}"])
    generated_text = response._result.candidates[0].content.parts[0].text
    metrics = generated_text.strip().split("\n")
    metrics = [metric.split('- ')[1] for metric in metrics if metric.startswith('- ')]
    return metrics

def process_query(query, history):
    companies = extract_companies(" ".join([obj["entity"] for obj in history] + [query]))
    json_list = []
    for company in companies:
        json_list.append({"entity": company.strip()})
    print(json_list)
    return json_list

def update_history(history, new_json):
    history.append(new_json)
    # Ensure history only keeps the last HISTORY_LENGTH entries
    history = history[-HISTORY_LENGTH:]
    return history

def load_history(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_history(filename, history):
    with open(filename, 'w') as f:
        json.dump(history, f)

# Load the conversation history from a file
conversation_history = load_history('history.json')

genai.configure(api_key=API_KEY)

# Example usage
query = "Give me some information about selsforse, quura, fleepcart"

# Process the query and update history
new_json_list = process_query(query, conversation_history)
for new_json in new_json_list:  # Update history for each company
    conversation_history = update_history(conversation_history, new_json)

# Save the conversation history to a file
save_history('history.json', conversation_history)

# Print the conversation history (limited to 4 entries)
print(conversation_history)