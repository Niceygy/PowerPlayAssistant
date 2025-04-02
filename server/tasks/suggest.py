from server.handlers.notsure import what_can_you_do


def handle_not_sure(request, power, database):
    system_name = request.args.get("system")
    return what_can_you_do(system_name, power, database)