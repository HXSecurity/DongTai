#!/usr/bin/env python
import logging

from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema

from dongtai_common.endpoint import R, TalentAdminEndPoint
from dongtai_common.models import User

logger = logging.getLogger("dongtai-webapi")


class UserPasswordReset(TalentAdminEndPoint):
    name = "api-v1-user-password-reset"
    description = _("Reset Password")

    @extend_schema(
        summary=_("Reset Password"),
        tags=[_("User")],
    )
    def post(self, request):
        try:
            user_id = request.data.get("userId")
            if user_id:
                user = User.objects.filter(id=user_id).first()
                if user:
                    username = user.get_username()
                    user.set_password(f"{username}@123")
                    user.save(update_fields=["password"])
                    msg = _("User {} password reset success").format(username)
                    return R.success(msg=msg)
                msg = _("User does not exist")
                logger.warning(msg)
                return R.failure(msg=msg)
            msg = _("UserID is empty")
            logger.error(_("UserID is empty"))
            return R.failure(msg=msg)
        except ValueError:
            msg = _("UserID must be a numeric")
            logger.error(msg, exc_info=True)
        except Exception as e:
            msg = _("Password reset failed, reasons: {E}").format(e)
            logger.error(msg, exc_info=True)
        return R.failure(msg="Password reset failed")
