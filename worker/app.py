import json

from google.cloud import pubsub_v1

from general_queue import convert_file

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path("misw4204-grupo9-docker", "converter-sub")


def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    print(f"Received {message}.")

    data = json.loads(message.data.decode('utf-8'))
    convert_file(task=data["task"], file=data["file"], user=data["user"])

    message.ack()


streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

with subscriber:
    try:
        streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()  # Trigger the shutdown.
        streaming_pull_future.result()  # Block until the shutdown is complete.
