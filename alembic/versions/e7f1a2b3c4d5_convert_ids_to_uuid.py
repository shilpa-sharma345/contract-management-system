"""convert primary keys to UUID

Revision ID: e7f1a2b3c4d5
Revises: 1ca0dbde9760
Create Date: 2026-06-09 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = 'e7f1a2b3c4d5'
down_revision: Union[str, None] = '1ca0dbde9760'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto"')

    op.add_column('users', sa.Column('uuid_id', UUID(as_uuid=True), nullable=True))
    op.execute('UPDATE users SET uuid_id = gen_random_uuid()')

    op.add_column('contracts', sa.Column('uploaded_by_uuid', UUID(as_uuid=True), nullable=True))
    op.execute('''
        UPDATE contracts c
        SET uploaded_by_uuid = u.uuid_id
        FROM users u
        WHERE c.uploaded_by = u.id
    ''')

    op.drop_constraint('contracts_uploaded_by_fkey', 'contracts', type_='foreignkey')

    op.drop_column('contracts', 'id')
    op.drop_column('contracts', 'uploaded_by')
    op.drop_column('users', 'id')

    op.alter_column('users', 'uuid_id', new_column_name='id')
    op.alter_column('contracts', 'uploaded_by_uuid', new_column_name='uploaded_by')

    op.add_column('contracts', sa.Column('id', UUID(as_uuid=True), nullable=True))
    op.execute('UPDATE contracts SET id = gen_random_uuid()')

    op.alter_column('users', 'id', nullable=False)
    op.alter_column('contracts', 'id', nullable=False)
    op.alter_column('contracts', 'uploaded_by', nullable=False)

    op.create_primary_key('users_pkey', 'users', ['id'])
    op.create_primary_key('contracts_pkey', 'contracts', ['id'])

    op.create_foreign_key(
        'contracts_uploaded_by_fkey',
        'contracts', 'users',
        ['uploaded_by'], ['id']
    )


def downgrade() -> None:
    raise NotImplementedError(
        "Downgrade from UUID primary keys is not supported. Restore from backup."
    )
