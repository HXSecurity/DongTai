import json

from django.conf import settings
from django.contrib.auth import SESSION_KEY
from django.contrib.sessions.backends.db import SessionStore as DBSessionStore
from django.contrib.sessions.base_session import AbstractBaseSession
from django.db import models

from dongtai_common.models.profile import IastProfile
from dongtai_common.models.user import User

SESSION_EXPIRY_PROFILE_KEY = "session_expiry"


class Session(AbstractBaseSession):
    user = models.ForeignKey(User, models.DO_NOTHING, null=True, db_constraint=False)

    @classmethod
    def get_session_store_class(cls):
        return SessionStore

    class Meta(AbstractBaseSession.Meta):
        db_table = "iast_session"


class SessionStore(DBSessionStore):
    @classmethod
    def get_model_class(cls):
        return Session

    def create_model_instance(self, data):
        """
        Return a new instance of the session model object, which represents the
        current session state. Intended to be used for saving the session data
        to the database.
        """
        return self.model(
            user_id=self.get(SESSION_KEY),
            session_key=self._get_or_create_session_key(),  # type: ignore
            session_data=self.encode(data),
            expire_date=self.get_expiry_date(),
        )

    def get_session_cookie_age(self):
        profile = IastProfile.objects.filter(key=SESSION_EXPIRY_PROFILE_KEY).values_list("value", flat=True).first()
        if profile is None:
            return settings.SESSION_COOKIE_AGE
        return json.loads(profile)[SESSION_EXPIRY_PROFILE_KEY]
