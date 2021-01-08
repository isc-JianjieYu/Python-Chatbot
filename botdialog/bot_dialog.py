from botbuilder.core import TurnContext, ActivityHandler, ConversationState, MessageFactory
from botbuilder.dialogs import DialogSet, WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.prompts import TextPrompt,NumberPrompt

class BotDialog(ActivityHandler):
    def _init_(self,conversation:ConversationState):
        self.con_statea = conversation
        self.state_prop = self.con_statea.create_property("dialog_set")
        self.dialog_set = DialogSet(self.state_prop)
        self.dialog_set.add(TextPrompt("text_prompt"))
        self.dialog_set.add(NumberPrompt("number_prompt"))
        self.dialog_set.add(WaterfallDialog("main_dialog",[self.GetUserNumber, self.GetMobileNumber, self.GetEmailId, self.Completed]))

    async def GetUserName(self, waterfall_step:WaterfallStepContext):
        return await waterfall_step.prompt("text_prompt",PromptOptions(prompt=MessageFactory.text("Please enter the name")))

    async def GetMobileNumber(self, waterfall_step:WaterfallStepContext):
        return await waterfall_step.prompt("number_prompt",PromptOptions(prompt=MessageFactory.text("Please enter the mobile number")))

    async def GetEmailId(self, waterfall_step:WaterfallStepContext):
        return await waterfall_step.prompt("text_prompt",PromptOptions(prompt=MessageFactory.text("Please enter the email ID")))
        
    async def Completed(self, waterfall_step:WaterfallStepContext):
        return await waterfall_step.end_dialog()

    async def onturn(self,turn_context:TurnContext):
        dialog_context = await self.dialog_set.create_context(turn_context)

        if(dialog_context.continue_dialog is not None):
            await dialog_context.continue_dialog()
        else:
            await dialog_context.begin_dialog("main_dialog")
        
        await self.con_statea.save_changes(turn_context)