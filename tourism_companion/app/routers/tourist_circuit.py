from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.deps import get_db
from app.schemas import TouristCircuit, TouristPoint
from app.models import TouristCircuit as TouristCircuitModel, TouristPoint as TouristPointModel
from typing import List

router = APIRouter()

@router.get("/tourist_circuit/{circuit_id}/points", response_model=List[TouristPoint])
async def get_circuit_points(circuit_id: int, db: Session = Depends(get_db)):
    points = db.query(TouristPointModel).filter_by(circuit_id=circuit_id).all()
    if not points:
        raise HTTPException(status_code=404, detail="No points found for this circuit")
    return [TouristPoint.from_orm(point) for point in points]

@router.post("/tourist_circuit/{circuit_id}/points/{point_id}/visit", response_model=TouristPoint)
async def mark_point_as_visited(circuit_id: int, point_id: int, db: Session = Depends(get_db)):
    point = db.query(TouristPointModel).filter_by(circuit_id=circuit_id, id=point_id).first()
    if not point:
        raise HTTPException(status_code=404, detail="Point not found")
    
    point.visited = True
    db.commit()
    db.refresh(point)

    # Check if all points are visited
    all_visited = db.query(TouristPointModel).filter_by(circuit_id=circuit_id, visited=False).count() == 0
    if all_visited:
        circuit = db.query(TouristCircuitModel).filter_by(id=circuit_id).first()
        # Notify user that the circuit is finished

    return TouristPoint.from_orm(point)

# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.deps import get_db
# from app.models import TouristCircuit, TouristPoint
# from typing import List

# router = APIRouter()

# @router.get("/tourist_circuit/{circuit_id}/points", response_model=List[TouristPoint])
# async def get_circuit_points(circuit_id: int, db: Session = Depends(get_db)):
#     points = db.query(TouristPoint).filter_by(circuit_id=circuit_id).all()
#     return points

# @router.post("/tourist_circuit/{circuit_id}/points/{point_id}/visit", response_model=TouristPoint)
# async def mark_point_as_visited(circuit_id: int, point_id: int, db: Session = Depends(get_db)):
#     point = db.query(TouristPoint).filter_by(circuit_id=circuit_id, id=point_id).first()
#     if not point:
#         raise HTTPException(status_code=404, detail="Point not found")
    
#     point.visited = True
#     db.commit()
#     db.refresh(point)

#     # Check if all points are visited
#     all_visited = db.query(TouristPoint).filter_by(circuit_id=circuit_id, visited=False).count() == 0
#     if all_visited:
#         circuit = db.query(TouristCircuit).filter_by(id=circuit_id).first()
#         # Notify user that the circuit is finished

#     return point
