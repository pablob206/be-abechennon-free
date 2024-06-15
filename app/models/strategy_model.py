"""Strategies models module"""

# Built-In
from datetime import datetime

# Third-Party
from mongoengine import DateTimeField, DictField, DynamicDocument, ListField, StringField


class Strategies(DynamicDocument):
    """Strategies"""

    name = StringField(required=True)
    description = StringField(required=False)
    createdAt = DateTimeField(required=False, default=datetime.utcnow)
    updatedAt = DateTimeField(required=False, onupdate=datetime.utcnow)
    data = ListField(DictField(), required=True)

    class Config:
        """config"""

        arbitrary_types_allowed = True
