
from typing import List, TypedDict, Dict, Any

from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, START, StateGraph
from src.agentwrap.easy_llm import load_chat_model,prompt_executor
from src.agentwrap.table_tools import parse_table,get_table_min_max
from src.agentwrap.env import set_environment_variables

status = set_environment_variables()
print(status)

llm = load_chat_model(model_name="google_genai/gemini-2.0-flash-001", temperature=0)

SYSTEM_PROMPT_SUMMARIZE = "You are a helpful assistant that summarizes text clearly and concisely."

TABLE_SUMMARY_PROMPT = (
    """
    Write a concise summary of the following table data:\n{context}\n
    For each column, mention the minimum and maximum values, and specify the row(s) where these values occur. 
    Highlight any notable patterns, trends, or outliers you observe in the data.
    """
)

initial_summary_chain = prompt_executor(
    system_prompt=SYSTEM_PROMPT_SUMMARIZE,
    user_prompt=TABLE_SUMMARY_PROMPT,
    llm=llm,
    return_chain = True
)


TABLE_SUMMARY_REFINE_PROMPT = (
"""

Existing summary up to this point:
{existing_answer}

New context (table data):
------------
{context}
------------

Given the new context, refine the original summary. 
Be sure to accurately identify the minimum and maximum values for each column, and specify which rows they occur in. 
If the previous summary made a mistake about min/max values, correct it.
"""
)

refine_summary_chain = prompt_executor(
    system_prompt="You are refining a summary of tabular data.",
    user_prompt=TABLE_SUMMARY_REFINE_PROMPT,
    llm=llm,
    return_chain = True
)


# State for the LangGraph
class State(TypedDict):
    contents: List[str]  # Each string is a table (e.g., CSV or markdown)
    index: int
    summary: str
    table_stats: Dict[str, Any]  # Holds min/max info for each table


async def generate_initial_summary(state:State,config:RunnableConfig):
    table_str = state["contents"][0]
    table = parse_table(table_str)
    stats = get_table_min_max(table)
    summary = await initial_summary_chain.ainvoke(table_str,config)
    return {"summary":summary,"index":1,"table_stats":{0:stats}}



async def refine_summary(state: State, config: RunnableConfig):
    idx = state["index"]
    table_str = state["contents"][idx]
    table = parse_table(table_str)
    stats = get_table_min_max(table)
    all_stats = dict(state.get("table_stats", {}))
    all_stats[idx] = stats
    summary = await refine_summary_chain.ainvoke(
        {"existing_answer": state["summary"], "context": table_str},
        config,
    )
    return {"summary": summary, "index": idx + 1, "table_stats": all_stats}


def should_refine(state: State):
    if state["index"] >= len(state["contents"]):
        return END
    else:
        return "refine_summary"

graph = StateGraph(State)
graph.add_node("generate_initial_summary", generate_initial_summary)
graph.add_node("refine_summary", refine_summary)

graph.add_edge(START, "generate_initial_summary")
graph.add_conditional_edges("generate_initial_summary", should_refine)
graph.add_conditional_edges("refine_summary", should_refine)
app = graph.compile()



# #####################
# # Initial summary prompt
# summarize_prompt = ChatPromptTemplate(
#     [
#         ("human", "Write a concise summary of the following table data:\n{context}\nBe sure to mention the minimum and maximum values for each column, and specify which rows they occur in."),
#     ]
# )
# initial_summary_chain = summarize_prompt | llm | StrOutputParser()

# # Refinement prompt
# refine_template = """
# You are refining a summary of tabular data.

# Existing summary up to this point:
# {existing_answer}

# New context (table data):
# ------------
# {context}
# ------------

# Given the new context, refine the original summary. 
# Be sure to accurately identify the minimum and maximum values for each column, and specify which rows they occur in. 
# If the previous summary made a mistake about min/max values, correct it.
# """
# refine_prompt = ChatPromptTemplate([("human", refine_template)])
# refine_summary_chain = refine_prompt | llm | StrOutputParser()

# # State for the LangGraph
# class State(TypedDict):
#     contents: List[str]  # Each string is a table (e.g., CSV or markdown)
#     index: int
#     summary: str
#     table_stats: Dict[str, Any]  # Holds min/max info for each table

# def parse_table(table_str: str) -> List[Dict[str, Any]]:
#     """
#     Parses a markdown or CSV table string into a list of dicts.
#     Assumes first row is header.
#     """
#     import csv
#     from io import StringIO

#     # Try to detect and remove markdown table pipes
#     lines = [line.strip() for line in table_str.strip().splitlines() if line.strip()]
#     if lines and lines[0].startswith("|") and "|" in lines[0]:
#         # Remove leading/trailing pipes and split
#         rows = [
#             [cell.strip() for cell in line.strip("|").split("|")]
#             for line in lines
#             if "---" not in line  # skip markdown separator
#         ]
#     else:
#         # Assume CSV
#         reader = csv.reader(StringIO(table_str))
#         rows = [row for row in reader if row]

#     if not rows or len(rows) < 2:
#         return []

#     header = rows[0]
#     data_rows = rows[1:]
#     table = []
#     for row in data_rows:
#         if len(row) != len(header):
#             continue
#         table.append({header[i]: row[i] for i in range(len(header))})
#     return table

# def get_table_min_max(table: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
#     """
#     For each numeric column, find min/max values and the row(s) they occur in.
#     Returns: {col: {"min": (value, [row_idxs]), "max": (value, [row_idxs])}}
#     """
#     import re

#     if not table:
#         return {}

#     header = list(table[0].keys())
#     col_values = {col: [] for col in header}
#     for row in table:
#         for col in header:
#             val = row[col]
#             # Try to convert to float if possible
#             try:
#                 num = float(re.sub(r"[^\d\.\-eE]", "", val))
#                 col_values[col].append(num)
#             except Exception:
#                 col_values[col].append(None)

#     stats = {}
#     for col, values in col_values.items():
#         # Only consider columns with at least one numeric value
#         numeric_vals = [(i, v) for i, v in enumerate(values) if v is not None]
#         if not numeric_vals:
#             continue
#         idxs, nums = zip(*numeric_vals)
#         min_val = min(nums)
#         max_val = max(nums)
#         min_idxs = [i for i, v in zip(idxs, nums) if v == min_val]
#         max_idxs = [i for i, v in zip(idxs, nums) if v == max_val]
#         stats[col] = {
#             "min": (min_val, min_idxs),
#             "max": (max_val, max_idxs),
#         }
#     return stats
# from langchain_core.runnables import RunnableConfig
# async def generate_initial_summary(state: State, config: RunnableConfig):
#     table_str = state["contents"][0]
#     table = parse_table(table_str)
#     stats = get_table_min_max(table)
#     summary = await initial_summary_chain.ainvoke(
#         table_str,
#         config,
#     )
#     return {"summary": summary, "index": 1, "table_stats": {0: stats}}

# async def refine_summary(state: State, config: RunnableConfig):
#     idx = state["index"]
#     table_str = state["contents"][idx]
#     table = parse_table(table_str)
#     stats = get_table_min_max(table)
#     # Combine all stats so far
#     all_stats = dict(state.get("table_stats", {}))
#     all_stats[idx] = stats

#     summary = await refine_summary_chain.ainvoke(
#         {"existing_answer": state["summary"], "context": table_str},
#         config,
#     )
#     return {"summary": summary, "index": idx + 1, "table_stats": all_stats}

# def should_refine(state: State) -> Literal["refine_summary", END]:
#     if state["index"] >= len(state["contents"]):
#         return END
#     else:
#         return "refine_summary"

# # Optionally, a node to check/correct min/max in the summary (post-processing)
# def check_min_max_in_summary(summary: str, table_stats: Dict[int, Dict[str, Any]]) -> str:
#     """
#     Optionally, post-process the summary to ensure min/max values are correct.
#     This is a placeholder for more advanced logic.
#     """
#     # For now, just return the summary.
#     return summary

# graph = StateGraph(State)
# graph.add_node("generate_initial_summary", generate_initial_summary)
# graph.add_node("refine_summary", refine_summary)

# graph.add_edge(START, "generate_initial_summary")
# graph.add_conditional_edges("generate_initial_summary", should_refine)
# graph.add_conditional_edges("refine_summary", should_refine)
# app = graph.compile()

# ---------------------------
# Example usage
# ---------------------------
if __name__ == "__main__":
    import asyncio

    # Example: two markdown tables as strings
    table1 = """
    | Name  | Age | Score |
    |-------|-----|-------|
    | Alice | 23  | 88    |
    | Bob   | 31  | 92    |
    | Carol | 27  | 85    |
    """

    table2 = """
    | Name   | Age | Score |
    |--------|-----|-------|
    | Dave   | 29  | 90    |
    | Eve    | 22  | 95    |
    | Frank  | 35  | 80    |
    """

    # Initial state
    state = {
        "contents": [table1, table2],
        "index": 0,
        "summary": "",
        "table_stats": {},
    }

    async def run_example():
        # Run the summarization/refinement graph
        result = await app.ainvoke(state)
        print("Final summary:\n", result["summary"])
        print("\nTable stats:\n", result["table_stats"])

    asyncio.run(run_example())
