import boto3
from flask import Flask, render_template, request
from botocore.exceptions import ClientError
app = Flask(__name__)


def email_sender(name, book, author, message):
    SENDER = "cristiano.balducci@gmail.com"
    RECIPIENT = "cristiano.balducci@gmail.com"
    SUBJECT = "Suggestion from " + name

    BODY_TEXT = book + " by " + author + "\n\n" + message
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


def write_suggestion(book, author):
    return True


def get_all_suggestions():
    AWS_REGION = "eu-west-1"
    client = boto3.client('dynamodb', region_name=AWS_REGION)
    response = client.scan(TableName='suggestions')
    return response['Items']


@app.route('/')
def render_static():
    return render_template('index.html')


@app.route('/listing', methods=['GET', 'POST'])
def render_listing():
    #write_suggestion(request.form.get('Author'),
    #                 request.form.get('Book'))
    listing = get_all_suggestions()
    return render_template('listing.html', listing=listing)


@app.route('/thankyou', methods=['GET', 'POST'])
def render_thanks():
    email_sender(request.form.get('Name'),
                 request.form.get('Book'),
                 request.form.get('Author'),
                 request.form.get('Message'))
    return render_template('listing.html')


if __name__ == "__main__":
    app.run()
