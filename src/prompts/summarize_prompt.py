TABLE_SUMMARY_PROMPT = (
    """
    Write a concise summary of the following table data:\n{context}\n
    For each column, mention the minimum and maximum values, and specify the row(s) where these values occur. 
    Highlight any notable patterns, trends, or outliers you observe in the data.
    """
)

TABLE_SUMMARY_REFINE_PROMPT = (
"""
You are refining a summary of tabular data.

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






