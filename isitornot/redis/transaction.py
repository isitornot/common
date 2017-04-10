from . import Pool


class Transaction:
    """A context manager for transactions. Example:
    async with Transaction() as t:
        await t.set('foo', 'bar')

    async with Transaction() as t:
        await t.set('foo', 'bar')
        raise Transaction.Discard()  # silently discard

    async with Transaction as t:
        await t.set('foo', 'bar')
        t.blah  # throws and exception and discards the transaction
    """

    class Discard(Exception):
        """Raise this exception to silently discard a transaction. Any other exception will discard and pass through."""
        pass

    async def __aenter__(self):
        async with Pool() as conn:
            self.transaction = await conn.multi()
        return self.transaction

    async def __aexit__(self, exc_type, exc_val, _):
        if exc_val is None:
            await self.transaction.exec()
            self.transaction = None
        else:
            await self.transaction.discard()
            self.transaction = None
            if exc_type == Transaction.Discard:
                return True
