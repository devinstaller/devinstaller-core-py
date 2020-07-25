##################################
Error codes
##################################

.. _specification-errors:

**********************
Specification errors
**********************

.. exec::
   from devinstaller import exceptions as e
   for key, value in e.spec_errors.items():
      print("\n")
      print(f".. _error-code-{key}:")
      print(f"\n{key}")
      print("==================")
      print(f"{value}")

.. _devinstaller-errors:

**********************
Devinstaller errors
**********************

.. exec::
   from devinstaller import exceptions as e
   for key, value in e.dev_errors.items():
      print("\n")
      print(f".. _error-code-{key}:")
      print(f"\n{key}")
      print("==================")
      print(f"{value}")
