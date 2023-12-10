Alembic підключений асинхронно завдяки зміні файлу migrations/env.py:

   1) def run_migrations() - приймає об'єкт Connection (підключення до бази даних) та використовує Alembic для виконання міграцій.
      context.configure налаштовує контекст Alembic з переданим підключенням та метаданими бази даних (target_metadata).
      Потім за допомогою context.begin_transaction() починається нова транзакція.
      context.run_migrations() фактично запускає процес міграції.
   2) async def run_async_migrations() - це асинхронна функція, яка використовує [asyncio] для керування асинхронними операціями.
      async_engine_from_config створює асинхронний двигун (engine) для роботи з базою даних на основі конфігурації SQLAlchemy.
      async with conectable.connect() встановлює асинхронне з'єднання з базою даних.
      await connection.run_sync(run_migrations) запускає синхронну функцію run_migrations за допомогою асинхронного з'єднання.
      await conectable.dispose() звільняє ресурси асинхронного з'єднання після завершення операції.
   3) def run_migrations_online() - це обгортка для запуску асинхронної функції run_async_migrations з використанням asyncio.run.
      У стандартному синхронному коді asyncio.run використовується для запуску корутини в блокуючому стилі ("запуск корутини в
      блокуючому стилі" означає використання asyncio.run для запуску асинхронної функції в блокуючій (синхронній) програмі).

PostgreSQL підключений асинхронно за допомогою [asyncpg]