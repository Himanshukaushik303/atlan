import sys, os, pathlib

sys.path.insert(0, os.path.abspath(".."))
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render
from googletrans import LANGUAGES
from google.cloud import translate_v2 as translate
from django.forms.models import model_to_dict
import gspread
import json
from .models import Responses
from twilio.rest import Client
import logging
import threading


def home(request):
    return render(request, "api/home.html")


def responseForm(request):
    return render(request, "api/addResponse.html")


def slangForm(request):
    supported_languages = [[code, name.capitalize] for code, name in LANGUAGES.items()]
    return render(
        request, "api/getSlang.html", context={"languages": supported_languages}
    )


def smsForm(request):
    return render(request, "api/sendSMS.html")


def googleSheetUrl(request):
    return render(request, "api/getUrl.html")


@api_view(["POST"])
def getSlang(request):
    data = request.data
    logging.info(f"Received request data for getSlang api: {data}")
    try:
        translate_client = translate.Client()
        result = translate_client.translate(
            data["text"], target_language=data["language"]
        )
        translated_text = result["translatedText"]
        logging.info(
            "Text '{}' translated to '{}' in language '{}'".format(
                data["text"], translated_text, data["language"]
            )
        )
        return Response(translated_text)
    except Exception as e:
        logging.error("An error occurred during translation: {}".format(str(e)))
        error_message = "An error occurred during translation: {}".format(str(e))
        return Response(error_message, status=500)


def validateRecords(request):
    data = request.data
    logging.info(f"Received request data for validation: {data}")
    monthly_income = int(data.get("income"))
    monthly_saving = int(data.get("saving"))

    try:
        if monthly_income is None or monthly_saving is None:
            raise ValueError("Both 'income' and 'saving' fields are required.")
        if monthly_income < monthly_saving:
            raise ValueError(
                "INVALID RECORD FOUND WITH MONTHLY INCOME LESS THAN MONTHLY SAVING"
            )
        return Response(data="Record is Valid", status=200, exception=False)
    except ValueError as ve:
        logging.error(f"Validation Error: {ve}")
        return Response(data=str(ve), status=400, exception=True)
    except Exception as e:
        logging.exception(f"Unexpected Error: {e}")
        return Response(
            data="An unexpected error occurred.", status=500, exception=True
        )


@api_view(["GET"])
def getUrl(request):
    thread = threading.Thread(target=addResponseToSheets, args=([],))
    thread.start()
    logging.info(f"Received request data for getting sheet url")
    try:
        sheet_id = os.environ.get("SHEET_ID")
        if not sheet_id:
            createSheet()
            sheet_id = os.environ.get("SHEET_ID")
        sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}"
        return Response(sheet_url)
    except Exception as e:
        logging.error(
            "An error occurred while fetching the Google Sheets URL: {}".format(str(e))
        )
        error_message = "An error occurred while fetching the Google Sheets URL. Please try again later."
        return Response(error_message, status=500)


@api_view(["POST"])
def sendSMS(request):
    data = request.data
    logging.info(f"Received request data for sendSMS api: {data}")
    try:
        client = getTwiilioClient()
        message = client.messages.create(
            body=data["message"],
            from_="+14326662078",
            to=data["mob"],
        )
        logging.info("Successfully sent message: {}".format(message.sid))
        return Response("Successfully sent message to the user.")
    except Exception as e:
        logging.error("An error occurred while sending the SMS: {}".format(str(e)))
        error_message = (
            "An error occurred while sending the SMS. Please try again later."
        )
        return Response(error_message, status=500)


@api_view(["POST"])
def addResponse(request):
    data = request.data
    logging.info(f"Received request data for addResponse api: {data}")
    try:
        validateRecordResponse = validateRecords(request)
        isResponseValid = True if validateRecordResponse.status_code == 200 else False
        if isResponseValid:
            response = Responses.objects.create(
                first_Name=data["fname"],
                last_Name=data["lname"],
                mobile_No=data["mob"],
                email_Id=data["email"],
                monthly_Saving=data["saving"],
                monthly_Income=data["income"],
            )
            logging.info("Successfully added response: {}".format(response.id))
            response_data = list(model_to_dict(response).values())
            thread = threading.Thread(target=addResponseToSheets, args=(response_data,))
            thread.start()
            return Response(data="Successfully Added Response")
        return Response(data="Response is Invalid.", status=400)
    except Exception as e:
        logging.error("An error occurred while adding a response: {}".format(str(e)))
        error_message = (
            "An error occurred while adding a response. Please try again later."
        )
        return Response(error_message, status=500)


def addResponseToSheets(request):
    unsynced_ids = get_unsynced_ids_from_backlog()
    unsynced_responses = [
        list(model_to_dict(response).values())
        for response in Responses.objects.filter(id__in=unsynced_ids)
    ]
    unsynced_responses.append(request)
    logging.info(f"Received request data for add to sheets : {unsynced_responses}")
    try:
        sheet_id = os.environ.get("SHEET_ID")
        if not sheet_id:
            createSheet()
            sheet_id = os.environ.get("SHEET_ID")
        gc = getGoogleSheetsClient()
        sheet = gc.open_by_key(sheet_id).sheet1
        sheet.append_rows(unsynced_responses)
        with open("api/BacklogIDs.txt", "w") as backlog_file:
            backlog_file.truncate(0)
        logging.info("Successfully added response to Google Sheets.")
    except Exception as e:
        logging.error(
            "An error occurred while adding a response to Google Sheets: {}".format(
                str(e)
            )
        )
        if request:
            save_unsynced_ids_to_backlog(request[0])
        raise


def createSheet():
    try:
        gc = getGoogleSheetsClient()
        new_sheet_title = "Response Data"
        new_sheet = gc.create(new_sheet_title)
        new_sheet.share("kaushikhimanshu303@gmail.com", perm_type="user", role="writer")
        sheet_id = str(new_sheet.id)
        with open(".env", "a") as f:
            f.write(f"SHEET_ID={sheet_id}\n")
        os.environ["SHEET_ID"] = sheet_id
        sheet = gc.open_by_key(sheet_id).sheet1
        model_columns = Responses._meta.get_fields(include_hidden=False)
        column_names = [field.name for field in model_columns]
        sheet.append_row(column_names)
        logging.info("Successfully created a new Google Sheets spreadsheet.")
    except Exception as e:
        logging.error(
            "An error occurred while creating a new Google Sheets spreadsheet: {}".format(
                str(e)
            )
        )
        raise


def getGoogleSheetsClient():
    try:
        credentials_file = os.path.join(
            pathlib.Path(__file__).resolve().parent.parent, "creds.json"
        )
        with open(credentials_file, "r") as f:
            credentials = json.load(f)
        client = gspread.service_account_from_dict(credentials)
        logging.info("Successfully created Google Sheets client.")
        return client
    except Exception as e:
        logging.error(
            "An error occurred while creating Google Sheets client: {}".format(str(e))
        )
        raise


def getTwiilioClient():
    try:
        account_sid = os.environ["ACCOUNT_SID"]
        auth_token = os.environ["AUTH_TOKEN"]
        client = Client(account_sid, auth_token)
        logging.info("Successfully created Twilio client.")
        return client
    except KeyError as e:
        logging.error(
            "KeyError: {} is not found in environment variables.".format(str(e))
        )
        raise
    except Exception as e:
        logging.error(
            "An error occurred while creating Twilio client: {}".format(str(e))
        )
        raise


def save_unsynced_ids_to_backlog(unsynced_ids):
    txt_filename = "BacklogIDs.txt"
    try:
        with open(os.path.join("api", txt_filename), "a") as txtfile:
            for unsynced_id in unsynced_ids:
                txtfile.write(f"{unsynced_id}\n")
        logging.info("Unsynced IDs saved to the backlog successfully.")
    except Exception as e:
        logging.error(f"Error while saving unsynced IDs to the backlog: {e}")


def get_unsynced_ids_from_backlog():
    unsynced_ids = []
    txt_filename = "BacklogIDs.txt"
    try:
        with open(os.path.join("api", txt_filename), "r") as txtfile:
            for line in txtfile:
                unsynced_ids.append(int(line.strip()))
        logging.info("Unsynced IDs retrieved from the backlog successfully.")
    except FileNotFoundError:
        logging.info("Backlog file not found. Returning an empty list.")
    except Exception as e:
        logging.error(f"Error while retrieving unsynced IDs from the backlog: {e}")
    return unsynced_ids
