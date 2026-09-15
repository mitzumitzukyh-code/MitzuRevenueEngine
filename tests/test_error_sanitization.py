from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient


def test_unhandled_error_response_does_not_leak_exception_detail():
    app = FastAPI()

    @app.exception_handler(Exception)
    async def handler(request, exc):
        return JSONResponse(status_code=500, content={"detail": "internal server error"})

    @app.get("/boom")
    def boom():
        raise RuntimeError("database-password-should-never-leak")

    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/boom")
    assert response.status_code == 500
    assert response.json() == {"detail": "internal server error"}
    assert "database-password" not in response.text
