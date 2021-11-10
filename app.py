from os import error
from flask import Flask, render_template, request
from mbta_helper import find_stop_near

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/MBTA/", methods=["GET", "POST"])
def MBTA():
    if request.method == "POST":
        place_name = str(request.form["place_name"])
        MBTA_stop = find_stop_near(place_name)

        if MBTA_stop:
            return render_template(
                "MBTA_result.html",
                station_name = MBTA_stop[0],
                wheelchair_accessible = MBTA_stop[1],
            )
        else:
            return render_template("MBTA_address.html", error=True)
    return render_template("MBTA_address.html", error=None)


if __name__ == "__main__":
    app.run(debug=True)
