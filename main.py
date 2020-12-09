import strategies
import generators
import queries

strategies.PasswordsLoginsLimitedStrategy(
    login_generator=generators.PopularStringGenerator(),
    password_generator=generators.PopularStringGenerator(),
    query=queries.try_local_server,
).run()