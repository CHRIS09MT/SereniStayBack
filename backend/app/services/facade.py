from app.persistence.repository_interface import (
    UserRepository, ServiceRepository,
    SpaRepository, BookingRepository)
from app.models.user import User
from app.models.spa import Spa, CreateSpa
from app.models.service import Service
from app.models.booking import Booking
from uuid import UUID


class Facade:
    def __init__(self):
        self.user_db = UserRepository()
        self.spa_db = SpaRepository()
        self.service_db = ServiceRepository()
        self.booking_db = BookingRepository()



# ___________________________________User______________________________________________________
    
    async def create_user(self, user_data):
        user = User(**user_data)
        return await self.user_db.add(user.model_dump())
    
    async def update_user(self, user_id: UUID, user_data):
        return await self.user_db.update(str(user_id), user_data)
    
    async def get_user_by_attribute(self, attr_name, attr_value):
        return await self.user_db.get_by_attribute(attr_name, attr_value)
    
    async def get_all_users(self):
        return await self.user_db.get_all()
    
    async def delete_user(self, user_id: UUID):
        try:
            return await self.user_db.delete(user_id)
        except ValueError as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": str(e)}
        
    async def authenticate_user(self, email: str, password: str):
        """
        Search the user in the database and verify the password.
        """
        user_dict = await self.user_db.get_by_attribute("email", email)

        if not user_dict:
            return None

        if isinstance(user_dict, dict) and "user" in user_dict:
            user_dict = user_dict["user"]

        required_fields = {"email", "hashed_password"}
        if not required_fields.issubset(user_dict.keys()):
            return None

        try:
            user_model = User(**user_dict)

        except Exception as e:
            return None

        if not user_model.verify_password(password, user_model.hashed_password):
            return None

        return user_model



# ___________________________________Service______________________________________________________

    async def create_service(self, service_data):
        service = Service(**service_data)
        return await self.service_db.add(service.model_dump())
    
    async def update_service(self, service_id: UUID, service_data):
        return await self.service_db.update(service_id, service_data)
    
    async def delete_service(self, service_id: UUID):
        try:
            return await self.service_db.delete(service_id)
        except ValueError as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": str(e)}



# ___________________________________Booking______________________________________________________
    
    async def create_booking(self, booking_data):
        booking = Booking(**booking_data)
        return await self.booking_db.add(booking.model_dump())
    
    async def get_booking_by_id(self, booking_id: UUID):
        return await self.booking_db.get_by_id(str(booking_id))
    
    async def get_all_bookings(self):
        return await self.booking_db.get_all()
    
    async def update_booking(self, booking_id: UUID, booking_data):
        return await self.booking_db.update(booking_id, booking_data)
    
    async def delete_booking(self, booking_id: UUID):
        try:
            return await self.booking_db.delete(booking_id)
        except ValueError as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": str(e)}


# ___________________________________Spa______________________________________________________

    async def create_spa(self, spa_data: dict):
        """Create a new spa and return the full object"""
        spa = Spa(**spa_data)
        spa_id = await self.spa_db.add(spa.model_dump())  # Guardar y obtener el ID

        # Recuperar el spa completo desde la BD
        return await self.spa_db.get_by_attribute("_id", spa_id)  # Asegurar que devuelve un Spa

