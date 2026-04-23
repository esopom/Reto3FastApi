import json
# Clase que nos permite trabajar con los datos de prueba
class FutbolData:

    #Propiedades que almacenarán todos los datos
    partidos=[]
    filePartidos = None

    def __init__(self):
        #Carga de los ficheros de datos de prueba
        self.filePartidos=open('data/futboldata.json')
        self.partidos = json.load(self.filePartidos)
        self.filePartidos.close()

#partidos
    #Devolucion asincrona de datos de aPartidos
    async def get_partidos(self,skip,total):
        return {'partidos':self.partidos['partidos'][skip:(total+skip)]}
    async def get_allIPartidos(self):
        return self.partidos

    # Devolucion asincrona de partidos de un equipo en concreto
    async def get_partidosEquipo(self,equipo: str):
        # si no se encuentra el alimento se devolverá el nulo en vez de un objeto JSON
        partidos=[]
        #Recorremos todos los datos JSON
        for item in self.partidos['partidos']:
            #Comparamos el id que es int
            if item['equipolocal']==equipo:
                partidos.append(item)
            elif item['equipovisitante']==equipo:
                partidos.append(item)
        return partidos

    # Devolucion asincrona de un partido
    async def get_partido(self,partido_id: int):
        # si no se encuentra el alimento se devolverá el nulo en vez de un objeto JSON
        partido=None
        #Recorremos todos los datos JSON
        for item in self.partidos['partidos']:
            #Comparamos el id que es int
            if item['id']==partido_id:
                partido=item
                break
        return partido

    async def write_partido(self, partido: partidos):
        self.filePartidos=open('data/futboldata.json','w')
        #Conseguimos el último id de la lista
        ultimo_partido=self.partidos['partidos'][-1]['id']
        #Añadimos un nuevo id al partido nuevo
        partidoDict=partido.model_dump()
        partidoDict['id']=ultimo_partido+1
        self.partidos['partidos'].append(partidoDict)
        json.dump(self.partidos,self.filePartidos,indent=2)
        self.filePartidos.close()
        return partidoDict
    
    # Recibimos y actualizamos un nuevo partido
    async def update_partido(self, partido_id: int, partido: partidos):
        self.filePartidos=open('data/futboldata.json','w')
        #Buscamos el partido
        partidoEncontrado=None
        partidoPos=0
        #Recorremos todos los datos JSON
        for item in self.partidos['partidos']:
            #Comparamos el id que es int
            if item['id']==partido_id:
                partidoEncontrado=item
                break
            partidoPos=partidoPos+1
        #Si se ha encontrado
        if(partidoEncontrado):
            #Realizamos la actualization
            partidoDict = partido.model_dump()
            for elem in partidoDict:
                if(partidoDict[elem]):
                #cambiamos el valor
                    self.partidos['partidos'][partidoPos][elem]=partidoDict[elem]
            json.dump(self.partidos,self.filePartidos,indent=2)
            self.filePartidos.close()
            return self.partidos['partidos'][partidoPos]
        else:
            return None

    # Borramos un ingrediente
    async def delete_partido(self, partido_id: int):
        self.filePartidos=open('data/futboldata.json','w')
        #Buscamos el partido
        partidoEncontrado=None
        partidoPos=0
        #Recorremos todos los datos JSON
        for item in self.partidos['partidos']:
            #Comparamos el id que es int
            if item['id']==partido_id:
                partidoEncontrado=item
                break
            partidoPos=partidoPos+1
        #Si se ha encontrado
        if(partidoEncontrado):
            self.partidos['partidos'].pop(partidoPos)
            json.dump(self.partidos,self.filePartidos,indent=2)
            self.filePartidos.close()
            return {"info":"borrado partido "+str(partido_id)}
        else:
            return None