Alembic ���������� ���������� ������� ��� ����� migrations/env.py:

   1) def run_migrations() - ������ ��'��� Connection (���������� �� ���� �����) �� ����������� Alembic ��� ��������� �������.
      context.configure ��������� �������� Alembic � ��������� ����������� �� ���������� ���� ����� (target_metadata).
      ���� �� ��������� context.begin_transaction() ���������� ���� ����������.
      context.run_migrations() �������� ������� ������ �������.
   2) async def run_async_migrations() - �� ���������� �������, ��� ����������� [asyncio] ��� ��������� ������������ ����������.
      async_engine_from_config ������� ����������� ������ (engine) ��� ������ � ����� ����� �� ����� ������������ SQLAlchemy.
      async with conectable.connect() ���������� ���������� �'������� � ����� �����.
      await connection.run_sync(run_migrations) ������� ��������� ������� run_migrations �� ��������� ������������ �'�������.
      await conectable.dispose() ������� ������� ������������ �'������� ���� ���������� ��������.
   3) def run_migrations_online() - �� �������� ��� ������� ���������� ������� run_async_migrations � ������������� asyncio.run.
      � ������������ ����������� ��� asyncio.run ��������������� ��� ������� �������� � ���������� ���� ("������ �������� �
      ���������� ����" ������ ������������ asyncio.run ��� ������� ���������� ������� � ��������� (���������) �������).

PostgreSQL ���������� ���������� �� ��������� [asyncpg]