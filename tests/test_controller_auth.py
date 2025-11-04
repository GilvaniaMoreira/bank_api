"""Testes unitários para o controller de autenticação."""
import pytest
from unittest.mock import patch, MagicMock

from src.schemas.auth import LoginIn


class TestAuthController:
    """Testes para o controller de autenticação."""

    @pytest.mark.asyncio
    async def test_login_success(self):
        """Testa login com sucesso."""
        login_in = LoginIn(user_id=123)
        
        with patch("src.controller.auth.sign_jwt") as mock_sign_jwt:
            mock_sign_jwt.return_value = {"access_token": "mock_token_123"}
            
            from src.controller.auth import login
            result = await login(login_in)
            
            assert result["access_token"] == "mock_token_123"
            mock_sign_jwt.assert_called_once_with(user_id=123)

    @pytest.mark.asyncio
    async def test_login_different_user_id(self):
        """Testa login com diferentes user_ids."""
        login_in = LoginIn(user_id=456)
        
        with patch("src.controller.auth.sign_jwt") as mock_sign_jwt:
            mock_sign_jwt.return_value = {"access_token": "mock_token_456"}
            
            from src.controller.auth import login
            result = await login(login_in)
            
            assert result["access_token"] == "mock_token_456"
            mock_sign_jwt.assert_called_once_with(user_id=456)

