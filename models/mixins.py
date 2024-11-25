"""These are mixins that all models should inherit from"""

from datetime import datetime

import sqlalchemy as sa
import sqlalchemy.orm as sao


class IDMixIn:
    """Mixin for ID fields"""

    id: sao.Mapped[int] = sao.mapped_column(primary_key=True, autoincrement=True)


class TimestampMixIn:
    """Mixin for timestamp fields that uses database timestamp"""

    created_at: sao.Mapped[datetime] = sao.mapped_column(
        server_default=sa.func.now(),
    )
    updated_at: sao.Mapped[datetime | None] = sao.mapped_column(
        default=None, onupdate=sa.func.now()
    )
