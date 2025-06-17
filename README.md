[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/pagos-ai-pagos-mcp-badge.png)](https://mseep.ai/app/pagos-ai-pagos-mcp)

# Pagos Data MCP Server

## Capabilities

- Get BIN data for a given BIN number.

## Configuration

### Pagos API Key

Follow the instructions in the [Pagos API Key](https://docs.pagos.ai/bin-data/getting-started-with-bin-data#generate-an-api-key) documentation to create an API key.


### Clone the repository locally and install uv

On MacOs, install uv with Homebrew:

``` bash
brew install uv
```

Clone the repository:

``` bash
git clone https://github.com/pagos-ai/pagos-mcp.git
```


### Add the MCP Server to Desktop Claude

On MacOs, update config file `~/Library/Application\ Support/Claude/claude_desktop_config.json` and update elements with your systems specific values.

``` json
{
    "mcpServers": {
        "bin-data": {
            "command": "uv",
            "args": [
                "--directory",
                "</path/to/pagos-mcp-server>",
                "run",
                "pagos-mcp-server.py"
            ],
            "env": {
                "PAGOS_API_KEY": "<your-pagos-api-key>"
            }
        }
    }
}
```
