# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext, MessageFactory, UserState, CardFactory
from botbuilder.core.teams import TeamsActivityHandler
from botbuilder.schema import ChannelAccount, MessageReaction, HeroCard, CardImage, CardAction, ActionTypes, Mention
from botbuilder.schema.teams import TeamsChannelAccount, TeamInfo, ChannelInfo
from typing import List
import requests
import sys
import json


class MyBot(TeamsActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    async def on_message_activity(self, turn_context: TurnContext):
        USER = '_system'
        PASS = 'trakcare'
        TurnContext.remove_recipient_mention(turn_context.activity)
        text = turn_context.activity.text.strip().lower()
        lsText = text.split(" ")
        if text in ("hello", "hi"):
            await turn_context.send_activity("Hi, I'm the InterSystems Bot. Here to help you!")
        elif text in ("intro", "help"):
            await self.__send_intro_card(turn_context)
        elif text in ("patients", "list patients"):
            #URL for GET request
            url = "http://trak.australiasoutheast.cloudapp.azure.com/rest/persons/all"
            response = requests.get(url, auth=(USER, PASS))
            arryPatients = json.loads(response.text)
            for patient in arryPatients:
                add = formatPatient(patient)
                await turn_context.send_activity(add)
        elif lsText[0] == "patient":
            url = "http://trak.australiasoutheast.cloudapp.azure.com/rest/persons/" + lsText[1]
            response = requests.get(url, auth=(USER, PASS))
            patient = json.loads(response.text)
            printing = formatPatient(patient)
            await turn_context.send_activity(printing)
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
        title="Get list of patients",
        text="Get list of patients",
        display_text="Get list of patients",
        value="https://docs.microsoft.com/en-us/azure/bot-service/?view=azure-bot-service-4.0",
                        ),
                        CardAction(
        type=ActionTypes.open_url,
        title="View most recent results",
        text="View most recent results",
        display_text="View most recent results",
        value="https://stackoverflow.com/questions/tagged/botframework",
                        ),
                        CardAction(
        type=ActionTypes.open_url,
        title="Upcoming appointments",
        text="Upcoming appointments",
        display_text="Upcoming appointments",
        value="https://docs.microsoft.com/en-us/azure/bot-service/bot-builder-howto-deploy-azure?view=azure-bot-service-4.0",
                        ),
                    ],
                )
        
        return await turn_context.send_activity(
                    MessageFactory.attachment(CardFactory.hero_card(card))
                )

def formatPatient(patient : dict):
    add = "Name: " + patient["Name"] + "\n\nTitle: " + patient["Title"] + "\n\nCompany: " + patient["Company"] + "\n\nPhone: " + patient["Phone"] + "\n\nDOB: " + patient["DOB"] + "\n\n"
    return add