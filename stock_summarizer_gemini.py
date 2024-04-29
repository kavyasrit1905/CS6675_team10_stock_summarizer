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
generation_config=genai.GenerationConfig(temperature=1)
gemini_chat = model.start_chat()

# constants
tickers_list = ['NVDA', 'AMD']
articles_data_path = "stock_summary_data.json"
custom_prompt_selector = {
    "beginner": [False, "Provide stock analysis for a beginner investor including the revenue model, business stand and position in the market. "],
    "expert": [True, "Provide stock analysis for an expert investor including the risk factor by classifying it among High, low or medium; returns expected in high(greater than 15% per annum), medium(between 5% to 15% per annum) ,low(less than 5% per annum); Suggested investment duration among short term(within months) or longterm(within years). For every every decision you make provide a reason correleating it with stock price and market perfromance. "],
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

# fetch from frontend
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
                # print('\n Summarize Article: ', response.text)
                try:
                    summaries.append(response.text)
                    print('\n Summarize: ', summaries)
                except:
                    print ("Incorrect JSON format returned.")
                    time.sleep(10)

    return summaries


def combine_all_articles(prompt_to_combine, final_prompt, combine_stock_news):
    print('Prompts to combine: ', prompt_to_combine)
    print('Final prompt: ', final_prompt)
    response = gemini_chat.send_message(prompt_to_combine + str(combine_stock_news) + final_prompt + "Summaries are: " + ''.join(summaries))
    return response.text


news_articles_prompt = "You are stock news analyzer. Store key content of the news that impacts profit and loss of the company, Strengths, weaknesses, opportunities, threats."
summaries = summarize_all_news_articles(news_articles_prompt, news_article_summarizer_function)


file_name = "gemini_combined_summaries_expert.json"
prompt_to_combine = "Based on the list of summaries of articles content you have in a json format article, combine and summarize the news articles in a json format. Do not miss any key information that is useful for the user to decide stock performance."
final_summary = combine_all_articles(prompt_to_combine, final_prompt, combine_stock_news)

with open(file_name, "w") as file:
    file.write(final_summary)

def test_sentiment_analysis():
    prompt = "You are a stock news article analyzer. Perform sentiment analysis and output a single a word if its *positive*, *negative* or *neutral*."
    function = [
        {
            "name": "Provide_news_article_sentiment",
            "description": "Provide the news article sentiment of the stock news in a JSON format.",
            "parameters": {
                "type": "object",
                "properties": {
                    "sentiment": {
                        "type": "string",
                        "description": f"{prompt}"
                    },
                }
            }
        }
    ]
    sentiment_analysis_actual = []
    sentiment_analysis_predicted = []
   
    count = 0
    
    for company in data["companies"]:
      print("Name:", company["name"])
      content_count = 0
      for article in company["articles"]:
          content_count += len(article["content"])
          sentiment_analysis_actual.append(article["stock_news_sentiment"])
          response = gemini_chat.send_message(prompt + article["content"])
          try:
              output = response.text
              sentiment_analysis_predicted.append(output.lower().replace("*", ""))
          except:
              print ("Incorrect JSON format returned.")
              time.sleep(10)
      print(f"Total Content length: {content_count}")
    return sentiment_analysis_actual, sentiment_analysis_predicted
 
 
# sentiment_analysis_actual, sentiment_analysis_predicted = test_sentiment_analysis()
 
# import seaborn as sns
# from sklearn.metrics import confusion_matrix
# import matplotlib.pyplot as plt

# # Actual and predicted lists
# actual = sentiment_analysis_actual
# predicted = sentiment_analysis_predicted
# print('\Actual Sentiment: ', actual)
# print('\Predicted Sentiment: ', predicted)
 
# # Define the categories
# categories = ["positive", "negative", "neutral"]
 
# # Create confusion matrix
# cm = confusion_matrix(actual, predicted, labels=categories)
 
# # Display confusion matrix
# plt.figure(figsize=(8, 6))
# sns.heatmap(cm, annot=True, fmt="d", xticklabels=categories, yticklabels=categories, cmap="Greens")
# plt.xlabel("Predicted")
# plt.ylabel("Actual")
# plt.title("Confusion Matrix")
# plt.show()


def summarize_single_article(prompt, function, content):
    start_time = time.time()
    summary = []
    print("Summarized one news article.")
    try:
        response = gemini_chat.send_message("You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.\n\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information." + prompt + content)
        output = response.text
        print('\n\nOutput: ', output)
        summary.append(output)
    except:
        print ("Incorrect JSON format returned.")
        time.sleep(10)
    end_time = time.time()
    print('Time: ', end_time - start_time)
    return summary, end_time - start_time



news_articles_prompt = "You are stock news analyzer. Store key content of the news that impacts profit and loss of the company, Strengths, weaknesses, opportunities, threats."
times = []
content_lengthss = []
for company in data["companies"]:
   print("Name:", company["name"])
   for article in company["articles"]:
      print("Date:", article["date"])
      print("URL:", article["url"])
      print("Content:", len(article["content"]))
      _, time_taken = summarize_single_article(news_articles_prompt, news_article_summarizer_function, article["content"])
      print(time_taken)
      content_lengthss.append(len(article["content"]))
      times.append(time_taken)


# Plot of latency for gemini-pro individual news article summaries
# import matplotlib.pyplot as plt

# content_length = [3793, 9028, 1244, 2919, 1097, 5527, 288, 2730, 5707, 686, 2049, 2861, 3604, 2732, 2796, 5328, 2737, 2510, 2802, 2591, 2976, 2733, 2760, 4464, 1033, 2714, 2715, 1703, 1696, 1269]
# times = [3.651094913482666, 4.908170938491821, 7.154149770736694, 6.8840248584747314, 5.951460123062134, 7.4626381397247314, 7.370919942855835, 10.1405508518219, 9.747560024261475, 6.842607736587524, 8.950924158096313, 8.046592950820923, 9.11188793182373, 11.591891765594482, 12.061607122421265, 12.031057834625244, 11.506290912628174, 11.960825681686401, 14.00536298751831, 13.98695993423462, 14.543370008468628, 14.43639087677002, 13.115972757339478, 14.687117099761963, 13.054604053497314, 10.724524974822998, 10.744472742080688, 10.755383968353271, 10.547285079956055, 10.545813083648682]
# print(len(content_length))
# print(len(times))
# # Plotting the graph
# plt.figure(figsize=(12, 6))
# plt.scatter(content_length, times, color='green', label='Times')
# plt.xlabel('Content Length')
# plt.ylabel('Times')
# plt.title('Content Length vs. Times')
# plt.legend()
# plt.grid(True)
# plt.show()