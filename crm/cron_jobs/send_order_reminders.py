#!/usr/bin/env python3

import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE = "/tmp/order_reminders_log.txt"
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"


def log_message(message: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} - {message}\n")


def main():
    transport = RequestsHTTPTransport(url=GRAPHQL_ENDPOINT, verify=False)
    client = Client(transport=transport, fetch_schema_from_transport=False)

    seven_days_ago = (
        (datetime.datetime.now() - datetime.timedelta(days=7)).date().isoformat()
    )

    query = gql(
        """
    query($dateSince: Date!) {
      orders(filter: {order_date_Gte: $dateSince}) {
        edges {
          node {
            id
            customer {
              email
            }
          }
        }
      }
    }
    """
    )

    params = {"dateSince": seven_days_ago}

    try:
        result = client.execute(query, variable_values=params)
        orders = result.get("orders", {}).get("edges", [])
        for edge in orders:
            order = edge.get("node", {})
            order_id = order.get("id")
            email = order.get("customer", {}).get("email", "no-email")
            log_message(f"Reminder: Order ID {order_id} for customer {email}")
        print("Order reminders processed!")
    except Exception as e:
        log_message(f"Error during GraphQL query: {e}")
        print("Failed to process order reminders.")


if __name__ == "__main__":
    main()
