import google.generativeai as genai
import os
from IPython.display import Markdown
import os
import json
import time
import ast

gemini_api_key = os.environ["GEMINI_API_KEY"]
genai.configure(api_key = gemini_api_key)


model = genai.GenerativeModel('gemini-pro')
gemini_chat = model.start_chat()

# response = model.generate_content("Do a SWOT analysis based on this " + text1)
# print('Response: ', response)

# print('\n\n')
# # Markdown(response.text)

# print('Response: ', response.text)


# constants
tickers_list = ['NVDA', 'AMD']
articles_data_path = "stock_summary_data.json" # TO DO: upload this to repo
custom_prompt_selector = {
    "beginner": [True, "Provide stock analysis for a beginner investor including the revenue model, business stand and position in the market. "],
    "expert": [False, "Provide stock analysis for an expert investor including the risk factor by classifying it among High, low or medium; returns expected in high(greater than 15% per annum), medium(between 5% to 15% per annum) ,low(less than 5% per annum); Suggested investment duration among short term(within months) or longterm(within years). For every every decision you make provide a reason correleating it with stock price and market perfromance. "],
    "SWOT": [True, "Include SWOT analysis, by listing top 3 strengths, weaknesses, Opportunities and Threats. If possible add if the above points are for short term or long term. "],
    "competitive": [True, "Compare the current stock and its potential competitor interms of 'Market size', 'revenue stream', their strengths. For every comparison provide which stock is better. And in the end provide which stock is better based on your overall analysis. "]
}

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

                # response = model.generate_content("You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.\n\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information." + prompt + article["content"])
                response = gemini_chat.send_message("You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.\n\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information." + prompt + article["content"])
                print('\n Summarize Article: ', response.text)


                # # client = OpenAI()
                # messages.append({"role":"user","content":article["content"]})
                # completion = client.chat.completions.create(
                #   model="gpt-3.5-turbo",
                #   messages=messages,
                #   functions = function,
                #   function_call='auto'
                # )
                # print("Summarized one news article.")

                # args = completion.choices[0].message.function_call.arguments
                try:
                    # output = json.loads(response)
                    # summaries.append(output)
                    summaries.append(response.text)
                    print('\n Summarize: ', summaries)
                except:
                    print ("Incorrect JSON format returned.")
                    time.sleep(10)

    return summaries





def combine_all_articles(prompt_to_combine, final_prompt, combine_stock_news):
    print('\n Prompts to combine: ', prompt_to_combine)
    print('\n Final prompt: ', final_prompt)
    response = gemini_chat.send_message(str(combine_stock_news) + final_prompt + "Summaries are: " + ''.join(summaries))
    # response = model.generate_content("You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.\n\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information." + str(combine_stock_news) + final_prompt)
    print('AI RESPONSE: ', response.text)
    # client = OpenAI()
    # messages=[{"role": "user", "content": prompt_to_combine}]
    # messages.append({"role":"user","content":f" {summaries}"})
    # completion = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=messages
    #   )
    # combined_summary = completion.choices[0].message.content

    # messages=[{"role": "user", "content": final_prompt}]
    # messages.append({"role":"user","content":f" {combined_summary}"})

    # completion = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=messages,
    #     functions = combine_stock_news,
    #     function_call='auto'
    #   )

    # args = completion.choices[0].message.function_call.arguments

    # try:
    #     output = ast.literal_eval(args)
    # except:
    #     output = json.loads(args)
    return response.text
    # return {current_ticker:output}

news_articles_prompt = "You are stock news analyzer. Store key content of the news that impacts profit and loss of the company, Strengths, weaknesses, opportunities, threats."
summaries = summarize_all_news_articles(news_articles_prompt, news_article_summarizer_function)

print('SUMMARIES LIST: \n', summaries)

file_name = "TEST_combined_summaries_expert.json"
prompt_to_combine = "Based on the list of summaries of articles content you have in a json format article, combine and summarize the news articles in a json format. Do not miss any key information that is useful for the user to decide stock performance."
final_summary = combine_all_articles(prompt_to_combine, final_prompt, combine_stock_news)
print('\n\nFINAL SUMMARY: \n\n', final_summary)
with open(file_name, "w") as file:
    file.write(final_summary)
    # json.dump(final_summary, file)