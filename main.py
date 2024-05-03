# from lxml import etree
import json
import random
import time

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
def chatgpt3_5(question: str) -> str:
    OPENAI_API_KEY = 'sk-X5mQrrIlAIYjtCsF22C1E1775c5048D1A21b5262367545A6'
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'user', 'content': question + "已大学生视角回答问题,不用介绍你是什么模型。"}]}
    response = requests.post('https://lite.chsdw.top/v1/chat/completions', headers=headers,
                             data=json.dumps(data)).json()
    return response['choices'][0]['message']['content']


def reply():
    # 切换到新的标签
    page = driver.window_handles[-1]
    driver.switch_to.window(page)
    # 等待问题加载出来
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div/div[2]/div[1]/div/ul/li[2]/div[2]/span")))
    except:
        print('元素未渲染')
        driver.quit()
    # 获取问题
    issues_list = driver.find_elements(By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div/div[2]/div[1]/div/ul/li")
    issues_list.pop(0)
    # 随机回答20道题
    random.shuffle(issues_list)
    # 遍历每个问题
    for issues_bar in issues_list[:41]:
        # 切换到问题页面
        driver.switch_to.window(page)
        print('进入问题')
        issues_element = issues_bar.find_element(By.TAG_NAME, "span")
        issues = issues_element.text
        issues_element.click()
        # 切换页面
        page2 = driver.window_handles[-1]
        driver.switch_to.window(page2)
        # 判断是否回答
        time.sleep(2)
        answer_button = EC.invisibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div[4]/span"))
        if answer_button(driver):
            continue
        else:
            driver.find_element(By.XPATH, "/html/body/div[2]/div/div[4]").click()

        # 获取问题答案
        answer = chatgpt3_5(issues)
        # 填入答案
        answer_window = driver.find_element(By.XPATH,
                                            "/html/body/div[2]/div/div[5]/div/div/div[2]/div[1]/div[1]/div/textarea")
        answer_window.send_keys(answer)
        # 提交
        driver.find_element(By.XPATH, "/html/body/div[2]/div/div[5]/div/div/div[2]/div[1]/div[2]/div").click()
        time.sleep(2)


def run():
    # 进入答题
    class_list = driver.find_elements(By.XPATH,
                                      "/html/body/div[1]/section/div[2]/section[2]/section/div/div/div/div[2]/div[1]/div[2]/ul")
    class_page = driver.window_handles[-1]
    for i in class_list:
        driver.switch_to.window(class_page)
        i.find_elements(By.TAG_NAME, "a")[1].click()
        # 回答问题
        reply()
    driver.quit()


if __name__ == '__main__':
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.get('https://onlineweb.zhihuishu.com/onlinestuh5')
    # 密码登录
    with open('./config.json', "r", encoding="utf-8") as f:
        user_config = json.load(f)
    if user_config['isPasswordLogin']:
        user = driver.find_element(By.ID, "lUsername")
        user.send_keys(user_config['account'])
        password = driver.find_element(By.ID, "lPassword")
        password.send_keys(user_config['password'])
        driver.find_element(By.XPATH, "/html/body/div[6]/div/form/div[1]/span").click()
    else:
        print('请扫码')
        driver.execute_script("window.open('https://passport.zhihuishu.com/login?service=https%3A%2F%2Fonlineservice-api.zhihuishu.com%2Fgateway%2Ff%2Fv1%2Flogin%2Fgologin%3Ffromurl%3Dhttps%253A%252F%252Fonlineweb.zhihuishu.com%252Fonlinestuh5#qrCodeLogin','_self')")
    try:
        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[1]/section/div[2]/section[2]/section/div/div/div/div[2]/div[1]/div[2]/ul")))
    except Exception:
        print("不通过,关闭浏览器")
        driver.quit()
    run()
