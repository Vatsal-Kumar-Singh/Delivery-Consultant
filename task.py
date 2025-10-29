from crewai import Task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from agents import website_analyst, competitor_analyst, competitor_researcher, report_writer

analysis_task = Task(
    description='Provide a search optimization report with detailed analysis of the website: {website}',
    expected_output=(
        "A comprehensive 1-2 page long report consisting of total score,  weaknesses, actionable insights according to the domain"
        " of the website:  {website} "
    ),
    agent = website_analyst,
    tools=[SerperDevTool(), ScrapeWebsiteTool()],  
)

competitor_finding_task = Task(
    description='Find relevant competitors for the website: {website}',
    expected_output=(
        "A list of top 5-10 competitors for the website: {website} in the same domain along with the urls of their websites."
    ),
    agent=competitor_analyst,
    tools=[SerperDevTool(), ScrapeWebsiteTool()],
)

competitor_researching_task = Task(
    description='Find a comparative analysis of competitors for the website: {website}',
    expected_output=(
        "A brief report consisting of comparative analysis of the top competitors for the website: {website} "
        "in the same domain, including deep competitive insights"
        " along with suggested keywords to appear before competitors in search ranking. {website}."
    ),
    agent=competitor_researcher,
    tools=[SerperDevTool(), ScrapeWebsiteTool()],
)

writing_task = Task(
    description='Craft a professional and comprehensive SEO report based on the website: {website}',
    expected_output=(
        "A comprehensive and detailed 2-3 page SEO report consisting of structured informative sections"
        " based on the website: {website} and the findings from the analysis and competitor research tasks."
    ),
    agent=report_writer,
    tools=[SerperDevTool(), ScrapeWebsiteTool()],
)