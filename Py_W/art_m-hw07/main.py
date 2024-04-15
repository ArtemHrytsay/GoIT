import seed
import sqlalchemy as sa
import sqlalchemy.orm as orm

_engine = None
_session = None

class Connection:
    def engine(args = None):
        global _engine
        if _engine is None:
            if args and args.url:
                url = args.url
            else:
                url = "postgresql+psycopg2://postgres:hw07@localhost:5432/postgres"
            _engine  = sa.create_engine(url)
        return _engine

    def session():
        global _session
        if _session is None:
            _session = orm.sessionmaker(bind=Connection.engine())()
        return _session
    
    def connect(args = None):
        Connection.engine(args)
        Connection.session()
        return _engine, _session


def main():
    Connection.connect()

    try:
        open(".lock","r")
    except FileNotFoundError as e:
        seed.seed(Connection.session())
        open(".lock","w")


if __name__ == "__main__":
    main()
