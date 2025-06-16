from __future__ import annotations

from typing import Any

from bot import BotService
from operator_service import OperatorService
from langgraph.graph import Graph, END
import argparse


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--draw-graph",
        action="store_true",
        help="Save workflow graph as workflow.png and exit.",
    )
    args = parser.parse_args()

    def save_graph(graph: Graph, path: str = "workflow.png") -> None:
        """Render the workflow to a PNG file if pygraphviz is available."""
        try:
            import pygraphviz as pgv
        except ImportError:
            print("pygraphviz がインストールされていないため、グラフを保存できません。")
            return

        g = pgv.AGraph(directed=True)
        for node in graph.nodes:
            label = "START" if node == "__start__" else "END" if node == "__end__" else node
            g.add_node(label)
        for src, dst in graph.edges:
            src_label = "START" if src == "__start__" else "END" if src == "__end__" else src
            dst_label = "START" if dst == "__start__" else "END" if dst == "__end__" else dst
            g.add_edge(src_label, dst_label)
        for src, branches in graph.branches.items():
            for cond, branch in branches.items():
                if branch.ends:
                    for key, dest in branch.ends.items():
                        dst_label = "END" if dest == "__end__" else dest
                        g.add_edge(src, dst_label, label=str(key))
                if branch.then:
                    dst_label = "END" if branch.then == "__end__" else branch.then
                    g.add_edge(src, dst_label, label=str(cond))
        g.layout("dot")
        g.draw(path)

    bot = BotService()
    operator = OperatorService()

    def bot_node(data: dict[str, str]) -> dict[str, Any]:
        message = data["message"]
        response, confidence = bot.generate_response(message)
        return {"message": message, "response": response, "confidence": confidence}

    def needs_operator(data: dict[str, Any]) -> bool:
        message = data["message"]
        for kw in ("OP", "オペレーター", "人間"):
            if kw in message:
                return True
        return False

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

    if args.draw_graph:
        save_graph(workflow)
        print("workflow.png を生成しました。")
        return

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
