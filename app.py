from flask import Flask, jsonify, request
from flask import render_template
from services.hashtag_analysis_consumer import Consumer

app = Flask(__name__)
labels = []
values = []

consumer = Consumer()

@app.route("/hashtags")
def get_chart_page():
    global labels, values
    return render_template('hashtag_chart.html', values=values, labels=labels)


@app.route('/hashtags/refresh')
def refresh_graph_data():
    global labels, values
    #print("labels now: " + str(labels))
    #print("data now: " + str(values))
    return jsonify(sLabel=labels, sData=values)


@app.route('/hashtags', methods=['POST'])
def update_data():
    update_request = request.get_json()

    global labels, values
    if not update_request:
        return "error", 400

    hashtags = []
    counts = []
    for js_value in update_request:
        hashtags.append(js_value['hashtag'])
        counts.append(js_value['count'])

    labels = hashtags
    values = counts

    #print("labels received: " + str(labels))
    #print("data received: " + str(values))
    return "success", 201


if __name__ == "__main__":
    consumer.start()
    #app.run(host='localhost', port=9001)


