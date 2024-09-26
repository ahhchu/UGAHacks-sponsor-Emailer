from flask import render_template, Flask, request, session, jsonify, stream_with_context, Response, url_for
from werkzeug.utils import secure_filename
import os
import pandas as pd
import clean  # Import the clean.py script
import email_sender


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
app = Flask(__name__)
app.secret_key = 'dev'
UPLOAD_FOLDER = 'data/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/authorize', methods=['POST'])
def authorize():
    flow = email_sender.get_flow(redirect_uri=url_for('oauth2callback', _external=True))
    authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
    session['state'] = state
    return jsonify({'authorization_url': authorization_url})  # Return the URL to the client for a popup or iframe


# Step 2: Handle OAuth2 callback and store credentials
@app.route('/oauth2callback')
def oauth2callback():
    state = session.get('state')
    flow = email_sender.get_flow(redirect_uri=url_for('oauth2callback', _external=True))
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials
    session['credentials'] = email_sender.credentials_to_dict(credentials)
    return jsonify({'status': 'success'})  # Let the frontend know the auth was successful

# Step 3: Send Emails asynchronously and track progress
@app.route('/send_emails', methods=['POST'])
def send_emails():
    if 'credentials' not in session:
        return jsonify({'error': 'User not authenticated'}), 401

    credentials_dict = session['credentials']
    credentials = Credentials(**credentials_dict)
    service = email_sender.build_gmail_service(credentials)

    # Trigger email sending in the background
    @stream_with_context
    def email_stream():
        # Read CSV data and send emails
        df = pd.read_csv('data/batch.csv')  # Make sure the CSV file is correctly placed
        total_emails = len(df)
        sent_count = 0

        for index, row in df.iterrows():
            personalized_subject = f"UGA Hacks and {row['Company Name']} Partnership"
            email_body = email_sender.EMAIL_TEMPLATE.format(name=row['First Name'], company_name=row['Company Name'])
            message = email_sender.create_message(email_sender.SENDER_EMAIL, row['Email'], personalized_subject, email_body)
            email_sender.send_email(service, message)
            sent_count += 1
            time.sleep(2)  # Simulate time delay

            # Send update back to the client
            yield f"data: {sent_count}/{total_emails}\n\n"  # SSE format

    return Response(email_stream(), content_type='text/event-stream')

@app.route('/exchange-code', methods=['POST'])
def exchange_code():
    print(request.json.get('code'),"This is exchange_code")
    return jsonify({'data':"test response"},600)
# Route to handle CSV file upload and cleaning via AJAX
@app.route('/clean-data', methods=['POST'])
def clean_data():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part found'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Try reading the CSV file
            df = pd.read_csv(file_path)

            # Check if the DataFrame is empty
            if df.empty:
                return jsonify({'error': 'The uploaded CSV file is empty'}), 400

            # Proceed with cleaning the data using the clean.py script
            cleaned_df = clean.clean(file_path)

            # Convert the cleaned DataFrame to JSON and return it
            cleaned_data_json = cleaned_df.to_dict(orient='records')
            print(cleaned_data_json)
            if len(cleaned_data_json) == 0:
                return jsonify({'error': 'The CSV file contains no new entries'}), 600
            return jsonify(cleaned_data_json)

    except pd.errors.EmptyDataError:
        return jsonify({'error': 'The CSV file is empty or improperly formatted'}), 400
    except Exception as e:
        return jsonify({'error': f'Error processing the file: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
