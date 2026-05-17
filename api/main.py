from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
import models, schemas
import security

models.Base.metadata.create_all(bind=engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI(
    title="Reservation API",
    description="API for managing room reservations",
    version="1.0.0"
)

# --------------------------------------------------------------------------
# OBTENER UNA SESION EN LA BASE DE DATOS PARA REALIZAR OPERACIONES
# --------------------------------------------------------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() #Cerrar base de datos despues de usarla

@app.get("/")
def read_api():
    return {"message": "Welcome to the Reservation API!"}

# --------------------------------------------------------------------------
# ENDPOINT PARA CREAR UN NUEVO USUARIO
# --------------------------------------------------------------------------
@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    #Verificaremos si el correo ya existe en la base de datos
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    #Si el correo no existe, creamos un nuevo usuario
    nuevo_usuario = models.User(
        username=user.username,
        email=user.email,
        password=security.get_password_hash(user.password) # Llamamos a la función get_password_hash para hashear la contraseña antes de guardarla en la base de datos
    )

    #Guardamos el nuevo usuario en la base de datos
    db.add(nuevo_usuario)
    db.commit() #Confiraremos la transaccion para guardar el nuevo usuario en la base de datos
    db.refresh(nuevo_usuario) #Refrescar el objeto para obtener el ID generado

    return nuevo_usuario

# --------------------------------------------------------------------------
# ENDPOINT PARA CREAR UNA NUEVA SALA
# --------------------------------------------------------------------------
@app.post("/room/", response_model=schemas.RoomResponse)
def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    nueva_sala = models.Room(
        name_room=room.name_room,
        capacity=room.capacity
    )

    db.add(nueva_sala)
    db.commit() #Confirmamos la transaccion para guardar la nueva sala en la base de datos
    db.refresh(nueva_sala) #Refrescar el objeto para obtener el ID generado

    return nueva_sala

# --------------------------------------------------------------------------
# ENDPOINT PARA OBTENER TOKEN DE AUTENTICACION (JWT)
# --------------------------------------------------------------------------
@app.post("/login/", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    # Buscaremos al usuario en la base de datos por su correo
    # OJO: form_data.username se usa aqui porque OAuth2PasswordRequestForm espera un campo "username" para el correo, aunque en nuestro modelo de usuario se llame "email"
    user = db.query(models.User).filter(models.User.email == form_data.username).first()

    #Si el usuario no existe o la contraseña no es correcta, se devolvera un error de autenticacion
    if not user or not security.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    #Si las credenciales son correctas, se creara un token JWT con la informacion del usuario (en este caso, su ID) y se devolvera al cliente
    access_token = security.create_access_token(data={"sub": str(user.email)}) # Usamos el correo del usuario como "sub" (subject) en el token JWT

    return {"access_token": access_token, "token_type": "bearer"}

# --------------------------------------------------------------------------
# ENDPOINT para obtener la informacion del usuario autenticado usando el token JWT
# --------------------------------------------------------------------------
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    excepcion_credenciales = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        email: str | None = payload.get("sub")
        if email is None:
            raise excepcion_credenciales
    except JWTError:
        raise excepcion_credenciales
    
    #Buscaremos al usuario en la base de datos
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise excepcion_credenciales
    
    return user

# --------------------------------------------------------------------------
# ENDPOINT PARA CREAR UNA NUEVA RESERVA
# --------------------------------------------------------------------------
@app.post("/reservation/", response_model=schemas.ReservationResponse)
def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):

    #Haremos validaciones basicas de integridad
    conflicto = db.query(models.Reservation).filter(
        models.Reservation.room_id == reservation.room_id,
        models.Reservation.date_reservation == reservation.date_reservation,
        models.Reservation.time_start < reservation.time_end,
        models.Reservation.time_end > reservation.time_start
    ).first()

    #En caso de que ya exista una reservacion en la sala en la misma fecha y con un rango de horas que se crucen, se rechazara la solicitud de reserva, devolviendo un error al cliente
    #Logica del cruce: (Inicio_A < Fin_B) y (Fin_A > Inicio_B) -> Si esto se cumple, entonces hay un cruce entre las horas de la nueva reserva y una reserva existente
    if conflicto:
        raise HTTPException(status_code=400, detail="Reservation conflicts with an existing one or invalid time range")

    #Si no hay conflictos, se creara la nueva reserva con la informacion proporcionada por el cliente y se guardara en la base de datos
    nueva_reserva = models.Reservation(
        user_id=reservation.user_id,
        room_id=reservation.room_id,
        date_reservation=reservation.date_reservation,
        time_start=reservation.time_start,
        time_end=reservation.time_end
    )

    db.add(nueva_reserva)
    db.commit()
    db.refresh(nueva_reserva)

    return nueva_reserva

# --------------------------------------------------------------------------
# ENDPOINT PARA OBTENER TODAS LAS RESERVAS DEL USUARIO AUTENTICADO
# --------------------------------------------------------------------------
@app.get("/reservations/", response_model=list[schemas.ReservationResponse])
def list_reservations(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    #Obtenemos todas las reservas del usuario autenticado
    reservas = db.query(models.Reservation).filter(models.Reservation.user_id == current_user.id).all() #Filtramos las reservas por el ID del usuario autenticado para obtener solo sus reservas
    return reservas