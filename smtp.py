import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def AnalysisEmail(SendTo):

    # Define email variables
    sender_email = "admin@bestlinehosting.com"
    receiver_email = SendTo
    password = "Lahore-123"
    subject = "Analysis Report"
    body = "Hi,\n This is your required analysis file attached here with."

    # Create a multipart email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # Attach a file (make sure the file exists)
    attachment_filename = 'SEOAnalysis.txt'
    with open(attachment_filename, 'rb') as file:
        attach = MIMEApplication(file.read(), _subtype='txt')
        attach.add_header('Content-Disposition', 'attachment', filename=attachment_filename)
        msg.attach(attach)

    # Sending the email
    with smtplib.SMTP('mail.bestlinehosting.com', 587) as server:
        server.starttls()  # Secure the connection
        server.login(sender_email, password)
        server.send_message(msg)

    print("Email sent successfully with attachment.")


