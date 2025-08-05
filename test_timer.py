from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["UnityMcpServer/src/server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool('timer', {'time': 5, 'unit': 'sec'})
            print(result.content)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())