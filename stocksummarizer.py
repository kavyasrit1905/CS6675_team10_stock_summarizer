# -*- coding: utf-8 -*-
"""StockSummarizer.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HQy0tJNkwmYs1IkTDtjmA27-ilwZc4As
"""

! pip install --upgrade openai

# imports
import openai
import os
import json
import time
import ast
from openai import OpenAI

# constants
tickers_list = ['NVDA', 'AMD']
articles_data_path = "/content/stock_summary_data.json" # TO DO: upload this to repo
custom_prompt_selector = {
    "beginner": [False, "Provide stock analysis for a beginner investor including the revenue model, business stand and position in the market. "],
    "expert": [True, "Provide stock analysis for an expert investor including the risk factor by classifying it among High, low or medium; returns expected in high(greater than 15% per annum), medium(between 5% to 15% per annum) ,low(less than 5% per annum); Suggested investment duration among short term(within months) or longterm(within years). For every every decision you make provide a reason correleating it with stock price and market perfromance. "],
    "SWOT": [True, "Include SWOT analysis, by listing top 3 strengths, weaknesses, Opportunities and Threats. If possible add if the above points are for short term or long term. "],
    "competitive": [True, "Compare the current stock and its potential competitor interms of 'Market size', 'revenue stream', their strengths. For every comparison provide which stock is better. And in the end provide which stock is better based on your overall analysis. "]
}
os.environ["OPENAI_API_KEY"] = "YOUR_OPEN_API_KEY"

news_article_summarizer_function = [
        {
            "name": "formatted_news_article_summary",
            "description": "Format the summary of the stock news in a JSON format.",
            "parameters": {
                "type": "object",
                "properties": {
                    "summary_line": {
                        "type": "string",
                        "description": "Based on the news article content summarize the news article interms of correleation with stock price and impact. Do not include its strength or weaknesses or threats or anything about the performance."
                    },
                    "Strengths": {
                        "type": "string",
                        "description": "Based on the content given, provide 2 strengths. If there are no strengths, return 'NONE'"
                    },
                    "Weaknesses": {
                        "type": "string",
                        "description": "Based on the content given, provide 2 weaknesses. If there are no weaknesses, return 'NONE'"
                    },
                    "Opportunities": {
                        "type": "number",
                        "description": "Based on the content given, provide 2 opportunities. If there are no opportunities, return 'NONE'"
                    },
                    "Threats": {
                        "type": "string",
                        "description": "Based on the content given, provide 2 threats. If there are no threats, return 'NONE'."
                    }
                }
            }
        }
]

combine_stock_news = [
 {
            "name": "combined_news_article_summary",
            "description": "Combine the news articles summaries in a JSON format.",
            "parameters": {
                "type": "object",
                "properties": {
                    "summary_line": {
                        "type": "string",
                        "description": "Based on the list of summaries of articles content you have in a json format article, combine and summarize the news article interms of correleation with stock price and impact. Do not include its strength or weaknesses or threats or anything about the performance. Do not miss any key infromation that is useful for the user to decide stock performance."
                    },
                    "Strengths": {
                        "type": "string",
                        "description": "Based on the list of summariers given, provide top 4 strengths. If there are no strengths, return 'NONE'"
                    },
                    "Weaknesses": {
                        "type": "string",
                        "description": "Based on the list of summariers given, provide top 4  weaknesses. If there are no weaknesses, return 'NONE'"
                    },
                    "Opportunities": {
                        "type": "number",
                        "description": "Based on the list of summariers given, provide top 4  opportunities. If there are no opportunities, return 'NONE'"
                    },
                    "Threats": {
                        "type": "string",
                        "description": "Based on the list of summariers given, provide top 4  threats. If there are no threats, return 'NONE'."
                    }
                }
            }
        }
]

# TO DO:  fetch from frontend
current_ticker = 'NVDA'
new_custom_prompt_selector = custom_prompt_selector.copy()
# TO DO: Based on frontend input
# new_custom_prompt_selector["beginner"] =
# new_custom_prompt_selector["expert"] =
# new_custom_prompt_selector["SWOT"] =
# new_custom_prompt_selector["competitive"] =

# construct prompt based on user input
def get_final_prompt(new_custom_prompt_selector):
    final_prompt = ""
    for prompt_type in new_custom_prompt_selector:
        if custom_prompt_selector[prompt_type][0]:
            final_prompt = final_prompt + custom_prompt_selector[prompt_type][1]
    print(final_prompt)
    return final_prompt
final_prompt = get_final_prompt(new_custom_prompt_selector)

# Code for fetching list of articles
with open(articles_data_path, "r") as file:
    json_data = file.read()
data = json.loads(json_data)

# Code for printing number of articles for each
# Extract information based on ticker name
for company in data["companies"]:
    if company["ticker"] == current_ticker:
        print("Name:", company["name"])
        for article in company["articles"]:
            print("Date:", article["date"])
            print("URL:", article["url"])
            print("Content:", len(article["content"]))

def summarize_all_news_articles(prompt, function):
    summaries = []
    messages=[{"role": "system", "content": prompt}]
    for company in data["companies"]:
        if company["ticker"] == current_ticker:
            print("Name:", company["name"])
            for article in company["articles"]:
                print("Date:", article["date"])
                print("URL:", article["url"])
                print("Content:", len(article["content"]))

                client = OpenAI()
                messages.append({"role":"user","content":article["content"]})
                completion = client.chat.completions.create(
                  model="gpt-3.5-turbo",
                  messages=messages,
                  functions = function,
                  function_call='auto'
                )
                print("Summarized one news article.")

                args = completion.choices[0].message.function_call.arguments
                try:
                    output = json.loads(args)
                    summaries.append(output)
                except:
                    print ("Incorrect JSON format returned.")
                    time.sleep(10)

    return summaries





def combine_all_articles(prompt_to_combine, final_prompt, function):
    client = OpenAI()
    messages=[{"role": "user", "content": prompt_to_combine}]
    messages.append({"role":"user","content":f" {summaries}"})
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
      )
    combined_summary = completion.choices[0].message.content

    messages=[{"role": "user", "content": final_prompt}]
    messages.append({"role":"user","content":f" {combined_summary}"})

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        functions = function,
        function_call='auto'
      )

    args = completion.choices[0].message.function_call.arguments

    try:
        output = ast.literal_eval(args)
    except:
        output = json.loads(args)
    return {current_ticker:output}

news_articles_prompt = "You are stock news analyzer. Store key content of the news that impacts profit and loss of the company, Strengths, weaknesses, opportunities, threats."
summaries = summarize_all_news_articles(news_articles_prompt, news_article_summarizer_function)

print(summaries)

file_name = "combined_summaries_expert.json"
prompt_to_combine = "Based on the list of summaries of articles content you have in a json format article, combine and summarize the news articles ina json format. Do not miss any key information that is useful for the user to decide stock performance."
final_summary = combine_all_articles(prompt_to_combine, final_prompt, combine_stock_news)
with open(file_name, "w") as file:
    json.dump(final_summary, file)