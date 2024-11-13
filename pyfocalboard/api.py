from datetime import datetime
from typing import TypeVar

from requests import Response, Session

from pyfocalboard.types import (
    HTTP_CODES,
    ApiError,
    Block,
    BlockBody,
    Board,
    BoardAndBlocks,
    BoardBody,
    BoardsStatistics,
    Card,
    CardBody,
    CardPatch,
    Category,
    CategoryBody,
    Channel,
    ClientConfig,
    FileUploadResponse,
    LoginRequest,
    Member,
    MemberBody,
    Onboarding,
    Sharing,
    SharingBody,
    Subscription,
    Team,
    User,
    UserPreference,
)

T = TypeVar("T")


class FocalboardApi:
    MM_PLUGIN_API_URL = "/plugins/focalboard/api/v2"
    STANDALONE_API_URL = "/api/v2"

    def __init__(
        self,
        token: str | None,
        server: str,
        is_standalone=False,
        non_standard_api_url: str | None = None,
    ):
        self._server = server
        self._client = Session()
        self._client.headers["X-Requested-With"] = "XMLHttpRequest"
        self.api_url = (
            FocalboardApi.STANDALONE_API_URL
            if is_standalone
            else FocalboardApi.MM_PLUGIN_API_URL
        )
        self.api_url = (
            self.api_url if not non_standard_api_url else non_standard_api_url
        )

        if token:
            self._client.headers["Authorization"] = "Bearer " + token

    def _check_response(self, response: Response) -> None:
        if HTTP_CODES.Ok <= response.status_code < HTTP_CODES.BadRequest:
            return

        if response.headers.get("Content-Type", "") == "application/json":
            data = response.json()
            if isinstance(data, dict) and "error" in data and "errorCode" in data:
                raise Exception(ApiError.from_dict(data))

        raise Exception(
            ApiError(
                error=f"Invalid status code. {response.text()}",
                errorCode=response.status_code,
            )
        )

    # MARK: Block
    def get_blocks(
        self, board_id: str, parent_id: str | None = None, type: str | None = None
    ) -> list[Block]:
        """
        Returns team boards

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getBlocks](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getBlocks)
        """
        response = self._client.get(
            f"{self._server}{self.api_url}/boards/{board_id}/blocks",
            params={
                "parent_id:": parent_id,
                "type": type,
            },
        )
        self._check_response(response)
        data = response.json()
        return [Block.from_dict(item) for item in data]

    def patch_block(
        self,
        board_id: str,
        block_id: str,
        block: BlockBody,
        disable_notify: bool = False,
    ) -> None:
        """
        Partially updates a block

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-patchBlock](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-patchBlock)
        """
        response = self._client.patch(
            f"{self._server}{self.api_url}/boards/{board_id}/blocks/{block_id}",
            json=block.to_dict(),
            params=dict(disable_notify="true" if disable_notify else "false"),
        )
        self._check_response(response)

    def update_blocks(
        self,
        board_id: str,
        blocks: list[Block],
        disable_notify: bool = False,
    ) -> None:
        """
        Insert blocks. The specified IDs will only be used to link blocks with existing ones, the rest will be replaced by server generated IDs

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-updateBlocks](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-updateBlocks)
        """
        response = self._client.post(
            f"{self._server}{self.api_url}/boards/{board_id}/blocks",
            json=[block.to_dict() for block in blocks],
            params=dict(disable_notify="true" if disable_notify else "false"),
        )
        self._check_response(response)

    def patch_blocks(
        self,
        board_id: str,
        block_ids: list[str],
        blocks: list[BlockBody],
        disable_notify: bool = False,
    ) -> None:
        """
        Partially updates batch of blocks

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-patchBlocks](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-patchBlocks)
        """
        response = self._client.patch(
            f"{self._server}{self.api_url}/boards/{board_id}/blocks",
            json=dict(
                block_ids=block_ids, block_patches=[block.to_dict() for block in blocks]
            ),
            params=dict(disable_notify="true" if disable_notify else "false"),
        )
        self._check_response(response)

    def delete_block(self, board_id: str, block_id: str) -> None:
        """
        Deletes a block

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-deleteBlock](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-deleteBlock)
        """
        response = self._client.delete(
            f"{self._server}{self.api_url}/boards/{board_id}/blocks/{block_id}",
        )
        self._check_response(response)

    def duplicate_block(self, board_id: str, block_id: str) -> None:
        """
        Returns the new created blocks

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-duplicateBlock](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-duplicateBlock)
        """
        response = self._client.post(
            f"{self._server}{self.api_url}/boards/{board_id}/blocks/{block_id}/duplicate",
        )
        self._check_response(response)
        data = response.json()
        return [Block.from_dict(item) for item in data]

    def undelete_block(self, board_id: str, block_id: str) -> None:
        """
        Undeletes a block

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-undeleteBlock](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-undeleteBlock)
        """
        response = self._client.post(
            f"{self._server}{self.api_url}/boards/{board_id}/blocks/{block_id}/undelete",
        )
        self._check_response(response)

    # MARK: Board
    def search_all_boards(self, query: str = "") -> list[Board]:
        """
        Returns the boards that match with a search term

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-searchAllBoards](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-searchAllBoards)
        """

        response = self._client.get(
            f"{self._server}{self.api_url}/boards/search", params=dict(q=query)
        )
        self._check_response(response)
        data = response.json()
        return [Board.from_dict(item) for item in data]

    def search_boards(self, team_id: str, query: str = "") -> list[Board]:
        """
        Returns the boards that match with a search term in the team

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-searchBoards](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-searchBoards)
        """
        response = self._client.get(
            f"{self._server}{self.api_url}/teams/{team_id}/boards/search",
            params=dict(q=query),
        )
        self._check_response(response)
        data = response.json()
        return [Board.from_dict(item) for item in data]

    def search_linkable_boards(self, team_id: str, query: str = "") -> list[Board]:
        """
        Returns the boards that match with a search term in the team and the user has permission to manage members

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-searchLinkableBoards](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-searchLinkableBoards)
        """
        response = self._client.get(
            f"{self._server}{self.api_url}/teams/{team_id}/boards/search/linkable",
            params=dict(q=query),
        )
        self._check_response(response)
        data = response.json()
        return [Board.from_dict(item) for item in data]

    def get_boards(self, team_id: str) -> list[Board]:
        """
        Returns team boards

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getBoards](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getBoards)
        """
        response = self._client.get(
            f"{self._server}{self.api_url}/teams/{team_id}/boards"
        )
        self._check_response(response)
        data = response.json()
        return [Board.from_dict(item) for item in data]

    def get_board(self, board_id: str) -> Board:
        """
        Returns a board

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getBoard](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getBoard)
        """
        response = self._client.get(f"{self._server}{self.api_url}/boards/{board_id}")
        self._check_response(response)
        data = response.json()
        return Board.from_dict(data)

    def create_board(self, team_id: str, board: BoardBody) -> Board:
        """
        Creates a new board

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-createBoard](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-createBoard)
        """
        response = self._client.post(
            f"{self._server}{self.api_url}/boards",
            json=dict(teamID=team_id, **board.to_dict()),
        )
        self._check_response(response)
        data = response.json()
        return Board.from_dict(data)

    def patch_board(self, board_id: str, board: BoardBody) -> Board:
        """
        Partially updates a board

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-patchBoard](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-patchBoard)
        """
        response = self._client.patch(
            f"{self._server}{self.api_url}/boards/{board_id}",
            json=board.to_dict(),
        )
        self._check_response(response)
        data = response.json()
        return Board.from_dict(data)

    def delete_board(self, board_id: str) -> None:
        """
        Removes a board

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-deleteBoard](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-deleteBoard)
        """
        response = self._client.delete(
            f"{self._server}{self.api_url}/boards/{board_id}",
        )
        self._check_response(response)

    def join_board(self, board_id: str) -> None:
        """
        Become a member of a board

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-joinBoard](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-joinBoard)
        """
        response = self._client.post(
            f"{self._server}{self.api_url}/boards/{board_id}/join"
        )
        self._check_response(response)

    def leave_board(self, board_id: str) -> None:
        """
        Remove your own membership from a board

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-leaveBoard](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-leaveBoard)
        """
        response = self._client.post(
            f"{self._server}{self.api_url}/boards/{board_id}/leave"
        )
        self._check_response(response)

    def get_members_for_board(self, board_id: str) -> list[Member]:
        """
        Returns the members of the board

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getMembersForBoard](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getMembersForBoard)
        """
        response = self._client.get(
            f"{self._server}{self.api_url}/boards/{board_id}/members"
        )
        self._check_response(response)
        data = response.json()
        return [Member.from_dict(item) for item in data]

    def get_sharing(self, board_id: str) -> Sharing:
        """
        Returns sharing information for a board

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getSharing](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getSharing)
        """
        response = self._client.get(
            f"{self._server}{self.api_url}/boards/{board_id}/sharing"
        )
        self._check_response(response)
        data = response.json()
        return Sharing.from_dict(data)

    def post_sharing(self, board_id: str, sharing: SharingBody) -> Sharing:
        """
        Sets sharing information for a board

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-postSharing](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-postSharing)
        """
        response = self._client.post(
            f"{self._server}{self.api_url}/boards/{board_id}/sharing",
            json=sharing.to_dict(),
        )
        self._check_response(response)
        data = response.json()
        return Sharing.from_dict(data)

    def duplicate_board(self, board_id: str) -> BoardAndBlocks:
        """
        Returns the new created board and all the blocks

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-duplicateBoard](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-duplicateBoard)
        """
        response = self._client.post(
            f"{self._server}{self.api_url}/boards/{board_id}/duplicate"
        )
        self._check_response(response)
        data = response.json()
        return BoardAndBlocks.from_dict(data)

    def add_member(
        self, board_id: str, user_id: str, member: MemberBody | None = None
    ) -> Member:
        """
        Adds a new member to a board

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-addMember](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-addMember)
        """
        response = self._client.post(
            f"{self._server}{self.api_url}/boards/{board_id}/members",
            json=dict(userID=user_id, **(member.to_dict() if member else {})),
        )
        self._check_response(response)
        data = response.json()
        return Member.from_dict(data)

    def update_member(self, board_id: str, user_id: str, member: MemberBody) -> Member:
        """
        Updates a board member

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-updateMember](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-updateMember)
        """
        response = self._client.put(
            f"{self._server}{self.api_url}/boards/{board_id}/members/{user_id}",
            json=member.to_dict(),
        )
        self._check_response(response)
        data = response.json()
        return Member.from_dict(data)

    def delete_member(
        self,
        board_id: str,
        user_id: str,
    ) -> None:
        """
        Deletes a member from a board

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-deleteMember](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-deleteMember)
        """
        response = self._client.delete(
            f"{self._server}{self.api_url}/boards/{board_id}/members/{user_id}",
        )
        self._check_response(response)

    def archive_board_export(self, board_id: str) -> bytes:
        """
        Exports an archive of all blocks for one boards.

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-archiveExportBoard](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-archiveExportBoard)
        """
        response = self._client.get(
            f"{self._server}{self.api_url}/boards/{board_id}/archive/export",
        )
        self._check_response(response)
        return response.content

    def update_board_category(
        self, team_id: str, board_id: str, category_id: str
    ) -> None:
        """
        Set the category of a board

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-updateCategoryBoard](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-updateCategoryBoard)
        """
        response = self._client.post(
            f"{self._server}{self.api_url}/teams/{team_id}/categories/{category_id}/boards/{board_id}",
        )
        self._check_response(response)

    def undelete_board(self, board_id: str) -> None:
        """
        Undeletes a board

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-undeleteBoard](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-undeleteBoard)
        """
        response = self._client.post(
            f"{self._server}{self.api_url}/boards/{board_id}/undelete",
        )
        self._check_response(response)

    # MARK: Board and blocks
    def insert_boards_and_blocks(
        self, boards: list[BoardBody], blocks: list[BlockBody]
    ) -> None:
        """
        Creates new boards and blocks

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-insertBoardsAndBlocks](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-insertBoardsAndBlocks)
        """
        response = self._client.post(
            f"{self._server}{self.api_url}/boards-and-blocks",
            json=dict(
                boards=[board.to_dict() for board in boards],
                blocks=[
                    {
                        "createAt": int(datetime.now().timestamp()),
                        "updateAt": int(datetime.now().timestamp()),
                        **block.to_dict(),
                    }
                    for block in blocks
                ],
            ),
        )
        self._check_response(response)
        data = response.json()
        return BoardAndBlocks.from_dict(data)

    def patch_boards_and_blocks(
        self,
        board_ids: list[str],
        boards: list[BoardBody],
        block_ids: list[str],
        blocks: list[BlockBody],
    ) -> None:
        """
        Patches a set of related boards and blocks

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-patchBoardsAndBlocks](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-patchBoardsAndBlocks)
        """
        response = self._client.patch(
            f"{self._server}{self.api_url}/boards-and-blocks",
            json=dict(
                boardIDs=board_ids,
                boardPatches=[board.to_dict() for board in boards],
                blockIDs=block_ids,
                blockPatches=[
                    {
                        "createAt": int(datetime.now().timestamp()),
                        "updateAt": int(datetime.now().timestamp()),
                        **block.to_dict(),
                    }
                    for block in blocks
                ],
            ),
        )
        self._check_response(response)
        data = response.json()
        return BoardAndBlocks.from_dict(data)

    def delete_boards_and_blocks(
        self, board_ids: list[str], block_ids: list[str]
    ) -> None:
        """
        Deletes boards and blocks

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-deleteBoardsAndBlocks](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-deleteBoardsAndBlocks)
        """
        response = self._client.delete(
            f"{self._server}{self.api_url}/boards-and-blocks",
            json=dict(boards=board_ids, blocks=block_ids),
        )
        self._check_response(response)

    # MARK: Cards
    def get_cards(
        self, board_id: str, page: int = 0, per_page: int = 100
    ) -> list[Card]:
        """
        Fetches cards for the specified board.

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getCards](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getCards)
        """
        response = self._client.get(
            f"{self._server}{self.api_url}/boards/{board_id}/cards",
            params=dict(page=page, per_page=per_page),
        )
        self._check_response(response)
        data = response.json()
        return [Card.from_dict(item) for item in data]

    def get_card(self, card_id: str) -> Card:
        """
        Fetches the specified card.

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getCard](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getCard)
        """
        response = self._client.get(f"{self._server}{self.api_url}/cards/{card_id}")
        self._check_response(response)
        data = response.json()
        return Card.from_dict(data)

    def create_card(
        self, board_id: str, card: CardBody | None = None, disable_notify: bool = False
    ) -> Card:
        """
        Creates a new card for the specified board.

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-createCard](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-createCard)
        """
        response = self._client.post(
            f"{self._server}{self.api_url}/boards/{board_id}/cards",
            json=(card.to_dict() if card else {}),
            params=dict(disable_notify="true" if disable_notify else "false"),
        )
        self._check_response(response)
        data = response.json()
        return Card.from_dict(data)

    def patch_card(
        self, card_id: str, card: CardPatch | None, disable_notify: bool = False
    ) -> Card:
        """
        Patches the specified card.

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-patchCard](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-patchCard)
        """
        response = self._client.patch(
            f"{self._server}{self.api_url}/cards/{card_id}",
            json=card.to_dict(),
            params=dict(disable_notify="true" if disable_notify else "false"),
        )
        self._check_response(response)
        data = response.json()
        return Card.from_dict(data)

    # MARK: Team
    def get_teams(self) -> list[Team]:
        """
        Returns information of all the teams

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getTeams](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getTeams)
        """
        response = self._client.get(f"{self._server}{self.api_url}/teams")
        self._check_response(response)
        data = response.json()
        return [Team.from_dict(item) for item in data]

    def get_team(self, team_id: str) -> Team:
        """
        Returns information of the root team

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getTeam](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getTeam)
        """
        response = self._client.get(f"{self._server}{self.api_url}/teams/{team_id}")
        self._check_response(response)
        data = response.json()
        return Team.from_dict(data)

    def get_team_users(
        self, team_id: str, search: str | None = None, exclude_bots: bool = False
    ) -> list[User]:
        """
        Returns team users

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getTeamUsers](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getTeamUsers)
        """
        response = self._client.get(
            f"{self._server}{self.api_url}/teams/{team_id}/users",
            params=dict(
                search=search, exclude_bots="true" if exclude_bots else "false"
            ),
        )
        self._check_response(response)
        data = response.json()
        return [User.from_dict(item) for item in data]

    def onboard(self, team_id: str) -> Onboarding:
        """
        Onboards a user on Boards.

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-onboard](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-onboard)
        """
        response = self._client.post(
            f"{self._server}{self.api_url}/teams/{team_id}/onboard"
        )
        self._check_response(response)
        data = response.json()
        return Onboarding.from_dict(data)

    def get_templates(self, team_id: str) -> list[Board]:
        """
        Returns team templates

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getTemplates](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getTemplates)
        """
        response = self._client.get(
            f"{self._server}{self.api_url}/teams/{team_id}/templates"
        )
        self._check_response(response)
        data = response.json()
        return [Board.from_dict(item) for item in data]

    def archive_export_team(self, team_id: str) -> bytes:
        """
        Exports an archive of all blocks for one boards.

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-archiveExportTeam](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-archiveExportTeam)
        """
        response = self._client.get(
            f"{self._server}{self.api_url}/teams/{team_id}/archive/export",
        )
        self._check_response(response)
        return response.content

    def archive_import(self, team_id: str, file: bytes) -> None:
        """
        Import an archive of boards.

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-archiveImport](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-archiveImport)
        """
        response = self._client.post(
            f"{self._server}{self.api_url}/teams/{team_id}/archive/import",
            files=dict(file=file),
        )
        self._check_response(response)

    # MARK: User
    def get_me(self) -> User:
        """
        Returns the currently logged-in user

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getMe](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getMe)
        """
        response = self._client.get(f"{self._server}{self.api_url}/users/me")
        self._check_response(response)
        data = response.json()
        return User.from_dict(data)

    def get_user(self, user_id: str) -> User:
        """
        Returns a user

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getUser](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getUser)
        """
        response = self._client.get(f"{self._server}{self.api_url}/users/{user_id}")
        self._check_response(response)
        data = response.json()
        return User.from_dict(data)

    def get_my_memberships(self) -> list[Member]:
        """
        Returns the currently users board memberships

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getMyMemberships](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getMyMemberships)
        """
        response = self._client.get(
            f"{self._server}{self.api_url}/users/me/memberships"
        )
        self._check_response(response)
        data = response.json()
        return [Member.from_dict(item) for item in data]

    # MARK: Category
    def get_category_boards(self, team_id: str) -> list[Category]:
        """
        Gets the user's board categories

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getUserCategoryBoards](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getUserCategoryBoards)
        """
        response = self._client.get(
            f"{self._server}{self.api_url}/teams/{team_id}/categories"
        )
        self._check_response(response)
        data = response.json()
        return [Category.from_dict(item) for item in data]

    def create_category(
        self, team_id: str, user_id: str, category: CategoryBody
    ) -> Category:
        """
        Create a category for boards

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-createCategory](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-createCategory)
        """
        response = self._client.post(
            f"{self._server}{self.api_url}/teams/{team_id}/categories",
            json=dict(teamID=team_id, userID=user_id, **category.to_dict()),
        )
        self._check_response(response)
        data = response.json()
        return Category.from_dict(data)

    def update_category(
        self, team_id: str, user_id: str, category_id: str, category: CategoryBody
    ) -> Category:
        """
        Create a category for boards

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-updateCategory](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-updateCategory)
        """
        response = self._client.put(
            f"{self._server}{self.api_url}/teams/{team_id}/categories/{category_id}",
            json=dict(
                teamID=team_id, userID=user_id, id=category_id, **category.to_dict()
            ),
        )
        self._check_response(response)
        data = response.json()
        return Category.from_dict(data)

    def delete_category(self, team_id: str, category_id: str) -> None:
        """
        Delete a category

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-deleteCategory](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-deleteCategory)
        """
        response = self._client.delete(
            f"{self._server}{self.api_url}/teams/{team_id}/categories/{category_id}",
        )
        self._check_response(response)

    def get_user_config(self) -> list[UserPreference]:
        """
        Returns an array of user preferences

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getUserConfig](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getUserConfig)
        """
        response = self._client.get(f"{self._server}{self.api_url}/users/me/config")
        self._check_response(response)
        data = response.json()
        return [UserPreference.from_dict(item) for item in data]

    def update_user_config(
        self, user_id: str, user_preference: UserPreference
    ) -> list[UserPreference]:
        """
        Updates user config

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-updateUserConfig](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-updateUserConfig)
        """
        response = self._client.put(
            f"{self._server}{self.api_url}/users/{user_id}/config",
            json=user_preference.to_dict(),
        )
        self._check_response(response)
        data = response.json()
        return [UserPreference.from_dict(item) for item in data]

    def get_users(self, user_ids: list[str]) -> list[User]:
        """
        Returns a user list

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getUsersList](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getUsersList)
        """
        response = self._client.post(
            f"{self._server}{self.api_url}/users", json=user_ids
        )
        self._check_response(response)
        data = response.json()
        return [User.from_dict(item) for item in data]

    # MARK: Subscription
    def get_subscriptions(self, subscriber_id: str) -> list[Subscription]:
        """
        Gets subscriptions for a user.

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getSubscriptions](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getSubscriptions)
        """
        response = self._client.get(
            f"{self._server}{self.api_url}/subscriptions/{subscriber_id}"
        )
        self._check_response(response)
        data = response.json()
        return [Subscription.from_dict(item) for item in data]

    def create_subscription(self, block: Block, user_id: str) -> Subscription:
        """
        Creates a subscription to a block for a user. The user will receive change notifications for the block.

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-createSubscription](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-createSubscription)
        """
        response = self._client.post(
            f"{self._server}{self.api_url}/subscriptions",
            json=dict(
                blockID=block.id,
                BlockType=block.type,
                subscriberID=user_id,
                SubscriberType="user",
            ),
        )
        self._check_response(response)
        data = response.json()
        return Subscription.from_dict(data)

    def delete_subscriptions(self, block_id: str, user_id: str) -> None:
        """
        Deletes a subscription a user has for a a block. The user will no longer receive change notifications for the block.

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-deleteSubscription](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-deleteSubscription)
        """
        response = self._client.delete(
            f"{self._server}{self.api_url}/subscriptions/{block_id}/{user_id}"
        )
        self._check_response(response)

    # MARK: Channel
    def search_my_channels(self, team_id: str, search: str = "") -> list[Channel]:
        """
        Returns the user available channels

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-searchMyChannels](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-searchMyChannels)
        """
        response = self._client.get(
            f"{self._server}{self.api_url}/teams/{team_id}/channels",
            params=dict(search=search),
        )
        self._check_response(response)
        data = response.json()
        return [Channel.from_dict(item) for item in data]

    def get_channel(self, team_id: str, channel_id: str) -> Channel:
        """
        Returns the requested channel

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getChannel](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getChannel)
        """
        response = self._client.get(
            f"{self._server}{self.api_url}/teams/{team_id}/channels/{channel_id}"
        )
        self._check_response(response)
        data = response.json()
        return Channel.from_dict(data)

    # MARK: File
    def get_file(self, team_id: str, board_id: str, filename: str) -> bytes:
        """
        Returns the contents of an uploaded file

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getFile](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getFile)
        """
        response = self._client.get(
            f"{self._server}{self.api_url}/files/teams/{team_id}/{board_id}/{filename}"
        )
        self._check_response(response)
        return response.content

    def upload_file(
        self, team_id: str, board_id: str, file: bytes
    ) -> FileUploadResponse:
        """
        Upload a binary file, attached to a root block

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-uploadFile](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-uploadFile)
        """
        response = self._client.post(
            f"{self._server}{self.api_url}/teams/{team_id}/{board_id}/files",
            files=dict(file=file),
        )
        self._check_response(response)
        data = response.json()
        return FileUploadResponse.from_dict(data)

    # MARK: Statistics
    def get_statistics(self) -> BoardsStatistics:
        """
        Fetches the statistic of the server.

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-handleStatistics](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-handleStatistics)
        """
        response = self._client.get(f"{self._server}{self.api_url}/statistics")
        self._check_response(response)
        data = response.json()
        return BoardsStatistics.from_dict(data)

    # MARK: Auth
    def login(self, auth: LoginRequest):
        """
        Login user

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-login](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-login)
        """
        response = self._client.post(
            f"{self._server}{self.api_url}/login", json=auth.to_dict()
        )
        self._check_response(response)
        data = response.json()
        self._client.headers["Authorization"] = "Bearer " + data.token

    def logout(self):
        """
        Logout user

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-logout](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-logout)
        """
        response = self._client.post(f"{self._server}{self.api_url}/logout")
        self._check_response(response)
        del self._client.headers["Authorization"]

    # MARK: System
    def client_config(self) -> ClientConfig:
        """
        Returns the client configuration

        [https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getClientConfig](https://htmlpreview.github.io/?https://github.com/mattermost/focalboard/blob/main/server/swagger/docs/html/index.html#api-Default-getClientConfig)
        """
        response = self._client.get(f"{self._server}{self.api_url}/clientConfig")
        self._check_response(response)
        data = response.json()
        return ClientConfig.from_dict(data)
