from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Literal

from dataclasses_json import CatchAll, Undefined, dataclass_json


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass(kw_only=True)
class ResourceMetadataUsers:
    ""

    createdBy: str
    modifiedBy: str


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass(kw_only=True)
class ResourceMetadataTime:
    ""

    createAt: int
    updateAt: int
    deleteAt: int


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass(kw_only=True)
class ResourceMetadata(ResourceMetadataUsers, ResourceMetadataTime):
    ""

    pass


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(kw_only=True)
class FieldOption:
    ""

    color: str
    id: str
    value: str
    _other: CatchAll


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(kw_only=True)
class Field:
    ""

    id: str | None = None
    name: str
    options: list[FieldOption] | None = None
    type: str | None = None
    _other: CatchAll


class BlockType(StrEnum):
    COMMENT = "comment"
    ""
    CARD = "card"
    ""
    TEXT = "text"
    ""
    ATTACHMENT = "attachment"
    ""
    DIVIDER = "divider"
    ""
    CHECKBOX = "checkbox"
    ""
    VIEW = "view"
    ""
    IMAGE = "image"
    ""


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass(kw_only=True)
class BlockBody:
    ""

    type: BlockType | None = None
    parentId: str | None = None
    schema: int | None = None
    title: str | None = None
    fields: dict | None = None
    boardId: str | None = None


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(kw_only=True)
class Block(ResourceMetadata, BlockBody):
    ""

    id: str
    _other: CatchAll


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass(kw_only=True)
class CardBody:
    ""

    title: str | None = None
    contentOrder: list[str] | None = None
    icon: str | None = None
    isTemplate: bool | None = None
    properties: dict[str, Any] | None = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass(kw_only=True)
class CardPatch:
    ""

    title: str | None = None
    contentOrder: list[str] | None = None
    icon: str | None = None
    updatedProperties: dict[str, Any] | None = None


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(kw_only=True)
class Card(ResourceMetadata, CardBody):
    ""

    id: str
    boardId: str
    _other: CatchAll


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(kw_only=True)
class Team:
    ""

    id: str
    title: str
    signupToken: str
    settings: Any | None
    modifiedBy: str
    updateAt: int
    _other: CatchAll


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(kw_only=True)
class Onboarding:
    ""

    teamID: str
    boardID: str
    _other: CatchAll


class BoardType(StrEnum):
    Open = "O"
    ""
    Private = "P"
    ""


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass(kw_only=True)
class BoardBody:
    ""

    type: BoardType | None = None
    channelId: str | None = None
    minimumRole: str | None = None
    title: str | None = None
    description: str | None = None
    icon: str | None = None
    showDescription: bool | None = None
    isTemplate: bool | None = None
    templateVersion: int | None = None
    properties: dict[str, str] | None = None
    cardProperties: list[Field] | None = None


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(kw_only=True)
class Board(ResourceMetadata, BoardBody):
    ""

    id: str
    teamId: str
    _other: CatchAll


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(kw_only=True)
class User:
    ""

    id: str
    username: str
    nickname: str
    firstname: str
    lastname: str
    create_at: int
    update_at: int
    delete_at: int
    is_bot: bool
    is_guest: bool
    roles: str
    _other: CatchAll
    permissions: list[str] | None = None


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(kw_only=True)
class Metadata:
    ""

    boardID: str
    hidden: bool
    _other: CatchAll


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass(kw_only=True)
class CategoryBody:
    ""

    name: str
    collapsed: bool | None = None
    sorting: str | None = None
    type: str | None = None
    boardMetadata: list[Metadata] | None = None
    sortOrder: int | None = None


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(kw_only=True)
class Category(ResourceMetadataTime, CategoryBody):
    ""

    id: str
    userID: str
    teamID: str
    _other: CatchAll


class SubscriberType(StrEnum):
    User = "user"
    ""
    Channel = "channel"
    ""


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(kw_only=True)
class Subscription:
    ""

    blockType: str
    blockId: str
    subscriberType: SubscriberType
    subscriberId: str
    notifiedAt: int
    createAt: int
    deleteAt: int
    _other: CatchAll


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass(kw_only=True)
class MemberBody:
    ""

    schemeAdmin: bool | None = None
    schemeEditor: bool | None = None
    schemeCommenter: bool | None = None
    schemeViewer: bool | None = None


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(kw_only=True)
class Member(MemberBody):
    ""

    boardId: str
    userId: str
    roles: str
    minimumRole: str
    synthetic: bool
    _other: CatchAll


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(kw_only=True)
class BoardAndBlocksBody:
    ""

    boards: list[BoardBody]
    blocks: list[BlockBody]
    _other: CatchAll


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(kw_only=True)
class BoardAndBlocks:
    ""

    boards: list[Board]
    blocks: list[Block]
    _other: CatchAll


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(kw_only=True)
class FileUploadResponse:
    ""

    fileId: str
    _other: CatchAll


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(kw_only=True)
class UserPreference:
    ""

    updatedFields: dict[str, str]
    deletedFields: list[str]
    _other: CatchAll


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(kw_only=True)
class LoginRequest:
    ""

    type: Literal["normal"] = "normal"
    username: str | None = None
    email: str | None = None
    password: str
    mfa_token: str | None = None
    _other: CatchAll


class ChannelType(StrEnum):
    Open = "O"
    ""
    Private = "P"
    ""


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(kw_only=True)
class Channel:
    ""

    id: str
    create_at: int
    update_at: int
    delete_at: int
    team_id: str
    type: ChannelType
    display_name: str
    name: str
    header: str
    purpose: str
    last_post_at: int
    total_msg_count: int
    extra_update_at: int
    creator_id: str
    scheme_id: str | None
    props: dict | None
    group_constrained: bool | None
    shared: bool | None
    total_msg_count_root: int
    policy_id: str | None
    last_root_post_at: int
    _other: CatchAll


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(kw_only=True)
class ClientConfig:
    ""

    telemetry: bool
    telemetryid: str
    enablePublicSharedBoards: bool
    teammateNameDisplay: bool
    featureFlags: dict[str, Literal["true"] | Literal["false"]]
    maxFileSize: int
    _other: CatchAll


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(kw_only=True)
class BoardsStatistics:
    ""

    board_count: int
    card_count: int
    _other: CatchAll


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass(kw_only=True)
class SharingBody:
    ""

    enabled: bool | None = None
    token: str | None = None


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(kw_only=True)
class Sharing(SharingBody):
    ""

    id: str
    enabled: bool
    token: str
    modifiedBy: str
    update_at: int
    _other: CatchAll


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(kw_only=True)
class ApiError:
    ""

    error: str
    errorCode: int
    _other: CatchAll


class HTTP_CODES:
    Ok = 200
    BadRequest = 400
