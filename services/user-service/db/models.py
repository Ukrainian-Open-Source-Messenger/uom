import enum
from sqlalchemy import Enum, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from db.base import BaseModelDB


# ===================== ENUMS =====================
class ChatType(enum.Enum):
    GROUP = "group"
    CHANNEL = "channel"
    DM = "dm"


# ===================== CHAT =====================
class Chat(BaseModelDB):
    __tablename__ = "chats"
    id: Mapped[bytes] = mapped_column(UUID, primary_key=True)
    type: Mapped[ChatType] = mapped_column(
        Enum(ChatType, native_enum=True), nullable=False
    )
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)

    messages: Mapped[list["Message"]] = relationship(
        back_populates="chat", cascade="all, delete-orphan"
    )
    channels: Mapped["Channel"] = relationship(
        back_populates="chat", cascade="all, delete-orphan"
    )
    members: Mapped[list["Member"]] = relationship(
        back_populates="chat", cascade="all, delete-orphan"
    )


# ===================== SERVER =====================
class Server(BaseModelDB):
    __tablename__ = "servers"
    id: Mapped[bytes] = mapped_column(UUID, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    owner_id: Mapped[bytes] = mapped_column(
        ForeignKey("users.id"), index=True, nullable=False
    )

    owner: Mapped["User"] = relationship(back_populates="servers")
    rooms: Mapped[list["Room"]] = relationship(
        back_populates="server", cascade="all, delete-orphan"
    )
    members: Mapped[list["Member"]] = relationship(
        back_populates="server", cascade="all, delete-orphan"
    )
    roles: Mapped[list["Role"]] = relationship(
        back_populates="server", cascade="all, delete-orphan"
    )
    invites: Mapped[list["InviteServer"]] = relationship(
        back_populates="server", cascade="all, delete-orphan"
    )
    limit_servers: Mapped[list["LimitServer"]] = relationship(
        back_populates="server", cascade="all, delete-orphan"
    )


# ===================== LIMIT SERVER =====================
class LimitServer(BaseModelDB):
    __tablename__ = "limit_servers"
    id: Mapped[bytes] = mapped_column(UUID, primary_key=True)
    server_id: Mapped[bytes] = mapped_column(
        ForeignKey("servers.id"), index=True, nullable=False
    )
    count_of_rooms: Mapped[int] = mapped_column(nullable=False, server_default="0")
    limit_of_rooms: Mapped[int] = mapped_column(nullable=False, server_default="100")
    count_of_roles: Mapped[int] = mapped_column(nullable=False, server_default="0")
    limit_of_roles: Mapped[int] = mapped_column(nullable=False, server_default="100")

    server: Mapped[Server] = relationship(back_populates="limit_servers")


# ===================== INVITE =====================
class InviteServer(BaseModelDB):
    __tablename__ = "invites"
    id: Mapped[bytes] = mapped_column(UUID, primary_key=True)
    code: Mapped[str] = mapped_column(nullable=False, unique=True)
    server_id: Mapped[bytes] = mapped_column(
        ForeignKey("servers.id"), index=True, nullable=False
    )
    server: Mapped[Server] = relationship(back_populates="invites")


# ===================== ROOM =====================
class Room(BaseModelDB):
    __tablename__ = "rooms"
    id: Mapped[bytes] = mapped_column(UUID, primary_key=True)
    chat_id: Mapped[bytes] = mapped_column(
        ForeignKey("chats.id"), index=True, nullable=False
    )
    server_id: Mapped[bytes] = mapped_column(
        ForeignKey("servers.id"), index=True, nullable=False
    )

    chat: Mapped[Chat] = relationship(back_populates="rooms")
    server: Mapped["Server"] = relationship(back_populates="rooms")
    permission_overrides: Mapped[list["RoomPermissionOverride"]] = relationship(
        back_populates="room", cascade="all, delete-orphan"
    )


# ===================== ROOM PERMISSION OVERRIDE =====================
class RoomPermissionOverride(BaseModelDB):
    __tablename__ = "room_permissions"
    id: Mapped[bytes] = mapped_column(UUID, primary_key=True)
    room_id: Mapped[bytes] = mapped_column(
        ForeignKey("rooms.id"), index=True, nullable=False
    )
    role_id: Mapped[bytes] = mapped_column(
        ForeignKey("roles.id"), index=True, nullable=False
    )
    allow: Mapped[int] = mapped_column(nullable=False)
    deny: Mapped[int] = mapped_column(nullable=False)

    room: Mapped[Room] = relationship(back_populates="permission_overrides")


# ===================== CHANNEL =====================
class Channel(BaseModelDB):
    __tablename__ = "channels"
    id: Mapped[bytes] = mapped_column(UUID, primary_key=True)
    chat_id: Mapped[bytes] = mapped_column(
        ForeignKey("chats.id"), index=True, nullable=False
    )
    owner_id: Mapped[bytes] = mapped_column(ForeignKey("users.id"), nullable=False)
    tag: Mapped[str] = mapped_column(nullable=True, unique=True)

    chat: Mapped[Chat] = relationship(back_populates="channels")
    owner: Mapped["User"] = relationship(back_populates="channels")
    roles: Mapped[list["Role"]] = relationship(
        back_populates="channel", cascade="all, delete-orphan"
    )
    members: Mapped[list["Member"]] = relationship(
        back_populates="channel", cascade="all, delete-orphan"
    )


# ===================== USER =====================
class User(BaseModelDB):
    __tablename__ = "users"
    id: Mapped[bytes] = mapped_column(UUID, primary_key=True)
    is_active: Mapped[bool] = mapped_column(nullable=False, server_default="true")
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    display_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=True, unique=True)
    password_hash: Mapped[str] = mapped_column(nullable=True)

    members: Mapped[list["Member"]] = relationship(back_populates="user")
    servers: Mapped[list["Server"]] = relationship(back_populates="owner")
    channels: Mapped[list["Channel"]] = relationship(back_populates="owner")
    limit_users: Mapped["LimitUser"] = relationship(back_populates="user")


# ===================== MEMBER =====================
class Member(BaseModelDB):
    __tablename__ = "members"
    id: Mapped[bytes] = mapped_column(UUID, primary_key=True)
    user_id: Mapped[bytes] = mapped_column(ForeignKey("users.id"), nullable=False)
    target_id: Mapped[bytes] = mapped_column(ForeignKey("chats.id"), nullable=False)

    role_id: Mapped[bytes] = mapped_column(ForeignKey("roles.id"), nullable=True)

    user: Mapped[User] = relationship(back_populates="members")
    target: Mapped[Chat] = relationship(back_populates="members")
    role: Mapped["Role"] = relationship(back_populates="members")
    server: Mapped["Server"] = relationship(back_populates="members", viewonly=True)
    channel: Mapped["Channel"] = relationship(back_populates="members", viewonly=True)

    __table_args__ = (
        Index("idx_user_target_unique", "user_id", "target_id", unique=True),
    )


# ===================== ROLE =====================
class Role(BaseModelDB):
    __tablename__ = "roles"
    id: Mapped[bytes] = mapped_column(UUID, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    permissions: Mapped[int] = mapped_column(nullable=False)
    server_id: Mapped[bytes] = mapped_column(
        ForeignKey("servers.id"), index=True, nullable=True
    )
    channel_id: Mapped[bytes] = mapped_column(
        ForeignKey("channels.id"), index=True, nullable=True
    )

    members: Mapped[list["Member"]] = relationship(back_populates="role")
    server: Mapped[Server] = relationship(back_populates="roles")
    channel: Mapped[Channel] = relationship(back_populates="roles")


# ===================== MESSAGE =====================
class Message(BaseModelDB):
    __tablename__ = "messages"
    id: Mapped[bytes] = mapped_column(UUID, primary_key=True)
    chat_id: Mapped[bytes] = mapped_column(
        ForeignKey("chats.id"), index=True, nullable=False
    )
    user_id: Mapped[bytes] = mapped_column(
        ForeignKey("users.id"), index=True, nullable=False
    )
    content: Mapped[str] = mapped_column(nullable=False)

    chat: Mapped[Chat] = relationship(back_populates="messages")
    user: Mapped[User] = relationship(back_populates="messages")


# ===================== LIMIT USER =====================
class LimitUser(BaseModelDB):
    __tablename__ = "limit_users"
    id: Mapped[bytes] = mapped_column(UUID, primary_key=True)
    user_id: Mapped[bytes] = mapped_column(
        ForeignKey("users.id"), index=True, nullable=False
    )
    count: Mapped[int] = mapped_column(nullable=False, server_default="0")
    limit: Mapped[int] = mapped_column(nullable=False, server_default="100")

    user: Mapped[User] = relationship(back_populates="limit_users")


# ===================== USER SETTINGS =====================
class UserSettings(BaseModelDB):
    pass


# ===================== SERVER SETTINGS =====================
class ServerSettings(BaseModelDB):
    pass
