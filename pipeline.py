from langchain_core.messages import ToolMessage

from agents import build_search_agent, build_scrape_agent, writer_chain, critic_chain
from rich import print

def get_tool_output(messages) -> str:
    """
    create_agent() runs a ReAct loop: Human -> AI(tool_call) -> Tool -> AI(final).
    The final AI message is Mistral's own synthesized/citation-annotated answer
    (that's the '{"type": "text", ...}, {"type": "reference", ...}' block format).
    What we actually want is the ToolMessage - the untouched string your
    web_search / scrape_url function returned. This grabs the LAST ToolMessage
    in the run (i.e. the result of the most recent tool call).
    """
    for msg in reversed(messages):
        if isinstance(msg, ToolMessage):
            return str(msg.content).strip()

    # Fallback (shouldn't normally happen): no tool was called, so just
    # return the last message's text, stripped of any block formatting.
    last_content = messages[-1].content
    if isinstance(last_content, list):
        return "".join(
            b.get("text", "") for b in last_content
            if isinstance(b, dict) and b.get("type") == "text"
        ).strip()
    return last_content

def run_pipeline(topic: str)-> dict :
    state = {}
    # Step 1: Search for information on the topic
    print("\n"+"="*50)
    print(f"Step 1: Searching for information on the topic: {topic}")
    print("="*50+"\n")
    search_agent = build_search_agent()
    search_result = search_agent.invoke(
        {'messages' : [{'role': 'user', 'content': topic}]}
    )
    state['search_result'] = get_tool_output(search_result['messages'])
    print(f"\nSearch Result:\n{state['search_result']}\n")

    # Step 2: Scrape the URLs found in the search result
    print("\n"+"="*50)
    print("Step 2: Scraping the URLs found in the search result")
    print("="*50+"\n")
    
    scrape_agent = build_scrape_agent()
    scrape_result = scrape_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_result'][:800]}"
        )]
    })
    # state['scrape_result'] = scrape_result['messages'][-1].content
    # print(f"\nScrape Result:\n{state['scrape_result']}\n")

    # FIX: this line was still using the raw final AI message before -
    # now correctly pulls the raw ToolMessage output, same as Step 1.
    state['scrape_result'] = get_tool_output(scrape_result['messages'])
    print(f"\nScrape Result:\n{state['scrape_result']}\n")

    # Step 3: Generate the final report
    print("\n"+"="*50)
    print("Step 3: Generating the final report")
    print("="*50+"\n")

    research_combined = (
        f"SEARCH RESULTS : \n {state['search_result']} \n\n"
        f"SCRAPE RESULTS : \n {state['scrape_result']}"
    )

    state['report'] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })
    print(f"\nFinal Report:\n{state['report']}\n")

    # Step 4: Critic report
    print("\n"+"="*50)
    print("Step 4: Critiquing the final report")
    print("="*50+"\n")
    state['critique_report'] = critic_chain.invoke({
        "report": state['report']
    })
    print(f"\nCritique Report:\n{state['critique_report']}\n")
    return state

if __name__ == "__main__":
    topic = input("Enter a topic to research: ")
    run_pipeline(topic)

