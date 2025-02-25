import os
import requests
from loguru import logger


def parse_txt_file(file_path):
    if not os.path.exists(file_path):
        logger.error(f"文件 '{file_path}' 未找到。")
        exit(1)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
            if not lines:
                logger.error("文件中没有有效数据。")
                exit(1)
            return lines
    except Exception as e:
        logger.error(f"读取文件 '{file_path}' 时发生错误：{e}")
        exit(1)


if __name__ == '__main__':
    address_list = parse_txt_file("./email.txt")
    for line in address_list:
        logger.info(f"正在处理行：{line}")
        try:
            # 使用"----"分割行
            parts = line.split('----')
            if len(parts) != 2:
                logger.error(f"跳过无效行：{line}")
                continue

            email = parts[0].strip()
            address = parts[1].strip()

            if not email or not address:
                logger.error(f"跳过无效行：{line}")
                continue

            data = {
                "waitlist_id": "25428",
                "email": email,
                "referral_link": "https://tallys.talus.network/waitlist",
                "first_name": address
            }

            # 确认正确的API端点URL
            url = "https://api.getwaitlist.com/api/v1/signup"  # 假设正确的路径是/register

            resp = requests.post(url=url, json=data, timeout=30)
            resp.raise_for_status()

            if resp.ok:
                resp_text = resp.text
                logger.info(f"服务器返回的原始响应内容：{resp_text}")

                # 解析响应内容
                try:
                    response_data = resp.json()
                    if "error" in response_data:
                        logger.error(f"地址：{address} 失败，原因：{response_data['error']}")
                    else:
                        # 处理成功的情况
                        logger.success(f"地址：{address} 成功，referral_link：{response_data.get('referral_link', '')}")
                except ValueError:
                    logger.error(f"地址：{address} 失败，原因：无法解析响应内容")

        except requests.exceptions.RequestException as e:
            logger.error(f"请求发生异常：{e}")
        except Exception as e:
            logger.error(f"发生未知异常：{e}")
