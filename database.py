import psycopg2
import json
import os
from flask import jsonify

# Load configuration from the JSON file
with open("./python-flask/config.json", "r") as file:
    config = json.load(file)

# Database configuration
db_config_from_file = config["postgres"]


def get_db_connection():
    connection = psycopg2.connect(
        host=db_config_from_file["host"],
        port=db_config_from_file["port"],
        database=db_config_from_file["database"],
        user=db_config_from_file["user"],
        password=db_config_from_file["password"],
    )
    return connection


def read_from_db(query, params=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def write_to_db(query, params=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    cursor.close()
    conn.close()


def initialize_db_tables():
    write_to_db(query_create_table_upstream_applications)
    write_to_db(query_create_table_downstream_applications)
    write_to_db(query_create_table_upstream_request_response_logs)
    write_to_db(query_create_table_queue_request_logs)
    write_to_db(query_create_table_queue_response_logs)
    write_to_db(query_create_table_hpoo_logs)
    write_to_db(query_create_table_migrated_flows)
    write_to_db(query_create_table_executions)


def insert_hpoo_logs(params):
    oo_run_id = params["oo_run_id"] if params["oo_run_id"] is not None else 0
    http_method = params["http_method"] if params["http_method"] is not None else ""
    request_url = params["request_url"] if params["request_url"] is not None else ""
    payload = params["payload"] if params["payload"] is not None else jsonify()
    query = params["query"] if params["query"] is not None else ""
    response = params["response"] if params["response"] is not None else jsonify()
    upstream_application_id = (
        params["upstream_application_id"]
        if params["upstream_application_id"] is not None
        else 1
    )

    query = f"""
    INSERT INTO hpoo_logs (oo_run_id, http_method, request_url, payload, query, response, upstream_application_id)
    VALUES ({oo_run_id}, '{http_method}', '{request_url}', '{json.dumps(payload)}', '{query}', '{json.dumps(response)}', {upstream_application_id});
    """

    write_to_db(query)


query_create_table_upstream_applications = """
CREATE TABLE IF NOT EXISTS upstream_applications (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  secret VARCHAR(255)
);
"""

query_create_table_downstream_applications = """
CREATE TABLE IF NOT EXISTS downstream_applications (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  secret VARCHAR(255)
);
"""

query_create_table_upstream_request_response_logs = """
CREATE TABLE IF NOT EXISTS upstream_request_response_logs (
  id SERIAL PRIMARY KEY,
  http_method VARCHAR(255),
  request_url VARCHAR(255),
  payload JSON,
  query VARCHAR(255),
  response JSON,
  upstream_application_id INT,
  timestamp TIMESTAMP(3) WITH TIME ZONE NOT NULL DEFAULT NOW()
);
"""

query_create_table_queue_request_logs = """
CREATE TABLE IF NOT EXISTS queue_request_logs (
  id SERIAL PRIMARY KEY,
  queue_message_name VARCHAR(255),
  payload JSON,
  upstream_application_id INT,
  timestamp TIMESTAMP(3) WITH TIME ZONE NOT NULL DEFAULT NOW()
);
"""

query_create_table_queue_response_logs = """
CREATE TABLE IF NOT EXISTS queue_response_logs (
  id SERIAL PRIMARY KEY,
  queue_message_name VARCHAR(255),
  payload JSON,
  status VARCHAR(64),
  timestamp TIMESTAMP(3) WITH TIME ZONE NOT NULL DEFAULT NOW()
);
"""

query_create_table_hpoo_logs = """
CREATE TABLE IF NOT EXISTS hpoo_logs (
  id SERIAL PRIMARY KEY,
  oo_run_id INT,
  http_method VARCHAR(255),
  request_url VARCHAR(255),
  payload JSON,
  query VARCHAR(255),
  response JSON,
  upstream_application_id INT,
  timestamp TIMESTAMP(3) WITH TIME ZONE NOT NULL DEFAULT NOW()
);
"""

query_create_table_migrated_flows = """
CREATE TABLE IF NOT EXISTS migrated_flows (
  id SERIAL PRIMARY KEY,
  flow_name VARCHAR(255),
  flow_uuid VARCHAR(255),
  facility VARCHAR(255)
);
"""

query_create_table_executions = """
CREATE TABLE IF NOT EXISTS executions (
  id SERIAL PRIMARY KEY,
  flow_name VARCHAR(255),
  downstream_application_id INT,
  execution_id VARCHAR(255),
  queue_message_payload JSON,
  facility_name VARCHAR(255),
  snt_code VARCHAR(255),
  event_id VARCHAR(255),
  current_action_id VARCHAR(255),
  server_name VARCHAR(255),
  customer_name VARCHAR(255),
  action_params_json JSON,
  res_server VARCHAR(255),
  res_port INT,
  status VARCHAR(255),
  trace_error VARCHAR(255),
  flow_output VARCHAR(255),
  flow_input VARCHAR(255),
  flow_vars VARCHAR(255),
  upstream_application_id INT,
  invoked_by_user VARCHAR(255),
  created_time TIMESTAMP(3) WITH TIME ZONE NOT NULL DEFAULT NOW(),
  updated_time TIMESTAMP(3) WITH TIME ZONE NOT NULL DEFAULT NOW()
);
"""
