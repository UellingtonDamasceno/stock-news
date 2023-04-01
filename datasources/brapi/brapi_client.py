import httpx


class BrapiClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_quote_list(self):
        return self.__get_data("api/quote/list")

    def __get_data(self, endpoint):
        with httpx.Client() as client:
            response = client.get(f"{self.base_url}/{endpoint}")
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(
                    f"Erro ao fazer requisição GET em {self.base_url}/{endpoint}. Status code: {response.status_code}")
