from flask import Blueprint

from CTFd.models import Challenges, Solves, Flags, db
from CTFd.plugins import register_plugin_assets_directory
from CTFd.plugins.challenges import CHALLENGE_CLASSES, BaseChallenge
from CTFd.plugins.flags import get_flag_class
from CTFd.utils.modes import get_model


class OneBloodValueChallenge(BaseChallenge):
    id = "oneblood"  # Unique identifier used to register challenges
    name = "oneblood"  # Name of a challenge type
    templates = {  # Templates used for each aspect of challenge editing & viewing
        "create": "/plugins/oneblood/assets/create.html",
        "update": "/plugins/oneblood/assets/update.html",
        "view": "/plugins/oneblood/assets/view.html",
    }
    scripts = {  # Scripts that are loaded when a template is loaded
        "create": "/plugins/oneblood/assets/create.js",
        "update": "/plugins/oneblood/assets/update.js",
        "view": "/plugins/oneblood/assets/view.js",
    }
    # Route at which files are accessible. This must be registered using register_plugin_assets_directory()
    route = "/plugins/oneblood/assets/"
    # Blueprint used to access the static_folder directory.
    blueprint = Blueprint(
        "oneblood_challenges",
        __name__,
        template_folder="templates",
        static_folder="assets",
    )
    challenge_model = Challenges  # Use the base Challenges model (no separate table needed)

    @classmethod
    def attempt(cls, challenge, request):
        """
        Check if the submission is correct and if the challenge hasn't been solved yet.
        """
        # Check if challenge has already been solved by anyone
        Model = get_model()
        solve_count = (
            Solves.query.join(Model, Solves.account_id == Model.id)
            .filter(
                Solves.challenge_id == challenge.id,
                Model.hidden == False,
                Model.banned == False,
            )
            .count()
        )

        if solve_count >= 1:
            return False, "Sorry, the flag is already taken!"

        # Check the submission against flags
        data = request.form or request.get_json()
        submission = data["submission"].strip()
        flags = Flags.query.filter_by(challenge_id=challenge.id).all()

        for flag in flags:
            flag_class = get_flag_class(flag.type)
            if flag_class.compare(flag, submission):
                return True, "Correct"

        return False, "Incorrect"


def load(app):
    CHALLENGE_CLASSES["oneblood"] = OneBloodValueChallenge
    register_plugin_assets_directory(
        app, base_path="/plugins/oneblood/assets/"
    )
