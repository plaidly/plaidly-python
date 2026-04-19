from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.payout import Payout
from ...types import Response


def _get_kwargs(
    payout_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/payouts/{payout_id}".format(
            payout_id=payout_id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Payout]:
    if response.status_code == 200:
        response_200 = Payout.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Payout]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    payout_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Payout]:
    """Get payout status

    Args:
        payout_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Payout]
    """

    kwargs = _get_kwargs(
        payout_id=payout_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    payout_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Payout]:
    """Get payout status

    Args:
        payout_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Payout
    """

    return sync_detailed(
        payout_id=payout_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    payout_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Payout]:
    """Get payout status

    Args:
        payout_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Payout]
    """

    kwargs = _get_kwargs(
        payout_id=payout_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    payout_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Payout]:
    """Get payout status

    Args:
        payout_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Payout
    """

    return (
        await asyncio_detailed(
            payout_id=payout_id,
            client=client,
        )
    ).parsed
