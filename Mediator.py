from __future__ import annotations
from abc import ABC
import gradio as gr


class Mediator(ABC):
    """
    The Mediator interface declares a method used by components to notify the
    mediator about various events. The Mediator may react to these events and
    pass the execution to other components.
    """

    def notify(self, sender: object, event: str) -> None:
        pass

class ConcreteMediator(Mediator):
    def __init__(self) -> None:
        pass
    def notify(self, sender: object, event: str) -> None:
        if event == "A":
            print("Mediator reacts on A and triggers following operations:")
        elif event == "D":
            print("Mediator reacts on D and triggers following operations:")

    def getPosition(self, text, request: gr.Request):
        if request:
            floor = request.query_params.get("floor")
            x = request.query_params.get("x")
            y = request.query_params.get("y")
            print("floor:", floor, ", x:",x,", y:",y)
        return text
mediator = ConcreteMediator() 


io = gr.Interface(mediator.getPosition, "textbox", "textbox").launch(share=True)