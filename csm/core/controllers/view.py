#!/usr/bin/env python3

"""
 ****************************************************************************
 Filename:          view.py
 Description:       Common base view

 Creation Date:     10/16/2019
 Author:            Naval Patel

 Do NOT modify or remove this copyright and confidentiality notice!
 Copyright (c) 2001 - $Date: 2015/01/14 $ Seagate Technology, LLC.
 The code contained herein is CONFIDENTIAL to Seagate Technology, LLC.
 Portions are also trade secret. Any use, duplication, derivation, distribution
 or disclosure of this code, for any reason, not expressly authorized is
 prohibited. All other rights are expressly reserved by Seagate Technology, LLC.
 ****************************************************************************
"""
from aiohttp import web


class CsmView(web.View):

    # derived class will provide service amd service_disatch  details
    _service = None
    _service_dispatch = {}

    # common routes to used by subclass
    _app_routes = web.RouteTableDef()

    def __init__(self, request):
        super(CsmView, self).__init__(request)

    def validate_get(self):
        pass

    async def get(self):
        """"
        Generic get call implementation
        """
        self.validate_get()
        if self.request.match_info:
            match_info = {}
            match_info.update(self.request.match_info)
            response_obj = await self._service_dispatch['get_specific'](**match_info)
        else:
            query_parameter = {}
            query_parameter.update(self.request.rel_url.query)
            response_obj = await self._service_dispatch['get'](**query_parameter)
        return response_obj