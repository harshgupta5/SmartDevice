from django.shortcuts import render
from django.http import JsonResponse
from .import pool
def  FetchStates(request):
    try:
        db,cmd=pool.connection()
        cmd.execute("select * from states")
        rows=cmd.fetchall()
        return JsonResponse(rows,safe=False)
    except Exception as e:
        return JsonResponse([],safe=False)


def FetchCities(request):
    try:
        stateid=request.GET['stateid']
        db, cmd = pool.connection()
        cmd.execute("select * from cities where stateid={}".format(stateid))
        rows = cmd.fetchall()
        return JsonResponse(rows, safe=False)
    except Exception as e:
        return JsonResponse([], safe=False)

