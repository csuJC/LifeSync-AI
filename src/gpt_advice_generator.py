import openai
from config import OPENAI_API_KEY, GPT_VERSION, SCHEDULE_PROMPT, PRESENT_LOCATION, USER_CAREER

def generate_advice_with_gpt(data, advice_part):
    print("\nGenerating advice with gpt...\n")
    try:
        openai.api_key = OPENAI_API_KEY
        # 根据advice_part变量来确定需要生成的建议部分
        parts = {
            "1": "请在一个h2段落内总结：今天天气情况，然后给我当天的穿搭建议、出行建议及注意事项（可能包括穿搭、防晒、雨具、防风等等）。",
            "2": "请在一句话内总结我的今日任务。",
            "3": "请结合现实作息和工作时间，确定这些任务的优先次序并提出任务时间安排建议。我只需要你提供具体、美观且详细的时间表。把任务详情和注意事项用小字写在时间轴里面并告诉我具体怎么做。",
            "4": "请在一个h2段落内总结：如果未来有需要提前花时间准备的任务，而且今天预估在准备周期中，请提醒我并告诉我怎么做。如果今天不在准备周期，就不用说。",
            "5": "请在一个h2段落内总结：你觉得要完成这些还需要注意什么？只用告诉我紧急且必须注意的事项。"
        }
        # 构建提示词前缀
        prompt_prefix = f"我是{USER_CAREER}，我住在{PRESENT_LOCATION}。\n"
        # 根据选择的部分添加到提示词
        prompt = prompt_prefix + parts[advice_part] + "\n\n"
        # 根据选择的部分添加相关信息
        if advice_part == "1":
            prompt += f"以下是当日天气：\n{data}。\n\n"
        elif advice_part == "2" or advice_part == "3":
            prompt += f"以下是任务安排：\n{data}。\n"
            if advice_part == "3":
                prompt += f"此外，如果没有被上述安排打断的话，{SCHEDULE_PROMPT}，如果和上述时间冲突就作废。\n\n"
        elif advice_part == "4":
            prompt += f"以下是未来任务安排：\n{data}。\n\n"
        elif advice_part == "5":
            prompt += f"\n{data}。\n\n"

        print(prompt)
        print("Waiting for response...\n")
        # 系统提示词
        response = openai.ChatCompletion.create(
            model=GPT_VERSION,
            messages=[
                {"role": "system", "content": f"你是秘书，你正在向雇主做早晨的汇报，协助他规划一整天的时间安排。请在汇报时体现出秘书的专业性和对他的关心，并使用中文。请用HTML格式（不要CSS），只要body部分。包括一个h2主标题和其余内容，不要任何寒暄，不要任何称呼，不要任何问候语或开场白。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4096,  
            temperature = 0.3 # more accurate
        )
        print("Generated.\n")
        print(response['choices'][0]['message']['content'].strip() if response['choices'] else "No guidance provided.")
        return response['choices'][0]['message']['content'].strip() if response['choices'] else "No guidance provided."
    except Exception as e:
        print(f"Error interacting with OpenAI GPT: {e}")
        return "There was an error generating advice."