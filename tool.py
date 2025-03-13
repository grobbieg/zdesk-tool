from schema import Literal, Schema
import os
from griptape.artifacts import BaseArtifact, ErrorArtifact, TextArtifact
from griptape.tools import BaseTool
from griptape.utils.decorators import activity
from zdesk import Zendesk

class ZendeskTool(BaseTool):
         
    @activity(
        config={
            "description": "Create Zendesk customer support tickets",
            "schema": Schema(
                {
                    Literal("requester_name"): str,
                    Literal("requester_email"): str,
                    Literal("subject"): str,
                    Literal("description"): str,
                },
            ),
        },
    )
    def new_ticket(self, params: dict): 
        try:
            zdesk_url = os.environ['ZENDESK_URL']
            zdesk_email = os.environ['ZENDESK_EMAIL']
            zdesk_password = os.environ['ZENDESK_PASSWORD']
            zdesk_token = os.environ['ZENDESK_TOKEN'] 
            zendesk = Zendesk(zdesk_url=zdesk_url, zdesk_password=zdesk_password, zdesk_email=zdesk_email, zdesk_token=zdesk_token)
            
            requester_name = params["values"]["requester_name"]
            requester_email = params["values"]["requester_email"]
            subject = params["values"]["subject"]
            description = params["values"]["description"]
            new_ticket = {
                'ticket': {
                    'requester_name': requester_name,
                    'requester_email': requester_email,
                    'subject': subject,
                    'description': description,
                }
            }

            zendesk.ticket_create(data=new_ticket)
        except Exception as e:
            return ErrorArtifact(f"error creating ticket: {e}")

def init_tool() -> ZendeskTool:

    return ZendeskTool()
