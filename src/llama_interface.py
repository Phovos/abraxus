import asyncio
import json
import http.client
from urllib.parse import urlparse

class LlamaInterface:
    def __init__(self):
        self.session = None
        self.mock_mode = False

    async def __aenter__(self):
        try:
            self.session = http.client.HTTPConnection('localhost', 11434)
            self.session.connect()
        except ConnectionRefusedError:
            print("Warning: Unable to connect to Llama server. Switching to mock mode.")
            self.mock_mode = True
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session and not self.mock_mode:
            self.session.close()

    async def _query_llama(self, prompt):
        if self.mock_mode:
            return f"Mock response for: {prompt}"

        if not self.session:
            raise RuntimeError("LlamaInterface must be used as an async context manager")

        payload = json.dumps({
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        })
        headers = {
            'Content-Type': 'application/json'
        }

        try:
            self.session.request('POST', '/api/generate', body=payload, headers=headers)
            response = self.session.getresponse()

            if response.status == 200:
                result = json.loads(response.read().decode())
                return result['response']
            else:
                raise Exception(f"API request failed with status {response.status}")
        except Exception as e:
            print(f"Error querying Llama: {e}")
            return f"Error response for: {prompt}"

    async def extract_concepts(self, text):
        prompt = f"Extract key concepts from the following text:\n\n{text}\n\nConcepts:"
        response = await self._query_llama(prompt)
        return [concept.strip() for concept in response.split(',')]

    async def process(self, task):
        return await self._query_llama(task)