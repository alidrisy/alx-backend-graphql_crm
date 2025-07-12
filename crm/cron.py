import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import requests


def log_crm_heartbeat():
    now = datetime.datetime.now()
    timestamp = now.strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"
    log_path = "/tmp/crm_heartbeat_log.txt"
    error_log_path = "/tmp/crm_error_log.txt"

    try:
        with open(log_path, "a", encoding="utf-8") as file:
            file.write(message)
    except Exception as e:
        with open(error_log_path, "a", encoding="utf-8") as err_file:
            err_file.write(f"{timestamp} Error writing to log file: {e}\n")

    try:
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            verify=False,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=False)

        query = gql(
            """
            query {
                hello
            }
        """
        )

        response = client.execute(query)
        print(f"GraphQL 'hello' field response: {response.get('hello')}")
    except Exception as e:
        with open(error_log_path, "a", encoding="utf-8") as err_file:
            err_file.write(f"{timestamp} GraphQL endpoint check failed: {e}\n")


def update_low_stock():
    graphql_url = "http://localhost:8000/graphql"

    mutation = """
    mutation {
      updateLowStockProducts {
        products {
          id
          name
          stock
        }
        message
      }
    }
    """

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(graphql_url, json={"query": mutation}, headers=headers)
        response.raise_for_status()
        data = response.json()

        updated_products = data["data"]["updateLowStockProducts"]["products"]
        message = data["data"]["updateLowStockProducts"]["message"]

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_path = "/tmp/low_stock_updates_log.txt"

        with open(log_path, "a", encoding="utf-8") as log_file:
            log_file.write(f"{timestamp} - {message}\n")
            for product in updated_products:
                log_file.write(
                    f"Updated product: {product['name']} - New stock: {product['stock']}\n"
                )
            log_file.write("\n")

    except Exception as e:
        with open("/tmp/low_stock_updates_log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(
                f"Error updating stock at {datetime.datetime.now()}: {str(e)}\n\n"
            )
