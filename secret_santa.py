import pandas as pd
import random
import smtplib
from email.message import EmailMessage


def data_retriever(csv_path):
    csv_reader = pd.read_csv(csv_path)
    df = pd.DataFrame(csv_reader)

    # sort data
    df = df[['Email address', 'Name', 'Wishlist']]
    df = df.rename(columns={'Email address': 'email', 'Name': 'name', 'Wishlist': 'wishlist'})

    # make data dictionary
    participants = {}
    for _, row in df.iterrows():
        participants[row['email']] = {
            'name': row['name'],
            'wishlist': row['wishlist']
        }

    return participants


def secretsanta(participants):
    # Extract emails and shuffle data order
    emails = list(participants.keys())
    random.shuffle(emails)

    matches = {}

    # Pair each email with the next one (send in order after shuffling the data to randomize the pairs)
    for i in range(len(emails)):
        giver_email = emails[i]
        receiver_email = emails[(i + 1) % len(emails)]

        matches[giver_email] = {
            'giver': participants[giver_email]['name'],
            'receiver': participants[receiver_email]['name'],
            'wishlist': participants[receiver_email]['wishlist']
        }

    return matches


def email_sender(matches, smtp_server, smtp_port, sender_email, sender_pass):
    # set up SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # secure connection
        server.login(sender_email, sender_pass)

        for giver_email, details in matches.items():
            msg = EmailMessage()
            msg['Subject'] = "Secret Santa"
            msg['From'] = sender_email
            msg['To'] = giver_email

            # email body
            email_body = f"""
            Hello {details['giver']}!

            It's Secret Santa time! 

            You have been matched with: {details['receiver']}

            Wishlist: 
            {details['wishlist']}
            """

            msg.set_content(email_body)

            # Send the email
            server.send_message(msg)
            print(f"Email sent to {giver_email}")


if __name__ == "__main__":
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # TLS port; SLS port -> 465
    sender_email = "EMAIL ADDRESS"
    sender_password = "SENDER APP PASSWORD FROM GOOGLE ACCOUNT"

    # use google form to collect data and download data in csv file format
    ss_data = data_retriever("email/name/and/wishlist/csv/file/path")
    matches = secretsanta(ss_data)

    # debug print
    # print(matches)

    # Send emails to participants
    email_sender(matches, smtp_server, smtp_port, sender_email, sender_password)