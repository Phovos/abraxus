import asyncio

from .llama_interface import LlamaInterface


class SymbolicKernel:
    def __init__(self, kb_dir, output_dir, max_memory):
        self.kb_dir = kb_dir
        self.output_dir = output_dir
        self.max_memory = max_memory
        self.llama = None
        self.running = False
        self.knowledge_base = set()  # Simplified knowledge base as a set of concepts

    async def __aenter__(self):
        self.llama = await LlamaInterface().__aenter__()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.llama:
            await self.llama.__aexit__(exc_type, exc, tb)

    async def initialize(self):
        self.llama = await LlamaInterface().__aenter__()
        # We're not loading files for now, but you can add that functionality
        # later if needed
        self.running = True

    async def process_task(self, task):
        if not self.running:
            raise RuntimeError("Kernel is not initialized or has been stopped")

        # Use the LlamaInterface to process the task
        result = await self.llama._query_llama(task)

        # Extract concepts from the result and add them to the knowledge base
        concepts = await self.llama.extract_concepts(result)
        self.knowledge_base.update(concepts)

        return result

    async def stop(self):
        self.running = False
        if self.llama:
            await self.llama.__aexit__(None, None, None)

    def get_status(self):
        return {"kb_size": len(self.knowledge_base), "running": self.running}

    async def query(self, query):
        if not self.running:
            raise RuntimeError("Kernel is not initialized or has been stopped")
        return await self.llama._query_llama(query)
