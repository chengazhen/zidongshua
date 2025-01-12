from DrissionPage import ChromiumOptions, ChromiumPage
from datetime import datetime
import random
import string
import time
import json


class TlineRegister:
    def __init__(self):
        self.page = None
        self.base_url = "https://www.tline.website/auth/login"
        self.accounts_file = "registered_accounts.json"

    def generate_random_info(self):
        """生成随机用户信息"""
        # 只使用字母和数字
        letters = string.ascii_letters  # 包含大小写字母
        digits = string.digits
        chars = letters + digits

        # 随机生成8-16位的长度
        username_length = random.randint(8, 16)

        # 确保至少包含一个字母和一个数字
        username = [
            random.choice(letters),  # 确保至少有一个字母
            random.choice(digits),  # 确保至少有一个数字
        ]

        # 生成剩余的字符
        remaining_length = username_length - 2
        username.extend(random.choices(chars, k=remaining_length))

        # 打乱顺序
        random.shuffle(username)

        # 转换为字符串
        username = "".join(username)

        password = "a327924366"
        return username, password

    def save_account(self, username, password, subscribe_url=None, status="success"):
        """保存账号信息到JSON文件"""
        try:
            try:
                with open(self.accounts_file, "r", encoding="utf-8") as f:
                    accounts = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                accounts = []

            account_info = {
                "username": username,
                "password": password,
                "security_question": "你最喜欢的甜点是什么？",
                "security_answer": "提拉米苏",
                "register_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": status,
                "subscribe_url": subscribe_url,
            }
            accounts.append(account_info)

            with open(self.accounts_file, "w", encoding="utf-8") as f:
                json.dump(accounts, f, ensure_ascii=False, indent=4)

            print(f"账号信息已保存到 {self.accounts_file}")
        except Exception as e:
            print(f"保存账号信息时出错: {str(e)}")

    def random_sleep(self, min_seconds=1, max_seconds=3):
        """随机等待一段时间"""
        time.sleep(random.uniform(min_seconds, max_seconds))

    def human_like_type(self, element, text):
        """模拟人类输入"""
        for char in text:
            element.input(char)
            time.sleep(random.uniform(0.1, 0.3))

    def clear_input(self, element):
        """清空输入框"""
        element.click()
        self.random_sleep(0.2, 0.5)
        element.clear()
        self.random_sleep(0.2, 0.5)

    def register_one(self):
        """注册一个账号"""
        try:
            # 配置浏览器
            co = ChromiumOptions()
            co.set_argument("--disable-blink-features=AutomationControlled")
            co.set_argument("--disable-extensions")
            co.set_argument("--no-sandbox")
            co.set_argument("--disable-gpu")

            # 创建页面实例
            self.page = ChromiumPage(addr_or_opts=co)

            # 打开登录页面
            print("步骤1：打开登录页面")
            self.page.get(self.base_url)
            self.random_sleep(2, 4)

            # 点击立即注册按钮
            print("正在查找登录页面上的立即注册按钮...")
            register_button = self.page.ele(
                'xpath://div[contains(@class, "btn-box")]//button[text()="立即注册"]'
            )
            if register_button:
                register_button.click()
                self.random_sleep(2, 3)
            else:
                print("未找到立即注册按钮")
                return False

            # 填写注册信息
            print("\n步骤2：填写注册信息")
            username, password = self.generate_random_info()

            # 输入账号
            username_input = self.page.ele(
                'css:input[placeholder="账号"], input[placeholder="帳號"]'
            )
            if username_input:
                self.clear_input(username_input)  # 先清空输入框
                self.human_like_type(username_input, username)
                self.random_sleep()

            # 输入密码
            password_inputs = self.page.eles('css:input[type="password"]')
            if len(password_inputs) >= 2:
                # 输入密码
                self.human_like_type(password_inputs[0], password)
                self.random_sleep()
                # 确认密码
                self.human_like_type(password_inputs[1], password)
                self.random_sleep()

            # 选择密码找回问题
            select_div = self.page.ele("css:div.el-select")
            if select_div:
                select_div.click()
                self.random_sleep()

                # 选择第一个选项
                first_option = self.page.ele(
                    "css:li.el-select-dropdown__item:first-of-type"
                )
                if first_option:
                    first_option.click()
                    self.random_sleep()

            # 输入答案
            answer_input = self.page.ele('css:input[placeholder="答案"]')
            if answer_input:
                self.human_like_type(answer_input, "提拉米苏")
                self.random_sleep()

            # 同意用户协议
            checkbox = self.page.ele('css:input[type="checkbox"]')
            if checkbox:
                checkbox.click()
                self.random_sleep()

            # 点击注册按钮
            submit_button = self.page.ele("css:button.el-button.form-btn")
            if submit_button:
                submit_button.click()
                self.random_sleep(3, 5)

            # 获取订阅信息
            subscribe_button = self.page.ele("css:button.btn-clash")
            if subscribe_button:
                subscribe_button.click()
                self.random_sleep(2, 3)

                copy_button = self.page.ele(
                    "css:button.dropdown-item.copy-text.copy-btn"
                )
                if copy_button:
                    subscribe_text = copy_button.attr("data-clipboard-text")
                    print(f"订阅文本: {subscribe_text}")

            print(f"注册成功！\n用户名: {username}\n密码: {password}")
            self.save_account(username, password, subscribe_text)
            return True

        except Exception as e:
            print(f"注册过程中出现错误: {str(e)}")
            if "username" in locals():
                self.save_account(username, password, None, "failed")
            return False
        finally:
            if self.page:
                self.page.quit()

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
            if i < count - 1:
                self.random_sleep(3, 6)

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
