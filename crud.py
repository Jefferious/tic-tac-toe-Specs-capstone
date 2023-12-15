from model import db, User, connect_to_db

if __name__ == '__main__':
    from server import app
    connect_to_db(app)

def create_user(email, password, wins, losses, draws):
     user = User(email=email, password=password,
     wins=wins,
     losses=losses,
     draws=draws)

     return user



def update_user_stats(user_id, new_wins, new_losses, new_draws):
    user = User.query.get(user_id)
    user.wins = new_wins
    user.losses = new_losses
    user.draws = new_draws

    db.session.commit()

def get_users():
    """Return all users."""

    return User.query.all()


def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()

def get_user_wins(user_id):
    """Return a user's amount of wins"""
    user = User.query.get(user_id)
    if user is not None:
        return user.wins
    return None

def get_user_losses(user_id):
    """Return a user's amount of losses"""
    user = User.query.get(user_id)
    if user is not None:
        return user.losses
    return None

def get_user_draws(user_id):
    """Return a user's amount of draws"""
    user = User.query.get(user_id)
    if user is not None:
        return user.draws
    return None