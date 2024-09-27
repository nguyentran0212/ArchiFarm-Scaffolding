from .base import BaseTool

class NetworkTool(BaseTool):
    @staticmethod
    def set_bandwidth(bandwidth: int):
        return f"Bandwidth set to {bandwidth} Mbps"

    @staticmethod
    def set_latency(latency: int):
        return f"Latency set to {latency} ms"

    @classmethod
    def get_operations(cls):
        return ["set_bandwidth", "set_latency"]