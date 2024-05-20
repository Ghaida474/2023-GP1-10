# Business Gate Project

## Introduction

The Kingdom's Vision 2030 serves as a guiding blueprint for Saudi Arabia's future, seeking to diversify the economy, reduce dependence on oil, and enhance public services such as health, education, infrastructure, recreation, and tourism. Universities within the Kingdom, particularly King Saud University (KSU), are instrumental in achieving these ambitious goals.

KSU stands as one of Saudi Arabia's premier higher education institutions, contributing significantly to the kingdom's academic and research landscape. A crucial part of KSU's contribution to Vision 2030 is through the King Abdullah Institution for Research and Consulting Studies (KAI), which operates as KSU’s business center and contractual interface, bridging academics and the market.

In line with Vision 2030, KSU has established twenty-two Business Units (BUs), each within a respective college. However, these BUs face challenges due to the lack of a robust system for managing daily activities, leading to communication gaps, resource management issues, and complexities in everyday tasks.

To address these challenges and improve workflow management, we introduce the Business Gate project. This platform aims to improve the operational efficiency of BUs at KSU, streamline operations, enhance communication, and facilitate resource management.

## Technology

The Business Gate project utilizes the following technologies:

- HTML/CSS
- JavaScript
- Python
- Dart/Flutter
- SQL
- Django


## Prerquisites
- python 3.12 or later version you can download python from https://www.python.org
- source-code editor
- pip which is included by Default when downloading python 3.4 or later
- Virtualenv you can follow this tutorial to install Virtualenv https://youtu.be/_MAdUhH49so?si=R7v00XBcmuzy69Lm
- Git
- redis
- PostgresSQL you can download it from https://www.postgresql.org/download/

## Launching Instructions for BusinessGate website 

To run this project, follow these steps:


1. Clone the repository to your local machine

2. Navigate to the Project Directory
   - from Terminal or Command prompt navigate to the directory by cd /path/to/the/directory/2023-GP1-10
   - replace /path/to/the/directory with the actual path
   - we will reder to this widow as the original Terminal window 
3. Create a Virtual Environment
   - by following the instruction python3 -m venv nameOfVirtualEnvironment
   - Replace nameOfVirtualEnvironment with the name you want for your virtual environment. For example, you could name it myenv
   - From here on out, we'll use myenv as the reference name for the virtual environment in these instructions
4. Activate the Virtual Environment
   - On Unix or MacOS use the following command: source venv/bin/activate
   - On Windows use the following command:.\venv\Scripts\activate
5. Install Dependencies
   - pip install -r requirements.txt
   - cd react-chat
   - npx create-react-app ce-quick-start
   - cd ce-quick-start
   - npm install react-chat-engine
   - npm install react-chat-engine-pretty
   - npm run build
6. Apply migrations
   - cd 2023-GP1-10
   - python manage.py makemigrations
   - python manage.py migrate
8. run redis server
    - in separate Terminal or Command prompt window  then the one used for the project let refer to it terminal(2) run command: brew services start redis
9. Run the Celery Worker
    - in separate Terminal or Command prompt window  then the one used for the project let refer to it terminal(3) run command:
      celery -A BusinessGate worker --loglevel=info
10. Run the Celery Beat
    - in separate Terminal or Command prompt window  then the one used for the project let refer to it terminal(4) run command:
  celery -A BusinessGate beat -l info
11. Run the Django Development Server
    - from the original Terminal window run this command: python manage.py runserver


## Host Site
http://munira22.pythonanywhere.com/
