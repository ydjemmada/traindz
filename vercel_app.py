import os
import sys

# Add the 'backend' directory to the Python path
# This assumes vercel_app.py is in the root and backend is a subdirectory
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sntf_project.settings")

app = get_wsgi_application()
