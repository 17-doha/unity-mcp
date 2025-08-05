from typing import Any, Dict
from mcp.server.fastmcp import Context

async def handle_timer(ctx: Context, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle timer tool requests.
    
    Args:
        ctx: The MCP context
        params: Dictionary containing:
            - time: float value representing the time amount
            - unit: string representing the time unit ("hrs", "min", or "sec")
    
    Returns:
        Dictionary containing the response from Unity
    """
    try:
        # Validate required parameters
        if 'time' not in params:
            return {"error": "Time parameter is required"}
            
        time_value = float(params['time'])
        unit = params.get('unit', 'sec').lower()
        
        # Validate time value
        if time_value <= 0:
            return {"error": "Time value must be greater than zero"}
            
        # Validate unit
        valid_units = {'hrs', 'hours', 'min', 'minutes', 'sec', 'seconds'}
        if unit not in valid_units:
            return {"error": f"Invalid unit. Must be one of: {', '.join(valid_units)}"}
        
        # Call Unity's timer tool
        response = await ctx.bridge.unity_editor.HandleTimer({
            "time": time_value,
            "unit": unit
        })
        
        return response
        
    except ValueError as e:
        return {"error": f"Invalid time value: {str(e)}"}
    except Exception as e:
        return {"error": f"Error handling timer request: {str(e)}"}