from devinstaller_core import extension as ex
from devinstaller_core import settings as s
from devinstaller_core import utilities as u

CODE = "py"
NAME = "Python"


class ExtSpec(ex.ExtSpec):
    LANGUAGE_CODE = CODE
    LANGUAGE_NAME = NAME

    def run(self, command: str):
        """Execute the given string in python
        """

        def new_print(*args, **kwargs):
            verbose = s.settings.DDOT_VERBOSE
            if verbose:
                print(*args, **kwargs)
            return None

        # safe_python = s.settings.DDOT_SAFE_PYTHON
        # safe_python = True
        # if safe_python:
        #     proceed = u.ui.confirm(f"Proceed with: {command}")
        #     if not proceed:
        #         return
        exec(command, {"print": new_print})


class ExtProg(ex.ExtProg):
    LANGUAGE_CODE = CODE
    LANGUAGE_NAME = NAME

    def launch(self, python_fun_name: str):
        pass
