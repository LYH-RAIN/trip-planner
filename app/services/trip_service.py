from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import and_, or_, desc
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta, date, time
import math # For ceil in pagination
import json # For parsing JSON fields from DB if necessary

from app.models.trip import Trip, TripDay, TripPlace, TripFood, TripTransportation
from app.models.user import User # Assuming User model has 'id', 'nickname', 'avatar_url'
# Assuming a TripCollaborator model might exist if you store collaborators in DB explicitly
# from app.models.trip import TripCollaborator

from app.schemas.trip import (
    TripCreate, TripUpdate, 
    TripFullResponse, # Changed from TripResponse
    TripListResponse, TripListItemResponse, TripCollaboratorInfo, # Added new schemas
    TripOverviewResponse, TripDayOverviewItem, # Renamed TripDayResponse to TripDayOverviewItem
    TripDayDetailResponse,
    TripDayUpdate, TripFoodsResponse, TripFoodResponseItem, # Renamed TripFoodResponse
    ItineraryItem, WeatherInfo, AccommodationInfo, PointInfo,
    NavigationInfo, LocationPoint,
    TripCancelRequest, TripCancelResponseData, TripDayUpdateItineraryItem # Added for cancel and itinerary update
)
from app.core.exceptions import NotFoundError, PermissionError, ValidationError
from app.services.weather_service import WeatherService
# Placeholder for a potential Location/POI service if needed for name resolution
# from app.services.location_service import LocationService

class TripService:
    def __init__(self, db: Session):
        self.db = db
        self.weather_service = WeatherService()
        # self.location_service = LocationService() # If POI name resolution is needed

    def create_trip(self, trip_data: TripCreate, user_id: int) -> TripFullResponse:
        # 计算行程天数
        days = (trip_data.end_datetime.date() - trip_data.start_datetime.date()).days + 1
        if days <= 0:
            raise ValidationError("行程结束日期必须在开始日期之后")

        # Resolve POI names if your Trip model stores them and TripCreate only has IDs
        # For now, this example assumes Trip model fields like departure_poi_id, destinations (list of POI IDs)
        # departure_name_resolved = self.location_service.get_poi_name(trip_data.departure) # Example
        # destination_names_resolved = [self.location_service.get_poi_name(poi_id) for poi_id in trip_data.destinations]

        db_trip = Trip(
            user_id=user_id,
            title=trip_data.title,
            description=trip_data.description,
            departure_poi_id=trip_data.departure, 
            # departure_name=departure_name_resolved, # If you have this field
            destinations=trip_data.destinations, # Storing as list of POI IDs
            # destination_names=destination_names_resolved, # If you store resolved names
            start_datetime=trip_data.start_datetime,
            end_datetime=trip_data.end_datetime,
            start_timezone=trip_data.start_timezone,
            end_timezone=trip_data.end_timezone,
            days=days,
            people_count=trip_data.people_count,
            travel_mode=trip_data.travel_mode,
            preferences=trip_data.preferences,
            budget=trip_data.budget,
            tags=trip_data.tags,
            is_public=trip_data.is_public,
            # Default values for fields not in TripCreate
            status=0,  # Planning
            generation_status=0, # Not generated
            view_count=0,
            like_count=0,
            share_count=0,
            # cover_image: will be None by default unless set
            # overview: will be None by default
            # estimated_cost: will be None by default
        )

        self.db.add(db_trip)
        self.db.commit()
        self.db.refresh(db_trip)

        self._create_trip_days(db_trip)
        self.db.refresh(db_trip) # Refresh again in case _create_trip_days modifies trip state (e.g. relationships)

        # Prepare collaborators for the response
        creator_user_model = self.db.query(User).filter(User.id == user_id).first()
        collaborators_info_list = []
        if creator_user_model:
             collaborators_info_list.append(TripCollaboratorInfo(
                 user_id=creator_user_model.id,
                 avatar_url=creator_user_model.avatar_url, # Ensure User model has avatar_url
                 role="owner"
             ))
        
        # Construct the TripFullResponse.
        # Using .from_orm() is preferred if the model is set up for it.
        # Otherwise, manual instantiation is necessary.
        # We need to ensure all fields of TripFullResponse are present.
        
        # Assuming Trip.destinations stores list of POI IDs, and TripFullResponse also expects list of POI IDs.
        # If TripFullResponse expects list of names, resolution is needed here or in Trip.destinations_resolved property.
        
        return TripFullResponse(
            id=db_trip.id,
            user_id=db_trip.user_id,
            title=db_trip.title,
            description=db_trip.description,
            departure=db_trip.departure_poi_id, # This should be the POI ID as per TripCreate
            destinations=db_trip.destinations,   # This should be list of POI IDs as per TripCreate
            start_datetime=db_trip.start_datetime,
            end_datetime=db_trip.end_datetime,
            start_timezone=db_trip.start_timezone,
            end_timezone=db_trip.end_timezone,
            days=db_trip.days,
            people_count=db_trip.people_count,
            travel_mode=db_trip.travel_mode,
            preferences=db_trip.preferences,
            budget=db_trip.budget,
            tags=db_trip.tags,
            is_public=db_trip.is_public,
            overview=db_trip.overview,
            estimated_cost=db_trip.estimated_cost,
            status=db_trip.status,
            generation_status=db_trip.generation_status, # Ensure Trip model has this
            view_count=db_trip.view_count, # Ensure Trip model has this
            like_count=db_trip.like_count, # Ensure Trip model has this
            share_count=db_trip.share_count, # Ensure Trip model has this
            cover_image=db_trip.cover_image, # Ensure Trip model has this
            collaborators=collaborators_info_list,
            collaborator_count=len(collaborators_info_list),
            created_at=db_trip.created_at,
            updated_at=db_trip.updated_at
        )

    def get_trips(
            self,
            user_id: int,
            status: Optional[str] = None,
            trip_id: Optional[int] = None,
            page: int = 1,
            page_size: int = 20,
            include_days: Optional[bool] = False
    ) -> TripListResponse:
        query = self.db.query(Trip)
        
        if trip_id:
            # If trip_id is provided, fetch only that trip
            # Apply joinedload for days and their related data if include_days is true
            options = []
            if include_days:
                options.append(
                    selectinload(Trip.days_relationship) # Assuming 'days_relationship' is the name in Trip model for TripDay
                    .joinedload(TripDay.places) # Assuming relation to TripPlace for attractions
                ) 
                # Add other relationships to TripDay if needed for _build_trip_day_overview_item

            trip_model = query.options(*options).filter(Trip.id == trip_id).first()
            
            if not trip_model:
                raise NotFoundError(f"行程ID {trip_id} 未找到")
            
            self._get_trip_with_permission(trip_model, user_id) # Check permission using the fetched trip object

            list_item = self._convert_trip_to_list_item_response(trip_model, include_days)
            return TripListResponse(
                total=1, page=1, page_size=1, total_pages=1,
                has_next=False, has_prev=False, trips=[list_item]
            )

        # General query for list, filter by user_id (owner) or collaborator status
        # For simplicity, keeping user_id filter. Real app might check a collaborators table.
        query = query.filter(Trip.user_id == user_id)

        if status and status.lower() != "all":
            status_map = { "planning": 0, "completed": 1, "cancelled": 2, "inprogress": 3 }
            if status.lower() in status_map:
                query = query.filter(Trip.status == status_map[status.lower()])
            else:
                raise ValidationError(f"无效的状态值: {status}")

        total = query.count()
        total_pages = math.ceil(total / page_size)
        
        # Apply joinedload for days if include_days is true for the list
        query_options = []
        if include_days:
            query_options.append(
                selectinload(Trip.days_relationship) # Adjust to your actual relationship name
                .joinedload(TripDay.places) # Example, adjust as needed for _build_trip_day_overview_item
            )

        trips_models = query.options(*query_options).order_by(desc(Trip.created_at)).offset((page - 1) * page_size).limit(page_size).all()
        
        response_trips = [self._convert_trip_to_list_item_response(trip_model, include_days) for trip_model in trips_models]

        return TripListResponse(
            total=total, page=page, page_size=page_size,
            total_pages=total_pages,
            has_next=(page < total_pages),
            has_prev=(page > 1),
            trips=response_trips
        )

    def _convert_trip_to_list_item_response(self, trip: Trip, include_days: bool) -> TripListItemResponse:
        # Collaborators
        owner = self.db.query(User).filter(User.id == trip.user_id).first() # Optimized to fetch only if needed below
        collaborators_info = []
        if owner: # Assuming owner is always a collaborator
            collaborators_info.append(TripCollaboratorInfo(
                user_id=owner.id, avatar_url=owner.avatar_url, role="owner"))
        # Add logic for other collaborators if your Trip model has a relationship for them

        weather_info_data = None
        if trip.weather_info: # Assuming weather_info is a JSON string column in Trip model
            try:
                weather_info_data = json.loads(trip.weather_info)
            except json.JSONDecodeError:
                weather_info_data = None # Or log an error

        days_overview_data: Optional[List["TripDayOverviewItem"]] = None
        if include_days:
            days_overview_data = []
            # Ensure trip.days_relationship is loaded if using selectinload, or query here
            # If not preloaded: trip_days_models = self.db.query(TripDay).filter(TripDay.trip_id == trip.id)...
            trip_days_models = sorted(trip.days_relationship, key=lambda d: d.day_index) if trip.days_relationship else []

            for day_model in trip_days_models:
                days_overview_data.append(self._build_trip_day_overview_item(day_model))
        
        # Create the TripListItemResponse
        # Note: This assumes TripListItemResponse has an 'days_overview' field if include_days is true.
        # If it doesn't, this part needs adjustment or the schema needs an update.
        item_data = {
            "id": trip.id,
            "title": trip.title,
            "description": trip.description,
            "cover_image": trip.cover_image,
            "start_datetime": trip.start_datetime,
            "end_datetime": trip.end_datetime,
            "days": trip.days,
            "travel_mode": trip.travel_mode,
            "people_count": trip.people_count,
            "status": trip.status,
            "is_public": trip.is_public, # Keep as int, consistent with TripFullResponse and DB
            "weather_info": weather_info_data,
            "estimated_cost": trip.estimated_cost,
            "budget": trip.budget,
            "tags": trip.tags, # Assuming Trip.tags is already a list of strings
            "collaborators": collaborators_info,
            "collaborator_count": len(collaborators_info), # Or from a direct count if available
            "user_id": trip.user_id,
            "created_at": trip.created_at,
            "updated_at": trip.updated_at
        }
        if include_days:
             item_data["days_overview"] = days_overview_data

        return TripListItemResponse(**item_data)

    def get_trip_overview(self, trip_id: int, user_id: int) -> TripOverviewResponse:
        # Use options to preload related days and their necessary sub-relations for overview
        options = [
            selectinload(Trip.days_relationship) # Assuming 'days_relationship' for TripDay
                .joinedload(TripDay.places), # For attractions in TripDayOverviewItem
            # Add other relations for TripDay if needed by _build_trip_day_overview_item
            # e.g., .joinedload(TripDay.start_point_relation_name), .joinedload(TripDay.end_point_relation_name)
        ]
        trip_model = self.db.query(Trip).options(*options).filter(Trip.id == trip_id).first()

        if not trip_model:
            raise NotFoundError(f"行程ID {trip_id} 未找到")
        
        self._get_trip_with_permission(trip_model, user_id) # Pass the fetched model

        # Construct TripFullResponse for trip_info part
        # This can reuse parts of create_trip's response construction logic for consistency
        creator_user_model = self.db.query(User).filter(User.id == trip_model.user_id).first()
        collaborators_info_list = []
        if creator_user_model:
             collaborators_info_list.append(TripCollaboratorInfo(
                 user_id=creator_user_model.id,
                 avatar_url=creator_user_model.avatar_url,
                 role="owner"
             ))
        # Add other collaborators if applicable

        trip_info_response = TripFullResponse(
            id=trip_model.id, user_id=trip_model.user_id, title=trip_model.title,
            description=trip_model.description, departure=trip_model.departure_poi_id,
            destinations=trip_model.destinations, start_datetime=trip_model.start_datetime,
            end_datetime=trip_model.end_datetime, start_timezone=trip_model.start_timezone,
            end_timezone=trip_model.end_timezone, days=trip_model.days,
            people_count=trip_model.people_count, travel_mode=trip_model.travel_mode,
            preferences=trip_model.preferences, budget=trip_model.budget,
            tags=trip_model.tags, is_public=trip_model.is_public,
            overview=trip_model.overview, estimated_cost=trip_model.estimated_cost,
            status=trip_model.status, generation_status=trip_model.generation_status,
            view_count=trip_model.view_count, like_count=trip_model.like_count,
            share_count=trip_model.share_count, cover_image=trip_model.cover_image,
            collaborators=collaborators_info_list,
            collaborator_count=len(collaborators_info_list),
            created_at=trip_model.created_at, updated_at=trip_model.updated_at
        )
        
        days_overview_items: List["TripDayOverviewItem"] = []
        # Ensure days_relationship is sorted if not implicitly by DB query
        sorted_days = sorted(trip_model.days_relationship, key=lambda d: d.day_index) if trip_model.days_relationship else []
        for day_model in sorted_days:
            days_overview_items.append(self._build_trip_day_overview_item(day_model))

        return TripOverviewResponse(
            trip_info=trip_info_response,
            days_overview=days_overview_items
        )

    def _build_trip_day_overview_item(self, day: TripDay) -> "TripDayOverviewItem":
        # Attractions: Ensure day.places is loaded (e.g., via joinedload/selectinload)
        # or query them here: self.db.query(TripPlace).filter(TripPlace.day_id == day.id, ...).all()
        attraction_models = [p for p in day.places if p.category == "景点"][:2] if day.places else [] # Example
        
        attractions_data = [{"name": att.name, "image_url": att.image_url} for att in attraction_models]

        return TripDayOverviewItem(
            day_index=day.day_index,
            date=day.date,
            title=day.title,
            city=day.city,
            is_generated=day.is_generated == 1,
            estimated_cost=day.estimated_cost,
            start_location=self._build_point_info_for_overview(day.start_point_name, day.start_point_time, day.start_point_poi_id),
            end_location=self._build_point_info_for_overview(day.end_point_name, day.end_point_time, day.end_point_poi_id),
            weather=self._build_weather_info(day), 
            attractions=attractions_data
        )
        
    def _build_point_info_for_overview(self, name: Optional[str], time_val: Optional[time], poi_id: Optional[str] = None) -> Optional[PointInfo]:
        if not name:
            return None
        # For overview, type might not be strictly necessary unless displayed
        return PointInfo(name=name, time=time_val, poi_id=poi_id, type=None) 


    def get_trip_day_detail(self, trip_id: int, day_index: int, user_id: int) -> TripDayDetailResponse:
        # Preload TripDay with its related itinerary items (places, foods, transportations)
        options = [
            selectinload(Trip.days_relationship)
                .joinedload(TripDay.places), # Assuming TripDay.places is the relationship to TripPlace
            selectinload(Trip.days_relationship)
                .joinedload(TripDay.foods),  # Assuming TripDay.foods is the relationship to TripFood
            selectinload(Trip.days_relationship)
                .joinedload(TripDay.transportations), # Assuming TripDay.transportations
        ]
        trip_model = self.db.query(Trip).options(*options).filter(Trip.id == trip_id).first()

        if not trip_model:
            raise NotFoundError(f"行程ID {trip_id} 未找到")

        self._get_trip_with_permission(trip_model, user_id)

        day_model = None
        for d in trip_model.days_relationship: # Iterate through preloaded days
            if d.day_index == day_index:
                day_model = d
                break
        
        if not day_model:
            raise NotFoundError(f"行程第 {day_index} 天未找到")

        itinerary_items = self._build_itinerary(day_model)

        return TripDayDetailResponse(
            trip_id=trip_id,
            day_index=day_index, 
            date=day_model.date,
            title=day_model.title,
            city=day_model.city,
            weather=self._build_weather_info(day_model), 
            total_places=day_model.place_count, 
            itinerary=itinerary_items
        )

    def update_trip_day(self, trip_id: int, day_index: int, day_data: TripDayUpdate,
                        user_id: int) -> TripDayDetailResponse:
        trip_model = self.db.query(Trip).filter(Trip.id == trip_id).first() # Fetch trip first
        if not trip_model:
            raise NotFoundError(f"行程ID {trip_id} 未找到")
        
        self._get_trip_with_permission(trip_model, user_id, check_edit_permission=True)

        day = self.db.query(TripDay).filter(
            and_(TripDay.trip_id == trip_id, TripDay.day_index == day_index)
        ).first()

        if not day:
            raise NotFoundError(f"行程第 {day_index} 天未找到")

        update_payload = day_data.dict(exclude_unset=True)

        simple_fields = ["title", "summary", "city", "theme", "estimated_cost"]
        for field in simple_fields:
            if field in update_payload:
                setattr(day, field, update_payload[field])
        
        if "weather" in update_payload and day_data.weather:
             weather_update_data = day_data.weather.dict(exclude_unset=True)
             for key, value in weather_update_data.items():
                 # Assuming TripDay model has fields like weather_condition, temperature etc.
                 db_weather_field_name = key # if direct match
                 if hasattr(day, db_weather_field_name):
                     setattr(day, db_weather_field_name, value)
                 # Or if they are prefixed e.g. weather_condition on DB model
                 # elif hasattr(day, f"weather_{key}"): 
                 #    setattr(day, f"weather_{key}", value)


        if "itinerary" in update_payload and day_data.itinerary is not None:
            self._update_day_itinerary_from_schema(day, day_data.itinerary) # Pass the list of Pydantic models

        day.updated_at = datetime.utcnow() # Explicitly set updated_at for TripDay if it has such a field
        self.db.commit()
        self.db.refresh(day)

        # After update, fetch details again to return fresh data
        return self.get_trip_day_detail(trip_id, day_index, user_id)

    def _update_day_itinerary_from_schema(self, day: TripDay, itinerary_updates: List[TripDayUpdateItineraryItem]):
        # Delete existing items for this day
        self.db.query(TripPlace).filter(TripPlace.day_id == day.id).delete(synchronize_session='fetch')
        self.db.query(TripFood).filter(TripFood.day_id == day.id).delete(synchronize_session='fetch')
        self.db.query(TripTransportation).filter(TripTransportation.day_id == day.id).delete(synchronize_session='fetch')
        
        day.place_count = 0
        day.food_count = 0
        
        # This section requires significant implementation based on how you map
        # TripDayUpdateItineraryItem (which has amap_poi_id, type, time, duration, etc.)
        # to your DB models (TripPlace, TripFood) and how TripTransportation is generated.
        # This involves:
        # 1. Fetching POI details from amap_poi_id (likely via a location service).
        # 2. Creating TripPlace/TripFood instances with resolved data.
        # 3. Auto-generating TripTransportation between items based on 'next_transport' and locations.
        # 4. Handling visit_order for places/foods and transport_order for transportations.

        # Simplified placeholder loop:
        current_visit_order_place = 0
        current_visit_order_food = 0
        # last_location_details = None # For generating transport

        for item_schema in itinerary_updates:
            # poi_details = self.location_service.get_details(item_schema.amap_poi_id) # Example
            # if not poi_details: continue

            # if last_location_details and item_schema.next_transport: # or previous item's next_transport
                # Generate TripTransportation from last_location_details to poi_details
                # using item_schema.next_transport (mode)
                # new_transport = TripTransportation(...)
                # self.db.add(new_transport)
            pass # Corrected indentation for this block


            if item_schema.type.lower() == "attraction": # Or "place"
                current_visit_order_place += 1
                # new_db_item = TripPlace(
                #     trip_id=day.trip_id, day_id=day.id, day_index=day.day_index,
                #     visit_order=current_visit_order_place,
                #     name=poi_details.name, # From resolved POI
                #     # ... map other fields from poi_details and item_schema ...
                #     amap_poi_id=item_schema.amap_poi_id,
                #     start_time=datetime.strptime(item_schema.time, "%H:%M").time() if item_schema.time else None, # Parse time string
                #     duration=item_schema.duration,
                #     price=item_schema.price,
                # )
                # self.db.add(new_db_item)
                day.place_count += 1
                # last_location_details = poi_details
            elif item_schema.type.lower() == "food":
                current_visit_order_food += 1
                # new_db_item = TripFood(...)
                # self.db.add(new_db_item)
                day.food_count +=1
                # last_location_details = poi_details
            elif item_schema.type.lower() == "accommodation": # Or hotel
                # Update TripDay's accommodation fields or a separate TripAccommodation model
                # day.accommodation_name = poi_details.name
                # day.accommodation_poi_id = item_schema.amap_poi_id
                # last_location_details = poi_details
                pass # Corrected indentation for this block
            # Add other types like "custom" if needed

        day.is_generated = True # Mark as (re)generated
        self.db.flush()


    def get_trip_foods(self, trip_id: int, user_id: int) -> TripFoodsResponse:
        trip_model = self.db.query(Trip).filter(Trip.id == trip_id).first()
        if not trip_model:
            raise NotFoundError(f"行程ID {trip_id} 未找到")
        self._get_trip_with_permission(trip_model, user_id)

        # If TripFood has a direct relationship from Trip (e.g. trip.foods_relationship)
        # and it's efficient, use it. Otherwise, query TripFood table.
        foods_models = self.db.query(TripFood).filter(TripFood.trip_id == trip_id).order_by(TripFood.day_index, TripFood.visit_order).all()
        
        response_foods = [TripFoodResponseItem.from_orm(food_model) for food_model in foods_models]

        return TripFoodsResponse(
            trip_id=trip_id,
            total=len(response_foods),
            foods=response_foods
        )

    def cancel_trip(self, trip_id: int, user_id: int, confirm: bool) -> TripCancelResponseData: # confirm is now mandatory
        if not confirm: # This check might be redundant if API ensures confirm=true from TripCancelRequest
            raise ValidationError("取消操作必须被确认") 

        trip_model = self.db.query(Trip).filter(Trip.id == trip_id).first()
        if not trip_model:
            raise NotFoundError(f"行程ID {trip_id} 未找到")

        self._get_trip_with_permission(trip_model, user_id, check_edit_permission=True)

        if trip_model.status == 2: 
             raise ValidationError("行程已被取消")

        trip_model.status = 2 
        trip_model.updated_at = datetime.utcnow() 
        
        self.db.commit()
        self.db.refresh(trip_model)

        return TripCancelResponseData(
            id=trip_model.id,
            status=trip_model.status,
            cancel_time=trip_model.updated_at 
        )

    def _get_trip_with_permission(self, trip: Trip, user_id: int, check_edit_permission: bool = False):
        """Helper to check permissions directly on a fetched Trip object. Raises error if not permitted."""
        # trip object is passed directly to avoid re-fetching
        if not trip: # Should not happen if called after a fetch, but as a safeguard
            raise NotFoundError("行程未找到 (permission check)")

        is_owner = (trip.user_id == user_id)
        
        # View permission: owner or public trip or (if implemented) a collaborator with view rights
        can_view = is_owner or (trip.is_public == 1) 
        # Add collaborator check here if you have a TripCollaborators table/relationship
        # e.g., or self.db.query(TripCollaborator).filter(trip_id=trip.id, user_id=user_id, can_view=True).count() > 0
        
        if not can_view:
            raise PermissionError("无权限访问此行程")

        if check_edit_permission:
            # Edit permission: owner or (if implemented) a collaborator with edit rights
            can_edit = is_owner
            # Add collaborator check here for edit rights
            # e.g., or self.db.query(TripCollaborator).filter(trip_id=trip.id, user_id=user_id, can_edit=True).count() > 0
            if not can_edit:
                raise PermissionError("无权限修改此行程")
        # No explicit return, raises error if permission denied


    def _create_trip_days(self, trip: Trip):
        current_date_val = trip.start_datetime.date()
        days_to_create = []
        for i in range(1, trip.days + 1):
            day_city_placeholder = None
            if trip.destinations and isinstance(trip.destinations, list) and len(trip.destinations) > 0:
                day_city_placeholder = str(trip.destinations[0]) # Using first POI ID as placeholder for city

            day_datetime = datetime.combine(current_date_val, time(9,0))
            
            day = TripDay(
                trip_id=trip.id,
                day_index=i,
                date=current_date_val,
                datetime=day_datetime, 
                timezone=trip.start_timezone,
                title=f"DAY {i}",
                city=day_city_placeholder, # City name/ID to be properly set later
                is_generated=False 
            )
            days_to_create.append(day)
            current_date_val += timedelta(days=1)
        
        self.db.add_all(days_to_create)
        self.db.commit() # Commit after adding all day skeletons

    def _build_weather_info(self, day: TripDay) -> Optional[WeatherInfo]:
        # This method assumes TripDay model has direct fields for weather info
        # or a related weather object.
        # Example: if day.weather_condition, day.temperature are direct fields on TripDay model
        if not day.weather_condition and not day.temperature: 
            return None

        # Ensure all fields required by WeatherInfo are available on 'day' or mapped
        return WeatherInfo(
            condition=getattr(day, 'weather_condition', None),
            temperature=getattr(day, 'temperature', None), # e.g., "10-15°C"
            icon=getattr(day, 'weather_icon', None),
            humidity=getattr(day, 'humidity', None),
            wind=getattr(day, 'wind', None),
            precipitation=getattr(day, 'precipitation', None),
            uv_index=getattr(day, 'uv_index', None),
            sunrise=getattr(day, 'sunrise', None), # Should be time object
            sunset=getattr(day, 'sunset', None)   # Should be time object
            # condition_text was in your previous version of _build_weather_info, ensure day model has it
            # condition_text=getattr(day, 'weather_condition_text', None),
        )

    def _build_accommodation_info(self, day: TripDay) -> Optional[AccommodationInfo]:
        # Assumes TripDay model has direct fields for accommodation or a related object
        if not day.accommodation_name:
            return None
        return AccommodationInfo(
            name=day.accommodation_name,
            address=day.accommodation_address,
            price=day.accommodation_price,
            rating=day.accommodation_rating,
            latitude=day.accommodation_latitude,
            longitude=day.accommodation_longitude,
            contact=day.accommodation_contact,
            accommodation_poi_id=day.accommodation_poi_id
        )

    def _build_point_info(self, day: TripDay, point_type: str) -> Optional[PointInfo]:
        # Assumes TripDay model has direct fields for start/end points
        name, time_val, type_val, poi_id_val = None, None, None, None
        if point_type == "start":
            name = day.start_point_name
            time_val = day.start_point_time
            type_val = day.start_point_type
            poi_id_val = day.start_point_poi_id
        elif point_type == "end":
            name = day.end_point_name
            time_val = day.end_point_time
            type_val = day.end_point_type
            poi_id_val = day.end_point_poi_id
        
        if not name:
                return None
        return PointInfo(name=name, time=time_val, type=type_val, poi_id=poi_id_val)


    def _build_itinerary(self, day: TripDay) -> List[ItineraryItem]:
        """为某一天构建详细的行程项目列表 (ItineraryItem)"""
        # Ensure day.places, day.foods, day.transportations are loaded via relationship loading
        # or query them here.
        
        items: List[ItineraryItem] = []
        
        # Places (Attractions)
        db_places = sorted(day.places, key=lambda p: p.visit_order) if day.places else []
        for place in db_places:
            items.append(ItineraryItem(
                time=place.start_time.strftime("%H:%M") if place.start_time else None,
                type=place.category or "attraction", # Use category if available, else default
                name=place.name,
                description=place.notes or (f"门票: {place.price}" if place.price else None),
                images=json.loads(place.images) if isinstance(place.images, str) else place.images or ([place.image_url] if place.image_url else []),
                latitude=place.latitude,
                longitude=place.longitude,
                duration=place.duration,
                amap_poi_id=place.amap_poi_id,
                price=place.price,
                navigation=NavigationInfo(amap_url=place.amap_navigation_url, web_url=place.web_navigation_url)
                # Populate other fields from ItineraryItem schema if available in TripPlace
            ))
            
        # Foods
        db_foods = sorted(day.foods, key=lambda f: f.visit_order) if day.foods else []
        for food in db_foods:
            items.append(ItineraryItem(
                time=food.start_time.strftime("%H:%M") if food.start_time else None,
                type=food.category or "food",
                name=food.name,
                description=food.description or (f"人均: {food.price}" if food.price else None),
                images=json.loads(food.images) if isinstance(food.images, str) else food.images or ([food.image_url] if food.image_url else []),
                latitude=food.latitude,
                longitude=food.longitude,
                duration=food.duration, # If food items have duration
                amap_poi_id=food.amap_poi_id,
                price=food.price, # Per person price
                navigation=NavigationInfo(amap_url=food.amap_navigation_url, web_url=food.web_navigation_url)
            ))

        # Transportations
        db_transportations = sorted(day.transportations, key=lambda t: t.transport_order) if day.transportations else []
        for trans in db_transportations:
            items.append(ItineraryItem(
                time=trans.start_time.strftime("%H:%M") if trans.start_time else None,
                type="transportation",
                name=f"{trans.transportation_mode} 从 {trans.from_name} 到 {trans.to_name}",
                description=trans.description,
                duration=trans.duration,
                distance=trans.distance,
                mode=trans.transportation_mode, 
                from_location=LocationPoint(name=trans.from_name, latitude=trans.from_latitude, longitude=trans.from_longitude),
                to_location=LocationPoint(name=trans.to_name, latitude=trans.to_latitude, longitude=trans.to_longitude),
                navigation=NavigationInfo(amap_url=trans.amap_navigation_url, web_url=trans.web_navigation_url)
            ))
            
        # Sort all collected items by time
        # This requires careful handling of None times and consistent time formatting
        def sort_key(item: ItineraryItem):
            if item.time:
                try:
                    # If time is "HH:MM" string
                    return datetime.strptime(item.time, "%H:%M").time()
                except ValueError:
                    return datetime.max.time() # Put unparseable times last
            return datetime.max.time() # Put None times last

        items.sort(key=sort_key) 
        return items

    # _build_itinerary_item helper is removed as logic is now more specific within _build_itinerary

    # _update_day_itinerary is replaced by _update_day_itinerary_from_schema to match new schema
    # The old _update_day_itinerary was complex and assumed a different input ItineraryItem structure.
    # The new one would parse TripDayUpdateItineraryItem and recreate DB entries.
    # This is a major piece of logic related to how users edit their day.
    # Given the complexity, I've added a high-level sketch in _update_day_itinerary_from_schema.
    # You will need to implement the detailed conversion from TripDayUpdateItineraryItem 
    # (which has amap_poi_id, type, time, duration, price, next_transport)
    # to creating/updating TripPlace, TripFood, and TripTransportation (auto-generated) entries.
