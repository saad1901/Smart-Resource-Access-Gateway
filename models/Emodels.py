from config.dependencies import Base
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Numeric, Date, Time, UUID, Enum, Table, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from enum import Enum as PyEnum

# Association table for Tournament.additional_images (ManyToMany)
tournament_additional_images = Table(
    'tournament_additional_images',
    Base.metadata,
    Column('tournament_id', Integer, ForeignKey('app_tournament.id')),
    Column('image_id', Integer, ForeignKey('app_tournament_image.id'))
)

class CategoryType(str, PyEnum):
    SPORTS = 'sports'
    ESPORTS = 'esports'
    CULTURAL = 'cultural'
    ACADEMIC = 'academic'
    TECHNOLOGY = 'technology'
    OTHER = 'other'

class Category(Base):
    __tablename__ = 'app_category'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(255), unique=True)
    description = Column(Text, nullable=True)
    icon = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    type = Column(String(20))
    tournaments = relationship("Tournament", back_populates="category")

# class TournamentImage(Base):
#     __tablename__ = 'app_tournamentimage'
#     id = Column(Integer, primary_key=True)
#     tournament_id = Column(Integer, ForeignKey('app_tournament.id'), nullable=True)
#     image = Column(String(255))
#     caption = Column(String(200), nullable=True)
#     is_primary = Column(Boolean, default=False)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     tournament = relationship("Tournament", back_populates="tournament_images", foreign_keys=[tournament_id])
    # additional_tournaments = relationship(
    #     "Tournament",
    #     secondary=tournament_additional_images,
    #     back_populates="additional_images"
    # )

class Upis(Base):
    __tablename__ = 'app_upis'
    id = Column(Integer, primary_key=True)
    upi_id = Column(String(100), unique=True)
    nickname = Column(String(100), unique=True, nullable=True)
    name = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    tournaments = relationship("Tournament", back_populates="upi")

class TournamentStatus(str, PyEnum):
    PUBLISHED = 'published'
    ONGOING = 'ongoing'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    DRAFT = 'draft'

class Tournament(Base):
    __tablename__ = 'app_tournament'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(255), unique=True)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey('app_category.id'))
    organizer_id = Column(Integer, ForeignKey('auth_user.id'), nullable=True)
    start_date = Column(Date)
    end_date = Column(Date)
    tournament_time = Column(Time, default=datetime.strptime('10:00', '%H:%M').time())
    registration_deadline = Column(DateTime)
    venue = Column(String(200))
    address = Column(Text, nullable=True)
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))
    postal_code = Column(String(20), nullable=True)
    max_participants = Column(Integer)
    min_participants = Column(Integer, default=2)
    entry_fee = Column(Numeric(10, 2))
    prize_pool = Column(Numeric(10, 2))
    tournament_format = Column(String(100))
    rules = Column(Text)
    banner_image = Column(String(255),nullable=True)
    status = Column(String(20), default='draft')
    is_featured = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    contact_email = Column(String(255))
    contact_phone = Column(String(20))
    whatsapp_number = Column(String(20), nullable=True)
    facebook_event = Column(String(255), nullable=True)
    instagram_post = Column(String(255), nullable=True)
    upi_id_id = Column(Integer, ForeignKey('app_upis.id'), nullable=True)
    category = relationship("Category", back_populates="tournaments")
    organizer = relationship("User", back_populates="organized_tournaments")
    upi = relationship("Upis", back_populates="tournaments")
    # tournament_images = relationship("TournamentImage", back_populates="tournament", foreign_keys=[TournamentImage.tournament_id])
    # additional_images = relationship(
    #     "TournamentImage",
    #     secondary=tournament_additional_images,
    #     back_populates="additional_tournaments"
    # )
    participants = relationship("Participant", back_populates="tournament")
    prizes = relationship("TournamentPrize", back_populates="tournament")
    sponsors = relationship("TournamentSponsor", back_populates="tournament")
    announcements = relationship("TournamentAnnouncement", back_populates="tournament")

class PaymentStatus(str, PyEnum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'
    REFUNDED = 'refunded'

class Transaction(Base):
    __tablename__ = 'app_transaction'
    id = Column(Integer, primary_key=True)
    amount = Column(Numeric(10, 2))
    payment_status = Column(String(20), default='pending')
    payment_date = Column(DateTime, nullable=True)
    payment_reference = Column(String(100), nullable=True)
    payment_screenshot = Column(String(255), nullable=True)
    ticket_count = Column(Integer, default=1)
    ticket_numbers = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = Column(Text, nullable=True)
    participant = relationship("Participant", back_populates="transaction", uselist=False)

class ParticipantStatus(str, PyEnum):
    REGISTERED = 'registered'
    CONFIRMED = 'confirmed'
    CHECKED_IN = 'checked_in'
    ELIMINATED = 'eliminated'
    WINNER = 'winner'
    DISQUALIFIED = 'disqualified'
    REJECTED = 'rejected'

class Gender(str, PyEnum):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'

class Participant(Base):
    __tablename__ = 'app_participant'
    id = Column(Integer, primary_key=True)
    tournament_id = Column(Integer, ForeignKey('app_tournament.id'))
    registration_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    full_name = Column(String(200))
    address = Column(String(300), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(20))
    wp = Column(String(10), nullable=True)
    age = Column(Integer)
    gender = Column(String(10))
    registration_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default='registered')
    check_in_time = Column(DateTime, nullable=True)
    special_requirements = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    transaction_id = Column(Integer, ForeignKey('app_transaction.id'), unique=True)
    optinWhatsapp = Column(Boolean, default=True)
    tournament = relationship("Tournament", back_populates="participants")
    transaction = relationship("Transaction", back_populates="participant", uselist=False)
    prizes_won = relationship("TournamentPrize", back_populates="winner")
    chess_profile = relationship("ChessPlayer", back_populates="participant", uselist=False)
    __table_args__ = (
        UniqueConstraint('tournament_id', 'email', name='_tournament_email_uc'),
    )

class TournamentPrize(Base):
    __tablename__ = 'app_tournamentprize'
    id = Column(Integer, primary_key=True)
    tournament_id = Column(Integer, ForeignKey('app_tournament.id'))
    position = Column(Integer)
    prize_amount = Column(Numeric(10, 2))
    description = Column(Text, nullable=True)
    winner_id = Column(Integer, ForeignKey('app_participant.id'), nullable=True)
    tournament = relationship("Tournament", back_populates="prizes")
    winner = relationship("Participant", back_populates="prizes_won")
    __table_args__ = (
        UniqueConstraint('tournament_id', 'position', name='_tournament_position_uc'),
    )

class TournamentSponsor(Base):
    __tablename__ = 'app_tournamentsponsor'
    id = Column(Integer, primary_key=True)
    tournament_id = Column(Integer, ForeignKey('app_tournament.id'))
    name = Column(String(200))
    logo = Column(String(255))
    website = Column(String(255), nullable=True)
    sponsorship_level = Column(String(50))
    contribution = Column(Numeric(10, 2))
    description = Column(Text, nullable=True)
    tournament = relationship("Tournament", back_populates="sponsors")

class TournamentAnnouncement(Base):
    __tablename__ = 'app_tournamentannouncement'
    id = Column(Integer, primary_key=True)
    tournament_id = Column(Integer, ForeignKey('app_tournament.id'))
    title = Column(String(200))
    content = Column(Text)
    is_important = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    tournament = relationship("Tournament", back_populates="announcements")

class ChessTitle(str, PyEnum):
    NONE = ''
    GM = 'GM'
    IM = 'IM'
    FM = 'FM'
    CM = 'CM'
    WGM = 'WGM'
    WIM = 'WIM'
    WFM = 'WFM'
    WCM = 'WCM'

class ChessSection(str, PyEnum):
    OPEN = 'open'
    U1600 = 'u1600'
    U1400 = 'u1400'
    U1200 = 'u1200'
    U1000 = 'u1000'

class ChessPlayer(Base):
    __tablename__ = 'app_chessplayer'
    participant_id = Column(Integer, ForeignKey('app_participant.id'), primary_key=True)
    fide_id = Column(String(20), nullable=True)
    national_id = Column(String(20), nullable=True)
    title = Column(String(5), nullable=True)
    fide_rating = Column(Integer, nullable=True)
    national_rating = Column(Integer, nullable=True)
    rapid_rating = Column(Integer, nullable=True)
    blitz_rating = Column(Integer, nullable=True)
    section = Column(String(10))
    federation = Column(String(100))
    club_academy = Column(String(200), nullable=True)
    is_arbiter = Column(Boolean, default=False)
    previous_tournaments = Column(Text, nullable=True)
    achievements = Column(Text, nullable=True)
    participant = relationship("Participant", back_populates="chess_profile", uselist=False)

class LogModal(Base):
    __tablename__ = 'app_logmodal'
    id = Column(Integer, primary_key=True)
    sec = Column(String(100), nullable=True)
    key = Column(String(100), nullable=True)
    value = Column(String(500), nullable=True)
    sec_id = Column(Integer, nullable=True)

class EventData(Base):
    __tablename__ = 'app_eventdata'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=True)
    email = Column(String(50), nullable=True)
    phone = Column(String(15), nullable=True)
    wp = Column(String(15), nullable=True)
    add = Column(String(150), nullable=True)

class ApiData(Base):
    __tablename__ = 'app_apidata'
    id = Column(Integer, primary_key=True)
    sid = Column(String(150), nullable=True)
    token = Column(String(150), nullable=True)
    wp = Column(String(15), nullable=True)
    active = Column(Boolean, default=True)

class User(Base):
    __tablename__ = 'auth_user'
    id = Column(Integer, primary_key=True)
    password = Column(String)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    date_joined = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_superuser = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    organized_tournaments = relationship("Tournament", back_populates="organizer")

class BlackJWT(Base):
    __tablename__ = 'app_blacklist'
    id = Column(Integer, primary_key=True)
    token = Column(String)