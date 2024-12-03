import asyncio

from posts.inner_functions import send_telegram_message


def send_test_message():
    results = asyncio.run(send_telegram_message('Message to test chat_bot'))
    print(results)

if __name__ == "__main__":
    send_test_message()


