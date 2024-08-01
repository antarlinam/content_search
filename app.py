from flask import Flask, render_template, request, redirect, url_for
import json
import difflib
import re

app = Flask(__name__)

def load_data():
    """
    Load user and content data from JSON files.

    Returns:
        tuple: A tuple containing two lists, one for users and another for content. 
        The lists inturn contain dictionaries for each user and content respectively
    """
    with open('data/users.json') as f:
        users = json.load(f)
    with open('data/content.json') as f:
        content = json.load(f)
    return users, content

def match_content(users, content):
    """
    Match content to users based on their interests and content tags. Matched 
    content is segregated into content categories which are then displayable 
    in there individual tables

    Args:
        users (list): List of user data, each with a list of interests.
        content (list): List of content data, each with a list of tags.

    Returns:
        dict: A dictionary mapping user keys to matched content.

    Assumptions:
        Users are assumed to be unique in each country, however a user 
        name is allowed to repeat across countries.
        An additional TAG of CONTENT_CATEGORY have been added to add 
        complexity to the output
    """
    matched_content = {}
    for user in users:
        user_key = f"{user['name'].lower()}-{user['interests'][0]['value']}"  # Convert user name to lowercase and add the country key to it
        user_matched_content = {'Movies': [], 'Games': [], 'TV Shows': []}
        for interest in user['interests']:
            for item in content:
                for tag in item['tags']:
                    if tag['type'] == interest['type'] and tag['value'] == interest['value'] and tag.get('threshold', 0) >= interest.get('threshold', 0):
                        for next_tag in item['tags']:
                            if next_tag['type'] == 'content_category':
                                category = next_tag['value']
                                if category == "Movies":
                                    user_matched_content['Movies'].append(item)
                                elif category == "Games":
                                    user_matched_content['Games'].append(item)
                                elif category == "TV Shows":
                                    user_matched_content['TV Shows'].append(item)
        if any(user_matched_content[category] for category in user_matched_content):
            matched_content[user_key] = {'user': user, 'content': user_matched_content}
    return matched_content

users, content = load_data()
matched_content = match_content(users, content)

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Handle the main page for user input and show results or suggestions.

    If a POST request is made, process the input name and check for exact or 
    similar matches.
    Display the matched content or suggestions accordingly.

    Returns:
        render_template: Renders the appropriate HTML template with context.
    """
    if request.method == 'POST':
        name = request.form['name'].strip()  # Strip spaces

        # Validation: Check for valid characters (letters, apostrophes, hyphens)
        if not name or not re.match(r"^[a-zA-Z][a-zA-Z\s'-]*$", name):
            return render_template('index.html', error='Please enter a valid name. Only alphabets, spaces, apostrophes, and hyphens are allowed.')

        name = name.lower()  # Convert input name to lowercase

        matched_users = [key for key in matched_content.keys() if key.split('-')[0] == name]  # Exact case-insensitive match

        # Exact match logic
        if matched_users:
            relevant_users = [matched_content[user_key] for user_key in matched_users if any(matched_content[user_key]['content'][category] for category in matched_content[user_key]['content'])]
            if relevant_users:
                if len(relevant_users) > 1:
                    return render_template('index.html', multiple_users=True, matched_users=relevant_users)
                else:
                    user_data = relevant_users[0]
                    return redirect(url_for('get_content', name=user_data['user']['name'], country=user_data['user']['interests'][0]['value']))
        
        # If no exact matches, look for similar names. Similarity thresholds can be manipulated but defaults have been preserved
        similar_names = difflib.get_close_matches(name, [user['name'].lower() for user in users])
        if similar_names:
            similar_names_proper_case = [user['name'] for user in users if user['name'].lower() in similar_names]
            return render_template('index.html', error=f'User <span class="highlight">{name}</span> not found. Did you mean:', similar_names=similar_names_proper_case, users=users)
        else:
            return render_template('index.html', error=f'User <span class="highlight">{name}</span> not found. No similar names found. Please try again.')
    return render_template('index.html')

@app.route('/content/<name>/<country>', methods=['GET'])
def get_content(name, country):
    """
    Display matched content for a specific user.

    Args:
        name (str): The name of the user.
        country (str): The country tag for the user.

    Returns:
        render_template: Renders the relevant content HTML 
        template or a no-content message.
    """
    user_key = f"{name.lower()}-{country}"  # Use lowercase for consistent key access
    user_content = matched_content.get(user_key, None)
    if user_content:
        user = user_content['user']
        user_matched_content = user_content['content']
        has_matches = any(user_matched_content[category] for category in user_matched_content)
        return render_template('relevant_content.html', user=user, matched_content=user_matched_content, has_matches=has_matches)
    return render_template('no_content.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)
