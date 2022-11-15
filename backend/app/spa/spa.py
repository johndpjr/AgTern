from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response


class SinglePageApplication(StaticFiles):
    async def get_response(self, path: str, scope) -> Response:
        try:
            response = await super().get_response(path, scope)
            if response.status_code == 404:
                response = await super().get_response("index.html", scope)
                response.status_code = 404
                return response
            else:
                return response
        except HTTPException as err:
            if err.status_code == 404:
                response = await super().get_response("index.html", scope)
                response.status_code = 404
                return response
            else:
                raise err
