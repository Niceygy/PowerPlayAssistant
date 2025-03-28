from server.handlers.notsure import what_can_you_do


def handle_not_sure(request, power, database):
    return what_can_you_do()