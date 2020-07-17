##################################
Error codes
##################################

.. exec::
   from devinstaller import exceptions as e
   for key, value in e.rules.items():
      print("\n")
      print(f".. _error-code-{key}:")
      print(f"\n{key}")
      print("==================")
      print(f"{value}")
