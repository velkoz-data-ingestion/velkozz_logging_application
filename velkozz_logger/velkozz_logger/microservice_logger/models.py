# Importing Project Objects:
from .. import db

# Genetic Log Data Model: 
class MicroServiceLog(db.Model):

    __tablename__ = "microservice-logs"

    name = db.Column(
        db.String(100),
        index=False,
        unique=False,
        nullable=False
    )
    
    msg = db.Column(
        db.Text,
        index=False,
        unique=False,
        nullable=True
    )

    app_name = db.Column(
        db.String(100),
        index=False,
        unique=False,
        nullable=True
    )

    process_type = db.Column(
        db.String(100),
        index=False,
        unique=False,
        nullable=True
    )
    
    timestamp = db.Column(
        db.TIMESTAMP,
        primary_key=True,
        index=True,
        unique=False,
        nullable=True
    )

    status_code = db.Column(
        db.Integer,
        index=False,
        unique=False,
        nullable=True
    )

    levelname = db.Column(
        db.String(100),
        index=False,
        unique=False,
        nullable=True
    )

    created = db.Column(
        db.TIMESTAMP,
        index=False,
        unique=False,
        nullable=True
    )
    
    lineno = db.Column(
        db.Integer, 
        index=False,
        unique=False,
        nullable=True
    )

    funcName = db.Column(
        db.String(100),
        index=False,
        unique=False,
        nullable=True
    )
    
    msecs = db.Column(
        db.Float,
        index=False,
        unique=False,
        nullable=True
    )

    relativeCreated = db.Column(
        db.TIMESTAMP,
        index=False,
        unique=False,
        nullable=True
    )
    
    thread = db.Column(
        db.Float,
        index=False,
        unique=False,
        nullable=True
    )

    threadName = db.Column(
        db.String(100),
        index=False,
        unique=False,
        nullable=True   
    )

    processName = db.Column(        
        db.String(100),
        index=False,
        unique=False,
        nullable=True
    )

    process = db.Column(
        db.String(100),
        index=False,
        unique=False,
        nullable=True
    )

    def __repr__(self): 
        return f"{self.app_name}{self.processName}{self.timestamp}"

# Microservice Objects:
class Microservice(db.Model):

    __tablename__ = "microservices"

    microservice_name = db.Column(
        db.String(100),
        primary_key=True,
        unique=True
    )

    microservice_description = db.Column(
        db.String(200),
        nullable=True,
        unique=False
    )

    date_added = db.Column(
        db.TIMESTAMP,
        nullable=True
    )

    def __repr__(self): 
        return f"{self.microservice_name}"
