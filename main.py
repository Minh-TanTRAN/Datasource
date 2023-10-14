from flask import Flask, request
import logging
import requests
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest
import os



app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)


prefix_google = """
    <!-- Google tag (gtag.js) -->
    <script async
    src="https://www.googletagmanager.com/gtag/js?id=G-P8H5EB609C"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', ' G-P8H5EB609C');
    </script>
    """

@app.route("/")
def hello_world():
 return prefix_google + "Hello World"

@app.route("/logger", methods=["GET", "POST"])
def logger():
    # print a message in Python
    app.logger.info("Connexion Logger")

    if request.method == 'POST':
        # take the text in the text box
        text_from_textbox = request.form['textbox']

        # print a message in the browser console with the text from the text box
        browser_log = f"""
        <script>
            console.log('Connexion Logger');
            console.log('Boîte de texte : {text_from_textbox}');
        </script>
        """

    else:
    # print a message in the browser console
        browser_log = """
        <script>
            console.log('Connexion Logger');
        </script>
        """

    # Formulaire HTML avec une boîte de texte
    textbox_form = """
    <form method="POST">
        <label for="textbox">Text Box :</label><br>
        <input type="text" id="textbox" name="textbox"><br><br>
        <input type="submit" value="Soumettre">
    </form>
    """
    # Bouton pour effectuer une requête Google
    google_button = """
    <form method="GET" action="/perform_google_request">
        <input type="submit" value="Effectuer la requête Google">
    </form>
    """
    # Bouton pour effectuer une requête Google Analytics
    google_analytics_button = """
    <form method="GET" action="/perform_google_analytics_request">
        <input type="submit" value="Effectuer la requête Google analytics">
    </form>
    """

    # Bouton pour récupérer le nombre de visiteurs
    nombre_visiteurs_button = """
    <form method="GET" action="/fetch-google-analytics-data">
        <input type="submit" value="Récupérer le nombre de visiteurs">
    </form>
    """
    
    
    return "logger page" + browser_log + textbox_form + google_button + google_analytics_button  + nombre_visiteurs_button

@app.route("/perform_google_request", methods=["GET", "POST"])
def perform_google_request():
    # On obtient la réponse de Google
    response = requests.get("https://www.google.com")
    # On obtient les cookies si la réponse est 200
    if response.status_code == 200:
        response_message = response.cookies.get_dict()
    else:
        response_message = "Request to Google failed."

    return str(response_message)

@app.route("/perform_google_analytics_request", methods=["GET", "POST"])
def perform_google_analytics_request():
    # On obtient la réponse de Google Analytics
    response = requests.get("https://analytics.google.com/analytics/web/#/p408045968/reports/intelligenthome")
    
    # On obtient les cookies si la réponse est 200
    if response.status_code == 200:
        response_message = response.cookies.get_dict()
    else:
        response_message = "Request to Google analytics failed."

    return str(response_message)

@app.route('/fetch-google-analytics-data', methods=['GET'])
def fetch_google_analytics_data():

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'form.json'
    PROPERTY_GA4_ID = 'G-P8H5EB609C'
    starting_date = "10daysAgo"
    ending_date = "yesterday"

    client = BetaAnalyticsDataClient()

    # function qui retourne la requête de l'API Google Analytics
    def get_visitor_count(client, property_id):
        request = RunReportRequest(
            property=f"properties/{property_id}",
            date_ranges=[{"start_date": starting_date, "end_date": ending_date}],
            metrics=[{"name": "activeUsers"}]
        )
        response = client.run_report(request)
        return response

    # récupère nombre visiteurs actifs
    response = get_visitor_count(client, PROPERTY_GA4_ID)

    # affiche nombre visiteurs actifs
    if response and response.row_count > 0:
        metric_value = response.rows[0].metric_values[0].value
    else:
        metric_value = "N/A"

    return f'Number of active visitors : {metric_value}'

if __name__ == '_main_':
    app.run(debug=True)
