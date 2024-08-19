def total_individual(request):
    total=0
    if request.session.has_key('carrito'):
        for key, value in request.session["carrito"].items():
            total = total + float(value["precio"])
    return {"total":total}

def total_factura (request):
    total_fac=0
    if request.session.has_key('carrito'):
        for key, value in request.session["carrito"].items():
            total_fac = total_fac + float(value["precio"])
    return {"total":total_fac}