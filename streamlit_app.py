import streamlit as st
from openai import OpenAI
import time
import re


placeholderstr = "請輸入關於本新聞的問題..." if st.session_state['lang_setting'] == "繁體中文" else "Ask anything about the news..."

user_name = "Maggie"
user_image = "https://cafe24img.poxo.com/dinotaeng/web/product/medium/202305/d102e826d93d2d2c2a18a32f044959e4.png"


def stream_data(stream_str):
    for word in stream_str.split(" "):
        yield word + " "
        time.sleep(0.15)


# News context (chinese version)
news_context_ch = {
    "title": "南韓戰機誤炸造成15人受傷",
    "date": "2025年3月6日",
    "author": ["Jake Kwon", "Hosu Lee", "Koh Ewe"],
    "location": "南韓寶川市",
    "news_website": "BBC新聞",
    "summary": (
        "兩架南韓KF-16戰機在進行例行訓練時，誤將八枚炸彈投放到寶川市，導致15名平民受傷，並造成多棟建築物受損。軍方承認，炸彈是因為輸入錯誤的坐標而掉落。空軍目前已經暫停所有實彈演習，並承諾會提供賠償。"
    ),
    "cause_of_incident": "事件發生的原因是其中一位飛行員在操作過程中輸入了錯誤的坐標，這導致炸彈意外掉落在民用區域，造成了15名平民受傷並損壞了多棟建築物。",
    "casualties": "有15個人受傷，其中2個人傷勢較重，傷到了骨頭並且有彈片傷。",
    "damage": "受損的範圍包括一座教堂、附近住宅的窗戶，以及一個長者照護中心。這些地方的損壞進一步加劇了事件對當地社區的影響。",
    "investigation_response": "南韓空軍正在調查此事件，並已暫停所有實彈演習。將提供受影響者賠償。",
    "suspended_exercises": "對，所有實彈演習已因這起事件而暫停，空軍表示將會進行內部調查並對相關責任人進行處理。",
    "previous_incident": "在2022年，有一次聯合演習中，一枚短程彈道導彈發生故障並墜毀，雖然引起火災，但沒有爆炸。跟此新聞事件類似。",
    "related_news": [
        "每三分鐘一命：為何印度的道路是全球最危險的",
        "82歲的印度祖母依然刀槍不入",
        "設計於美國，製造於中國：蘋果為何陷入困境"
    ],
    "bullet_summary": [
        "15人受傷，其中2人重傷",
        "事件發生在南韓寶川市，涉及戰機誤炸",
        "事故發生於實彈軍事演習中",
        "一名飛行員輸入錯誤的坐標，導致炸彈掉落",
        "造成教堂及附近住宅損壞",
        "事故後，居民被撤離，並未發現未爆炸的炸彈",
        "因事件，實彈演習已被暫停",
        "事件涉及與美軍的聯合演習",
        "2022年發生過類似事件"
    ],
    "external_link": "https://bbc.com/news/articles/c2ernge8193o",
    "images":"https://ichef.bbci.co.uk/news/1536/cpsprodpb/216e/live/e439c260-fa46-11ef-86ff-f583a2c90fa2.jpg.webp",
    "investigation_update": "目前調查仍在進行中，南韓空軍尚未提供其他更新。"
}


# News context (english version)
news_context_en = {
    "title": "Fifteen hurt after SK fighter jets drop bombs by accident",
    "date": "March 6, 2025",
    "author": ["Jake Kwon", "Hosu Lee", "Koh Ewe"],
    "location": "Pocheon, South Korea",
    "news_website": "BBC News",
    "summary": (
        "Two South Korean KF-16 fighter jets accidentally dropped eight bombs over the city of Pocheon during a routine training. "
        "Fifteen civilians were injured, and multiple buildings were damaged. The military acknowledged that the bombs were dropped "
        "due to incorrect coordinates being entered. The air force has suspended live-fire drills and promised compensation."
    ),
    "cause_of_incident": "The incident occurred because the pilot of one of the jets inputted the wrong coordinates, which caused the bombs to land in a civilian area.",
    "casualties": "15 people were injured, with two seriously injured, including fractures and shrapnel wounds.",
    "damage": "Damage included a church building, shattered windows in nearby houses, and a senior care center.",
    "investigation_response": "The South Korean Air Force is investigating the incident and has suspended all live-fire exercises. Compensation will be provided to those affected.",
    "suspended_exercises": "Yes, all live-fire exercises have been suspended as a result of this incident.",
    "previous_incident": "In 2022, during a joint drill, a short-range ballistic missile malfunctioned and crashed, causing a fire but no explosions.",
    "related_news": [
        "A death every three minutes: Why India's roads are among the world's deadliest",
        "India's sword-wielding grandmother still going strong at 82",
        "Designed in US, made in China: Why Apple is stuck"
    ],
    "bullet_summary": [
        "15 people injured, 2 seriously",
        "Fighter jets dropped bombs accidentally in Pocheon, South Korea",
        "The incident occurred during a live-fire military exercise",
        "The wrong coordinates were entered by one pilot",
        "Damage to a church and nearby houses",
        "Residents evacuated, no unexploded bombs found",
        "Live-fire exercises suspended",
        "Joint drill with US forces involved",
        "Similar incident occurred in 2022"
    ],
    "external_link": "https://bbc.com/news/articles/c2ernge8193o",
    "images":"https://ichef.bbci.co.uk/news/1536/cpsprodpb/216e/live/e439c260-fa46-11ef-86ff-f583a2c90fa2.jpg.webp",
    "investigation_update": "As of now, the investigation is ongoing, and no additional updates have been provided by the South Korean Air Force."
}





def main():
    st.set_page_config(
        page_title='K-Assistant - The Residemy Agent',
        layout='wide',
        initial_sidebar_state='auto',
        menu_items={
            'Get Help': 'https://streamlit.io/',
            'Report a bug': 'https://github.com',
            'About': 'About your application: **Hello world**'
            },
        page_icon="img/favicon.ico"
    )

    # Show title and description.
    st.title(f"💬 {user_name}'s Chatbot")

    with st.sidebar:
        selected_lang = st.selectbox("Language", ["English", "繁體中文"], index=1)
        if 'lang_setting' in st.session_state:
            lang_setting = st.session_state['lang_setting']
        else:
            lang_setting = selected_lang
            st.session_state['lang_setting'] = lang_setting

        st_c_1 = st.container(border=True)
        with st_c_1:
            st.image("https://cafe24img.poxo.com/dinotaeng/web/product/medium/202305/d102e826d93d2d2c2a18a32f044959e4.png")

        # 根據語言設定不同的顯示文字
    if lang_setting == "English":
        title_text = f"💬 {user_name}'s News Chatbot"
        desc_text = "Here’s a news article for you. Feel free to ask anything about it—just give it a try! (This is a simple chatbot that doesn’t use the OpenAI API, but gives you custom responses.))"
    else:  # 繁體中文
        title_text = f"💬 {user_name} 新聞特派員"
        desc_text = "小小新聞特派員上線，我提供了一則新聞，對於新聞內容有任何好奇的地方，可以盡量問我～我會盡力解答的！(這是一個不使用 OpenAI API 的簡易聊天機器人，提供客製化的回應。)"


    st_c_chat = st.container(border=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []
    else:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                if user_image:
                    st_c_chat.chat_message(msg["role"],avatar=user_image).markdown((msg["content"]))
                else:
                    st_c_chat.chat_message(msg["role"]).markdown((msg["content"]))
            elif msg["role"] == "assistant":
                st_c_chat.chat_message(msg["role"]).markdown((msg["content"]))
            else:
                try:
                    image_tmp = msg.get("image")
                    if image_tmp:
                        st_c_chat.chat_message(msg["role"],avatar=image_tmp).markdown((msg["content"]))
                except:
                    st_c_chat.chat_message(msg["role"]).markdown((msg["content"]))



    def generate_response(prompt):
            # 根據語言設置選擇回應語言
            lang = st.session_state.get('lang_setting', '繁體中文')

            if lang == "繁體中文":
                if re.search(r"(標題是什麼|新聞標題|標題為何|新聞標題是什麼|新聞主題)", prompt_lower):
                    return f"**標題**: {news_context_ch['title']}"

                elif re.search(r"(新聞作者|作者|作者是誰|誰寫的|誰撰寫的|文章作者)", prompt_lower):
                    return f"**作者**: {', '.join(news_context_ch['author'])}"

                elif re.search(r"(發佈日期是什麼|發布日期|什麼時候發佈的|發布時間|新聞公佈時間|這篇文章何時發佈)", prompt_lower):
                    return f"**發佈日期**: {news_context_ch['date']}"

                elif re.search(r"(這篇新聞從哪裡來|新聞來源|新聞發布的網站|網站|新聞網站|這篇新聞來自哪個平台)", prompt_lower):
                    return f"**新聞網站**: {news_context_ch['news_website']}"

                elif re.search(r"(發布地點|地點是在哪|報導地點|發布地點是在哪)", prompt_lower):
                    return f"**地點**: {news_context_ch['location']}"

                elif re.search(r"(摘要|重點整理|重點|簡短的摘要|統整|新聞大意|大概的內容|概述內容|新聞內容)", prompt_lower):
                    return f"**摘要**: {news_context_ch['summary']}"

                elif re.search(r"(原因|事故的原因|事故原因|為什麼會發生|發生原因|肇事原因|原因是什麼|事故原因為何|造成事故的原因是什麼)", prompt_lower):
                    return f"**事故原因**: {news_context_ch['cause_of_incident']}"

                elif re.search(r"(有多少人受傷|傷亡情況|受傷情況|有沒有死亡|傷亡|受傷|死亡)", prompt_lower):
                    return f"**傷亡情況**: {news_context_ch['casualties']}"

                elif re.search(r"(損害|有什麼損害|損壞|有什麼損失|損失)", prompt_lower):
                    return f"**損害狀況**: {news_context_ch['damage']}"

                elif re.search(r"(這件事有沒有調查|調查|調查結果|調查的情況|怎麼處理這個事件|處理方法)", prompt_lower):
                    return f"**調查回應**: {news_context_ch['investigation_response']}"

                elif re.search(r"(演習有停擺嗎|演習|取消|演習被取消了嗎|演習暫停了嗎|演習暫停|暫停|停擺)", prompt_lower):
                    return f"**演習停擺**: {news_context_ch['suspended_exercises']}"

                elif re.search(r"(過去有發生過這樣的事嗎|以前有類似的事件嗎|這次事件以前有過嗎|類似事件|發生過)", prompt_lower):
                    return f"**過去事件**: {news_context_ch['previous_incident']}"

                elif re.search(r"(重點摘要列點|列點|新聞摘要|列點重點)", prompt_lower):
                    return "**列點摘要**:\n" + "\n".join([f"- {point}" for point in news_context_ch['bullet_summary']])

                elif re.search(r"(重點|新聞重點|重點是什麼|主要信息|關鍵信息|關鍵資訊|關鍵)", prompt_lower):
                    return ("**新聞重點**: 15人受傷，兩人重傷，事故發生在例行軍事演習中，並由於錯誤的座標輸入導致炸彈誤掉在平民區。")

                elif re.search(r"(測驗|問題|小挑戰)", prompt_lower):
                    return (
                        "**小測驗問題**: 請問這起爆炸事故的主要原因是什麼？\n"
                        "A. 天氣因素\n"
                        "B. 駕駛員錯誤 (正確)\n"
                        "C. 技術故障\n"
                        "D. 軍事衝突"
                    )

                elif re.search(r"(閱讀更多|讀更多|更多|完整文章|詳情|查看完整文章)", prompt_lower):
                    return f"**閱讀更多**:({news_context_ch['external_link']})"

                elif re.search(r"(調查更新|最新進展|調查狀況)", prompt_lower):
                    return f"**調查狀況**: {news_context_ch['investigation_update']}"

                elif re.search(r"(相關新聞|有類似的新聞嗎|相似的新聞報導)", prompt_lower):
                    return "**相關新聞**:\n" + "\n".join([f"- {title}" for title in news_context_ch['related_news']])

                elif re.search(r"(圖片|照片|影像|圖像|現場照片)", prompt_lower):
                    return f"**圖片**:\n![圖1]({news_context_ch['images']})"

                elif re.search(r"(是誰|是什麼|什麼時候|在哪裏|怎麼|為什麼)", prompt_lower):
                    return (
                        "這個聊天機器人可以回答這篇新聞的問題，例如：\n"
                        "- 新聞標題是什麼？\n"
                        "- 文章作者是誰？\n"
                        "- 什麼時候發佈的？\n"
                        "- 從哪裡發布的？\n"
                        "- 這篇新聞是關於什麼的？\n"
                        "- 事故的原因是什麼？\n"
                        "- 是否有人受傷？\n"
                        "- 有什麼損害發生嗎？\n"
                        "- 調查回應是什麼？\n"
                        "- 演習有停擺嗎？\n"
                        "- 有沒有類似的事故發生過？\n"
                        "- 顯示重點摘要。\n"
                        "- 強調重點。\n"
                        "- 顯示相關新聞。\n"
                        "- 小測驗。\n"
                        "- 顯示外部連結或後續更新資訊。"
                    )

            # 英文回答 (English)
            elif lang == "English":
                if re.search(r"\b(title|headline|news title|what is the name of this news|what's the name of this news|name of the news|news name|give me the title)\b", prompt_lower):
                    return f"**Title**: {news_context_en['title']}"

                elif re.search(r"\b(author|authors|written by|who wrote|who is the author|who's the author|name of the author|news writer|article by)\b", prompt_lower):
                    return f"**Author(s)**: {', '.join(news_context_en['author'])}"

                elif re.search(r"\b(date|publish date|publication date|when was (it|this) published|when is (it|this) published|when did (it|this|the incident) come out|news date|article date|release date|published on)\b", prompt_lower):
                    return f"**Date of Publication**: {news_context_en['date']}"

                elif re.search(r"\b(where was it (published|reported)?|news website|source|which site|which website|news platform|from which site|posted on which website|media outlet|news source|where is this article from|published on which platform)\b", prompt_lower):
                    return f"**News Website**: {news_context_en['news_website']}"

                elif re.search(r"\b(location|where is this news report from|report location|report from location)\b", prompt_lower):
                    return f"**Location**: {news_context_en['location']}"

                elif re.search(r"\b(summary|summarize|summarise|brief summary|can you summarize|can you briefly explain|what is this about|what is this news about|what is news about|what is it about|short summary|in short|quick summary|news summary)\b", prompt_lower):
                    return f"**Summary**: {news_context_en['summary']}"

                elif re.search(r"\b(cause|reason|what (was|is) the cause|what caused (it|this|the incident)|why did (it|this|that|the incident|the event) happen|why (did it|was it)|how did it happen|possible reason|main cause|root cause)\b", prompt_lower):
                    return f"**Cause of the Incident**: {news_context_en['cause_of_incident']}"

                elif re.search(r"\b(casualties|injuries|injured|deaths|killed|hurt|fatalities|victims|anyone (injured|hurt|killed)|how many (people )?(were )?(injured|hurt|killed)|was anyone (injured|hurt|killed)|any (casualties|injuries|deaths|fatalities)|how bad was the damage|extent of damage|damage report)\b", prompt_lower):
                    return f"**Casualties and Injuries**: {news_context_en['casualties']}"

                elif re.search(r"\b(damage|how bad was the damage|what was damaged|extent of damage|destruction|property damage|damage report|was there any damage|how much damage)\b", prompt_lower):
                    return f"**Damage**: {news_context_en['damage']}"

                elif re.search(r"\b(investigation|response|what actions are being taken|how is it being handled|is there an investigation|what's the status of the investigation|response to the incident|how is the issue being addressed)\b", prompt_lower):
                    return f"**Investigation and Response**: {news_context_en['investigation_response']}"

                elif re.search(r"\b(suspend|exercise|were exercises suspended|have exercises been cancelled|was there a suspension|are the exercises on hold|is the exercise cancelled|any suspension of exercises)\b", prompt_lower):
                    return f"**Exercises Suspension**: {news_context_en['suspended_exercises']}"

                elif re.search(r"\b(previous incident|similar incident|past incident|any prior incidents|was there a previous incident|has this happened before)\b", prompt_lower):
                    return f"**Previous Incidents**: {news_context_en['previous_incident']}"

                elif re.search(r"\b(bullet point|bullet point summary|key points|main points|highlights|key takeaways)\b", prompt_lower):
                    return "**Key Points Summary**:\n" + "\n".join([f"- {point}" for point in news_context_en['bullet_summary']])

                elif re.search(r"\b(emphasize|highlight|main takeaway|important takeaway|key message)\b", prompt_lower):
                    return ("**Key Takeaway**: 15 people injured, two critically, in a military exercise accident caused by wrong coordinates. Explosive dropped on a civilian area.")

                elif re.search(r"\b(quiz|question|test|challenge|ask)\b", prompt_lower):
                    return (
                        "**Quiz Question**: What was the primary cause of the explosion?\n"
                        "A. Weather factors\n"
                        "B. Pilot error (Correct)\n"
                        "C. Technical malfunction\n"
                        "D. Military conflict"
                    )

                elif re.search(r"\b(external link|read more|full article|more details|continue reading|full source)\b", prompt_lower):
                    return f"**Read more**: ({news_context_en['external_link']})"

                elif re.search(r"\b(update|latest update|investigation update|news update)\b", prompt_lower):
                    return f"**Investigation Update**: {news_context_en['investigation_update']}"

                elif re.search(r"\b(related|related news|related articles|similar news|news related)\b", prompt_lower):
                    return "**Related News**:\n" + "\n".join([f"- {title}" for title in news_context_en['related_news']])
                
                elif re.search(r"\b(image|pictures|photos|visuals|media|pic)\b", prompt_lower):
                    return f"**Image**:\n![Image 1]({news_context_en['images']})"

                elif re.search(r"\b(who|what|when|where|how|why)\b", prompt_lower):
                    return (
                        "This chatbot can answer questions about the news article, such as:\n"
                        "- What's the title?\n"
                        "- Who is the author?\n"
                        "- When was it published?\n"
                        "- Where did this incident happen?\n"
                        "- What is this news about?\n"
                        "- What caused the incident?\n"
                        "- Were there any casualties?\n"
                        "- Was there any damage?\n"
                        "- What is the investigation response?\n"
                        "- Were exercises suspended?\n"
                        "- Was there a similar past incident?\n"
                        "- Show me the key points summary.\n"
                        "- Show the key takeaway.\n"
                        "- Show related news.\n"
                        "- Take the quiz.\n"
                        "- Show external links or updates."
                    )
                


    # Chat function section (timing included inside function)
    def chat(prompt: str):
        st_c_chat.chat_message("user",avatar=user_image).write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = generate_response(prompt)
        # response = f"You type: {prompt}"
        st.session_state.messages.append({"role": "assistant", "content": response})
        st_c_chat.chat_message("assistant").write_stream(stream_data(response))

    
    if prompt := st.chat_input(placeholder=placeholderstr, key="chat_bot"):
        chat(prompt)

if __name__ == "__main__":
    main()




# 根據語言設定不同的顯示文字
if lang_setting == "English":
    title_text = f"💬 {user_name}'s News Chatbot"
    desc_text = "Here’s a news article for you. Feel free to ask anything about it—just give it a try! (This is a simple chatbot that doesn’t use the OpenAI API, but gives you custom responses.))"
else:  # 繁體中文
    title_text = f"💬 {user_name} 新聞特派員"
    desc_text = "小小新聞特派員上線，我提供了一則新聞，對於新聞內容有任何好奇的地方，可以盡量問我～我會盡力解答的！(這是一個不使用 OpenAI API 的簡易聊天機器人，提供客製化的回應。)"



