import datetime
import os
from string import Template

from dateutil import tz, parser
from googleapiclient.discovery import build
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email


DEFAULT_GREETING = "Hallo $customer_name!"
DEFAULT_BODY1 = "Ihre Reservierung ist angekommen. Wir freuen uns auf Sie!"
DEFAULT_BODY2 = """
    Bis zu Ihrem Termin genießen Sie doch eine Tasse Kaffee bei Tims Kaffeebude.
    Nur 50m entfernt. Mit dieser Email erhalten Sie außerdem 15% Rabatt auf alle Bestellungen.
    Zeigen Sie diese Email einfach bei der Bestellung vor.
"""
DEFAULT_FAREWELL = "Bis dahin!"


def main(request):
    """Create new calendar API event

    we assume durations of 30min.
    """
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return '', 204, headers

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    request_json = request.get_json()
    try:
        calendar_id = request_json["account"]
        customer_mail = request_json["customer"]
        customer_name = request_json["name"]
        start_time = parser.isoparse(request_json["date"])

        email_content = {
            "greeting": request_json.get("email_greeting", DEFAULT_GREETING),
            "body1": request_json.get("email_body1", DEFAULT_BODY1),
            "body2": request_json.get("email_body2", DEFAULT_BODY2),
            "farewell": request_json.get("email_farewell", DEFAULT_FAREWELL),
        }
    except KeyError:
        return "Invalid request. Following fields are required: `account`, `customer`, `name`, `date`.", 400, headers

    service = build('calendar', 'v3', cache_discovery=False)

    # Call the Calendar API
    event = service.events().insert(
        calendarId=calendar_id,
        body={
            "summary": "Appointment",
            "start": {"dateTime": start_time.isoformat()},
            "end": {"dateTime": (start_time + datetime.timedelta(minutes=30)).isoformat()},
            "description": f"Gast: {customer_name} (<{customer_mail}>)",
        }
    ).execute()

    # send confirmation mail
    if event:
        sg = SendGridAPIClient(os.environ['EMAIL_API_KEY'])
        with open("email_template.html") as f:
            html_content = f.read()

        # substitute the custom content first
        for key, content in email_content.items():
            email_content[key] = Template(content).substitute(
                customer_name=customer_name,
            )

        # substitute the email with the content
        html_content = Template(html_content).substitute(
            start_time=start_time.strftime("%H:%M"),
            email_greeting=email_content["greeting"],
            email_body1=email_content["body1"],
            email_body2=email_content["body2"],
            email_farewell=email_content["farewell"],
        )

        message = Mail(
            to_emails=customer_mail,
            from_email=Email('ana_shopping@sabsch.com', "Ana Shopping Service"),
            subject="Ihr Termin wurde gebucht",
            html_content=html_content
        )

        try:
            sg.send(message)
        except HTTPError as e:
            return e.message, 500, headers

        return "", 200, headers
