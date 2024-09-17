from flask import Flask, jsonify
from database import initialize_db_tables
from hpoo_proxy import proxy_get_call, proxy_post_call
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.config["JSON_JSONIFY_HTTP_ERRORS"] = True

initialize_db_tables()

@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return e
    res = {
        "code": 500,
        "errorType": "Internal Server Error",
        "errorMessage": e.message if hasattr(e, "message") else f"{e}",
    }
    return jsonify(res), 500


@app.route("/")
def basepath():
    return {
        "message": "You've called Ansible gateway REST api!",
    }


@app.route("/v1/executions")
def handle_get_executions():
    return proxy_get_call()


@app.route("/v1/executions", methods=["POST"])
def handle_post_executions():
    return proxy_post_call()


@app.route("/v1/executions/<csv_execution_ids>/summary")
def handle_get_executions_summary(csv_execution_ids):
    return proxy_get_call()


@app.route("/v1/executions/<execution_id>/execution-log")
def handle_get_execution_log(execution_id):
    return proxy_get_call(execution_id)


@app.route("/v1/executions/<execution_id>/steps")
def handle_get_execution_steps(execution_id):
    return proxy_get_call(execution_id)


@app.route("/v1/flows/library")
def handle_get_flows_library():
    return proxy_get_call()


if __name__ == "__main__":
    app.run(debug=True)
