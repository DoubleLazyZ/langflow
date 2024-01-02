from typing import Union
from langflow import CustomComponent
from langchain.tools import Tool
from langchain.agents import tool
from langchain.agents.agent_toolkits.base import BaseToolkit
import requests
from langchain.schema import Document

class GraphQLToolkit(CustomComponent):
    display_name: str = "GraphQLTool"
    description: str = "GraphQLToolkit"
    beta = True

    field_config = {
        "wise_gen_ai_env": {
            "display_name": "WISE-GenAI-ENV",
            "info": "The WISE-GenAI-ENV to make the request to",
            "field_type": "Document",  # Specifying as Document type
        },
        "graphql_endpoint": {
            "field_type": "str",
        },
        "graphql_query": {
            "field_type": "str",
            "multiline": True,
        },
    }
    
    def build_config(self):
        self.repr_value
        return {
            "wise_gen_ai_env": {
                "info": self.repr_value
            }
        }

    def build(
        self,
        wise_gen_ai_env: Document,
        graphql_endpoint: str,
        graphql_query: str
    ) -> Union[Tool, BaseToolkit]:

        @tool
        def execute_graphql_query(text: str):
            """Execute a GraphQL query."""
            # Extracting the cookie or relevant data from the Document
            cookie = wise_gen_ai_env.page_content.encode('utf-8')

            headers = {
                "Content-Type": "application/json",
                "Cookie": cookie.decode('utf-8')
            }

            try:
                response = requests.post(graphql_endpoint, json={'query': graphql_query}, headers=headers)
                response.raise_for_status()
                
                if response.status_code == 200:
                    return Document(page_content=str(response.json()))
                else:
                    return Document(page_content=str(response.status_code))
            except requests.exceptions.RequestException as e:
                return Document(page_content=f"Network Error: {str(e)}")
            except Exception as e:
                return Document(page_content=f"Error: {str(e)}")
        self.repr_value= [wise_gen_ai_env, graphql_endpoint, graphql_query]
        return [execute_graphql_query]  # type: ignore

# Usage:
# Create an instance of GraphQLToolkit and call the build method with appropriate parameters.
# Example: your_instance.build(your_wise_gen_ai_env_document, 'https://example.com/graphql', '{ yourGraphQLQuery }')
