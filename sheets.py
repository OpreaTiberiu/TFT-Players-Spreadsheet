import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


class Sheets:
    def __init__(self, sheet_id=""):
        self.creds = None
        self.sheet_id = sheet_id
        self.setup_creds()
        self.service = build("sheets", "v4", credentials=self.creds)

    def setup_creds(self):
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            self.creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("cred.json", SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(self.creds.to_json())

    def create_sheet(self, title="ro_players"):
        try:
            spreadsheet = {"properties": {"title": title}}
            sheet_service = self.service.spreadsheets()
            spreadsheet = sheet_service.create(
                body=spreadsheet, fields="spreadsheetId"
            ).execute()
            self.sheet_id = spreadsheet.get("spreadsheetId")
        except HttpError as err:
            print(err)

    def add_data(self, values=None):
        if not self.sheet_id or self.sheet_id == "":
            if not self.get_sheet_from_drive():
                self.create_sheet()
        try:
            body = {"values": values}
            max_row = len(values)
            max_col = chr(ord("@") + len(values[0]))

            result = (
                self.service.spreadsheets()
                .values()
                .append(
                    spreadsheetId=self.sheet_id,
                    range=f"A1:{max_col}{max_row}",
                    valueInputOption="USER_ENTERED",
                    body=body,
                )
                .execute()
            )
            print(f"{(result.get('updates').get('updatedCells'))} cells appended.")
            return result

        except HttpError as error:
            print(f"An error occurred: {error}")
            return error

    def get_sheet_from_drive(self, name="ro_players"):
        try:
            drive_service = build("drive", "v3", credentials=self.creds)
            # Call the Drive v3 API
            results = drive_service.files().list(pageSize=100, fields="*").execute()
            items = results.get("files", [])

            if not items:
                print("No files found.")
                return False
            for item in items:
                if item["name"] == name:
                    self.sheet_id = item["id"]
                    return item
            return False
        except HttpError as error:
            print(f"An error occurred: {error}")
            return False

    def get_values(self, range_name="A:Z"):
        # for multiple sheets https://stackoverflow.com/questions/38245714/get-list-of-sheets-and-latest-sheet-in-google-spreadsheet-api-v4-in-python
        # for formatting https://developers.google.com/sheets/api/samples/conditional-formatting#:~:text=The%20Google%20Sheets%20API%20allows,be%20controlled%20through%20conditional%20formatting.
        try:
            result = (
                self.service.spreadsheets()
                .values()
                .get(
                    spreadsheetId=self.sheet_id,
                    range=range_name,
                    valueRenderOption="UNFORMATTED_VALUE",
                )
                .execute()
            )
            rows = result.get("values", [])
            print(f"{len(rows)} rows retrieved")
            return result
        except HttpError as error:
            print(f"An error occurred: {error}")
            return error

    def update(self, values):
        try:
            body = {"values": values}
            max_row = len(values)
            max_col = chr(ord("@") + len(values[0]))
            result = (
                self.service.spreadsheets()
                .values()
                .update(
                    spreadsheetId=self.sheet_id,
                    range=f"A1:{max_col}{max_row}",
                    valueInputOption="USER_ENTERED",
                    body=body,
                )
                .execute()
            )
            print(f"{result.get('updatedCells')} cells updated.")
            return result
        except HttpError as error:
            print(f"An error occurred: {error}")
            return error
