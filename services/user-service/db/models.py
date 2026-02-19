import enum
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from db.base import BaseModelDB


# ===================== ENUM =====================
class ChatType(enum.Enum):
    ROOM = "room"
    CHANNEL = "channel"
    DM = "dm"


# ===================== CHAT =====================
class Chat(BaseModelDB):
    __tablename__ = "chats"
    id: Mapped[bytes] = mapped_column(UUID, primary_key=True)
    type: Mapped[ChatType] = mapped_column(Enum(ChatType, native_enum=True), nullable=False)

    rooms: Mapped[list["Room"]] = relationship(back_populates="chat", cascade="all, delete-orphan")
    channels: Mapped[list["Channel"]] = relationship(back_populates="chat", cascade="all, delete-orphan")
    user_in_chats: Mapped[list["UserInChat"]] = relationship(back_populates="chat", cascade="all, delete-orphan")
    messages: Mapped[list["Message"]] = relationship(back_populates="chat", cascade="all, delete-orphan")


# ===================== SERVER =====================
class Server(BaseModelDB):
    __tablename__ = "servers"
    id: Mapped[bytes] = mapped_column(UUID, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    owner_id: Mapped[bytes] = mapped_column(ForeignKey("users.id"), nullable=False)

    owner: Mapped["User"] = relationship(back_populates="servers")
    rooms: Mapped[list["Room"]] = relationship(back_populates="server", cascade="all, delete-orphan")
    user_in_servers: Mapped[list["UserInServer"]] = relationship(back_populates="server", cascade="all, delete-orphan")
    invites: Mapped[list["InviteServer"]] = relationship(back_populates="server", cascade="all, delete-orphan")


# ===================== ROOM =====================
class Room(BaseModelDB):
    __tablename__ = "rooms"
    id: Mapped[bytes] = mapped_column(UUID, primary_key=True)
    chat_id: Mapped[bytes] = mapped_column(ForeignKey("chats.id"), nullable=False)
    server_id: Mapped[bytes] = mapped_column(ForeignKey("servers.id"), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)

    chat: Mapped[Chat] = relationship(back_populates="rooms", cascade="all, delete-orphan")
    server: Mapped["Server"] = relationship(back_populates="rooms")
    room_permission_overrides: Mapped[list["RoomPermissionOverride"]] = relationship(
        back_populates="room", cascade="all, delete-orphan"
    )
    user_in_rooms: Mapped[list["UserInRoom"]] = relationship(back_populates="room", cascade="all, delete-orphan")


# ===================== CHANNEL =====================
class Channel(BaseModelDB):
    __tablename__ = "channels"
    id: Mapped[bytes] = mapped_column(UUID, primary_key=True)
    chat_id: Mapped[bytes] = mapped_column(ForeignKey("chats.id"), nullable=False)
    owner_id: Mapped[bytes] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    tag: Mapped[str] = mapped_column(nullable=True, unique=True)

    chat: Mapped[Chat] = relationship(back_populates="channels", cascade="all, delete-orphan")
    owner: Mapped["User"] = relationship(back_populates="channels")
    roles: Mapped[list["Role"]] = relationship(back_populates="channel", cascade="all, delete-orphan")
    user_in_channels: Mapped[list["UserInChannel"]] = relationship(back_populates="channel", cascade="all, delete-orphan")


# ===================== USER =====================
class User(BaseModelDB):
    __tablename__ = "users"
    id: Mapped[bytes] = mapped_column(UUID, primary_key=True)
    is_active: Mapped[bool] = mapped_column(nullable=False, server_default="true")
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    display_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=True, unique=True)
    password_hash: Mapped[str] = mapped_column(nullable=True)

    user_in_rooms: Mapped[list["UserInRoom"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    user_in_channels: Mapped[list["UserInChannel"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    user_in_servers: Mapped[list["UserInServer"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    servers: Mapped[list["Server"]] = relationship(back_populates="owner")
    channels: Mapped[list["Channel"]] = relationship(back_populates="owner")


# ===================== USER IN ROOM =====================
class UserInRoom(BaseModelDB):
    __tablename__ = "user_in_rooms"
    user_id: Mapped[bytes] = mapped_column(ForeignKey("users.id"), nullable=False)
    room_id: Mapped[bytes] = mapped_column(ForeignKey("rooms.id"), nullable=False)

    user: Mapped[User] = relationship(back_populates="user_in_rooms")
    room: Mapped[Room] = relationship(back_populates="user_in_rooms")
    room_permission_overrides: Mapped[list["RoomPermissionOverride"]] = relationship(
        back_populates="user_in_rooms", cascade="all, delete-orphan"
    )


# ===================== USER IN CHANNEL =====================
class UserInChannel(BaseModelDB):
    __tablename__ = "user_in_channels"
    user_id: Mapped[bytes] = mapped_column(ForeignKey("users.id"), nullable=False)
    channel_id: Mapped[bytes] = mapped_column(ForeignKey("channels.id"), nullable=False)
    role_id: Mapped[bytes] = mapped_column(ForeignKey("roles.id"), nullable=False)

    user: Mapped[User] = relationship(back_populates="user_in_channels")
    channel: Mapped[Channel] = relationship(back_populates="user_in_channels")
    role: Mapped["Role"] = relationship(back_populates="user_in_channels")


# ===================== USER IN SERVER =====================
class UserInServer(BaseModelDB):
    __tablename__ = "user_in_servers"
    user_id: Mapped[bytes] = mapped_column(ForeignKey("users.id"), nullable=False)
    server_id: Mapped[bytes] = mapped_column(ForeignKey("servers.id"), nullable=False)
    role_id: Mapped[bytes] = mapped_column(ForeignKey("roles.id"), nullable=False)

    user: Mapped[User] = relationship(back_populates="user_in_servers")
    server: Mapped[Server] = relationship(back_populates="user_in_servers")
    role: Mapped["Role"] = relationship(back_populates="user_in_servers")


# ===================== ROLE =====================
class Role(BaseModelDB):
    __tablename__ = "roles"
    id: Mapped[bytes] = mapped_column(UUID, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    permissions: Mapped[int] = mapped_column(nullable=False)
    server_id: Mapped[bytes] = mapped_column(ForeignKey("servers.id"), nullable=True)
    channel_id: Mapped[bytes] = mapped_column(ForeignKey("channels.id"), nullable=True)

    user_in_channels: Mapped[list["UserInChannel"]] = relationship(back_populates="role")
    channel: Mapped[Channel] = relationship(back_populates="roles")
    user_in_servers: Mapped[list["UserInServer"]] = relationship(back_populates="role")
    servers: Mapped[list["Server"]] = relationship(back_populates="role")


# ===================== ROOM PERMISSION OVERRIDE =====================
class RoomPermissionOverride(BaseModelDB):
    __tablename__ = "room_permissions"
    id: Mapped[bytes] = mapped_column(UUID, primary_key=True)
    room_id: Mapped[bytes] = mapped_column(ForeignKey("rooms.id"), nullable=False)
    user_in_room_id: Mapped[bytes] = mapped_column(ForeignKey("user_in_rooms.user_id"), nullable=False)

    role_id: Mapped[bytes] = mapped_column(ForeignKey("roles.id"), nullable=True)
    allow: Mapped[int] = mapped_column(nullable=False)
    deny: Mapped[int] = mapped_column(nullable=False)

    room: Mapped[Room] = relationship(back_populates="room_permission_overrides")
    user_in_rooms: Mapped[list["UserInRoom"]] = relationship(back_populates="room_permission_overrides")


# ===================== MESSAGE =====================
class Message(BaseModelDB):
    __tablename__ = "messages"
    id: Mapped[bytes] = mapped_column(UUID, primary_key=True)
    chat_id: Mapped[bytes] = mapped_column(ForeignKey("chats.id"), nullable=False)
    user_id: Mapped[bytes] = mapped_column(ForeignKey("users.id"), nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[int] = mapped_column(nullable=False)
    server_id: Mapped[bytes] = mapped_column(ForeignKey("servers.id"), nullable=False)

    chat: Mapped[Chat] = relationship(back_populates="messages")
    user: Mapped[User] = relationship(back_populates="messages")
    server: Mapped[Server] = relationship(back_populates="messages")


# ===================== INVITE =====================
class InviteServer(BaseModelDB):
    __tablename__ = "invites"
    id: Mapped[bytes] = mapped_column(UUID, primary_key=True)
    code: Mapped[str] = mapped_column(nullable=False, unique=True)
    server_id: Mapped[bytes] = mapped_column(ForeignKey("servers.id"), nullable=False)
    server: Mapped[Server] = relationship(back_populates="invites")
