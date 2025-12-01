teddy-bear-chatbot

Multi AI Agents Providing a Social Chatbot Experience

Agents Intensive - Capstone Project for
5-Day AI Agents Intensive Course with Google

Submission Track: Freestyle

Chatbots are fun! They are always there when you need someone to talk to.
And this one can be customized to your whims. Just provide, by text,
descriptions, appearance, personality, etc., information about the companion
that you want to talk to. This first AI agent will create your character.
After that, the first AI agent will hand off to the second AI agent
who will role play as your character.There is also a third AI agent
whose job is to do any Google searches that you need and returning
the results. InMemorySessionService and InMemoryMemoryService is implemented.

This build was mostly worked on Google Cloud Shell.

1st agent is writer_agent who also acts as runner. gemini-2.5-pro.
    actor_agent is agent as a tool.
2nd agent is actor_agent. gemini-2.5-pro.
    Tools gives load_memory function.
    search_agent is agent as a tool.
3rd agent is search_agent. gemini-2.5-flash.
    Tools gives google_search functionality.
HttpRetryOptions is implemented.

actor_agent is given the ability to decide when to search the memory
and also uses after_agent_callback to auto_save_to_memory.

If I had more time, I would like to implement VertexAiMemoryBankService
and RAG. I'd also like to implement Model Armor.
That's why the teddy bear has armor! With those set up,
I'm looking forward to making an iPhone app and connecing to my agents
in the cloud. Of course, that would mean expanding the functionality
like being able to switch between different AI chatbots, having  a nice
UI so that I can type in myself the different categories of chatbot
personalities. After that, I'm looking forward to implementing
text-to-speech and speech-to-text and AI image generation. So much to learn
but it's fun!

Included is a sample character sheet. Thank you to @0thedice0
for creating the character.
https://aicharactercards.com/charactercards/anime-manga/0thedice0/susan/

And thanks to Zoltan#8287 for making an AI character editor
which can open character cards.
https://desune.moe/aichared/
