import os

from dotenv import load_dotenv

load_dotenv(override=True)

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
SENDGRID_FROM_EMAIL = os.environ.get("SENDGRID_FROM_EMAIL")
SENDGRID_TO_EMAIL = os.environ.get("SENDGRID_TO_EMAIL")


def send_contact_email(visitor_email: str, visitor_name: str = "", message: str = "") -> dict:
    if not all([SENDGRID_API_KEY, SENDGRID_FROM_EMAIL, SENDGRID_TO_EMAIL]):
        print("⚠️  SendGrid not configured.")
        return {"sent": False, "reason": "SendGrid not configured"}
    try:
        import sendgrid
        from sendgrid.helpers.mail import Content, Email, Mail, To

        lines = [
            "<p>A visitor wants to connect via the resume chat assistant.</p>",
            f"<p><strong>Email:</strong> {visitor_email}</p>",
        ]
        if visitor_name:
            lines.insert(1, f"<p><strong>Name:</strong> {visitor_name}</p>")
        if message:
            lines.append(f"<p><strong>Message:</strong> {message}</p>")

        sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
        mail = Mail(
            Email(SENDGRID_FROM_EMAIL), To(SENDGRID_TO_EMAIL),
            "New Contact Request – Resume Chat",
            Content("text/html", "\n".join(lines)),
        ).get()
        resp = sg.client.mail.send.post(request_body=mail)
        success = 200 <= resp.status_code < 300
        print(f"SendGrid response: {resp.status_code}")
        return {"sent": success}
    except Exception as exc:
        print(f"Email error: {exc}")
        return {"sent": False, "reason": str(exc)}


send_contact_email_json = {
    "name": "send_contact_email",
    "description": (
        "Send a contact request email to Sruthy Plakkat on behalf of the visitor. "
        "Use this tool when the visitor's question cannot be answered from the resume AND "
        "their email address is known. Also use it when the visitor explicitly asks to get "
        "in touch or have their details forwarded. Do NOT call this if no email is available."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "visitor_email": {
                "type": "string",
                "description": "The visitor's email address.",
            },
            "visitor_name": {
                "type": "string",
                "description": "The visitor's name, if provided.",
            },
            "message": {
                "type": "string",
                "description": "The question or message to forward to Sruthy.",
            },
        },
        "required": ["visitor_email"],
        "additionalProperties": False,
    },
}

tools = [{"type": "function", "function": send_contact_email_json}]
