from botbuilder.core import (
    ActivityHandler,
    TurnContext,
    UserState,
    CardFactory,
    MessageFactory,
)
from botbuilder.schema import (
    ChannelAccount,
    HeroCard,
    CardImage,
    CardAction,
    ActionTypes,
)

from data_models import WelcomeUserState
import requests, sys, json, subprocess

# Greet users who interact with the bot for first time
class WelcomeUserBot(ActivityHandler):
    def __init__(self, user_state: UserState):
        if user_state is None:
            raise TypeError(
                "[WelcomeUserBot]: Missing parameter. user_state is required but None was given"
            )

        self._user_state = user_state

        self.user_state_accessor = self._user_state.create_property("WelcomeUserState")

        self.WELCOME_MESSAGE = "R2D2 is at your service !"

        self.INFO_MESSAGE = "I am here to make your life easy"

        self.LOCALE_MESSAGE = "Current locale is "

        self.PATTERN_MESSAGE = "Not sure what you should do next ?\nTry typing help or intro"

    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)

        # save changes to WelcomeUserState after each turn
        await self._user_state.save_changes(turn_context)

    async def on_members_added_activity(
        self, members_added: ChannelAccount, turn_context: TurnContext
    ):
        """
        Greet when users are added to the conversation.
        Note that all channels do not send the conversation update activity.
        If you find that this bot works in the emulator, but does not in
        another channel the reason is most likely that the channel does not
        send this activity.
        """
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    f"Hi there { member.name }. " + self.WELCOME_MESSAGE
                )

                await turn_context.send_activity(self.INFO_MESSAGE)

                await turn_context.send_activity(
                    f"{ self.LOCALE_MESSAGE } { turn_context.activity.locale }."
                )

                await turn_context.send_activity(self.PATTERN_MESSAGE)

    async def on_message_activity(self, turn_context: TurnContext):
        """
        Respond to messages sent from the user.
        """
        # Get the state properties from the turn context.
        welcome_user_state = await self.user_state_accessor.get(
            turn_context, WelcomeUserState
        )

        if not welcome_user_state.did_welcome_user:
            welcome_user_state.did_welcome_user = True
            
            # Will be on first message from user
            await turn_context.send_activity(
                "How are you today ?"
            )

            name = turn_context.activity.from_property.name
            await turn_context.send_activity(
                f"I am here to help you {name}"
            )

        else:
            # removes mention from the user input in channels or group
            TurnContext.remove_recipient_mention(turn_context.activity)
            # makes the text in lower case and strips of any spaces
            text = turn_context.activity.text.lower().strip() 
            
            """
            #Use these credentials for using the local IRIS instance using basic auth
            USER = '_system'
            PASS = 'SYS'
            """
            # token needs to be entered manually.
            token = 'QlBZMmXe3bo6rMw9a3f9wO1rVeg7jFnqgv5Q-tISbXUtZPemt_2H_4slcMb3aeizavaRGksg0IsRlF6vomv6pA'
            call_header = {'accept':'application/json','Authorization': 'Bearer ' + token}

            # splits the user input and makes a list
            ltxt = text.split(" ")
            
            # keywords that will be used by the bot to compare the user input
            if text in ("hello", "hi"):
                await turn_context.send_activity(f"Did you say { text } ?")
            elif text in ("intro", "help"):
                await self.__send_intro_card(turn_context)
            elif text in ("list of patients", "results", "upcoming appointments"):
                await turn_context.send_activity("Connect me to TrakCare first !!")
            elif text in ("list patients", "patients"):
                #URL for GET request
                url = 'https://tcfhirsandbox.intersystems.com.au/fhir/dstu2/Patient/137'
                #Run GET
                response = requests.get(url, headers=call_header, verify=True)
                try:
                    r_dict = json.loads(response.text)
                    await turn_context.send_activity(f"{r_dict}")
                    """sr = 1
                    name_list = " "
                    for p in r_dict:
                        name_list = name_list + str(sr) + ". " + p["Name"] + "\n\n"
                        sr+=1
                        await turn_context.send_activity(name_list)"""
                    """for p in r_dict:
                        pat = fmat(p)
                        await turn_context.send_activity(f"{pat}")"""
                except:
                    await turn_context.send_activity('Your token has experied !')
            elif ltxt[0] == "patient":
                try:
                    if ltxt [1] != "0":
                        url = "https://tcfhirsandbox.intersystems.com.au/fhir/dstu2/Patient/" + ltxt[1]
                        response = requests.get(url, headers=call_header, verify=False)
                        #r_dict = json.loads(response.text)
                        #pat = fmat(r_dict)
                        await turn_context.send_activity(f"{response.text}")
                except:
                    await turn_context.send_activity("Patient not found !")
            else:
                await turn_context.send_activity(self.WELCOME_MESSAGE)

    async def __send_intro_card(self, turn_context: TurnContext):
        card = HeroCard(
            title="R2D2 your personal assistant",
            text="You can ask me anything related to your patients.\n"
            "Below are few things you can try :)",
            images=[CardImage(url="https://aka.ms/bf-welcome-card-image")],
            buttons=[
                CardAction(
                    type=ActionTypes.open_url,
                    title="Get list of patients",
                    text="Get list of patients",
                    display_text="Get list of patients",
                    value="Put a hyperlink",
                ),
                CardAction(
                    type=ActionTypes.open_url,
                    title="View most recent results",
                    text="View most recent results",
                    display_text="View most recent results",
                    value="Put a hyperlink",
                ),
                CardAction(
                    type=ActionTypes.open_url,
                    title="Upcoming appointments",
                    text="Upcoming appointments",
                    display_text="Upcoming appointments",
                    value="Put a hyperlink",
                ),
            ],
        )

        return await turn_context.send_activity(
            MessageFactory.attachment(CardFactory.hero_card(card))
        )

#Formats Data
def fmat(pdata:dict):
    op = "Name : " + pdata["Name"] + "\n\nTitle : " + pdata["Title"] + "\n\nCompany : " + pdata["Company"] + "\n\nPhone : " + pdata["Phone"] + "\n\nDOB : " + pdata["DOB"]
    return op