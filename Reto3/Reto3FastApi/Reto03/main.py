from fastapi import FastAPI, HTTPException, Response, status, Body, Path, Query
from pydantic import BaseModel, Field
from typing import Optional, Union, Annotated


from futboldata import FutbolData

futbol = FutbolData()
app = FastAPI(
    title="FutbolApi",
    description="ApiRestFul para la gestión de futbol",
    version="0.0.1",
    contact={
        "name":"Adrian Tomas",
        "url":"http://www.mastermind.ac"
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }
)

class Partido(BaseModel):
    id: Optional[int] = None
    anyo : int
    fase: str
    equipolocal: str
    goleslocales: int = Field(ge=0, description="Los goles locales no pueden ser negativos")
    golesvisitante: int = Field(ge=0, description="Los goles visitantes no pueden ser negativos")
    equipovisitante: str
    estaequipoanfitrion: int



@app.get("/partidos")
async def get_partidos(
    total: Annotated[int, Query(gt=0, description="Cantidad de partidos a devolver")] = 10,
    skip: Annotated[int, Query(gt=0, description="Cantidad de partidos a omitir")] = 1
):
    return await futbol.get_partidos(skip,total)

@app.get("/todospartidos")
async def get_todospartidos():
    return await futbol.get_allIpartidos()

@app.get("/partidos/{partido_id}")
async def get_partido(partido_id: Annotated[int, Path(title="El ID del partido a buscar", description="Identificador único del partido", gt=0)]):
    partido = await futbol.get_partido(partido_id)
    if partido is None:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return partido

@app.get("/partidosequipo/{equipo_id}")
async def get_partidoequipo(equipo_id: str):
    partidos = await futbol.get_partidosEquipo(equipo_id)
    if not partidos:
        raise HTTPException(status_code=404, detail="No se encontraron partidos para el equipo")
    return partidos

@app.post("/partidos")
async def write_partido(partido: Annotated[Partido, Body(description="Datos del partido a crear")]):
    return await futbol.write_partido(partido)

@app.put("/partidos/{partido_id}")
async def update_partido(partido_id: int, partido: Partido):
    partido_actualizado = await futbol.update_partido(partido_id, partido)
    if partido_actualizado is None:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return partido_actualizado

@app.delete("/partidos/{partido_id}")
async def delete_partido(partido_id: Annotated[int, Path(title="El ID del partido a borrar", gt=0)]):
    partido_eliminado = await futbol.delete_partido(partido_id)
    if partido_eliminado is None:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return partido_eliminado


