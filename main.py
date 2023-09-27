from flask import Flask

app = Flask(__name__)

@app.route('/')

def hello_world():
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
    return prefix_google + "Hello World"




@app.route("/")
def root():
    return "Hello from Space! 🚀"
    