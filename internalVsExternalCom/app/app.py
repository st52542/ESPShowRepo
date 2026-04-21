from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def run_query(host: str, port: int, application_name: str):
    conn = psycopg2.connect(
        host=host,
        port=port,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        application_name=application_name,
        connect_timeout=3
    )

    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    current_timestamp AS db_time,
                    current_database() AS db_name,
                    current_user AS db_user,
                    inet_client_addr() AS client_addr,
                    inet_client_port() AS client_port,
                    inet_server_addr() AS server_addr,
                    inet_server_port() AS server_port,
                    current_setting('application_name') AS application_name
            """)
            row = cur.fetchone()

            return {
                "db_time": str(row[0]),
                "db_name": row[1],
                "db_user": row[2],
                "client_addr": str(row[3]) if row[3] is not None else None,
                "client_port": row[4],
                "server_addr": str(row[5]) if row[5] is not None else None,
                "server_port": row[6],
                "application_name": row[7]
            }
    finally:
        conn.close()


@app.get("/internal")
def internal():
    try:
        result = run_query(
            host="db",
            port=5432,
            application_name="internal_call"
        )

        return jsonify({
            "status": "ok",
            "type": "internal communication",
            "route": "app -> db:5432",
            "db_result": result
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "type": "internal communication",
            "route": "app -> db:5432",
            "message": str(e)
        }), 500


@app.get("/external-host")
def external_host():
    try:
        result = run_query(
            host="host.docker.internal",
            port=5432,
            application_name="external_call_via_host"
        )

        return jsonify({
            "status": "ok",
            "type": "external communication via host",
            "route": "app -> host.docker.internal:5432 -> db",
            "db_result": result
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "type": "external communication via host",
            "route": "app -> host.docker.internal:5432 -> db",
            "message": str(e)
        }), 500


@app.get("/external-localhost")
def external_localhost():
    try:
        result = run_query(
            host="localhost",
            port=5432,
            application_name="external_call_via_localhost"
        )

        return jsonify({
            "status": "ok",
            "type": "external communication via localhost",
            "route": "app -> localhost:5432 -> db",
            "db_result": result,
            "note": "Tohle vyjde jen pokud by PostgreSQL bezela primo uvnitr app containeru, nebo by app bezela v host network"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "type": "external communication via localhost",
            "route": "app -> localhost:5432 -> db",
            "message": str(e),
            "note": "Tohle je ocekavane. Uvnitr containeru localhost znamena tento app container, ne host machine"
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)