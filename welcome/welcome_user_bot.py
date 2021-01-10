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

        self.LOCALE_MESSAGE = """"You can use the 'activity.locale' property to welcome the
                        user using the locale received from the channel. If you are using the 
                        Emulator, you can set this value in Settings."""

        self.PATTERN_MESSAGE = "Not sure what you should do next ?\nTry typing help or intro"

    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)

        # save changes to WelcomeUserState after each turn
        await self._user_state.save_changes(turn_context)

    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
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
                    f"{ self.LOCALE_MESSAGE } Current locale is { turn_context.activity.locale }."
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
            # This example hardcodes specific utterances. You should use LUIS or QnA for more advance language
            # understanding.
            text = turn_context.activity.text.lower()
            if text in ("hello", "hi"):
                await turn_context.send_activity(f"Did you say { text } ?")
            elif text in ("intro", "help"):
                await self.__send_intro_card(turn_context)
            elif text in ("list of patients", "results", "upcoming appointments"):
                await turn_context.send_activity("Connect me to TrakCare first !!")
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