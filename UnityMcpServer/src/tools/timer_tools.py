from mcp.server.fastmcp import FastMCP, Context
from typing import Dict, Any
from unity_connection import get_unity_connection

def register_timer_tools(mcp: FastMCP):
    @mcp.tool()
    def create_timer(
        ctx: Context,
        timer_name: str,
        duration: float,
        repeat: bool = False,
    ) -> Dict[str, Any]:
        """
        Creates a timer in Unity.

        Args:
            timer_name: Name of the timer.
            duration: Duration in seconds.
            repeat: Whether the timer should repeat.

        Returns:
            Dictionary with 'success', 'message', and optional 'data'.
        """
        try:
            params = {
                "timerName": timer_name,
                "duration": duration,
                "repeat": repeat,
            }
            response = get_unity_connection().send_command("create_timer", params)
            if response.get("success"):
                return {"success": True, "message": response.get("message", "Timer created."), "data": response.get("data")}
            else:
                return {"success": False, "message": response.get("error", "Failed to create timer.")}
        except Exception as e:
            return {"success": False, "message": f"Python error creating timer: {str(e)}"}