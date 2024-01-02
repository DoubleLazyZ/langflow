from langflow import CustomComponent
from langchain.tools import Tool
from langchain.agents import tool
from langchain.schema import Document
import requests
from typing import Optional, Union

class UnpackedGetRequestEncode(CustomComponent):
    display_name: str = " Unpacked GET Request"
    description: str = "Make a GET request to the given URL and process the response."
    output_types: list[str] = ["Document"]
    documentation: str = "https://docs.langflow.org/components/utilities#get-request"
    beta = True
    field_config = {
        "url_template": {
            "display_name": "URL Template",
            "info": "Template URL with placeholders for dynamic parts",
            "field_type": "str",
        },
        "config": {
            "display_name": "Configuration",
            "info": "JSON configuration for replacing parts in the URL template",
            "field_type": "dict",
        },
        "headers": {
            "display_name": "Headers",
            "info": "The headers to send with the request.",
        },
        "code": {"show": False},
        "timeout": {
            "display_name": "Timeout",
            "field_type": "int",
            "info": "The timeout to use for the request.",
            "value": 5,
        },
    }


    def build(
        self,
        url_template: str,
        config: dict,
        headers: Optional[dict] = None,
        timeout: int = 5,
    ) -> Union[Tool, Document]:
        if headers is None:
            headers = {"Content-Type": "application/json"}

        @tool
        def execute_get_request(text: str):
            """Execute a GET request."""
            actual_url = url_template.format(**config)  # Format the URL using the config
            with requests.Session() as session:
                try:
                    response = session.get(actual_url, headers=headers, timeout=timeout)
                    response.encoding = 'utf-8'
                    try:
                        response_json = response.json()
                        result = response_json
                    except Exception:
                        result = response.text

                    return Document(
                        page_content=str(result),
                        metadata={
                            "source": url_template,
                            "headers": headers,
                            "status_code": response.status_code,
                        },
                    )
                except requests.Timeout:
                    return Document(page_content="Request Timed Out", metadata={"source": url_template, "headers": headers, "status_code": 408})
                except Exception as exc:
                    return Document(page_content=str(exc), metadata={"source": url_template, "headers": headers, "status_code": 500})
        self.repr_value=[execute_get_request]
        return execute_get_request  # Returning the tool

# Usage:
# Create an instance of GetRequestEncode and call the build method with appropriate parameters.
# Example: your_instance.build('https://example.com/api', {'Authorization': 'Bearer your_api_key'}, 10)
