from flask import request, jsonify
import requests
import json
from database import insert_hpoo_logs

API_HOST = "http://reqres.in"


def proxy_get_call(run_id=None):
    headers = {k: v for k, v in request.headers if k.lower() != "host"}
    headers["Accept"] = "application/json"
    oo_run_id = run_id
    payload = jsonify()
    res = requests.get(
        # API_HOST + request.full_path, 
        "https://reqres.in/api/unknown/2",
        headers=headers
    )
    oo_response = res.json()
    insert_hpoo_logs({
        "oo_run_id": oo_run_id,
        "http_method": "GET",
        "request_url": request.full_path,
        "payload": payload,
        "query": request.query_string.decode(),
        "response": oo_response,
        "upstream_application_id": 1,
    })
    return oo_response


def proxy_post_call(run_id=None):
    headers = {k: v for k, v in request.headers if k.lower() != "host"}
    headers["Accept"] = "application/json"
    oo_run_id = run_id
    data = request.get_data()
    payload = json.loads(data.decode())
    res = requests.post(
        "https://reqbin.com/echo/post/json",
        data=data,
        json=request.get_json(),
        headers=headers,
    )
    oo_response = res.json()
    insert_hpoo_logs({
        "oo_run_id": oo_run_id,
        "http_method": "POST",
        "request_url": request.full_path,
        "payload": payload,
        "query": request.query_string.decode(),
        "response": oo_response,
        "upstream_application_id": 1,
    })
    return oo_response
