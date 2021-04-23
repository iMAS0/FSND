from app import db


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    talent_description = db.Column(db.String(400))
    shows = db.relationship('Show',cascade = "all,delete", backref = "venue" , lazy = True)

    def __repr__(self):
      return f'<venue''s name: {self.id}>'


class Artist(db.Model):
    __tablename__ = 'Artist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venues = db.Column(db.Boolean)
    venue_description = db.Column(db.String(400))
    shows = db.relationship('Show',cascade = "all,delete" , backref="artist", lazy=True)
  
    def __repr__(self):
      return f'<artist''s name: {self.id}>'

class Show(db.Model):
  __tablename__ = 'Shows'
  id = db.Column(db.Integer , primary_key=True)
  artist_id = db.Column(db.Integer , db.ForeignKey('Artist.id') , nullable=False)
  venue_id = db.Column(db.Integer , db.ForeignKey('Venue.id') , nullable=False)
  start_date = db.Column(db.DateTime , nullable = False)
  def __repr__(self):
    return f'<artist''s id: {self.artist_id} , venue''s id: {self.venue_id} >'
