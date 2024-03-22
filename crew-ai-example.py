import os
from crewai import Agent, Task, Crew, Process
from langchain_community.tools import DuckDuckGoSearchRun
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
os.environ["OPENAI_MODEL_NAME"]="gpt-3.5-turbo"

search_tool = DuckDuckGoSearchRun()

researcher = Agent(
    role='Senior Research Analyst',
    goal='Uncover cutting-edge developments in use of AI agents and crewAI specifically in software development',
    backstory="""You are a Senior Research Analyst at a leading tech think tank.
        Your expertise lies in identifying emerging trends and technologies in AI and utilising AI agents
        software development. You have a knack for dissecting complex data and presenting
        actionable insights.""",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool]
)

writer = Agent(
    role='Tech Content Strategist',
    goal='Craft compelling content on tech advancements',
    backstory="""You are a renowned Tech Content Strategist, known for your insightful
    and engaging articles on technology and innovation. With a deep understanding of
    the tech industry, you transform complex concepts into compelling narratives.""",
    verbose=True,
    # (optional) llm=ollama_llm, If you wanna use a local modal through Ollama, default is GPT4 with temperature=0.7
    allow_delegation=True
)

research_task = Task(
  description=(
    "Identify the next big trend in {topic}."
    "Focus on identifying pros and cons and the overall narrative."
    "Your final report should clearly articulate the key points"
    "its market opportunities, and potential risks."
  ),
  expected_output='A comprehensive 3 paragraphs long report on the latest AI trends.',
  tools=[search_tool],
  agent=researcher,
)

write_task = Task(
  description=(
    "Compose an insightful article on {topic}."
    "Focus on the latest trends and how it's impacting the industry."
    "This article should be easy to understand, engaging, and positive."
  ),
  expected_output='A 4 paragraph article on {topic} advancements formatted as markdown.',
  tools=[search_tool],
  agent=writer,
  async_execution=False,
  output_file='crewai-report.md'  # Example of output customization
)

crew = Crew(
  agents=[researcher, writer],
  tasks=[research_task, write_task],
  process=Process.sequential  # Optional: Sequential task execution is default
)

result = crew.kickoff(inputs={'topic': 'Using crewAI in software development'})
print(result)
