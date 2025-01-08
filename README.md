# About
Project for learning pytest. Used application for testing purpose: https://thinking-tester-contact-list.herokuapp.com/.  
I wrote automation tests using *pytest* to validate different operations with the app.

## Description
Performed Exploratory, API, and UI testing of Contact List App (https://thinking-tester-contact-list.herokuapp.com/).  
Used libs: pytest, pytest-html, requests, selenium.  
You can read detailed reports in `reports` folder. Also, you can import Postman collection. Requests with buggy responses are saved and named after the charter and note/bug number (see exploratory_test_charter file for the details).

## Features
- API and UI tests;
- Positive and negative test cases;
- Logging;
- Option to generate html report;

## Usage
1. Download this repository: `git clone https://github.com/Stinger-22/qa-contact-list.git`.
2. Create python virtual environment and activate it.
3. Install all dependencies: `pip install -r 'requirements.txt'`.
4. Run tests: `pytest`.  
To change logging level use `--log-cli-level=LEVEL`.  
To set log file use `--log-file=FILE`.  
To generate html report use `--html=FILE`.  
For more info about CLI parameters read docs.

## Project structure
```
.
├── contact-list.postman_collection.json
├── pyproject.toml
├── README.md
├── reports
├── requirements.txt
├── src
│   ├── __init__.py
│   └── util
│       ├── admin
│       │   ├── admin_api.py
│       │   ├── bearer_auth.py
│       │   └── __init__.py
│       └── __init__.py
└── tests
    ├── api
    │   ├── conftest.py
    │   ├── contact
    │   │   ├── conftest.py
    │   │   ├── __init__.py
    │   │   ├── test_api_contact.py
    │   │   └── test_cases_contact.py
    │   ├── __init__.py
    │   ├── test_cases_user.py
    │   └── user
    │       ├── conftest.py
    │       ├── __init__.py
    │       └── test_api_user.py
    ├── conftest.py
    ├── __init__.py
    ├── ui
    │   ├── conftest.py
    │   ├── __init__.py
    │   ├── pages.py
    │   ├── test_contact.py
    │   ├── test_log_in.py
    │   └── test_sign_up.py
    └── util
        ├── __init__.py
        └── test_case_parse.py
```

## Things to improve
- Test cases in one folder in json;
- Another approach to contact testing. I have a lot of reuse in post, put, patch;
- Contact list and contact in different classes;
- Firefox ui test is unstable;
- Contact page does not have UI tests;