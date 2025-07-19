# Pagos Data MCP Server

## Capabilities

- Get BIN data for a given BIN number.

## Configuration

### Pagos API Key

Follow the instructions in the [Pagos API Key](https://docs.pagos.ai/bin-data/getting-started-with-bin-data#generate-an-api-key) documentation to create an API key.

### Enhanced BIN Data 

Set to `"true"` for enhanced BIN response attributes which will provide the richest insights on the BIN. Set to `"false"` for basic BIN data. Defaults to `"false"` if value is not provided. Check your contract for any additional costs associated with enhanced bin data calls before setting to `"true"`.


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
                "PAGOS_API_KEY": "<your-pagos-api-key>",
                "ENHANCED_BIN_DATA": "true"
            }
        }
    }
}
```
