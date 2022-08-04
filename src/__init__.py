"""Main survey file.
"""
import os

from flask_login import current_user
from hemlock import User, Page
from hemlock.functional import compile, validate, test_response
from hemlock.questions import Check, Input, Label, Range, Select, Textarea
from hemlock import utils
from sqlalchemy_mutable.utils import partial


class Enemy:
    def __init__(self, health, stamina):
        self.health = health
        self.stamina = stamina


@User.route("/survey")
def seed():
    """Creates the main survey branch.

    Returns:
        List[Page]: List of pages shown to the user.
    """
    current_user.params = {
        "health": 50,
        "stamina": 40,
        "enemy": Enemy(50, 40)
    }
    return make_next_round(None)

def make_next_round(root):
    return [
        Page(
            action := Check(
                """
                Something is happening!

                What would you like to do?
                """,
                [
                    "Attack",
                    "Shield",
                    "Roll",
                    "Wait",
                    "Stats",
                    "Quit"
                ]
            )
        ),
        Page(
            Label(compile=partial(display_action, action)),
            navigate=make_next_round
        )
    ]


def display_action(label, action):
    if action.response == "Attack":
        current_user.params["stamina"] -= 18
        current_user.params["enemy"].health -= 25
    elif action.response == "Shield":
        current_user.params["stamina"] -= 6
    elif action.response == "Wait":
        current_user.params["stamina"] += 8

    label.label = (
        f"""
        Your action was {action.response}.

        Your health is {current_user.params["health"]}.

        Your stamina is {current_user.params["stamina"]}.

        Your enemy's health is {current_user.params["enemy"].health}.
        """
    )
