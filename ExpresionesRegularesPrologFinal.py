import re
print("------------------------------------------------------------------------------------------------------------\n")
print("SE QUIERE IMPRIMIR LAS DIRECCIONES CON EL FORMATO: CALLE XXA # XX A - XX APARTAMENTO XX BARRIO XXX XXXXX\n")
print("------------------------------------------------------------------------------------------------------------\n")
direccion=str(input("Ingrese una dirrección: \n"))
print("Dirección ingresada: ",direccion+"\n")
print("------------------------------------------------------------------------------------------------------------")



#regexnecesarios:

barrio = re.compile('BRR|BR|BARRIO')
buscarapartamento=re.compile('-*\s*(APT)O*-*\s[0-9][0-9]*[0-9]*-*') #defino esta para usarla en el reemplazo
numeroapartamento=re.compile('[0-9][0-9]*[0-9]*[0-9]*') ##Con esta extraigo el apartamento
patrongeneralcalle=re.compile('(CALLE|Cll)\s[0-9]*[0-9]*[0-9]*\s[A-M-P-Z]*\s*(No\.|#)')
numero=re.compile('No\.')
calle=re.compile('CALLE|Cll')
callecarrera=re.compile('[0-9][0-9]*[A-Z]*-\s[0-9][0-9]*-')
primernumeroletra=re.compile('[0-9][0-9]*[A-Z]*')
segundonumero = re.compile('\s[0-9][0-9]*')
patroncarrera=re.compile('(Kr|Carrera)\s[0-9][0-9]*[A-Z]*')
patronnumerocarrera=re.compile('[0-9][0-9]*[A-Z]*\s*[A-Z]*')
carrerabase=re.compile('#\s[0-9][0-9]*[A-Z]*')
patroncalledireccion=re.compile("No\.\s[0-9][0-9]*\s*[A-Z]*")
patroncallebase = re.compile("CALLE\s[0-9][0-9]*\s[A-Z]")
patronumerocasa=re.compile("- [0-9][0-9]*[0-9]*-")
patronnumerocasabase = re.compile("-[0-9][0-9]*[0-9]")
patroncambioapto=re.compile("201")
mocharapartamento=re.compile("APARTAMENTO")
if direccion.count("CALLE")>0 or direccion.count("Cll")>0:

    stringfinal=""
    ##defino un patron

    #hallo el resto de cadena que no cumple patron
    fin=(re.search(patrongeneralcalle,direccion).end())
    partefinal=direccion[fin:]
    #obtengo la cadena que cumple patron y procedo a formatear
    coincidencia=str(re.search(patrongeneralcalle,direccion)[0]) ##CALLE 102 #, CALLE 64 A No. , Cll 109 No. CALLE 22 No.

    #Patron para calle:

    ##Reemplazo en coincidencia por CALLE
    coincidencia=calle.sub("CALLE",coincidencia)
    #Patron para No. a #

    #detecto las direcciones que posean el No. para pasarlo a numero con sub
    coincidencia=numero.sub("#",coincidencia)

    stringfinal=coincidencia



    ###################################################################################################################3

    ##procedemos a sacar los numeros:



    fin2=(re.search(callecarrera,partefinal).end()) ##obtengo donde finaliza la captura de la ER

    partefinal2=str(partefinal[fin2:]) ##Dejo la parte final del String

    paranumeros=str(re.search(callecarrera,partefinal)[0]) # 94X- 62- debe pasar a  --> 94 - 62

    #Patron para obtener el primer número y posible letra del strin 94X

    numero1=re.match(primernumeroletra,paranumeros)[0] #Match porque está al principio y ya tengo el primer número.

    #Patron para segundo número y no tiene letra

    numero2=re.search(segundonumero,paranumeros)[0] ##Ahora ya tengo los 2 numeros, puedo reemplazar
    paranumeros=callecarrera.sub(str(numero1)+" -"+str(numero2),paranumeros)
    stringfinal+=" "+paranumeros


    ###############################################
    #cambiar rapidamente BR por BARRIO



    if direccion.count("APT")>0 or direccion.count("APTO")>0:

        ##Busco apartamento y listo:

        #hallemos el número
        aptofin=re.search(numeroapartamento,partefinal2).end()
        if aptofin==len(partefinal2):

            pos=partefinal2.find("- APT- 205")
            auxiliar=partefinal2[0:pos]
            partefinal2="- APT- 205"+auxiliar
            apto = re.search(numeroapartamento, partefinal2)[0]
            partefinal2 = buscarapartamento.sub(" APARTAMENTO " + str(apto), partefinal2)

            stringfinal += partefinal2
            stringfinal = str(barrio.sub("BARRIO", stringfinal))
            print(stringfinal)


        else:

            apto=re.search(numeroapartamento,partefinal2)[0]
            partefinal2 = buscarapartamento.sub(" APARTAMENTO " + str(apto), partefinal2)

            stringfinal += partefinal2
            stringfinal = str(barrio.sub("BARRIO", stringfinal))
            print("Dirección formateada: ",stringfinal)
        #print(re.search(buscarapartamento,partefinal2)[0])
        #partefinal2=buscarapartamento.sub("APARTAMENTO "+str(apto),partefinal2)


    else:

        stringfinal+=partefinal2
        stringfinal = str(barrio.sub("CASA BARRIO", stringfinal))
        print("Dirección formateada: ",stringfinal)
else:
    #Modelo a modificar
    base="CALLE 77 S # 60A-100 APARTAMENTO 201 BARRIO BELEN ZAFRA"
    #Sacar carrera y numero en la dirección ingresada

    #carrera y número como string
    carreraynumero=str(re.search(patroncarrera,direccion)[0])
    #patron para solo sacar el numero y letra de la carrera

    #numero y letra de carrera
    numerocarrera=re.search(patronnumerocarrera,carreraynumero)[0]
    #patron para obtener la parte correspodiente a carrera en la base

    #modificar la base, ya queda con la carrera puesta
    base=carrerabase.sub("# "+str(numerocarrera),base)
    ##obtener la calle de la dirección ingresada

    #Con esto obtengo No. NNx
    calledireccion=re.search(patroncalledireccion,direccion)[0]
    #Patron para solo extraer el número y letra de la calle, me sirve el anterior
    callenumeroletra=re.search(patronnumerocarrera,calledireccion)[0] #Acá obtuve el número y letra de la calle, falta meterlos a la base
    #Patron para cambiar la calle de la base:

    base=patroncallebase.sub("CALLE "+str(callenumeroletra),base)

    ##FALTA TOMAR EL OTRO NÚMERO DE LA CASA, METERLO Y DESPUES CUADRAR EL BARRIO Y EL APTO.

    #Patron para tomar el número de casa

    #Obtengo el string de la busqueda
    numerocasa=re.search(patronumerocasa,direccion)[0]
    #usando el subpatron anterior, obtengo el número de la casa
    casa=re.search(patronnumerocarrera,numerocasa)[0]

    #Patron para reemplazar en la base

    base=patronnumerocasabase.sub(" - "+str(casa),base)

    ##Cuadrar apartamento:
    if direccion.count("APTO")>0:
        cadenaapartamento = re.search(buscarapartamento, direccion)[0]
        numeroapto=re.search(numeroapartamento,cadenaapartamento)[0]

        base=patroncambioapto.sub(str(numeroapto),base)

        inicioapartamento = re.search(buscarapartamento, direccion).start()
        auxiliardireccion = direccion[0:inicioapartamento]  # Un auxiliar necesario para poder operar más abajo
        finbarrio = re.search(barrio, auxiliardireccion).end()  # donde termina el barrio para sacar el nombre
        auxiliardireccion = auxiliardireccion[finbarrio:]  # Contiene el nombre del barrio

        mocharbase = re.search(barrio, base).end()
        auxiliarbase = base[0:mocharbase]
        auxiliarbase += auxiliardireccion
        print("Dirección formateada: ",auxiliarbase)


    else:
        #cuadrar barrio
        #patron para barrio establecido anteriormente

        direccion=barrio.sub("BARRIO",direccion) #lo establezco como Barrio
        #obtener en que indice se acaba la palabra barrio
        finbarrio=re.search(barrio,direccion).end()
        #acá tengo el nombre del barrio
        nombrebarrio=direccion[finbarrio:]
        #Necesito mochar la parte correspondiente a apartamento en la base:

        posicionparamochar=re.search(mocharapartamento,base).start()
        auxiliarbase=base[0:posicionparamochar]
        auxiliarbase+=" CASA BARRIO"+nombrebarrio
        print("Dirección formateada:",auxiliarbase)
































