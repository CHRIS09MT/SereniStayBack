from app.persistence.repository_interface import (
    UserRepository, ServiceRepository,
    SpaRepository, BookingRepository, ReviewRepository)
from app.models.user import User
from app.models.spa import Spa
from app.models.service import Service
from app.models.booking import Booking
from app.models.review import Review
from uuid import UUID
from typing import List
from fastapi import HTTPException


class Facade:
    def __init__(self):
        self.user_db = UserRepository()
        self.spa_db = SpaRepository()
        self.service_db = ServiceRepository()
        self.booking_db = BookingRepository()
        self.review_db = ReviewRepository()



# ___________________________________User______________________________________________________
    
    async def create_user(self, user_data):
        user = User(**user_data)
        return await self.user_db.add(user.model_dump())
    
    async def update_user(self, user_id: UUID, user_data):
        return await self.user_db.update(str(user_id), user_data)
    
    async def get_user_by_id(self, attr_name, attr_value):
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
    
    async def create_multiple_services(self, services: List[dict]):
        """Guarda múltiples servicios en la base de datos"""
        service_ids = []
        for service in services:
            service_id = await self.service_db.add(service)  # Guarda cada servicio
            service_ids.append(service_id)
        return {"message": "Services created successfully", "service_ids": service_ids}
    
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
        """search a booking by id"""
        return await self.booking_db.get_by_id(str(booking_id))
    
    async def get_all_bookings(self):
        """show all bookings"""

        # bookings = await self.booking_db.get_all()

        # filtered_bookings = []
        # for booking in bookings

        return await self.booking_db.get_all()

    async def update_booking(self, booking_id: UUID, booking_data):
        existing_booking = await self.booking_db.get_by_id(str(booking_id))
        if not existing_booking:
            return {"error": "Booking not found"}
    
        current_status = existing_booking.get("status")
        new_status = booking_data.get("status")
    
        if new_status and current_status == "cancelled":
            return {"error": "Cannot modify a cancelled booking"}
    
        return await self.booking_db.update(booking_id, booking_data)
    
    async def delete_booking(self, booking_id: str):
        try:
            return await self.booking_db.cancel_booking(booking_id)
        except ValueError as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": str(e)}


# ___________________________________Spa______________________________________________________

    async def create_spa(self, spa_data: dict):
        services = spa_data.pop("services", [])  # Extraer servicios antes de validar
        spa = Spa(**spa_data)
        spa_id = await self.spa_db.add(spa.model_dump())  # Guardar spa y obtener ID
    
        # Guardar los servicios en la colección de servicios con referencia al spa
        for service in services:
            service["spa_id"] = spa_id  # Agregar referencia al spa
            await self.service_db.add(service)
    
        return await self.spa_db.get_by_attribute("id", spa_id)


    async def list_spas(self):
        return await self.spa_db.get_all()




# ___________________________________Review______________________________________________________

    async def create_review(self, text):
        """create a review"""

        review = Review(**text)  # BaseEntity ya genera el id

        # Guardar en MongoDB
        review_id = await self.review_db.add(review.model_dump())  
        return {"success": True, "review_id": review_id}
    

    async def get_reviews(self, spa_id: UUID):
        """Get all reviews for a specific spa"""

        reviews = await self.review_db.get_by_attribute("spa_id", str(spa_id))

        if not reviews:
            raise HTTPException(status_code=404, detail="No reviews found for this spa")

        return reviews
