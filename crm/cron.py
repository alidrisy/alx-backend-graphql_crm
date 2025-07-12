import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


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
    now = datetime.datetime.now()
    timestamp = now.strftime("%d/%m/%Y-%H:%M:%S")
    error_log_path = "/tmp/update_low_stock_error.txt"

    try:
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            verify=False,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=False)

        mutation = gql(
            """
            mutation {
                updateLowStockProducts {
                    success
                    message
                    errors
                    products {
                        id
                        name
                        stock
                        price
                    }
                }
            }
            """
        )

        response = client.execute(mutation)
        data = response.get("updateLowStockProducts")
        print(f"Success: {data.get('success')}")
        print(f"Message: {data.get('message')}")
        print(f"Errors: {data.get('errors')}")
        print("Updated Products:")
        for product in data.get("products", []):
            print(f"- {product['name']} (Stock: {product['stock']})")

    except Exception as e:
        with open(error_log_path, "a", encoding="utf-8") as err_file:
            err_file.write(f"{timestamp} GraphQL mutation failed: {e}\n")
