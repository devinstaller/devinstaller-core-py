"""The main place where all devinstaller modules are imported so that they can be used by third party
"""

import pluggy

hookimpl = pluggy.HookimplMarker("devinstaller")
"""Marker to be imported and used in plugins (and for own implementations)"""
