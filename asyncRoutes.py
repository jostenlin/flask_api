from flask_restful import Resource
from flask import request

permissionRouter = {
    "path": "/permission",
    "meta": {"title": "权限管理", "icon": "lollipop", "rank": 10},
    "children": [
        {
            "path": "/permission/page/index",
            "name": "PermissionPage",
            "meta": {"title": "页面权限111", "roles": ["admin", "common"]},
        },
        {
            "path": "/permission/button/index",
            "name": "PermissionButton",
            "meta": {
                "title": "按钮权限222",
                "roles": ["admin", "common"],
                "auths": ["btn_add", "btn_edit", "btn_delete"],
            },
        },
    ],
}


class AsyncRoutes(Resource):
    def get(self):
        return {"success": True, "data": [permissionRouter]}
