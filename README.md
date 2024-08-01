# Simple Flask Web Application

This is a simple Flask web application that matches users with relevant content based on their interests. The developer has inspired themselves
from Netflix and in no way intend to cause any copyright violations. It is assumed that Anaconda/Miniconda is installed in the system

## Setup

1. Unzip the folder and navigate to within the flask_app directory. You should be able to see "app.py" when you use the "ls" command
2. Open terminal and navigate to the unzipped folder
3. Write the following command :
    ```
    conda create -n "flask_app_env" python=3.11 Flask=3.0.3


4. Run the application with the following command:
    ```bash
    python app.py
    ```
5. Navigate to:
    127.0.0.1:5000
    to access the application

## File Structure

- `app.py`: Main application file.
- `templates/index.html`: HTML template for fetching user input.
- `templates/relevant_content.html`: HTML template for displaying the relevant content.
- `templates/no_content.html`: HTML template for displaying error message when no content is available.
- `static/`: Directory for static files (CSS, JS) and images.
- `data/users.json`: JSON file containing user information and interests.
- `data/content.json`: JSON file containing tagged content.
- `tests/`: Directory containing unit tests.
- `README.md`: This is the readme file.
- `UI_test.xlsx` : Test cases of UI

## Running Tests

To run the tests:
```bash
python -m unittest discover tests
