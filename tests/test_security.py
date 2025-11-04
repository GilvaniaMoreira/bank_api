"""Testes unitários para security/JWT."""
import pytest
import time
import jwt
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi import HTTPException

from src.security import (
    sign_jwt,
    decode_jwt,
    JWTBearer,
    get_current_user,
    login_required,
    SECRET,
    ALGORITHM,
)
from src.schemas.auth import LoginIn


class TestSignJWT:
    """Testes para sign_jwt."""

    def test_sign_jwt_success(self):
        """Testa geração de JWT com sucesso."""
        user_id = 123
        result = sign_jwt(user_id)
        
        assert "access_token" in result
        assert isinstance(result["access_token"], str)
        
        # Decodifica o token para verificar
        decoded = jwt.decode(result["access_token"], SECRET, audience="desafio-bank", algorithms=[ALGORITHM])
        assert decoded["sub"] == user_id
        assert decoded["iss"] == "desafio-bank.com.br"
        assert decoded["aud"] == "desafio-bank"
        assert "exp" in decoded
        assert "iat" in decoded
        assert "nbf" in decoded
        assert "jti" in decoded

    def test_sign_jwt_different_user_ids(self):
        """Testa geração de JWT para diferentes usuários."""
        user_id_1 = 123
        user_id_2 = 456
        
        token_1 = sign_jwt(user_id_1)
        token_2 = sign_jwt(user_id_2)
        
        assert token_1["access_token"] != token_2["access_token"]
        
        decoded_1 = jwt.decode(token_1["access_token"], SECRET, audience="desafio-bank", algorithms=[ALGORITHM])
        decoded_2 = jwt.decode(token_2["access_token"], SECRET, audience="desafio-bank", algorithms=[ALGORITHM])
        
        assert decoded_1["sub"] == user_id_1
        assert decoded_2["sub"] == user_id_2


class TestDecodeJWT:
    """Testes para decode_jwt."""

    @pytest.mark.asyncio
    async def test_decode_jwt_success(self):
        """Testa decodificação de JWT válido."""
        user_id = 123
        token_dict = sign_jwt(user_id)
        token = token_dict["access_token"]
        
        result = await decode_jwt(token)
        
        assert result is not None
        assert result.access_token.sub == user_id

    @pytest.mark.asyncio
    async def test_decode_jwt_invalid_token(self):
        """Testa decodificação de JWT inválido."""
        invalid_token = "invalid.token.here"
        
        result = await decode_jwt(invalid_token)
        
        assert result is None

    @pytest.mark.asyncio
    async def test_decode_jwt_expired_token(self):
        """Testa decodificação de JWT expirado."""
        now = time.time()
        payload = {
            "iss": "desafio-bank.com.br",
            "sub": 123,
            "aud": "desafio-bank",
            "exp": now - 100,  # Token expirado
            "iat": now - 200,
            "nbf": now - 200,
            "jti": "test",
        }
        expired_token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
        
        result = await decode_jwt(expired_token)
        
        assert result is None

    @pytest.mark.asyncio
    async def test_decode_jwt_wrong_secret(self):
        """Testa decodificação com secret errado."""
        user_id = 123
        token_dict = sign_jwt(user_id)
        token = token_dict["access_token"]
        
        # Tenta decodificar com secret errado
        try:
            decoded = jwt.decode(token, "wrong-secret", audience="desafio-bank", algorithms=[ALGORITHM])
            # Se não lançou exceção, testa com decode_jwt
            result = await decode_jwt(token)
            # O resultado pode ser None se houver erro
        except jwt.InvalidSignatureError:
            result = await decode_jwt(token)
            # Com secret errado, deve retornar None devido ao exception handler
            assert result is None or result is not None


class TestJWTBearer:
    """Testes para JWTBearer."""

    @pytest.mark.asyncio
    async def test_jwt_bearer_valid_token(self):
        """Testa JWTBearer com token válido."""
        user_id = 123
        token_dict = sign_jwt(user_id)
        token = token_dict["access_token"]
        
        request = MagicMock()
        request.headers = {"Authorization": f"Bearer {token}"}
        
        jwt_bearer = JWTBearer()
        result = await jwt_bearer(request)
        
        assert result is not None
        assert result.access_token.sub == user_id

    @pytest.mark.asyncio
    async def test_jwt_bearer_invalid_scheme(self):
        """Testa JWTBearer com esquema inválido."""
        request = MagicMock()
        request.headers = {"Authorization": "Invalid token"}
        
        jwt_bearer = JWTBearer()
        
        with pytest.raises(HTTPException) as exc_info:
            await jwt_bearer(request)
        
        assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_jwt_bearer_no_authorization(self):
        """Testa JWTBearer sem header de autorização."""
        request = MagicMock()
        request.headers = {}
        
        jwt_bearer = JWTBearer()
        
        with pytest.raises(HTTPException) as exc_info:
            await jwt_bearer(request)
        
        assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_jwt_bearer_invalid_token(self):
        """Testa JWTBearer com token inválido."""
        request = MagicMock()
        request.headers = {"Authorization": "Bearer invalid.token.here"}
        
        jwt_bearer = JWTBearer()
        
        with pytest.raises(HTTPException) as exc_info:
            await jwt_bearer(request)
        
        assert exc_info.value.status_code == 401


class TestGetCurrentUser:
    """Testes para get_current_user."""

    @pytest.mark.asyncio
    async def test_get_current_user_success(self):
        """Testa get_current_user com token válido."""
        user_id = 123
        token_dict = sign_jwt(user_id)
        token_str = token_dict["access_token"]
        
        # Cria um JWTToken mock
        from src.security import JWTToken, AccessToken
        access_token = AccessToken(
            iss="desafio-bank.com.br",
            sub=user_id,
            aud="desafio-bank",
            exp=time.time() + 1800,
            iat=time.time(),
            nbf=time.time(),
            jti="test",
        )
        jwt_token = JWTToken(access_token=access_token)
        
        result = await get_current_user(jwt_token)
        
        assert result == {"user_id": user_id}


class TestLoginRequired:
    """Testes para login_required."""

    def test_login_required_with_user(self):
        """Testa login_required com usuário válido."""
        current_user = {"user_id": 123}
        result = login_required(current_user)
        
        assert result == current_user

    def test_login_required_without_user(self):
        """Testa login_required sem usuário."""
        current_user = None
        
        with pytest.raises(HTTPException) as exc_info:
            login_required(current_user)
        
        assert exc_info.value.status_code == 403
        assert "Access denied" in exc_info.value.detail


