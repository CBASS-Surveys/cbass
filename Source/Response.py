class Response:
    response_id = None
    response_value = None
    response_description = None

    def __init__(self, response_id, response_value, response_description):
        self.response_id = response_id
        self.response_value = response_value
        self.response_description = response_description
