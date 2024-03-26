class MockSession:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def query(self, model):
        # Return a mock query object
        return self

    def filter(self, condition):
        # Return self to simulate chaining methods
        return self

    def first(self):
        # Return None to simulate no existing user
        return None

    def add(self, entity):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass

    def refresh(self, entity):
        pass

    def close(self):
        pass  
