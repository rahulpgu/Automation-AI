from app.services.conversation_history import (
    initialize_database,
    create_session,
    save_message,
    get_messages
)


initialize_database()

session_id = "test-session-001"

create_session(session_id)

save_message(
    session_id,
    "user",
    "How many employees are there?"
)

save_message(
    session_id,
    "assistant",
    "There are 10 employees."
)

messages = get_messages(session_id)

print(messages)