class Carritos:
    def __init__(self, request):
        self.items = []
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        
        if not carrito:
            self.session["carrito"] = {}
            self.carrito = self.session["carrito"]
        else:
            self.carrito = carrito
    
    def verificar_guardar(self, item):
        id = str(item.id)
        if id not in self.carrito.keys():
            self.carrito[id] = {
                "item_id": item.id,
                "nombre": item.nombre,
                "precio": str(item.precio),
                "descripcion": item.descripcion,
                "cantidad": 1, 
            }
        self.guardar_carrito()

    def agregar(self, item, quantity=1):
        id = str(item.id)
        if id not in self.carrito.keys():
            self.carrito[id] = {
                "item_id": item.id,
                "nombre": item.nombre,
                "precio": str(item.precio),
                "descripcion": item.descripcion,
                "cantidad": quantity,
                "total": float(item.precio) * quantity
            }
        else:
            self.carrito[id]["cantidad"] += quantity
            self.carrito[id]["total"] = float(self.carrito[id]["precio"]) * self.carrito[id]["cantidad"]

        self.guardar_carrito()
        return {
            'count': len(self.carrito),
            'total': self.calcular_total()
        }

    def calcular_total(self):
        return sum(float(item['total']) for item in self.carrito.values())


    def guardar_carrito(self):  
        self.session["carrito"] = self.carrito
        self.session.modified = True
    
    def eliminar(self, item):
        id = str(item.id)
        if id in self.carrito:
            del self.carrito[id]
            self.guardar_carrito()
    
    def restar(self, item):
        id = str(item.id)
        if id in self.carrito.keys():
            for key, value in self.carrito.items():
                if key == id:
                    value["cantidad"] = value["cantidad"] - 1
                    value["total"] = float(value["precio"]) * float(value["cantidad"])
                    if value["cantidad"] < 1:
                        self.eliminar(item)
                    break
            self.guardar_carrito()
        
    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True

    def quitar(self, item):
        id = str(item.id)
        if id in self.carrito.keys():
            del self.carrito[id]
            self.guardar_carrito()
        
