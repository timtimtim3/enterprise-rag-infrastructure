from app.services.helpers import build_messages


def test_build_messages_with_minimal_inputs():
    system_prompt = "You are an AI knowledge assistant"
    user_query = "Hi, how are you?"
    messages = build_messages(system_prompt=system_prompt, user_query=user_query)
    assert messages == [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ]


def test_build_messages_preserves_message_order():
    system_prompt = "System prompt"
    user_query = "Current query"

    app_context_1 = "Context 1"
    app_context_2 = "Context 2"
    app_context_messages = [app_context_1, app_context_2]

    user_history = "Earlier query"
    assistant_history = "Earlier answer"
    history = [
        {"role": "user", "content": user_history},
        {"role": "assistant", "content": assistant_history},
    ]

    messages = build_messages(
        system_prompt=system_prompt,
        user_query=user_query,
        app_context_messages=app_context_messages,
        history_messages=history,
    )
    assert messages == [
        {"role": "system", "content": system_prompt},
        {"role": "system", "content": app_context_1},
        {"role": "system", "content": app_context_2},
        {"role": "user", "content": user_history},
        {"role": "assistant", "content": assistant_history},
        {"role": "user", "content": user_query},
    ]    


def test_build_messages_handles_none_context_and_history():
    messages = build_messages(
        system_prompt="System",
        user_query="Question",
        app_context_messages=None,
        history_messages=None,
    )

    assert len(messages) == 2
    