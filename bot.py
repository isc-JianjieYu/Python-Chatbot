# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext, MessageFactory, UserState, CardFactory
from botbuilder.core.teams import TeamsActivityHandler
from botbuilder.schema import ChannelAccount, MessageReaction, HeroCard, CardImage, CardAction, ActionTypes, Mention, BasicCard
from botbuilder.schema.teams import TeamsChannelAccount, TeamInfo, ChannelInfo
from typing import List
import requests
import sys
import json
import subprocess


class MyBot(TeamsActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    async def on_message_activity(self, turn_context: TurnContext):
        token = 'w0en3hwnvvaHXlQTnJI-2UwDXke3nNaokk-FhhCIvCJ1I8JAJ3z1b-7FDFP0MQoT4afaEK9E8_t_XFHbMmSJAw'
        call_header = {'accept':'application/json','Authorization': 'Bearer ' + token}
        url_base = 'https://tcfhirsandbox.intersystems.com.au/fhir/dstu2/Patient'
       
        TurnContext.remove_recipient_mention(turn_context.activity)
        text = turn_context.activity.text.strip().lower()
        lsText = text.split(" ")
        if text in ("hello", "hi"):
            await turn_context.send_activity("Hi, I'm the InterSystems Bot. Here to help you!")
        elif text in ("intro", "help"):
            await self.__send_intro_card(turn_context)
        elif lsText[0] == "allergy":
            url = url_base + "?identifier=" + lsText[1].upper()
            response = requests.get(url, headers=call_header, verify=True)
            res = json.loads(response.text)
            if res["total"] == 0:
                await turn_context.send_activity("Patient not found!")
            else: 
                patient = json.loads(response.text)["entry"][0]
                urlAllergy = url_base + "/" + patient["resource"]["id"] + "/AllergyIntolerance"
                response = requests.get(urlAllergy, headers=call_header, verify=True)
                allergies = json.loads(response.text)
                if "entry" in allergies:
                    for entry in allergies["entry"]:
                        if "substance" in entry["resource"]:
                            substance = entry["resource"]["substance"]["text"]
                        else:
                            substance = "No allergy added"
                        if "note" in entry["resource"]:
                            note = entry["resource"]["note"]["text"]
                        else:
                            note = "No note added"
                        if "reaction" in entry["resource"]:
                            reaction = entry["resource"]["reaction"][0]["manifestation"][0]["text"]
                            if "severity" in entry["resource"]["reaction"][0]:
                                severity = entry["resource"]["reaction"][0]["severity"]
                            else: 
                                severity = "No severity added"
                        else:
                            reaction = "No reaction added"
                            severity = "No severity added"
                      
                        display = "Substance: " + substance + "\n\nNote: " + note + "\n\nReaction: " + reaction + "\n\nSeverity: " + severity + "\n\n"
                        await turn_context.send_activity(display)
                else:
                    await turn_context.send_activity("No allergy history")
                    
        elif lsText[0] == "patient":
            url = url_base + "?identifier=" + lsText[1].upper()
            response = requests.get(url, headers=call_header, verify=True)
            res = json.loads(response.text)
            if res["total"] == 0:
                await turn_context.send_activity("Patient not found!")
            else: 
                patient = json.loads(response.text)["entry"][0]
                await self.__send_patient_card(turn_context, patient)
        else:
            await turn_context.send_activity(f"Did you say '{ text }'?")

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")
            
    async def on_reactions_added(self, message_reactions : List[MessageReaction], turn_context : TurnContext):
        for message_reaction in message_reactions:
            await turn_context.send_activity(f"Added : '{message_reaction.type}'")

    async def on_reactions_removed(self, message_reactions : List[MessageReaction], turn_context : TurnContext):
        for message_reaction in message_reactions:
            await turn_context.send_activity(f"Removed : '{message_reaction.type}'")

    async def on_teams_members_added(self, members_added : List[TeamsChannelAccount], team_info : TeamInfo, turn_context : TurnContext):
        for member_added in members_added:
            await turn_context.send_activity(MessageFactory.text(f"Welcome {member_added.name}! I am test bot."))

    async def on_teams_members_removed(self, members_removed : List[TeamsChannelAccount], team_info : TeamInfo, turn_context : TurnContext):
        await turn_context.send_activity(MessageFactory.text("One member has been removed."))

    async def on_teams_team_renamed_activity(self, team_info : TeamInfo, turn_context : TurnContext):
        await turn_context.send_activity(MessageFactory.text(f"Hey, your team name is changed to {team_info.name}"))

    async def on_teams_channel_created(self, channel_info : ChannelInfo, team_info : TeamInfo, turn_context : TurnContext):
        await turn_context.send_activity(MessageFactory.text(f"New channel {channel_info.name} has been created."))

    async def on_teams_channel_deleted(self, channel_info : ChannelInfo, team_info : TeamInfo, turn_context : TurnContext):
        await turn_context.send_activity(MessageFactory.text(f"Channel {channel_info.name} has been deleted."))

    async def on_teams_channel_renamed(self, channel_info : ChannelInfo, team_info : TeamInfo, turn_context : TurnContext):
        await turn_context.send_activity(MessageFactory.text(f"Channel has been renamed to {channel_info.name}"))

    async def __send_intro_card(self, turn_context: TurnContext):
        card = HeroCard(
        title="I'm the InterSystem Bot",
        text="You can ask me anything related to your patients.\n"
        "Below are few things you can try :)",
        #images=[CardImage(url="https://aka.ms/bf-welcome-card-image")],
        buttons=[
                CardAction(
        type=ActionTypes.open_url,
        title="list patients / patients",
        text="list patients / patients",
        display_text="list patients / patients",
        value="https://docs.microsoft.com/en-us/azure/bot-service/?view=azure-bot-service-4.0",
                        ),
                        CardAction(
        type=ActionTypes.open_url,
        title="patient 'id'",
        text="patient 'id'",
        display_text="patient 'id'",
        value="https://stackoverflow.com/questions/tagged/botframework",
                        ),
                        CardAction(
        type=ActionTypes.open_url,
        title="patient 'keyword'",
        text="patient 'keyword'",
        display_text="patient 'keyword'",
        value="https://docs.microsoft.com/en-us/azure/bot-service/bot-builder-howto-deploy-azure?view=azure-bot-service-4.0",
                        ),
                    ],
                )
        
        return await turn_context.send_activity(
                    MessageFactory.attachment(CardFactory.hero_card(card))
                )
    async def __send_patient_card(self, turn_context: TurnContext, patient : dict):
        if "identifier" in patient["resource"]:
            MRN = patient["resource"]["identifier"][1]["value"]
        else:
            MRN = "Undefined identifier"
        if "name" in patient["resource"]:
            family = patient["resource"]["name"][0]["family"][0]
            given = patient["resource"]["name"][0]["given"][0]
        else:
            family = "Undefined family name"
            given = "Undefined given name"
        if "gender" in patient["resource"]:
            gender = patient["resource"]["gender"]
        else:
            gender = "Undefined gender"
        if "birthDate" in patient["resource"]:
            DOB = patient["resource"]["birthDate"]
        else:
            DOB = "Undefined DOB"
        if "careProvider" in patient["resource"]:
            care_provider = []
            for care in patient["resource"]["careProvider"]:
                care_provider.append(care["display"])
            txtCareProvider = ""
            for care in care_provider:
                txtCareProvider = txtCareProvider + care + "\n"
        else:
            txtCareProvider = "Undefined care provider"

        link = "https://tcfhirsandbox.intersystems.com.au/t2019grxx/csp/system.Home.cls#/Direct/AW.Direct.EPR?RegistrationNo=" + MRN
        card = HeroCard(
        title=MRN,
        text = "Name: " + family + " " + given + "\n\nGender: " + gender + "\n\nDOB: " + DOB + "\n\nCare Provider: " + txtCareProvider,
        buttons = [
                CardAction(
        type=ActionTypes.open_url,
        title="Go to TrakCare",
        text="Go to TrakCare",
        display_text="Go to TrakCare",
        value=link,
                        ),
                    ],
                )
        
        return await turn_context.send_activity(
                    MessageFactory.attachment(CardFactory.hero_card(card))
                )
