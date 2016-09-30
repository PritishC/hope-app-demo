from .settings import *
from .aws_settings import *
import raven
from .logging import *

DEBUG = False
SECRET_KEY = ':<qFAR~0^b>*A;[WJj3ne*Fu{W5nvj<yVcEwp{Ag{r}RO$+<^^'
ALLOWED_HOSTS = ['*']

# Raven/Sentry
RAVEN_CONFIG = {
    'dsn': 'https://bfb14522923f4171860e74c7b0f54310:9a4841d1087c45e5a20b4a18f060722c@app.getsentry.com/85428',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(os.path.dirname(os.path.abspath(os.curdir))),
}
