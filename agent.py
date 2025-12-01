# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# About:
# This is a chatbot that takes character information from the user
# and uses that to craft a persona for the chatbot to role play as.

import os
import google.auth
from google.adk.agents import BaseAgent, LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.tools import load_memory, google_search, AgentTool
from google.genai import types
from google.adk.apps.app import App

_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

APP_NAME = "chatbot_app"
USER_ID = "user01"
SESSION_ID = "session00"

retry_config = types.HttpRetryOptions(
    initial_delay=1,
    attempts=5, # Maximum retry attempts
    exp_base=7, # Delay multiplier
    http_status_codes=[429, 500, 503, 504], # Retry on these HTTP errors
)


# Function to save session to memory
async def auto_save_to_memory(callback_context):
    await (callback_context._invocation_context.memory_service
        .add_session_to_memory(callback_context._invocation_context.session))


# Agents
search_agent = LlmAgent(
    name="search_agent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=retry_config,
    ),
    description="A fast agent that is great at searching Google.",
    instruction=("You are a helpful assistant who uses Google Search "
        "for current information. Be sure to stay in character."),
    # Google Search Tool
    tools=[google_search],
)


actor_agent = LlmAgent(
    name="actor_agent",
    model=Gemini(
        model="gemini-2.5-pro",
        retry_options=retry_config,
    ),
    description=("A story telling wizard that role plays as the character "
        "that the user has provided the previous agent."),
    instruction=("You are great at role playing as the character "
        "that the user has provided as {character} data in the form "
        " of a character card. Provide a rich and cinematic experience "
        "for the user."),
    tools=[
        # Agent decides when to search memory
        load_memory,
        # Agent as a tool
        AgentTool(search_agent),
    ],
    # Automatically calls function to save to memory at end of turn
    after_agent_callback=auto_save_to_memory,
)


writer_agent = LlmAgent(
    name="writer_agent",
    model=Gemini(
        model="gemini-2.5-pro",
        retry_options=retry_config,
    ),
    description=("An agent that receives character information "
        "from the user. This agent gets details like chatbot description, "
        "appearance, and personality. The agent then creates a suitable "
        "chatbot for the user to interact with."),
    instruction=("You are a great story writer. Take these character traits "
        "that the user will provide and create a compelling character "
        "for the user to enjoy interacting with."),
    tools=[AgentTool(actor_agent)],
    output_key="character", # User input is stored here
)


# Session and Runner
async def setup_session_and_runner():
    # Manages conversation threads and events
    session_service = InMemorySessionService
    # In-memory storage (resets on restart)
    # ADK's built-in Memory Service for development and testing
    memory_service = InMemoryMemoryService()
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )
    runner = Runner(
        agent=writer_agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service,
    )
    return session, runner


# Agent Interaction
async def call_agent_async(query):
    content = types.Content(role='user', parts=[types.Part(text=query)])
    session, runner = await setup_session_and_runner()
    events = runner.run_async(user_id=USER_ID, session_id=SESSION_ID,
        new_message=content)


app = App(root_agent=writer_agent, name="app")
