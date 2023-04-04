from locust import HttpUser, between, task, events
from locust.runners import MasterRunner
from locust.clients import ResponseContextManager



class APIUser(HttpUser):
    wait_time = between(1, 5)

    # Put your stress tests here.
    # See https://docs.locust.io/en/stable/writing-a-locustfile.html for help.
    # TODO
    @task
    def test_index(self):
        self.client.get("http://localhost/")

    @task
    def test_predict(self):
        files = [("file", ("dog.jpeg", open("dog.jpeg", "rb"), "image/jpeg"))]
        headers = {}
        payload = {}
        self.client.post(
            "http://localhost/predict",
            headers=headers,
            data=payload,
            files=files,
        )

@events.init.add_listener
def on_locust_init(environment, **_kwargs):
    if isinstance(environment.runner, MasterRunner):
        # Initialize a CSV file to store results
        with open('results.csv', 'w') as file:
            file.write('Timestamp, Method, Name, Response Time, Status Code\n')


@events.request.add_listener
def on_request_success(request_type, name, response_time, response_length, **_kwargs):
    if isinstance(request_type, ResponseContextManager):
        # Write successful requests to the CSV file
        with open('results.csv', 'a') as file:
            timestamp = int(round(response_time * 1000))
            status_code = request_type.status_code
            file.write(f'{timestamp},{request_type.method},{name},{response_time},{status_code}\n')


@events.request.add_listener
def on_request_failure(request_type, name, response_time, exception, **_kwargs):
    if isinstance(request_type, ResponseContextManager):
        # Write failed requests to the CSV file
        with open('results.csv', 'a') as file:
            timestamp = int(round(response_time * 1000))
            status_code = exception.response.status_code if exception.response else 'N/A'
            file.write(f'{timestamp},{request_type.method},{name},{response_time},{status_code}\n')