class Utilities:
    @staticmethod
    def token_to_base64(token):
        import base64
        # Add colon after token for Basic Auth (token:)
        auth_str = f"{token}:"
        return base64.b64encode(auth_str.encode()).decode('utf-8')