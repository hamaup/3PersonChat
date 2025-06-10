from bot import BotService
from handoff import HandoffService
from operator_service import OperatorService


def main():
    bot = BotService()
    handoff = HandoffService()
    operator = OperatorService()

    print("チャットを開始します。終了するには 'exit' を入力してください。")

    while True:
        user_message = input("あなた: ")
        if user_message.strip().lower() == "exit":
            print("終了します。")
            break

        response, confidence = bot.generate_response(user_message)
        if handoff.needs_handoff(user_message, confidence):
            operator_reply = operator.handle_message(user_message)
            print("オペレーター: " + operator_reply)
        else:
            print(f"Bot({confidence:.1f}): {response}")


if __name__ == "__main__":
    main()
