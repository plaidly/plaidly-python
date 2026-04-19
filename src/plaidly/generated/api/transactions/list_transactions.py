from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.transaction import Transaction
from ...types import Response


def _get_kwargs(
    wallet_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/wallets/{wallet_id}/transactions".format(
            wallet_id=wallet_id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list["Transaction"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Transaction.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["Transaction"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    wallet_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[list["Transaction"]]:
    """List transactions for a wallet

    Args:
        wallet_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['Transaction']]
    """

    kwargs = _get_kwargs(
        wallet_id=wallet_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    wallet_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[list["Transaction"]]:
    """List transactions for a wallet

    Args:
        wallet_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['Transaction']
    """

    return sync_detailed(
        wallet_id=wallet_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    wallet_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[list["Transaction"]]:
    """List transactions for a wallet

    Args:
        wallet_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['Transaction']]
    """

    kwargs = _get_kwargs(
        wallet_id=wallet_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    wallet_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[list["Transaction"]]:
    """List transactions for a wallet

    Args:
        wallet_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['Transaction']
    """

    return (
        await asyncio_detailed(
            wallet_id=wallet_id,
            client=client,
        )
    ).parsed
