from __future__ import annotations

from typing import Any

from bot import BotService
from handoff import HandoffService
from operator_service import OperatorService
from langgraph.graph import Graph, END


def main() -> None:
    bot = BotService()
    handoff = HandoffService()
    operator = OperatorService()

    def bot_node(data: dict[str, str]) -> dict[str, Any]:
        message = data["message"]
        response, confidence = bot.generate_response(message)
        return {"message": message, "response": response, "confidence": confidence}

    def needs_operator(data: dict[str, Any]) -> bool:
        return handoff.needs_handoff(data["message"], float(data["confidence"]))

    def operator_node(data: dict[str, Any]) -> dict[str, str]:
        reply = operator.handle_message(data["message"])
        return {"final": f"オペレーター: {reply}"}

    def output_node(data: dict[str, Any]) -> dict[str, str]:
        return {"final": f"Bot({data['confidence']:.1f}): {data['response']}"}

    workflow = Graph()
    workflow.add_node("bot", bot_node)
    workflow.add_node("operator", operator_node)
    workflow.add_node("output", output_node)
    workflow.set_entry_point("bot")
    workflow.add_conditional_edges("bot", needs_operator, path_map={True: "operator", False: "output"})
    workflow.add_edge("operator", END)
    workflow.add_edge("output", END)

    app = workflow.compile()

    print("LangGraph チャットを開始します。終了するには 'exit' を入力してください。")
    while True:
        user_message = input("あなた: ")
        if user_message.strip().lower() == "exit":
            print("終了します。")
            break
        result = app.invoke({"message": user_message})
        print(result["final"])


if __name__ == "__main__":
    main()
