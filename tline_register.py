from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import random
import string
import time
import json
from datetime import datetime

class TlineRegister:
    def __init__(self):
        self.driver = None
        self.base_url = "https://www.tline.website/auth/login"
        self.accounts_file = "registered_accounts.json"
        
    def generate_random_info(self):
        """生成随机用户信息"""
        # 生成8位随机用户名（字母+数字）
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        
        # 使用固定密码
        password = 'a327924366'
        
        return username, password
    
    def save_account(self, username, password, status="success"):
        """保存账号信息到JSON文件"""
        try:
            try:
                with open(self.accounts_file, 'r', encoding='utf-8') as f:
                    accounts = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                accounts = []
            
            account_info = {
                "username": username,
                "password": password,
                "security_question": "你最喜欢的甜点是什么？",
                "security_answer": "提拉米苏",
                "register_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": status
            }
            
            accounts.append(account_info)
            
            with open(self.accounts_file, 'w', encoding='utf-8') as f:
                json.dump(accounts, f, ensure_ascii=False, indent=4)
                
            print(f"账号信息已保存到 {self.accounts_file}")
        except Exception as e:
            print(f"保存账号信息时出错: {str(e)}")

    def wait_and_find_element(self, by, value, timeout=10, description="元素"):
        """等待并查找元素，带有重试机制"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((by, value))
                )
                print(f"找到{description}")
                return element
            except:
                print(f"未找到{description}，重试中...")
                time.sleep(1)
        raise TimeoutException(f"超时未找到{description}")

    def clear_input(self, element):
        """清空输入框"""
        # 先点击输入框，确保它被激活
        element.click()
        time.sleep(0.5)
        
        # 使用Ctrl+A全选
        element.send_keys(Keys.CONTROL + "a")
        time.sleep(0.5)
        
        # 按删除键
        element.send_keys(Keys.DELETE)
        time.sleep(0.5)
        
        # 再次清空以确保
        element.clear()
        time.sleep(0.5)
        
    def register_one(self):
        """注册一个账号"""
        try:
            self.driver = webdriver.Chrome()
            self.driver.maximize_window()  # 最大化窗口
            
            # 第一步：打开登录页面并点击立即注册
            print("步骤1：打开登录页面")
            self.driver.get(self.base_url)
            time.sleep(3)
            
            # 在登录页面找到并点击立即注册按钮
            print("正在查找登录页面上的立即注册按钮...")
            try:
                # 等待页面加载完成
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "pic-box"))
                )
                
                # 使用精确的XPath定位立即注册按钮
                register_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'btn-box')]//button[text()='立即注册']"))
                )
                
                print("找到立即注册按钮，正在点击...")
                register_button.click()
                time.sleep(3)  # 增加等待时间
                
            except Exception as e:
                print(f"点击立即注册时出错: {str(e)}")
                return False
            
            # 第二步：在注册页面填写信息
            print("\n步骤2：填写注册信息")
            try:
                # 生成随机用户信息
                username, password = self.generate_random_info()
                
                # 使用新的等待和查找方法
                # 账号输入框
                username_input = self.wait_and_find_element(
                    By.CSS_SELECTOR, 
                    "input[placeholder='账号'], input[placeholder='帳號']",
                    description="账号输入框"
                )
                
                # 清空并输入账号
                print("清空账号输入框...")
                self.clear_input(username_input)
                print("输入账号...")
                username_input.send_keys(username)
                time.sleep(1)
                
                # 密码输入框 - 尝试多个可能的placeholder
                password_input = self.wait_and_find_element(
                    By.CSS_SELECTOR, 
                    "input[type='password']",
                    description="密码输入框"
                )
                self.clear_input(password_input)
                password_input.send_keys(password)
                time.sleep(1)
                
                # 确认密码输入框 - 使用第二个密码输入框
                password_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='password']")
                if len(password_inputs) >= 2:
                    confirm_password_input = password_inputs[1]
                    self.clear_input(confirm_password_input)
                    confirm_password_input.send_keys(password)
                    time.sleep(1)
                
                # 点击密码找回问题下拉框
                print("点击密码找回问题下拉框...")
                select_div = self.wait_and_find_element(
                    By.CSS_SELECTOR,
                    "div.el-select",
                    description="密码找回问题选择框"
                )
                select_div.click()
                time.sleep(2)  # 等待下拉框展开
                
                # 选择第一个选项
                print("选择第一个问题选项...")
                first_option = self.wait_and_find_element(
                    By.CSS_SELECTOR,
                    "li.el-select-dropdown__item:first-of-type",
                    description="第一个问题选项"
                )
                first_option.click()
                time.sleep(1)
                
                # 输入答案
                print("输入密码找回答案...")
                answer_input = self.wait_and_find_element(
                    By.CSS_SELECTOR,
                    "input[placeholder='答案']",
                    description="密码找回答案输入框"
                )
                self.clear_input(answer_input)
                answer_input.send_keys("提拉米苏")
                time.sleep(1)
                
                # 同意用户协议
                try:
                    agreement_checkbox = self.driver.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
                    agreement_checkbox.click()
                    time.sleep(1)
                except:
                    print("未找到复选框，尝试继续...")
                
                # 点击注册按钮
                print("点击注册按钮...")
                submit_button = self.wait_and_find_element(
                    By.CSS_SELECTOR,
                    "button.el-button.form-btn",
                    description="注册按钮"
                )
                submit_button.click()
                
                # 等待注册成功
                time.sleep(3)
                
                print(f"注册成功！\n用户名: {username}\n密码: {password}")
                self.save_account(username, password)
                return True
                
            except Exception as e:
                print(f"填写注册信息时出错: {str(e)}")
                if 'username' in locals():
                    self.save_account(username, password, "failed")
                return False
            
        except TimeoutException:
            print("页面加载超时")
            if 'username' in locals():
                self.save_account(username, password, "failed")
            return False
        except Exception as e:
            print(f"注册过程中出现错误: {str(e)}")
            if 'username' in locals():
                self.save_account(username, password, "failed")
            return False
        finally:
            if self.driver:
                self.driver.quit()
    
    def batch_register(self, count):
        """批量注册指定数量的账号"""
        success_count = 0
        fail_count = 0
        
        print(f"开始注册 {count} 个账号...")
        
        for i in range(count):
            print(f"\n正在注册第 {i+1}/{count} 个账号...")
            if self.register_one():
                success_count += 1
            else:
                fail_count += 1
            # 每次注册后等待一段时间，避免被封
            if i < count - 1:  # 如果不是最后一个账号，就等待
                time.sleep(random.uniform(3, 6))
        
        print(f"\n注册完成！成功: {success_count} 个，失败: {fail_count} 个")
        print(f"账号信息已保存到 {self.accounts_file}")

if __name__ == "__main__":
    try:
        count = int(input("请输入要注册的账号数量: "))
        if count <= 0:
            raise ValueError("数量必须大于0")
        
        bot = TlineRegister()
        bot.batch_register(count)
    except ValueError as e:
        print(f"输入错误: {str(e)}")
    except Exception as e:
        print(f"程序出错: {str(e)}") 