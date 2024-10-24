import datetime
import requests
import json

API_KEY = # Replace with your actual Gemini API key
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"

def load_prompts_from_json():
    # Load JSON file containing topic, date, and prompts
    with open("topics_and_prompts.json", "r") as file:
        data = json.load(file)
    
    today = datetime.datetime.now().strftime("%d-%m-%Y")
    
    # Look for a topic that matches today's date
    for entry in data:
        if entry["Date"] == today:
            return entry["Topic"], entry["Prompts"]
    
    return None, None

def generate_content(topic, prompts):
    style_it = "Please incorporate emojis and various markdown styles (like **bold**, *italic*, `code`, and headers) to make the content visually engaging."
    content = ""
    headers = {'Content-Type': 'application/json'}
    
    for prompt in prompts:
        # Modify the prompt to include the style instruction
        data = {"contents": [{"parts": [{"text": f"{prompt.format(topic=topic)} {style_it}"}]}]}
        
        # Send request to Gemini API
        response = requests.post(API_URL, headers=headers, json=data)
        result = response.json()
        
        try:
            generated_text = result['candidates'][0]['content']['parts'][0]['text']
            content += f"{generated_text}\n\n"
        except KeyError:
            content += "Error: Failed to retrieve content for this prompt.\n\n"
    
    return content

def save_to_markdown(content, topic):
    today = datetime.datetime.now().strftime("%d-%m-%Y")
    filename = f"{today}_{topic.replace(' ', '_')}.md"

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Content saved to {filename}")

def main():
    # Load topic and prompts from JSON file based on today's date
    topic, prompts = load_prompts_from_json()
    
    if topic and prompts:
        print(f"Generating content for topic: {topic}")
        content = generate_content(topic, prompts)
        save_to_markdown(content, topic)
    else:
        print("No matching topic found for today's date.")

if __name__ == "__main__":
    main()
