from langgraph.graph import MessagesState


class AICompanionState(MessagesState):
    """State class for the AI Companion workflow.

    Extends MessagesState to track conversation history and maintains the last message received.

    Attributes:
        last_message (AnyMessage): The most recent message in the conversation, can be any valid
            LangChain message type (HumanMessage, AIMessage, etc.)
        workflow (str): The current workflow the AI Companion is in. Currently only "conversation".
        current_activity (str): The current activity of Ava based on the schedule.
        memory_context (str): The context of the memories to be injected into the character card.
    """

    summary: str
    workflow: str
    current_activity: str
    apply_activity: bool
    memory_context: str
