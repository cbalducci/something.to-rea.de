import boto3
from flask import Flask, render_template, request
from botocore.exceptions import ClientError
app = Flask(__name__)


def email_sender(name, book, author):
    SENDER = "cristiano.balducci@gmail.com"
    RECIPIENT = "cristiano.balducci@gmail.com"
    SUBJECT = "Suggestion from " + name

    BODY_TEXT = book + " by " + author
    AWS_REGION = "eu-west-1"
    CHARSET = "UTF-8"
    client = boto3.client('ses', region_name=AWS_REGION)
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])


@app.route('/')
def render_static():
    return render_template('index.html')


@app.route('/thankyou', methods=['GET', 'POST'])
def render_thanks():
    email_sender(request.form.get('Name'),
                 request.form.get('Book'),
                 request.form.get('Author'))
    return render_template('thankyou.html')


if __name__ == "__main__":
    app.run()
