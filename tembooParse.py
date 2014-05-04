# Instantiate the Choreo, using a previously instantiated TembooSession object, eg:

ACCOUNT_NAME = "mattgiguere"
APP_NAME = "myFirstApp"
APP_KEY = "b2d7c23af278460fbfc445a9e0e05c25"

# Instantiate the Choreo, using a previously instantiated TembooSession object, eg:
from temboo.core.session import TembooSession
from temboo.Library.Parse.Objects import RetrieveObject
session = TembooSession(ACCOUNT_NAME, APP_NAME, APP_KEY)
retrieveObjectChoreo = RetrieveObject(session)

# Get an InputSet object for the choreo
retrieveObjectInputs = retrieveObjectChoreo.new_input_set()

# Set inputs
APPLICATION_ID = "aOmfYWxfdaqrD9aMOtp7a3UinrfOAqNMyVxIjLzm"
REST_API_KEY = "AkHGq6xQCd67e8Tj9xcXY3PirvzZstur7DBaURuX"
MASTER_KEY = "0sbEqmUiRqarMV8zV5WN18pvOaS0N5O2ItUxbS7q"

retrieveObjectInputs.set_RESTAPIKey(REST_API_KEY)
retrieveObjectInputs.set_ObjectID("")
retrieveObjectInputs.set_ApplicationID(APPLICATION_ID)
retrieveObjectInputs.set_ClassName("QuestionAnswerKey")

# Execute choreo
retrieveObjectResults = retrieveObjectChoreo.execute_with_results(retrieveObjectInputs)

print(retrieveObjectResults)