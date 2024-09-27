from .base import BaseTool

class ComputeTool(BaseTool):
    @staticmethod
    def set_cpu_limit(limit: int):
        return f"CPU limit set to {limit}%"

    @staticmethod
    def set_memory_limit(limit: int):
        return f"Memory limit set to {limit} MB"

    @classmethod
    def get_operations(cls):
        return ["set_cpu_limit", "set_memory_limit"]