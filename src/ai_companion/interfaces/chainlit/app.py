import chainlit as cl
from langchain_core.messages import AIMessageChunk, HumanMessage
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

from ai_companion.graph import graph_builder
from ai_companion.settings import settings


@cl.on_chat_start
async def on_chat_start():
    """Initialize the chat session"""
    # thread_id = cl.user_session.get("id")
    cl.user_session.set("thread_id", 1)


@cl.on_message
async def on_message(message: cl.Message):
    """Handle incoming text messages."""
    msg = cl.Message(content="")

    if message.elements:
        await cl.Message(content="I can only process text messages right now. Please resend your message as text.").send()
        return

    content = (message.content or "").strip()
    if not content:
        await cl.Message(content="I didn't receive any text. Could you resend your message?").send()
        return

    # Process through graph with enriched message content
    thread_id = cl.user_session.get("thread_id")

    async with cl.Step(type="run"):
        async with AsyncSqliteSaver.from_conn_string(settings.SHORT_TERM_MEMORY_DB_PATH) as short_term_memory:
            graph = graph_builder.compile(checkpointer=short_term_memory)
            async for chunk in graph.astream(
                {"messages": [HumanMessage(content=content)]},
                {"configurable": {"thread_id": thread_id}},
                stream_mode="messages",
            ):
                if chunk[1]["langgraph_node"] == "conversation_node" and isinstance(chunk[0], AIMessageChunk):
                    await msg.stream_token(chunk[0].content)

            output_state = await graph.aget_state(config={"configurable": {"thread_id": thread_id}})

    await msg.send()
