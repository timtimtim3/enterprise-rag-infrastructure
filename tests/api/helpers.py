from app.api.schemas.chats import AskResponse, UsageInfo
from app.services.chat_service import AnswerGenerationError


async def fake_answer_chat_message(**kwargs):
    return AskResponse(
        chat_id=kwargs["chat"].chat_id,
        query_message_id="query-msg-1",
        answer_message_id="answer-msg-1",
        answer="Fake answer",
        model="fake-model",
        finish_reason="stop",
        usage=UsageInfo(
            completion_tokens=10,
            prompt_tokens=20,
            total_tokens=30,
        ),
        sources=[],
    )


async def fake_answer_chat_message_gen_fail(**kwargs):
    raise AnswerGenerationError()
