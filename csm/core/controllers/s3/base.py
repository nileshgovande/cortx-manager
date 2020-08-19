#!/usr/bin/env python3

"""
 ****************************************************************************
 Filename:          base.py
 Description:       Implementation of a base class for all S3 views
                    authenticated with S3 credentials

 Creation Date:     02/14/2020
 Author:            Oleg Babin

 Do NOT modify or remove this copyright and confidentiality notice!
 Copyright (c) 2001 - $Date: 2015/01/14 $ Seagate Technology, LLC.
 The code contained herein is CONFIDENTIAL to Seagate Technology, LLC.
 Portions are also trade secret. Any use, duplication, derivation, distribution
 or disclosure of this code, for any reason, not expressly authorized is
 prohibited. All other rights are expressly reserved by Seagate Technology, LLC.
 ****************************************************************************
"""
from contextlib import contextmanager
from eos.utils.log import Log
from csm.common.errors import CsmInternalError, CsmPermissionDenied
from csm.core.controllers.view import CsmView, CsmHttpException
from csm.core.services.sessions import S3Credentials
from csm.core.services.s3.utils import S3ServiceError


S3_SERVICE_ERROR = 0x3000


class S3BaseView(CsmView):
    """
    Simple base class for any S3 view which works with one service
    """

    def __init__(self, request, service_name):
        super().__init__(request)

        self._service = request.app.get(service_name, None)
        if self._service is None:
            raise CsmInternalError(desc=f"No such service '{service_name}'")

    @contextmanager
    def _guard_service(self):
        try:
            yield None
        except S3ServiceError as error:
            raise CsmHttpException(error.status,
                                   S3_SERVICE_ERROR,
                                   error.code,
                                   error.message)
        else:
            return


class S3AuthenticatedView(S3BaseView):
    """
    Simple base class for any S3 view which requires S3 credentials
    and works with one service
    """

    def __init__(self, request, service_name):
        super().__init__(request, service_name)

        # Fetch S3 access_key, secret_key and session_token from session
        self._s3_session = self.request.session.credentials
        if not issubclass(type(self._s3_session), S3Credentials):
            raise CsmPermissionDenied(desc="Invalid credentials - not S3 Account or IAM User")