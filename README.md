# GetHired-Backend

This repository contains the backend codebase of GET-HIRED job portal app developed using Django, Django Rest Framework, simple jwt and other technologies.You can find the frontend code in the [GetHired-
frontend repository](https://github.com/ashwin275/GetHired-Frontend).


## Overview

GET-HIRED Backend is responsible for managing the core functionalities of the job portal app, including user authentication, job post management, real-time communication, email verifications ,user and recruiter management.


## Features

- User authentication using JWT (token refreshing , token blacklisting).
- RESTful API endpoints for job seekers, recruiters, and administrators.
- Real-time chat between recruiters and job applicants using Django Channels and WebSocket with Redis as the message broker.
- Email verification using smtp.
- PostgreSQL for the database


## Getting Started

Follow these steps to set up and run the backend locally:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/ashwin275/GetHired-Backend.git

2. **Create a virtual environment and activate it:**
    
   ```bash
   python -m venv djvenv
   source djvenv/bin/activate   # On Windows: djvenv\Scripts\activate

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
    
4. **Set Up the PostgreSQL Database:**

   . Create a PostgreSQL database and update the database configuration in the settings.

   . Run migrations:
   ```bash
   
   python manage.py migrate

5. **Configure Email Settings:**
 
    . Update the email settings in the settings.py file for email verification.

7. **Run the Redis Server**:

    . Make sure you have Redis installed and running.
    . Update the CHANNEL_LAYERS setting in settings.py to use Redis as the message broker.

8. **Access the backend API at** http://127.0.0.1:8000/api/.



   

