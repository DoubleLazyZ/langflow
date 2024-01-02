from langflow import CustomComponent
from langchain.schema import Document



class WISEGenAIENV(CustomComponent):
    display_name: str = "WISE-GenAI-ENV"
    description: str = "Make a GET request to the given URL."
    output_types: list[str] = ["Document"]
    documentation: str = "https://docs.langflow.org/components/utilities#get-request"
    beta = True
    field_config = {
        "code": {"show": False},
        "ifptenant": {
            "display_name": "IFP Tenant",
            "info": "IFP Tenant to make the request to",
            "is_list": False,
            "required": False,
        },
        "eitoken": {
            "display_name": "EIToken",
            "info": "EI Token to make the request to",
            "is_list": False,
            "required": False,
        },
        "ifptoken": {
            "display_name": "IFPToken",
            "info": "IFP Token to make the request to",
            "is_list": False,
            "required": False,
        },
    }


    def build(
        self,
        ifptenant: str = "",
        eitoken: str = "",
        ifptoken: str = "",
    ) -> Document:
        return Document(page_content=str(f"IFPTenant={ifptenant}; EIToken={eitoken}; IFPToken={ifptoken}"))
