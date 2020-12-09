class BaseStrategy:
    def __init__(self, login_generator, password_generator, query):
        self.login_generator = login_generator
        self.password_generator = password_generator
        self.query = query

    def run(self):
        raise NotImplementedError


class DumbStrategy(BaseStrategy):

    def run(self):
        login = self.login_generator.generate()
        self.try_password_for_login(login)

    def try_password_for_login(self, login):
        self.password_generator.reset()
        while True:
            password = self.password_generator.generate()
            if password is None:
                break
            # print('Trying...', login, password)
            if self.query(login, password):
                print('SUCCESS', login, password)
                break


class LoginsDumbStrategy(DumbStrategy):

    def run(self):
        while True:
            login = self.login_generator.generate()
            if login is None:
                return
            self.try_password_for_login(login)


class PasswordsLoginsLimitedStrategy(BaseStrategy):

    def __init__(self, login_generator, password_generator, query,
                 limit_logins=100, limit_passwords=None):
        super().__init__(login_generator, password_generator, query)
        self.limit_logins = limit_logins
        self.limit_passwords = limit_passwords

    def run(self):
        i = 0
        while self.limit_passwords is None or i < self.limit_passwords:
            i += 1
            password = self.password_generator.generate()
            if password is None:
                break
            self.login_generator.reset()
            for j in range(self.limit_logins):
                login = self.login_generator.generate()
                if login is None:
                    break
                if self.query(login, password):
                    print('SUCCESS', login, password)
                    break