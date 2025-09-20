import atexit

from flask import (
    Flask,
    jsonify,
    make_response,
    render_template,
    request,
)
from flask_cors import CORS

from blueprints.api import api
from blueprints.contact import contact
from blueprints.docs import docs
from blueprints.limiter import limiter
from blueprints.seo import seo
from blueprints.stats import stats
from blueprints.url_shortener import url_shortener
from blueprints.redirector import url_redirector
from utils.mongo_utils import client

app = Flask(__name__)
CORS(app)
limiter.init_app(app)

app.register_blueprint(url_shortener)
app.register_blueprint(url_redirector)
app.register_blueprint(docs)
app.register_blueprint(seo)
app.register_blueprint(contact)
app.register_blueprint(api)
app.register_blueprint(stats)


@app.after_request
def add_security_headers(response):
    response.headers["Content-Security-Policy"] = "default-src 'self'; img-src *; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline' https://hcaptcha.com https://*.hcaptcha.com;"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response


@app.errorhandler(404)
def page_not_found(error):
    return (
        render_template(
            "error.html",
            error_code="404",
            error_message="URL NOT FOUND!",
            host_url=request.host_url,
        ),
        404,
    )


@app.errorhandler(429)
def ratelimit_handler(e):
    if request.path == "/contact":
        return render_template(
            "contact.html",
            error=f"ratelimit exceeded {e.description}",
            host_url=request.host_url,
        )
    if request.path == "/report":
        return render_template(
            "report.html",
            error=f"ratelimit exceeded {e.description}",
            host_url=request.host_url,
        )
    return make_response(jsonify(error=f"ratelimit exceeded {e.description}"), 429)


@atexit.register
def cleanup():
    try:
        client.close()
        print("MongoDB connection closed successfully")
    except Exception as e:
        print(f"Error closing MongoDB connection: {e}")


if __name__ == "__main__":
    app.run(port=8000, use_reloader=True)
