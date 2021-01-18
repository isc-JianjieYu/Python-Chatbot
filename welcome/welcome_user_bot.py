from os import SEEK_END
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
import requests
import json

#Globals for patient data
trak_url = ''
trak_name = ''
trak_recordNumber = ''
trak_gender = ''
trak_dob = ''
trak_careProvider= ''
trak_allergy_url = ''

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
                    f"Hi { member.name }. " + self.WELCOME_MESSAGE
                )

                await turn_context.send_activity(self.INFO_MESSAGE)

                await turn_context.send_activity(self.PATTERN_MESSAGE)

    async def on_message_activity(self, turn_context: TurnContext):
        """
        Respond to messages sent from the user.
        """
        # Using the global variables
        global trak_name
        global trak_allergy_url
        global trak_careProvider
        global trak_dob
        global trak_gender
        global trak_recordNumber
        global trak_url        
        
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
                f"What can I help you with {name} ?"
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
            token = 'ayaspPQg3a6aWKk6O5RHPtLLRFwSmuLrK9qKdFBr9rY8kgit4cNopfu22Mr329Ep7jBlvZdHblMpyHNyxWre4A'
            call_header = {'accept':'application/json','Authorization': 'Bearer ' + token}

            # splits the user input and makes a list
            ltxt = text.split(" ")
            
            # keywords that will be used by the bot to compare the user input
            if text in ("hello", "hi"):
                await turn_context.send_activity(f"Did you say { text } ?")
            elif text in ("go to trakcare", "trakcare"):
                await self.__send_intro_card(turn_context)
            elif text in ("list options", "options"):
                    await turn_context.send_activity('You can perform following querries:\n1. Get patient Medical Record Number and Care provider\nUse: patient 137\n\n2. Get Recent Observations\nUse: \n\n3. Get recent result of a patient\nUse: \n\n4. Get patient allergies\nUse: ')
            elif text in ("patient"):
                await turn_context.send_activity('Please type the patient ID after patient. Eg: "patient 137"')
            elif ltxt[0] == "patient":
                try:
                    if ltxt [1] != "0":
                        url = "https://tcfhirsandbox.intersystems.com.au/fhir/dstu2/Patient/" + ltxt[1]
                        response = requests.get(url, headers = call_header, verify = True)
                        r_dict = json.loads(response.text)
                        try: 
                            trakurl = (f"https://tcfhirsandbox.intersystems.com.au/t2019grxx/csp/system.Home.cls#/Direct/AW.Direct.EPR?RegistrationNo={str(r_dict['identifier'][1]['value'])}")
                            trak_name = (f"{r_dict['name'][0]['text']}")
                            trak_careProvider = (f"{r_dict['careProvider'][0]['display']}")
                            trak_recordNumber = (f"{r_dict['identifier'][1]['value']}")
                            trak_dob = (f"{r_dict['birthDate']}")
                            trak_gender = (f"{r_dict['gender']}")
                            trak_allergy_url = (f"https://tcfhirsandbox.intersystems.com.au/fhir/dstu2/Patient/{ltxt[1]}/AllergyIntolerance")
                            await turn_context.send_activity(f"Record Number : {trak_recordNumber}\n\n\t Name : {trak_name}\n\t  Sex : {trak_gender}\n\t  DOB : {trak_dob}\nCare Provider : {trak_careProvider}")
                        except:
                            await turn_context.send_activity("Patient not found !")
                except:
                    await turn_context.send_activity("Your token has experied !")
            elif text in ("allergy", "allergy intolerance"):
                try:
                    allergy_resposne = requests.get(trak_allergy_url, headers = call_header, verify = True)
                    a_dict = json.loads(allergy_resposne.text)
                    a_total = (f"{a_dict['total']}")
                    if a_total != "0":
                        await turn_context.send_activity(f"{a_total}")
                    else:
                        await turn_context.send_activity("This patient has no allergies.")
                except:
                    await turn_context.send_activity("Something is wrong ! Please check the source code")

            else:
                await turn_context.send_activity("I am SORRY!!!, I don't understand that.")

    async def __send_intro_card(self, turn_context: TurnContext):
        card = HeroCard(
            title=(f"Portal to TrakCare"),
            text= (f"Click the button below to go to {trak_name} TrakCare profile"),
            images=[CardImage(url="https://aka.ms/bf-welcome-card-image")],
            buttons=[
                CardAction(
                    type=ActionTypes.open_url,
                    title="Go to trakacare",
                    text="Go to trakacare",
                    display_text="Go to trakacare",
                    value= (trak_url),
                ),
            ],
        )

        return await turn_context.send_activity(
            MessageFactory.attachment(CardFactory.hero_card(card))
        )