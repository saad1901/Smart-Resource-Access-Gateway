from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Numeric, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum
from config.dependencies import Base2

class RoleChoices(enum.Enum):
    superadmin = "SuperAdmin"
    admin = "Admin"
    agent = "Agent"
    owner = "Owner"
    staff = "Staff"

class User(Base2):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(150), unique=True, nullable=False)
    password = Column(String(128))
    email = Column(String(254))
    first_name = Column(String(30))
    last_name = Column(String(150))
    is_active = Column(Boolean, default=True)
    is_staff = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    last_login = Column(DateTime)
    date_joined = Column(DateTime, default=datetime.utcnow)
    
    hint = Column(String(40))
    phone = Column(String(15))
    city = Column(String(100))
    role = Column(Enum(RoleChoices), default=RoleChoices.staff)
    staffof_id = Column(Integer, ForeignKey('hotels.id'))
    
    # staffof = relationship("Hotel", back_populates="staff_members")
    
    def __repr__(self):
        return f"<User(username='{self.username}')>"

class Hotel(Base2):
    __tablename__ = 'hotels'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    address = Column(Text)
    owner_id = Column(Integer, ForeignKey('users.id'))
    status = Column(Boolean, default=False)
    agent_id = Column(Integer, ForeignKey('users.id'))
    
    # owner = relationship("User", foreign_keys=[owner_id])
    # agent = relationship("User", foreign_keys=[agent_id])
    # staff_members = relationship("User", back_populates="staffof")
    # tables = relationship("Table", back_populates="hotel")
    # menu_categories = relationship("MenuCategory", back_populates="hotel")
    # menu_items = relationship("MenuItem", back_populates="hotel")
    # orders = relationship("Order", back_populates="hotel")
    # payment_details = relationship("PaymentDetails", back_populates="hotel")
    # inventory_items = relationship("InventoryItem", back_populates="hotel")
    
    def __repr__(self):
        return f"<Hotel(name='{self.name}')>"

class Table(Base2):
    __tablename__ = 'tables'
    
    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer, ForeignKey('hotels.id'))
    name = Column(String(100))
    occupied = Column(Boolean, default=False)
    
    # hotel = relationship("Hotel", back_populates="tables")
    # orders = relationship("Order", back_populates="table")
    
    def __repr__(self):
        return f"<Table(name='{self.name}')>"

class MenuCategory(Base2):
    __tablename__ = 'menu_categories'
    
    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer, ForeignKey('hotels.id'))
    name = Column(String(100))
    icon = Column(String(50))
    
    # hotel = relationship("Hotel", back_populates="menu_categories")
    # menu_items = relationship("MenuItem", back_populates="category")
    # inventory_items = relationship("InventoryItem", back_populates="category")
    
    def __repr__(self):
        return f"<MenuCategory(name='{self.name}')>"

class MenuItem(Base2):
    __tablename__ = 'menu_items'
    
    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer, ForeignKey('hotels.id'))
    category_id = Column(Integer, ForeignKey('menu_categories.id'))
    name = Column(String(100))
    price = Column(Numeric(6, 2))
    
    # hotel = relationship("Hotel", back_populates="menu_items")
    # category = relationship("MenuCategory", back_populates="menu_items")
    # order_items = relationship("OrderItems", back_populates="item")
    
    def __repr__(self):
        return f"<MenuItem(name='{self.name}', price={self.price})>"

class Order(Base2):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer, ForeignKey('hotels.id'))
    table_id = Column(Integer, ForeignKey('tables.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    total = Column(Numeric(6, 2), default=0)
    discount = Column(Numeric(6, 2), default=0)
    completed = Column(Boolean, default=False)
    phone_number = Column(String(15))
    completedby_id = Column(Integer, ForeignKey('users.id'))
    
    # hotel = relationship("Hotel", back_populates="orders")
    # table = relationship("Table", back_populates="orders")
    # completedby = relationship("User")
    # order_items = relationship("OrderItems", back_populates="order")
    
    def __repr__(self):
        return f"<Order(id={self.id}, hotel='{self.hotel.name}')>"

class OrderItems(Base2):
    __tablename__ = 'order_items'
    
    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer, ForeignKey('hotels.id'))
    item_id = Column(Integer, ForeignKey('menu_items.id'))
    order_id = Column(Integer, ForeignKey('orders.id'))
    quantity = Column(Integer, default=1)
    
    # hotel = relationship("Hotel")
    # item = relationship("MenuItem", back_populates="order_items")
    # order = relationship("Order", back_populates="order_items")
    
    def __repr__(self):
        return f"<OrderItems(item='{self.item.name}', quantity={self.quantity})>"

class PaymentDetails(Base2):
    __tablename__ = 'payment_details'
    
    id = Column(Integer, primary_key=True)
    upiid = Column(String(100))
    name = Column(String(100))
    hotel_id = Column(Integer, ForeignKey('hotels.id'))
    
    # hotel = relationship("Hotel", back_populates="payment_details")
    
    def __repr__(self):
        return f"<PaymentDetails(upiid='{self.upiid}')>"

class UnitChoices(enum.Enum):
    kg = "Kilograms"
    g = "Grams"
    l = "Liters"
    ml = "Milliliters"
    pcs = "Pieces"
    pkg = "Packages"
    box = "Boxes"

class StatusChoices(enum.Enum):
    in_stock = "In Stock"
    low_stock = "Low Stock"
    out_of_stock = "Out of Stock"

class InventoryItem(Base2):
    __tablename__ = 'inventory_items'
    
    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer, ForeignKey('hotels.id'))
    name = Column(String(100))
    description = Column(Text)
    quantity = Column(Numeric(10, 2))
    unit = Column(Enum(UnitChoices), default=UnitChoices.pcs)
    unit_price = Column(Numeric(10, 2))
    reorder_level = Column(Numeric(10, 2), default=10)
    status = Column(Enum(StatusChoices), default=StatusChoices.in_stock)
    category_id = Column(Integer, ForeignKey('menu_categories.id'))
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # hotel = relationship("Hotel", back_populates="inventory_items")
    # category = relationship("MenuCategory", back_populates="inventory_items")
    # transactions = relationship("InventoryTransaction", back_populates="item")
    
    def __repr__(self):
        return f"<InventoryItem(name='{self.name}', quantity={self.quantity} {self.unit})>"

class TransactionType(enum.Enum):
    purchase = "Purchase"
    usage = "Usage"
    adjustment = "Adjustment"
    writeoff = "Write-off"

class InventoryTransaction(Base2):
    __tablename__ = 'inventory_transactions'
    
    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer, ForeignKey('hotels.id'))
    item_id = Column(Integer, ForeignKey('inventory_items.id'))
    transaction_type = Column(Enum(TransactionType))
    quantity = Column(Numeric(10, 2))
    transaction_date = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)
    created_by_id = Column(Integer, ForeignKey('users.id'))
    unit_price = Column(Numeric(10, 2))
    
    # hotel = relationship("Hotel")
    # item = relationship("InventoryItem", back_populates="transactions")
    # created_by = relationship("User")
    
    def __repr__(self):
        return f"<InventoryTransaction(type='{self.transaction_type}', item='{self.item.name}')>"