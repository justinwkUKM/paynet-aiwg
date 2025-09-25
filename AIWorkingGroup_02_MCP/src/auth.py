from mcp.server.auth.provider import AccessToken, TokenVerifier


class SimpleTokenVerifier(TokenVerifier):
    """Simple token verifier for demonstration."""

    async def verify_token(self, token: str) -> AccessToken | None:
        if token == "sk-1234":
            return AccessToken(
               token=token,
               client_id="demo-client",
               subject="user1",
               scopes=["user"],
               expires_in=3600,
            )
        return None