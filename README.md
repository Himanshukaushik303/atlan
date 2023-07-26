# Atlan Assignment

## Recorded Video of all the APIs Working
[Download the video](https://github.com/Himanshukaushik303/atlan/blob/master/Atlan%20-%20Google%20Chrome%202023-07-27%2000-45-44.mp4)

## Table of Contents
- [How to Run](#how-to-run)
- [Task 1](#task-1)
- [Task 2](#task-2)
- [Task 3](#task-3)
- [Task 4](#task-4)


## How to Run
Instructions on how to run all the tasks collectively.
1. Clone the repo to your local system

    `https://github.com/Himanshukaushik303/atlan.git`

2. Create a virtual environment. You can use this [link](https://docs.python.org/3/library/venv.html) for reference.

    `python -m venv venv`

3. Activate your virtual environment using :

    `venv/Scripts/activate`

    Here venv is the name of virtual environment.

4. Install all the requirements required to run the project :

    `pip install -r requirements.txt`

5. Run the django server :

    `python manage.py runserver`
6. Checkout views.py in api directory for all the logic.


## Assumptions : 
I am assuming that i am working on the last layer of the backend and all the validation of the data in done in the previous layers. I am calling directly db with all the data in correct format received from frontend forms.
  
## Task 1

Task is to get slang in local language.

### Approaches
  ### Approach 1
    1. We can maintain a database for this having language as one column and text as another.  
    2. Then we will query the database for all the words and return the translated text.  
    3. We can use indexing to reduce latency or Elastic Search for getting the translated text.
  ### Pros/Cons :
    1. This approach will give offline suppport and customizabilty.
    2. Difficult to maintain the database and high latency and not very scalable.

  ### Approach 2
    1. We can use a pre trained NLP model to get the slangs in local language like Urban Dictionary models.
    2. We will integrate the ML model and use for either offline and online real time translation.
  ### Pros/Cons :
    1. This approach will give use ML models but prone to mistakes.
    2. ML models have lesser support for wide range of languages and updates come very late.

  ### Approach 3 (Used)
    1. We can use API services to get translate the text and get teh results in realtime.
    2. We will use Google Translate API to translate the text. Other options are available like Yendex, Urban Dictionary but lesser number of language support and less reliable.
  ### Pros/Cons :
    1. This is easy to maintain and integrate in the project and gives reliable results in real time.
    2. No customizabilty and api service is prone to go down which will give error in our project.

### Implementation
I have integrated the Google Cloud Translate Library using Service Account Credentials from Google Cloud.
<img src="https://github.com/Himanshukaushik303/atlan/blob/master/api/static/slang.png" width="100%" height="50%">


## Task 2
Task is to validate the response received.

### Usage
  For this task i have created a flow of Adding a response.
  For every new response coming in it will go to a validation check and if failed the response will not be added to the database and Invalid response message will be sent.
  If validation is passed the record will be added to the database.
  <img src="https://github.com/Himanshukaushik303/atlan/blob/master/api/static/addResponse.png" width="100%" height="50%">


## Task 3
Task is to get all the data in Google sheets.

### Approaches
  ### Approach 1
    1. After adding all the responses in the database we can generate a google sheet and add all the data when ever user clicks on getUrl to get Google sheet.
    2. We will have to add one extra field in database to add only those records which are not there or rewrite the whole sheet with all the records.
    3. Then we can either generate a downloadable file or give a url to open the sheet.

  ### Pros/Cons
    1. Very high latency if adding only unsynced records because we will have to scan whole database and redundant work if writing every time.
    2. For failed operations when sheets api is down, there is no way other than marking it unsynced and again follow the above approach.

  ### Approach 2
    1. We can use queues for storing the response and asynchronously add the response to the sheet.
    2. We can use Lambda or SQS queues for the same and handle sheet api failures.

  ### Pros/Cons
    1. Added cost for using the service.
    2. Over engineering if we can handle the requests using other methods.
    
  ### Approach 2 (Used)
    1. Assuming the flow of adding a response to the database if it is valid. After the response is successfully added to the database and succescful response is sent back, we will trigger a thread which will add this response to the google sheet and if failed then store this in file.
    2. Next time when we will recieve the addResponse request, we will add the response with failed responses to the sheet and remove them from failed file.
    3. When user will click on get the sheet, we will again trigger a thread which will check for responses from file which were not synced to the sheets and add them.

  ### Pros/Cons
    1. We dont need to wait for the thread to complete to send back teh successful response.
    2. Can run into problms like Deadlocks, race condition and heavy system usage for large number of request. Although can be prevented using threadpools and queuing the request.
    

### Usage
AddResponse(Request)-->Adds the response to db, triggers thread and sends back successful message.-->AddResponseToSheets(request)--> Check for failed response and adds to sheets-->if failed adds cuurent reponse also to failed response.
getUrl(Request)-->Triggers a thread and send back the url--> Check for failed response and adds to sheets-->
<img src="https://github.com/Himanshukaushik303/atlan/blob/master/api/static/getSheet.png" width="100%" height="50%">
<img src="https://github.com/Himanshukaushik303/atlan/blob/master/api/static/ResponseData.png" width="100%" height="50%">




## Task 4
Send an SMS to user,

### Usage
1. I have used Twillio library to send the SMS. We can use any of the SMS service, twillio is reliable.
2. I have exposed this api to show the working and taken input of test message.
3. But we also add this method inside the thread which executes after adding the response successfully in the database.
3. We can then send the SMS with the information from the response object like first name and mobile number.
<img src="https://github.com/Himanshukaushik303/atlan/blob/master/api/static/sms.jpg" width="40%" height="10%">


## Thank you


