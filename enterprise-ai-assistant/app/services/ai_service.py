import os

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import UserMessage
from azure.core.credentials import AzureKeyCredential

from app.config import GITHUB_MODEL, GITHUB_TOKEN
from google import genai
from app.config import GEMINI_API_KEY, GEMINI_MODEL 
from app.prompts.system_prompt import SYSTEM_PROMPT
import json

from app.tools.tool_dispatcher import (execute_tool,require_confirmation,)
from app.prompts.system_prompt import SYSTEM_PROMPT

class AIService:
    def __init__(self, model: str | None = None, api_key: str | None = None):
        self.pending_action = {}
        self.conversation_history = {}
        #self.model = model or GITHUB_MODEL
        #self.api_key = api_key or GITHUB_TOKEN
        self.model = model or GEMINI_MODEL
        self.api_key = api_key or GEMINI_API_KEY

        """self.client = ChatCompletionsClient(
            endpoint="https://models.github.ai/inference",
            credential=AzureKeyCredential(self.api_key),
        )"""
        self.client = genai.Client(
            api_key=self.api_key
        )

    """def ask(self, question: str) -> str:
        response = self.client.complete(
            model=self.model,
            messages=[
                UserMessage(content=question)
            ],
        )"""
    def ask(self, question: str,session_id: str) -> str:
        pending_action = self.pending_action.get(session_id)
        history = self.conversation_history.setdefault(session_id,[])
        if pending_action:

            if self.is_confirmation(question):
                tool_name = pending_action["tool"]
                arguments = pending_action["arguments"]

                self.pending_action.pop(session_id,None)

                result = execute_tool(
                    tool_name,
                    arguments,
                    confirmed=True
                )

                return f"Action completed successfully. Result: {result}"

            if self.is_rejection(question):
                self.pending_action.pop(session_id,None)
                return "Action cancelled."

            return "I have a pending action that requires confirmation. Please answer yes or no."
        conversation = [SYSTEM_PROMPT,f"User question {question}"]
        history.append(f"User{question}")
        conversation = [SYSTEM_PROMPT,*history]
        max_steps = 5
        for step in range(max_steps):
            print(f"\n---Agent step {step + 1} ---")
            response = self.client.models.generate_content(
                model = self.model,
                contents=conversation
            )
            answer = response.text.strip()

            print("Gemini:")
            print(answer)
            #Remove Markdown code fences if Gemini adds them
            if answer.startswith("```"):
                answer = answer.replace("```json","")
                answer = answer.replace("```","")
                answer = answer.strip()
            try:
                tool_request = json.loads(answer)
            except json.JSONDecodeError:
                #Gemini return normal answer
                return answer
            tool_name = tool_request.get("tool")
            arguments = tool_request.get("arguments", {})
            if require_confirmation(tool_name):
                self.pending_action[session_id] = {
                    "tool": tool_name,
                    "arguments": arguments
                }
                return {
                    "message": (f"I need your confirmation before executing "f"'{tool_name}' with argument {arguments}."f"Do you want me to proceed?")
                }
            if not tool_name:
                history.append(f"Assistant:{answer}")
                return answer
            print(f"Executing tool: {tool_name}" )
            print(f"Executing arguments: {arguments}")
            tool_result = execute_tool(tool_name,arguments)
            history.append(f"Tool:{tool_name}\n"f"Result:{tool_result}")
            print("Tool Result:")
            print(tool_result)
            conversation.append(
            f"""
    Tool called: {tool_name}

    Tool result:
    {tool_result}

    Use this result to continue answering the user's request.
    If another tool is required, return ONLY the tool JSON.
    If no more tools are required, provide the final answer naturally.
    """
        )

        return "I was unable to complete the request within the allowed number of steps."

    def is_rejection(self, question: str) -> bool:
        rejection_words = {
            "no",
            "n",
            "nope",
            "cancel",
            "stop",
            "don't",
            "dont"
        }

        return question.strip().lower() in rejection_words
    def is_confirmation(self, question: str) -> bool:
        confirmation_words = {
            "yes",
            "y",
            "yeah",
            "yep",
            "sure",
            "confirm",
            "proceed",
            "go ahead",
            "do it"
        }

        return question.strip().lower() in confirmation_words