from .network_tool import NetworkTool
from .compute_tool import ComputeTool
from .blockchain_tool import BlockchainTool

available_tools = {
    "network_tool": NetworkTool(),
    "compute_tool": ComputeTool(),
    "blockchain_tool": BlockchainTool().execute(blockchain_type="bitcoin", blockchain_name="bitcoin", run_experiment=True, architecture="blockchain")
}

def get_tool(tool_id: str):
    return available_tools.get(tool_id)