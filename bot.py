# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount, MessageReaction
from botbuilder.core.teams import TeamsActivityHandler
from botbuilder.schema.teams import TeamsChannelAccount, TeamInfo
from typing import List


class MyBot(TeamsActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    async def on_message_activity(self, turn_context: TurnContext):
        await turn_context.send_activity(f"You said '{ turn_context.activity.text }'")

    async def on_members_added_activity(self, members_added: ChannelAccount, turn_context: TurnContext):
     for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello ! How may I help you ?")

    async def on_reactions_added(self, message_reaction : List[MessageReaction], turn_context : TurnContext):
        for message_reaction in message_reaction:
            await turn_context.send_activity(f"Your message reaction : '{message_reaction.type}'")
    
    async def on_reactions_removed(self, message_reaction : List[MessageReaction], turn_context : TurnContext):
        for message_reaction in message_reaction:
            await turn_context.send_activity(f"You removed : '{message_reaction.type}'")

    async def on_teams_members_added(self, member_added : [TeamsChannelAccount], team_info : TeamInfo, turn_context : TurnContext):
        for member in member_added:
            await turn_context.send_activity(MessageFactory.text(f"Welcome {member.name}, R2D2 is at your service"))
    
    async def on_teams_members_removed(self, member_added : [TeamsChannelAccount], team_info : TeamInfo, turn_context : TurnContext):
        for member in member_added:
            await turn_context.send_activity(MessageFactory.text(f"{member.name} has been removed from this chat"))